import json
import psutil
import shutil



#temperature
# w = wmi.WMI(namespace="root\wmi")
# temperature_info = w.MSAcpi_ThermalZoneTemperature()[0]
# print (temperature_info.CurrentTemperature)

#CPU usage
def check_monitor():
    bytesperGB = 1024 * 1024 * 1024
    
    path = 'C:/Users'
    CPU_usage = psutil.cpu_percent()
    (total, used, free) = shutil.disk_usage(path)
    MEMORY_used = {
        "Total" : round((total)/bytesperGB,2),
        "Used" : round((used)/bytesperGB,2),
        "Free" : round((free)/bytesperGB,2)
    }
    RAM_used = psutil.virtual_memory()[2]
    
    value = {
        "CPU usage" : CPU_usage,
        "Memory usage" : MEMORY_used,
        "RAM usage" : RAM_used
    }
    return (value)

#
#
# CPU Temp --REQUIRES CPU TEMPERATURE TO BE RUNNING!--
#
a = check_monitor()

print (a)