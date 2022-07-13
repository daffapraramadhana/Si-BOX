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
    

def response(re):

    if re == 0:
        response["code"] = "0"
        response["message"] = "OK. Success"

    elif re ==  100:
        response["code"] = "100"
        response["message"] = "ERROR. Missing response"
        return(response)

    elif re == 101:
        response["code"] = "101"
        response["message"] = "ERROR. Missing parameter"

    return (response)






