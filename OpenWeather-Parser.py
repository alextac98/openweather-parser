import json
import csv
from datetime import datetime, timedelta
import pytz
import xlrd
# import pandas as pd

start_year = 2000
end_year = 2020

output_timezone = pytz.timezone('US/Eastern')

fields =   ['Year', 
            'Month', 
            'Day', 
            'Hour', 
            'Minute', 

            'Car Data',

            'Temperature [C]', 
            'Pressure [hPa]', 
            'Humidity [%]', 
            'Wind Speed [km/h]',
            'Wind Direction [deg]', 
            'Cloud Cover [%]', 
            'Precipitation Type', 
            'Precipitation Amount [cm]', 

            'CO2 ppm',
            'Std dev CO2',
            'No. CO2 Measurements'
        ]

if __name__ == '__main__':
    
    with open('data/BU_Weather_1971-2021.json') as file:
        raw_data = json.load(file)

    # Set up new data store dict
    weather_data = {}

    for row in raw_data:
        # Set up datetime object for easier management later
        
        time_no_tz = datetime.utcfromtimestamp(int(row.get('dt'))) # No timezone because UTC
        timezone = pytz.timezone('UTC')
        time = timezone.localize(time_no_tz).astimezone(output_timezone)

        temp = row.get('main').get('temp')
        temp_low = row.get('main').get('temp_min')
        temp_high = row.get('main').get('temp_max')
        temp_feels = row.get('main').get('feels_like')

        pressure = row.get('main').get('pressure')
        humidity = row.get('main').get('humidity')

        wind_speed = row.get('wind').get('speed') * 3.6
        wind_direction = row.get('wind').get('deg')
        
        cloud_cover = row.get('clouds').get('all')

        rain_obj = row.get('rain')
        snow_obj = row.get('snow')

        if rain_obj is not None:
            precipitation_type = "rain"
            if rain_obj.get('1h') is not None:
                precipitation_amount = rain_obj.get('1h') * 10 # mm to cm
            elif rain_obj.get('3h') is not None:
                precipitation_amount = rain_obj.get('3h') * 10 / 3 # Divide by 3 to get avg hourly rate
            else:
                precipitation_amount = 0
        elif snow_obj is not None:
            precipitation_type = "snow"
            if snow_obj.get('1h') is not None:
                precipitation_amount = snow_obj.get('1h') * 10 # mm to cm
            elif snow_obj.get('3h') is not None:
                precipitation_amount = snow_obj.get('3h') * 10 / 3 # Divide by 3 to get avg hourly rate
            else:
                precipitation_amount = 0
        else:
            precipitation_type = "None"
            precipitation_amount = 0

        condition = row.get('weather')[0].get('description')

        weather_data[time] = {
            "temp": temp,
            "temp_low": temp_low,
            "temp_high": temp_high,
            "pressure": pressure,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "wind_direction": wind_direction,
            "cloud_cover": cloud_cover,
            "precipitation_type": precipitation_type,
            "precipitation_amount": precipitation_amount,
            "condition": condition
        }

        if time.month == 12 and time.day == 31 and time.hour == 23:
            print("Finished parsing " + time.strftime('%Y'))

    co2_data = {}

    with open('data/NACP_PROJECT_BU.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        i = 3

        for row in csv_reader:
            if i != 0:
                i -= 1
                continue
            
            # Import time
            time_no_tz = datetime.utcfromtimestamp(int(row[0])) # No timezone because UTC
            timezone = pytz.timezone('UTC')
            time = timezone.localize(time_no_tz).astimezone(output_timezone)

            c02 = None if float(row[2]) == -9999 else float(row[2]) 
            std_dev = None if float(row[3]) == -9999 else float(row[3])
            n = None if int(row[4]) == -9999 else int(row[4])

            uncertainty = int(row[5])
            lat = float(row[6])
            longitude = float(row[7])
            elevation = float(row[8])
            inlet_height = float(row[9])
            
            co2_data[time] = {
                'co2_ppm': c02,
                'std_dev': std_dev,
                'num_of_measurements': n
            }

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

        file_name = f"data/car_data/MonthlyVolumeReport_AET13_{m}_{y}.xlsx" 

        wb = xlrd.open_workbook(file_name)
        sheet = wb.sheet_by_index(0)

        data = []

        for i in range(10, sheet.nrows):
            data.append(sheet.row_values(rowx=i, start_colx=1, end_colx=25))

        for row in range(len(data)):
            for col in range(len(data[row])):
                date = datetime(year=y, month=m, day=row+1, hour=col)
                car_data[output_timezone.localize(date)]= data[row][col]
    
    final_data = []
    final_data.append(fields)

    for key, value in car_data.items():
        year = key.year
        month = key.month
        day = key.day
        hour = key.hour
        minute = key.minute

        car_num = value

        weather = weather_data[key + timedelta(hours=-1)]

        co2 = co2_data.get(key, {})
        
        final_data.append([
            year,
            month,
            day,
            hour,
            minute,
            car_num,
            weather.get('temp'),
            weather.get('pressure'),
            weather.get('humidity'),
            weather.get('wind_speed'),
            weather.get('wind_direction'),
            weather.get('cloud_cover'),
            weather.get('precipitation_type'),
            weather.get('precipitation_amount'),
            co2.get('co2_ppm'),
            co2.get('std_dev'),
            co2.get('num_of_measurements')
        ])
    
    with open('final_data.csv', 'w') as file:
        write = csv.writer(file)
        write.writerows(final_data)
