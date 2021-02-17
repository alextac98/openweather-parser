import json
import csv
from datetime import datetime
import pytz

start_year = 2000
end_year = 2020

output_timezone = pytz.timezone('US/Eastern')

fields =   ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Temperature [C]', 'Low Temperature [C]', 'High Temperature [C]', 'Pressure [hPa]', 'Humidity [%]', 'Wind Speed [km/h]',
            'Wind Direction [deg]', 'Cloud Cover [%]', 'Precipitation Type', 'Precipitation Amount [cm]', 'Condition Description']

if __name__ == '__main__':
    
    with open('data/BU_Weather_1979-2021.json') as file:
        raw_data = json.load(file)

    # Set up new data store dict
    final_data = {}

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

        if time.year not in final_data:
            final_data[time.year] = []

        final_data.get(time.year).append([
            time.strftime("%Y"),
            time.strftime("%m"),
            time.strftime("%d"),
            time.strftime("%H"),
            time.strftime("%M"),
            temp,
            temp_low,
            temp_high,
            pressure,
            humidity,
            wind_speed,
            wind_direction,
            cloud_cover,
            precipitation_type,
            precipitation_amount,
            condition              
        ])
        if time.month == 12 and time.day == 31 and time.hour == 23:
            print("Finished parsing " + time.strftime('%Y'))

    for year in range(start_year, end_year + 1, 1):
        file_loc = "output/"
        file_name = 'BU_Weather_' + str(year) + ".csv"
        with open(file_loc + file_name, 'w') as file:
            write = csv.writer(file)
            write.writerow(fields)
            write.writerows(final_data.get(year))
