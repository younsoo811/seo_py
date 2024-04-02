import psutil
import matplotlib.pyplot as plt
import time

import tkinter
import tkinter.ttk
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
import tkinter.font

from threading import Timer
import keyboard

min=0.0
max=0.0

# CPU 사용량 모니터링
def monitor_cpu():
    global min,max
    while True:
        user_in=input()
        if user_in=='q':
            break
        cpu_percent = psutil.cpu_percent(interval=1)
        
        memory = psutil.virtual_memory().used*100/psutil.virtual_memory().total

        network = psutil.net_io_counters()
        sent_bytes = network.bytes_sent / (1024 * 1024) # 송신 데이터 양을 MB 단위로 변환
        recv_bytes = network.bytes_recv / (1024 * 1024) # 수신 데이터 양을 MB 단위로 변환

        print("CPU: ", cpu_percent*10)
        print("MEM: ", memory)
        print("SEN: ", sent_bytes)
        print("REC: ", recv_bytes, "\n")
        if min>cpu_percent*10:
            min=cpu_percent*10
            print("MIN: ", min, "=========")
        elif max<cpu_percent*10:
            max=cpu_percent*10
            print("MAX: ", max, "=========")
        main_label['text']="-MIN: "+str(min)+" -MAX: "+str(max)
        print(time.time())
    print("MIN: ", min, "=========")
    print("MAX: ", max, "=========")


# 사용 예시
if __name__ == "__main__":
    interval = 1 # 업데이트 간격 (초 단위)

    main_window = tkinter.Tk()
    main_window.title("MQTT Publisher")
    main_window.geometry("350x200+200+200")
    main_window.resizable(False, False)

    main_label=tkinter.Label(main_window, text = "test", height=2)
    main_label.grid(row = 0, column = 1, padx = 10, pady = 5)
    tkinter.Button(main_window, text="start", width=8, command=monitor_cpu).grid(row = 2, column = 2, padx = 10)
    main_window.mainloop()
    # monitor_memory(interval)
    # monitor_disk(interval)
    # monitor_network(interval)