#   part 1: Administrator authentication

import os
from platform import system

if(system() == "Windows"):
    import ctypes
    if(ctypes.windll.shell32.IsUserAnAdmin() == False):
        print("Permission denied")
        exit()

elif(system() == "Linux"):
    if(os.geteuid() != 0):
        print("Permission denied")
        exit()
else:
    print("Unsupported platform")
    exit()


#   part 2: Setting the loggor and create log directory

from logging import StreamHandler, handlers, getLogger, INFO, Formatter

if(os.path.isdir(os.path.join(os.path.dirname(__file__), "log")) == False):
    os.mkdir(os.path.join(os.path.dirname(__file__), "log"))

SYS_TM_log_handler = handlers.TimedRotatingFileHandler(os.path.join(os.path.dirname(
    __file__), "log", "sys_time_changing.log"), when='D', interval=1, backupCount=365*10*3)
SYS_TM_log_handler.setFormatter(Formatter(
    "%(asctime)s [%(levelname)s] thread(%(thread)d-%(threadName)s) %(pathname)s : %(module)s - %(funcName)s\n%(message)s\n"))

SYS_TM_console_handler = StreamHandler()


logger = getLogger(__file__)
logger.setLevel(INFO)
logger.addHandler(SYS_TM_log_handler)
logger.addHandler(SYS_TM_console_handler)


#   part 3: Define the function for changing sys time by command [date -s ...]

from time import strftime, localtime
def change_sys_time(year, month, day, hour, min, sec):
    before_change_time = strftime("%Y-%m-%d %H:%M:%S %A", localtime())

    if(system() == "Linux"):
        # date -s "2018-05-24 16:36:00"
        os.system('date -s "%d-%d-%d %02d:%02d:%02d"' % (year, month, day, hour, min, sec))
    elif(system() == "Windows"):
        os.system("date %d/%d/%d && time %02d:%02d:%02d" % (year, month, day, hour, min, sec))
    else:
        print("Unsupported platform")
        return None
    
    after_change_time = strftime("%Y-%m-%d %H:%M:%S %A", localtime())
    global logger
    logger.info("Change time from [%s] to [%s]." % (before_change_time,after_change_time))
    



if __name__ == "__main__":
    change_sys_time(2020,12,9,5,32,16)