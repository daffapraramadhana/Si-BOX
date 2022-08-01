import os
import json
import psutil
import shutil
import wmi
import pythoncom


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
    #get temp
    pythoncom.CoInitialize()
    temp = wmi.WMI(namespace="root\\wmi")
    TEMPERATURE = round((temp.MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature / 10.0)-273.15)

    value = {
        "CPU usage" : CPU_usage,
        "Memory usage" : MEMORY_used,
        "RAM usage" : RAM_used,
        "Temperature" : TEMPERATURE
    }
    return (value)

def restart():
    os.system('shutdown /r')