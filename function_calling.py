import anthropic
from cassandra_CRUD import PollutionDataProcessor
import tensorflow as tf
import numpy as np
from config import Config

class PollutionQueryHandler:
    def __init__(self, api_key):
        self.client = anthropic.Client(api_key=api_key)
        self.tools = [
            {
                "name": "query_pollution_data_openai",
                "description": "Người dùng muốn truy vấn dữ liệu ô nhiễm theo ngày/tháng/năm",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "year": {"type": "integer", "description": "Năm cần truy vấn"},
                        "month": {"type": "integer", "description": "Tháng cần truy vấn"},
                        "day": {"type": "integer", "description": "Ngày cần truy vấn"},
                    },
                    "required": ["year", "month", "day"]
                },
            },
            {
                "name": "predict_pollution_level",
                "description": "Dự đoán mức độ ô nhiễm dựa trên thông số môi trường và thời gian.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "Day": {"type": "integer", "description": "Ngày trong tháng"},
                        "Month": {"type": "integer", "description": "Tháng trong năm"},
                        "Year": {"type": "integer", "description": "Năm của dữ liệu"},
                        "Hour": {"type": "integer", "description": "Giờ của dữ liệu"},
                        "PT08_S1_CO": {"type": "number", "description": "Nồng độ CO đo từ cảm biến PT08.S1 "},
                        "C6H6_GT": {"type": "number", "description": "Nồng độ Benzen "},
                        "PT08_S5_O3": {"type": "number", "description": "Nồng độ O3 đo từ cảm biến PT08.S5 "},
                        "PT08_S2_NMHC": {"type": "number",
                                         "description": "Nồng độ NMHC đo từ cảm biến PT08.S2"},
                        "PT08_S4_NO2": {"type": "number", "description": "Nồng độ NO2 đo từ cảm biến PT08.S4"}
                    },
                    "required": [
                        "Day", "Month", "Year", "Hour",
                        "PT08_S1_CO", "C6H6_GT", "PT08_S5_O3",
                        "PT08_S2_NMHC", "PT08_S4_NO2"
                    ]
                }
            },

            {
                "name": "insert_data_to_database",
                "description": "Người dùng muốn thêm dữ liệu ô nhiễm vào database.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "Day": {"type": "integer", "description": "Ngày của dữ liệu (1-31)"},
                        "Month": {"type": "integer", "description": "Tháng của dữ liệu (1-12)"},
                        "Year": {"type": "integer", "description": "Năm của dữ liệu (ví dụ: 2024)"},
                        "Hour": {"type": "integer", "description": "Giờ của dữ liệu (0-23)"},
                        "PT08_S1_CO": {"type": "number", "description": "Nồng độ PT08.S1 (CO) "},
                        "C6H6_GT": {"type": "number", "description": "Nồng độ Benzen "},
                        "PT08_S5_O3": {"type": "number", "description": "Nồng độ PT08.S5 (O3) "},
                        "PT08_S2_NMHC": {"type": "number", "description": "Nồng độ PT08.S2 (NMHC)"},
                        "PT08_S4_NO2": {"type": "number", "description": "Nồng độ PT08.S4 (NO2) "},
                        "AQI_Label": {
                            "type": "integer",
                            "description": "Chỉ số chất lượng không khí: 0 (Tốt), 1 (Trung bình), 2 (Kém), 3 (Xấu), 4 (Nguy hại)"
                        }
                    },
                    "required": ["Day", "Month", "Year", "Hour", "PT08_S1_CO", "C6H6_GT", "PT08_S5_O3", "PT08_S2_NMHC",
                                 "PT08_S4_NO2", "AQI_Label"]
                }
            },

            {
                "name": "statistical_analysis",
                "description": "Thực hiện phân tích thống kê mức độ ô nhiễm",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "stat_type": { "type": "string", "description": "Loại thống kê (mean, median, mode, max, min)"},
                        "start_day": {"type": "integer","description": "Ngày bắt đầu (1-31)"},
                        "start_month": {"type": "integer","description": "Tháng bắt đầu (1-12)"},
                        "end_day": {"type": "integer","description": "Ngày kết thúc (1-31)"},
                        "end_month": {"type": "integer","description": "Tháng kết thúc (1-12)"},
                        "year": {"type": "integer","description": "Năm phân tích"}
                    },
                    "required": ["stat_type", "start_day", "start_month", "end_day", "end_month", "year"]
                }
            }
        ]

    def query_pollution_data_openai(self, year=None, month=None, day=None):
        query_params = {
            "year": year,
            "month": month,
            "day": day,
        }
        print("Đang truy vấn dữ liệu với:", query_params)
        processor = PollutionDataProcessor(["127.0.0.1"], "pollution_db")
        try:
            data = processor.query_pollution_data(**query_params)
            processor.close_connection()
            if data.empty:
                return {"message": "Không có dữ liệu phù hợp với truy vấn."}
            return data.to_dict(orient="records")
        except Exception as e:
            return {"error": f"Lỗi truy vấn Cassandra: {str(e)}"}

    def insert_data_to_database(self, Day, Month, Year, Hour, PT08_S1_CO, C6H6_GT, PT08_S5_O3, PT08_S2_NMHC,
                                PT08_S4_NO2, AQI_Label):
        processor = PollutionDataProcessor(["127.0.0.1"], "pollution_db")
        try:
            corrected_data = {
                "Day": Day,
                "Month": Month,
                "Year": Year,
                "Hour": Hour,
                "PT08_S1_CO": PT08_S1_CO,
                "C6H6_GT": C6H6_GT,
                "PT08_S5_O3": PT08_S5_O3,
                "PT08_S2_NMHC": PT08_S2_NMHC,
                "PT08_S4_NO2": PT08_S4_NO2,
                "AQI_Label": AQI_Label
            }

            insert_status = processor.add_pollution_data_from_nlp(**corrected_data)

            if insert_status == "inserted":
                return {"message": "Dữ liệu đã được thêm vào database."}
            elif insert_status == "exists":
                return {"message": "Dữ liệu đã tồn tại, không cần thêm."}
            else:
                return {"error": "Không rõ trạng thái chèn dữ liệu."}
        except Exception as e:
            return {"error": f"Lỗi khi chèn dữ liệu: {str(e)}"}

    def predict_pollution_level(self, Day, Month, Year, Hour, PT08_S1_CO, C6H6_GT, PT08_S5_O3, PT08_S2_NMHC, PT08_S4_NO2):
        try:
            self.model = tf.keras.models.load_model("model_ML/air_quality_model.h5")

            input_features = np.array([[Day, Month, Year, Hour, PT08_S1_CO, C6H6_GT, PT08_S5_O3, PT08_S2_NMHC, PT08_S4_NO2]])

            prediction = self.model.predict(input_features)
            predicted_class = int(np.argmax(prediction, axis=1)[0])

            pollution_levels = ["Thấp", "Trung bình", "Cao", "Nguy hiểm", "Rất nguy hại"]
            predicted_label = pollution_levels[predicted_class]
            return {"pollution_level": predicted_class, "description": predicted_label}
        except Exception as e:
            return {"error": f"Lỗi dự đoán: {str(e)}"}


    def statistical_analysis(self, stat_type: str, start_day: int, start_month: int, end_day: int, end_month: int,
                             year: int):
        processor = PollutionDataProcessor(["127.0.0.1"], "pollution_db")
        time_range = {
            "start_day": start_day,
            "start_month": start_month,
            "end_day": end_day,
            "end_month": end_month,
            "year": year
        }

        data = processor.query_pollution_data_for_stats(time_range)

        if not data:
            return {"message": "Không có dữ liệu để thống kê"}

        columns = ['PT08_S1_CO', 'C6H6_GT', 'PT08_S5_O3', 'PT08_S2_NMHC', 'PT08_S4_NO2', 'AQI_Label']
        data_dicts = [dict(zip(columns, row)) for row in data]

        data_array = np.array([[row[col] for col in columns] for row in data_dicts])

        stats_result = {}
        if stat_type == "mean":
            stats_result = dict(zip(columns, np.mean(data_array, axis=0)))
        elif stat_type == "median":
            stats_result = dict(zip(columns, np.median(data_array, axis=0)))
        elif stat_type == "std":
            stats_result = dict(zip(columns, np.std(data_array, axis=0)))
        elif stat_type == "max":
            stats_result = dict(zip(columns, np.max(data_array, axis=0)))
        elif stat_type == "min":
            stats_result = dict(zip(columns, np.min(data_array, axis=0)))
        elif stat_type == "count":
            stats_result = {"Total Records": len(data)}
        else:
            stats_result = {"error": "Loại thống kê không hợp lệ"}

        return {"stat_type": stat_type, "result": stats_result}

    def call_claude_function(self, prompt):
        try:
            response = self.client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=1000,
                tools=self.tools,
                messages=[{"role": "user", "content": prompt}],
            )

            print(f'Claude Raw Response: {response}')

            if not response or not isinstance(response.content, list) or len(response.content) == 0:
                return {"error": "Không có phản hồi hợp lệ từ Claude."}

            if isinstance(response.content, list) and response.content:
                tool_use_block = next((block for block in response.content if block.type == "tool_use"), None)

                if getattr(tool_use_block, 'type', None) == 'tool_use':
                    function_name = getattr(tool_use_block, 'name', None)
                    arguments = getattr(tool_use_block, 'input', {})

                    if not function_name:
                        return {"error": "Không tìm thấy tên hàm."}

                    if not isinstance(arguments, dict):
                        arguments = {}

                    function_map = {
                        "query_pollution_data_openai": self.query_pollution_data_openai,
                        "predict_pollution_level": self.predict_pollution_level,
                        "insert_data_to_database": self.insert_data_to_database,
                        "statistical_analysis": self.statistical_analysis
                    }

                    if function_name in function_map:
                        result = function_map[function_name](**arguments)
                    else:
                        result = {"error": "Hàm không hợp lệ."}

                    print(f'Kết quả từ hàm "{function_name}": {result}, với tham số: {arguments}')
                    return result

        except Exception as e:
            return {"error": f"Lỗi khi gọi Claude: {str(e)}"}

        return {"error": "Dữ liệu nhập vào không hợp lệ."}

    def rewrite_result_with_advice(self, result, source=None):

        if source is None:
            if isinstance(result, list):
                source = "query"
            elif isinstance(result, dict) and "pollution_level" in result:
                source = "predict"
            elif isinstance(result, dict) and result.get("message") in [
                                                                        "Hàm đã được thực thi!",
                                                                        "Dữ liệu đã được thêm vào database.",
                                                                        "Đã thêm dữ liệu thành công"]:
                source = "insert"
            elif isinstance(result, dict) and result.get("stat_type") in ["mean", "median", "max","min","count","std"]:
                source = "stats"
        else:
                source = "unknown"
        print("Source:", source)
        if source == "query":
            rewriting_prompt = f"""
            Bạn là chuyên gia phân tích dữ liệu môi trường.   
            Dữ liệu cảm biến:
            {result}  
            Yêu cầu đầu ra:
            - Ngày truy vấn.
            - Kiểm tra có dữ liệu không. Từ chối trả lời nếu không có dữ liệu.
            - Chỉ hiển thị giờ và mức độ ô nhiễm. 
            - Không viết diễn giải dài dòng.
            - Không cần nhận xét.

            Các mức độ nhiễm gồm: 0: thấp, 1: trung bình, 2: cao, 3: rất cao, 4: nguy hại
            
            Ví dụ đầu ra mong muốn (nếu có dữ liệu ô nhiễm):
            Ngày 20 tháng 5 năm 2004:
            - 0h,2h,3h,4h,20h,21h,22h,23h: Ô nhiễm thấp (0)  
            - 1h,5h,8h,13h,14h: Ô nhiễm cao (2)  
            - 6h,7h,9h,10h,11h,12h: Ô nhiễm rất cao (3)  
            - 15h,16h,17h,18h,19h: Ô nhiễm mức nguy hại (4)
            """
        elif source == "predict":
            rewriting_prompt = f"""
            Hãy diễn giải kết quả này một cách ngắn gọn, chỉ nêu ra mức độ ô nhiễm (nếu có) và đưa ra lời khuyên cho người dùng về việc có nên ra ngoài hay cần áp dụng các biện pháp bảo vệ. 
            Nếu kết quả chứa khóa "pollution_level" hoặc "description", hãy sử dụng các thông tin đó để đưa ra lời khuyên. 
            Có thể viết lại lời khuyên theo các mức độ ô nhiễm như sau:
            - Nếu ô nhiễm thấp (0, "Thấp"): "Chất lượng không khí tốt là một ngày tuyệt vời để ra ngoài."
            - Nếu ô nhiễm trung bình (1, "Trung bình"): "Chất lượng không khí ổn định, nhưng hãy quan tâm bản thân khi ra ngoài."
            - Nếu ô nhiễm cao (2, "Cao"): "Chất lượng không khí kém, nên hạn chế ra ngoài và đeo khẩu trang."
            - Nếu ô nhiễm nguy hiểm (3, "Nguy hiểm"): "Chất lượng không khí rất kém, hạn chế ra ngoài và tuân thủ hướng dẫn bảo vệ sức khỏe."
            - Nếu ô nhiễm cực cao (4, "Rất nguy hại"): "Cảnh báo ô nhiễm cực cao, hãy ở nhà và thực hiện các biện pháp an toàn."

            Đưa ra kết quả theo định dạng:
            [Mức độ] - [Lời khuyên]

            Dưới đây là kết quả hệ thống:
            {result}
            """
        elif source == "insert":
            rewriting_prompt = f"""
            Thông báo cho người dùng về việc dữ liệu đã được thêm vào cơ sở dữ liệu và người dùng có thể kiểm tra lại thông tin đã thêm bằng cách thử truy vấn lại.
            """
        elif source == "stats":
            stat_type = result.get("stat_type", None)
            stats_data = result.get("result", {})

            if stat_type in ["mean", "median", "std", "max", "min"]:
                formatted_data = "\n".join([f"- {key} : {value}" for key, value in stats_data.items()])

                if stat_type == "mean":
                    rewriting_prompt = f"""
                    Ghi lại tất cả kết quả thống kê trung bình (`mean`) của các chỉ số ô nhiễm và không nhận xét:
                    {formatted_data}
                    """
                elif stat_type == "median":
                    rewriting_prompt = f"""
                     Ghi lại tất cả kết quả thống kê trung vị (`median`) của các chỉ số ô nhiễm và không nhận xét:
                    {formatted_data}
                    """
                elif stat_type == "std":
                    rewriting_prompt = f"""
                    Ghi lại tất cả kết quả độ lệch chuẩn (`std`) của các chỉ số ô nhiễm và không nhận xét:
                    {formatted_data}
                    """
                elif stat_type == "max":
                    rewriting_prompt = f"""
                    Ghi lại tất cả mức độ ô nhiễm cao nhất (`max`) được ghi nhận trong khoảng thời gian đã chọn và không nhận xét:
                    {formatted_data}
                    """

                elif stat_type == "min":
                    rewriting_prompt = f"""
                    Ghi lại tất cả mức độ ô nhiễm thấp nhất (`min`) được ghi nhận trong khoảng thời gian đã chọn và không nhận xét:
                    {formatted_data}
                    """
            elif stat_type == "count":
                total_records = stats_data.get("Total Records", 0)
                rewriting_prompt = f"""
                Viết lại tổng số bản ghi dữ liệu (`count`):{total_records}
                """
            else:

                rewriting_prompt = "Dữ liệu không hợp lệ hoặc không thể diễn giải."

        else:
            return result
        try:
            print("Rewriting Prompt:", rewriting_prompt)

            response = self.client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=500,
                messages=[{"role": "user", "content": rewriting_prompt}],
            )
            print(result)
            if hasattr(response, 'content') and isinstance(response.content, list):
                text_blocks = [block.text for block in response.content if getattr(block, 'type', None) == 'text']
                return "\n".join(text_blocks)
        except Exception as e:
            return f"Lỗi khi viết lại kết quả: {str(e)}"
        return "Không thể viết lại kết quả."

if __name__ == "__main__":
    # Validate configuration before starting
    Config.validate_config()
    
    handler = PollutionQueryHandler(Config.ANTHROPIC_API_KEY)
    prompt = input("📝 Nhập truy vấn của bạn: ")
    result = handler.call_claude_function(prompt)
    final_result = handler.rewrite_result_with_advice(result)
    print(final_result)
