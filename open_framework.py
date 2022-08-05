from os import listdir
from os.path import isfile, join

def sort_by_key(file):
    return((file[0],file[1]))

def get_files():
    global returned_files, actual_filenames
    returned_files = []
    actual_filenames = []
    onlyfiles = [f for f in listdir("./") if isfile(join("./", f))]
    counter=0
    for file in onlyfiles:
        try:
            parts = file.split(".")
            if "txt" in parts:
                actual_filenames.append(file)
                name = parts[0].split("-")
                title = name[0]
                date_time = name[1].split("__")
                date = date_time[0].replace("_","/")
                time = date_time[1].replace("_", ":")
                
                returned_files.append((date, time, title, counter))
                counter+=1
                # now format the date and time to be readable to user.
                # each element in returned_files is of format
                # (readable name, readable date, readable time, actual file name)
        except:
            pass

    returned_files.sort(reverse=True, key=sort_by_key)
    return returned_files

def get_file(index):
    # print("index")
    # print(index)
    file = open(list(actual_filenames)[index], "r")
    file_contents = file.read()

    return file_contents
    # open file, return contents
