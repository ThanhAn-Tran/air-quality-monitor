from cassandra.cluster import Cluster
import pandas as pd

import uuid

from tensorboard.compat.tensorflow_stub.dtypes import double


class PollutionDataProcessor:
    def __init__(self, cluster_ips, keyspace, csv_path=None):
        self.cluster = Cluster(cluster_ips)
        self.session = self.cluster.connect(keyspace)
        self.csv_path = csv_path
        self.keyspace = keyspace

    def read_csv(self):
        if self.csv_path:
            return pd.read_csv(self.csv_path)
        raise ValueError("CSV path is not provided.")

    def insert_data(self, df):
        query = """
        INSERT INTO pollution_data (id, Day, Month, Year, Hour, PT08_S1_CO, C6H6_GT, PT08_S5_O3, PT08_S2_NMHC, PT08_S4_NO2, AQI_Label)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        for index, row in df.iterrows():
            try:
                self.session.execute(query, (
                    uuid.uuid4(),int(row["Day"]),int(row["Month"]),
                    int(row["Year"]),int(row["Hour"]), float(row["PT08.S1(CO)"]),
                    float(row["C6H6(GT)"]),float(row["PT08.S5(O3)"]),float(row["PT08.S2(NMHC)"]),
                    float(row["PT08.S4(NO2)"]),float(row["AQI_Label"])
                ))
            except Exception as e:
                print(f"Lỗi khi thêm dòng {index}: {e}")


    def query_pollution_data(self, year=None, month=None, day=None, hour=None):
        query = 'SELECT hour,AQI_Label,day,month,year FROM pollution_db.pollution_data'
        conditions = []
        params = []
        if year is not None:
            conditions.append('year = %s')
            params.append(year)
        if month is not None:
            conditions.append('month = %s')
            params.append(month)
        if day is not None:
            conditions.append('day = %s')
            params.append(day)
        if hour is not None:
            conditions.append('hour = %s')
            params.append(hour)
        if conditions:
            query += " WHERE " + " AND ".join(conditions) + " ALLOW FILTERING"
        try:
            rows = self.session.execute(query, params) if params else self.session.execute(query)
            return pd.DataFrame(rows)
        except Exception as e:
            print(f"Lỗi khi truy vấn dữ liệu: {e}")
            return pd.DataFrame()

    def insert_data_row_by_one(self, df):
        query = """
        INSERT INTO pollution_data (id, Day, Month, Year, Hour, PT08_S1_CO, C6H6_GT, PT08_S5_O3, PT08_S2_NMHC, PT08_S4_NO2, AQI_Label)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        for index, row in df.iterrows():
            try:
                self.session.execute(query, (
                    uuid.uuid4(),int(row["Day"]),int(row["Month"]),
                    int(row["Year"]),  int(row["Hour"]), float(row["PT08.S1(CO)"]),
                    float(row["C6H6(GT)"]),float(row["PT08.S5(O3)"]),float(row["PT08.S2(NMHC)"]),
                    float(row["PT08.S4(NO2)"]),float(row["AQI_Label"])
                ))
                print(f"Dữ liệu {row['Year']}-{row['Month']}-{row['Day']} {row['Hour']}h đã được chèn!")
            except Exception as e:
                print(f"Lỗi khi thêm dòng {index}: {e}")

    def add_pollution_data_from_nlp(self, PT08_S1_CO, C6H6_GT, PT08_S5_O3, PT08_S2_NMHC, PT08_S4_NO2, AQI_Label,
                                    Year, Month, Day, Hour):
        data = {
            "pt08_s1_co": float(PT08_S1_CO),
            "c6h6_gt": float(C6H6_GT),
            "pt08_s5_o3": float(PT08_S5_O3),
            "pt08_s2_nmhc": float(PT08_S2_NMHC),
            "pt08_s4_no2": float(PT08_S4_NO2),
            "aqi_label": float(AQI_Label),
            "year": int(Year),
            "month": int(Month),
            "day": int(Day),
            "hour": int(Hour)
        }

        check_query = """
        SELECT id FROM pollution_data WHERE Year=%s AND Month=%s AND Day=%s AND Hour=%s LIMIT 1 ALLOW FILTERING
        """
        existing = self.session.execute(check_query, (data["year"], data["month"], data["day"], data["hour"]))

        if existing.one() is None:
            df = pd.DataFrame([data])
            self.insert_data_row_by_one(df)
            print(" Dữ liệu từ NLP đã được thêm thành công!")
            return "inserted"
        else:
            print(f" Dữ liệu tại {data['year']}-{data['month']}-{data['day']} {data['hour']}h đã tồn tại, bỏ qua.")
            return "exists"

    def query_pollution_data_for_stats(self, time_range):
        session = self.cluster.connect(self.keyspace)

        query = """
            SELECT pt08_s1_co,c6h6_gt,pt08_s5_o3,pt08_s2_nmhc,pt08_s4_no2,aqi_label FROM pollution_data 
            WHERE year = %s 
            AND month >= %s AND month <= %s 
            AND day >= %s AND day <= %s
            ALLOW FILTERING
        """
        rows = session.execute(query, (time_range['year'], time_range['start_month'],
                                       time_range['end_month'], time_range['start_day'],
                                       time_range['end_day']))
        return list(rows)

    def close_connection(self):
        self.cluster.shutdown()

#if __name__ == "__main__":
    #processor = PollutionDataProcessor(["127.0.0.1"], "pollution_db", "Data/processed_AQI_data.csv")
    #data = processor.read_csv()
    #processor.insert_data(data)
    #print("Dữ liệu đã thêm thành công!")
    #processor.close_connection()
