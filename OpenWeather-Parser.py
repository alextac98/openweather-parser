import json
import csv
from datetime import datetime
import pytz

start_year = 2000
end_year = 2020

output_timezone = pytz.timezone('US/Eastern')

fields =   ['Year', 
            'Month', 
            'Day', 
            'Hour', 
            'Minute', 
            'Temperature [C]', 
            # 'Low Temperature [C]', 
            # 'High Temperature [C]', 
            'Pressure [hPa]', 
            'Humidity [%]', 
            'Wind Speed [km/h]',
            'Wind Direction [deg]', 
            'Cloud Cover [%]', 
            'Precipitation Type', 
            'Precipitation Amount [cm]', 
            # 'Condition Description'
        ]

if __name__ == '__main__':
    
    with open('data/BU_Weather_1979-2021.json') as file:
        raw_data = json.load(file)

    # Set up new data store dict
    weather_data = {}

    # for row in raw_data:
    #     # Set up datetime object for easier management later
        
    #     time_no_tz = datetime.utcfromtimestamp(int(row.get('dt'))) # No timezone because UTC
    #     timezone = pytz.timezone('UTC')
    #     time = timezone.localize(time_no_tz).astimezone(output_timezone)

    #     temp = row.get('main').get('temp')
    #     temp_low = row.get('main').get('temp_min')
    #     temp_high = row.get('main').get('temp_max')
    #     temp_feels = row.get('main').get('feels_like')

    #     pressure = row.get('main').get('pressure')
    #     humidity = row.get('main').get('humidity')

    #     wind_speed = row.get('wind').get('speed') * 3.6
    #     wind_direction = row.get('wind').get('deg')
        
    #     cloud_cover = row.get('clouds').get('all')

    #     rain_obj = row.get('rain')
    #     snow_obj = row.get('snow')

    #     if rain_obj is not None:
    #         precipitation_type = "rain"
    #         if rain_obj.get('1h') is not None:
    #             precipitation_amount = rain_obj.get('1h') * 10 # mm to cm
    #         elif rain_obj.get('3h') is not None:
    #             precipitation_amount = rain_obj.get('3h') * 10 / 3 # Divide by 3 to get avg hourly rate
    #         else:
    #             precipitation_amount = 0
    #     elif snow_obj is not None:
    #         precipitation_type = "snow"
    #         if snow_obj.get('1h') is not None:
    #             precipitation_amount = snow_obj.get('1h') * 10 # mm to cm
    #         elif snow_obj.get('3h') is not None:
    #             precipitation_amount = snow_obj.get('3h') * 10 / 3 # Divide by 3 to get avg hourly rate
    #         else:
    #             precipitation_amount = 0
    #     else:
    #         precipitation_type = "None"
    #         precipitation_amount = 0

    #     condition = row.get('weather')[0].get('description')

    #     weather_data[time] = {
    #         "temp": temp,
    #         "temp_low": temp_low,
    #         "temp_high": temp_high,
    #         "pressure": pressure,
    #         "humidity": humidity,
    #         "wind_speed": wind_speed,
    #         "wind_direction": wind_direction,
    #         "cloud_cover": cloud_cover,
    #         "precipitation_type": precipitation_type,
    #         "precipitation_amount": precipitation_amount,
    #         "condition": condition
    #     }

    #     if time.month == 12 and time.day == 31 and time.hour == 23:
    #         print("Finished parsing " + time.strftime('%Y'))

    co2_data = {}

    # with open('data/NACP_PROJECT_BU.csv') as csv_file:
    #     csv_reader = csv.reader(csv_file)
    #     i = 3

    #     for row in csv_reader:
    #         if i != 0:
    #             i -= 1
    #             continue
            
    #         # Import time
    #         time_no_tz = datetime.utcfromtimestamp(int(row[0])) # No timezone because UTC
    #         timezone = pytz.timezone('UTC')
    #         time = timezone.localize(time_no_tz).astimezone(output_timezone)

    #         c02 = float(row[2])
    #         std_dev = float(row[3])
    #         n = int(row[4])

    #         uncertainty = int(row[5])
    #         lat = float(row[6])
    #         long = float(row[7])
    #         elevation = float(row[8])
    #         inlet_height = float(row[9])
            
    #         co2_data[time] = {
    #             'c02_ppm': c02,
    #             'std_dev': std_dev,
    #             'num_of_measurements': n
    #         }

    car_data = {}

    y = 2016
    m = 11

    y_final = 2020
    m_final = 12

    while y != y_final or m != m_final:
        if m == 12:
            m = 1
            y += 1
        else:
            m += 1

        file_name = f"MonthlyVolumeReport_AET13_{m}_{y}.xlsx" 
        continue
    
    print()


    # for year in range(start_year, end_year + 1, 1):
    #     file_loc = "output/"
    #     file_name = 'BU_Weather_' + str(year) + ".csv"
    #     with open(file_loc + file_name, 'w') as file:
    #         write = csv.writer(file)
    #         write.writerow(fields)
    #         write.writerows(final_data.get(year))
