from ds18b20 import DS18B20

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

sensors_q = ["03172455d7ff", "0317243e28ff", "03172459f6ff", "0317243c31ff"]
ss = []
sensors = DS18B20.get_all_sensors()
for sensor in sensors:
	ss.append(sensor.get_id())

print(sensors_q)
print(ss)
print(diff(sensors_q, ss))
