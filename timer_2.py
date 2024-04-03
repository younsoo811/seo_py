from threading import Timer
import time
import keyboard
import psutil

import tkinter
import tkinter.ttk
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
import tkinter.font


min, max=100.0, 0.0
min_time, max_time="", ""
b=True
# 대기시간(출력기능 포함)
def waittingTimer(waitTime: int, msg: str = None, showPrintUnit=10):
    global min,max
    global min_time,max_time, b

    def message(i, message, msg=msg):
        global min,max
        global min_time,max_time
        if '완료' in message:
            print(f'\t[{msg} : {i}초에 {message}]')
        else:
            #print(f'\t[{msg} : {i}초 이상 {message}]')
            cpu_percent = psutil.cpu_percent(interval=1)
        
            memory = psutil.virtual_memory().used*100/psutil.virtual_memory().total

            network = psutil.net_io_counters()
            sent_bytes = network.bytes_sent / (1024 * 1024) # 송신 데이터 양을 MB 단위로 변환
            recv_bytes = network.bytes_recv / (1024 * 1024) # 수신 데이터 양을 MB 단위로 변환

            print("CPU: ", cpu_percent*10)
            print("MEM: ", memory)
            print("SEN: ", sent_bytes) # 송신
            if min>cpu_percent*10 and cpu_percent!=0.0:
                min=cpu_percent*10
                print("MIN: ", min, "=========")
                min_time=time.strftime('%Y-%m-%d %H:%M:%S')
            if max<cpu_percent*10:
                max=cpu_percent*10
                print("MAX: ", max, "=========")
                max_time=time.strftime('%Y-%m-%d %H:%M:%S')
            print("REC: ", recv_bytes, "\n") #수신


    print(f'{waitTime}초 이전에 종료하면 "ENTER"키를 누르십시오 . . .')

    flag = [True, 0]

    def timer(flag):
        while True:
            if t.finished.is_set():
                break

            if flag[1] >= waitTime:
                break

            flag[1] += 1
            if msg is not None:
                if waitTime < showPrintUnit:
                    message(flag[1], '대기중...')

                elif not (flag[1] % showPrintUnit):
                    message(flag[1], '대기중...')

            time.sleep(1)

        flag[0] = False

    def win():
        sub_window = tkinter.Tk()
        sub_window.title("Test")
        sub_window.geometry("350x200+200+200")
        sub_window.resizable(False, False)

        sub_main_label=tkinter.Label(sub_window, text = "checking...", height=2)
        sub_main_label.grid(row = 0, column = 2, padx = 10, pady = 5)
        tkinter.Button(sub_window, text="stop", width=8, command=lambda:[sub_window.destroy(), but()]).grid(row = 2, column = 2, padx = 10)
        sub_window.mainloop()

    def but():
        global b
        b=False
        

    startTimer = False
    while flag[0]:
        if keyboard.is_pressed('enter'):
            print('Enter키를 눌러 프로그램을 종료합니다.')
            t.cancel()
            t2.cancel()
            break

        if b==False:
            print('Enter키를 눌러 프로그램을 종료합니다.')
            t.cancel()
            t2.cancel()
            break

        if not startTimer:
            print("start_timer")
            t = Timer(0, timer, args=(flag,))
            t2 = Timer(1, win, args=())
            t.start()
            t2.start()
            startTimer = True
		
        # 과부하 방지를 위함
        time.sleep(.01)

    #t.cancel()
    #t2.cancel()
    message(flag[1], '완료!')
    min_cpu['text']= "CPU-MIN: "+str(min)
    max_cpu['text']= "CPU-MAX: "+str(max)
    min_label['text']="TIME: "+min_time
    max_label['text']="TIME: "+max_time
    min, max =100.0, 0.0
    min_time, max_time="",""
    b=True
    return True


if __name__ == '__main__':
    main_window = tkinter.Tk()
    main_window.title("Test")
    main_window.geometry("350x200+200+200")
    main_window.resizable(False, False)

    min_cpu=tkinter.Label(main_window, text = "MIN: 0.0",anchor=W, width=15 ,height=2)
    min_cpu.grid(row = 0, column = 1, padx = 10, pady = 5)
    max_cpu=tkinter.Label(main_window, text = "MAX: 0.0",anchor=W,width=15, height=2)
    max_cpu.grid(row = 1, column = 1, padx = 10, pady = 5)

    min_label=tkinter.Label(main_window, text = "test", height=2)
    min_label.grid(row = 0, column = 2, padx = 10, pady = 5)
    max_label=tkinter.Label(main_window, text = "test", height=2)
    max_label.grid(row = 1, column = 2, padx = 10, pady = 5)
    tkinter.Button(main_window, text="start", width=8, command=lambda: waittingTimer(100, '테스트', 1)).grid(row = 2, column = 2, padx = 10)
    main_window.mainloop()
    #waittingTimer(10, '테스트', 1)