from ds18b20 import DS18B20

read = DS18B20.get_all_sensors()

for sensor in read:
    print(sensor.get_id())
