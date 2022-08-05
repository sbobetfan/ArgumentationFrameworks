from datetime import datetime

def save(framework, filename):
    # generate file name as current date and time
    now = datetime.now()
    date_time = now.strftime("%d_%m_%Y__%H_%M_%S")
    FILE_NAME = filename + "-" + date_time + ".txt"

    f = open(FILE_NAME, "x")
    
    for a,b in framework:
        f.write(a + "->" + b + "\n")
    f.close()
    print("Framework " + filename + " saved")
    return True
