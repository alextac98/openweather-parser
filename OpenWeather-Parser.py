import json

if __name__ == '__main__':
    
    with open('data/BU_Weather_1971-2021.json') as file:
        raw_data = json.load(file)

        for hour in raw_data:
            print()

    print()

