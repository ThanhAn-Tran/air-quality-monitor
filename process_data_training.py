import pandas as pd

class AQIProcessor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(self.input_file, sep=";", decimal=',', encoding='utf-8')

    def process_time(self):
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d/%m/%Y')
        self.df['Year'] = self.df['Date'].dt.year
        self.df['Month'] = self.df['Date'].dt.month
        self.df['Day'] = self.df['Date'].dt.day
        self.df['DayOfWeek'] = self.df['Date'].dt.dayofweek
        self.df = self.df.dropna(subset=['Time'])
        self.df['Hour'] = self.df['Time'].astype(str).str[:2].astype(int)
        self.df.drop(columns=['Date', 'Time'], inplace=True)
        self.df.insert(0, 'id', range(1, len(self.df) + 1))

    def fill_missing_values(self):
        columns_to_fill = ['PT08.S1(CO)', 'PT08.S4(NO2)', 'PT08.S5(O3)', 'C6H6(GT)','PT08.S2(NMHC)']
        for col in columns_to_fill:
            mean_value = self.df.loc[self.df[col] != -200, col].mean()

            self.df[col] = self.df[col].replace(-200, mean_value)

            self.df[col].fillna(mean_value, inplace=True)

    def calculate_aqi(self, conc, breakpoints):
        for i in range(len(breakpoints) - 1):
            if breakpoints[i][0] <= conc <= breakpoints[i + 1][0]:
                aqi = ((breakpoints[i + 1][1] - breakpoints[i][1]) /
                       (breakpoints[i + 1][0] - breakpoints[i][0])) * (conc - breakpoints[i][0]) + breakpoints[i][1]
                return round(aqi)

        return breakpoints[-1][1]

    def calculate_all_aqi(self):
        co_breakpoints = [(0, 0), (941, 50), (1075, 100), (1221, 150), (1407, 200), (1704, 300)]
        no2_breakpoints = [(0, 0), (1242, 50), (1456, 100), (1662, 150), (1886, 200), (2349, 300)]
        o3_breakpoints = [(0, 0), (742, 50), (983, 100), (1255, 150), (1577, 200), (2086, 300)]

        self.df['AQI_CO'] = self.df['PT08.S1(CO)'].apply(lambda x: self.calculate_aqi(x, co_breakpoints))
        self.df['AQI_NO2'] = self.df['PT08.S4(NO2)'].apply(lambda x: self.calculate_aqi(x, no2_breakpoints))
        self.df['AQI_O3'] = self.df['PT08.S5(O3)'].apply(lambda x: self.calculate_aqi(x, o3_breakpoints))

        self.df['AQI'] = self.df[['AQI_CO', 'AQI_NO2', 'AQI_O3']].max(axis=1)

        # Thay thế giá trị None bằng giá trị trung bình
        self.df['AQI'].fillna(self.df['AQI'].mean(), inplace=True)

    def label_aqi(self):
        def categorize_aqi(aqi):
            if aqi <= 50:
                return 0  # Tốt
            elif aqi <= 100:
                return 1  # Trung bình
            elif aqi <= 150:
                return 2  # Không tốt cho nhóm nhạy cảm
            elif aqi <= 200:
                return 3  # Không tốt
            else:
                return 4  # Rất xấu

        self.df['AQI_Label'] = self.df['AQI'].apply(categorize_aqi)

    def save_data(self):
        self.df[['Day', 'Month', 'Year','Hour','PT08.S1(CO)','C6H6(GT)','PT08.S5(O3)','PT08.S2(NMHC)','PT08.S4(NO2)','AQI_Label']].to_csv(self.output_file, index=False)
        print("AQI data with labels saved successfully!")

    def process(self):
        self.load_data()
        self.process_time()
        self.fill_missing_values()
        self.calculate_all_aqi()
        self.label_aqi()
        self.save_data()


if __name__ == "__main__":
    processor = AQIProcessor("Data/AirQuality1.csv", "Data/processed_AQI_data.csv")
    processor.process()
