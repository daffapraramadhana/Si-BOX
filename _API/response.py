import time

def start_time():
    startTime = time.time_ns()
    return(startTime)

def end_time():
    endTime = time.time_ns()
    return(endTime)

def latency(s, e):
    latency = str(float(e - s)//1000000)
    return(latency)
    

def res(param):
    
    response = {
        "code" : "0",
        "latency" : "time",
        "message" : "Success",
        "param" : "None"
    }

    if param == 0:
        response["code"] = "0"
        response["message"] = "Success"
        return (response)

    elif param ==  100:
        response["code"] = "100"
        response["message"] = "ERROR. Missing Parameter"
        return(response)

    elif param == 400:
        response["code"] = "400"
        response["message"] = "ERROR. Missing Object"
        return (response)
    
    return (response)






