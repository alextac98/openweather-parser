import json
from datetime import datetime
import pytz

if __name__ == '__main__':
    
    with open('data/BU_Weather_1971-2021.json') as file:
        raw_data = json.load(file)

        for row in raw_data:
            # Set up datetime object for easier management later
            
            time_no_tz = datetime.utcfromtimestamp(int(row.get('dt'))) # No timezone because UTC
            timezone = pytz.timezone('UTC')
            time = timezone.localize(time_no_tz)

            temp = row.get('main').get('temp')
            temp_low = row.get('main').get('temp_min')
            temp_high = row.get('temp_max')
            temp_feels = row.get('main').get('feels_like')

            pressure = row.get('main').get('pressure')
            humidity = row.get('main').get('humidity')

            wind_speed = row.get('wind').get('speed')
            wind_direction = row.get('wind').get('deg')
            
            clouds = row.get('clouds').get('all')

            rain_obj = row.get('rain')
            snow_obj = row.get('snow')

            if rain_obj is not None:
                precipitation_type = "rain"
                if rain_obj.get('1h') is not None:
                    precipitation_amount = rain_obj.get('1h')
                elif rain_obj.get('3h') is not None:
                    precipitation_amount = rain_obj.get('3h') / 3 # Divide by 3 to get avg hourly rate
                else:
                    precipitation_amount = 0
            elif snow_obj is not None:
                precipitation_type = "snow"
                if snow_obj.get('1h') is not None:
                    precipitation_amount = snow_obj.get('1h')
                elif snow_obj.get('3h') is not None:
                    precipitation_amount = snow_obj.get('3h') / 3 # Divide by 3 to get avg hourly rate
                else:
                    precipitation_amount = 0
            else:
                precipitation_type = "None"
                precipitation_amount = 0

            condition = row.get('weather')[0].get('description')

    print()

