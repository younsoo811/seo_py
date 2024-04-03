import paho.mqtt.client as mqtt
import json
import time

import tkinter
import tkinter.ttk
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
import tkinter.font

def pub():
    entry_time = time_entry.get()
    entry_size = size_entry.get()
    main_label['text']=str(entry_size)+"mb/s ("+str(entry_time)+"s)"

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("connected OK")
        else:
            print("Bad connection Returned code=", rc)

    # 연결 정상적으로 끊어짐 (rc=0)
    def on_disconnect(client, userdata, flags, rc=0):
        print("disconnect: "+str(rc))


    # 새로운 클라이언트 생성
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.connect('localhost', 1883)

    client.loop_start()
    for j in range(0,int(entry_time)):
        count=1
        start_time=time.time()
        for i in range(0,int(entry_size)):
            #client.loop_start() 
            json_dic={"success":str(count), "packet_num":str(entry_size)}
            client.publish('common', json.dumps(json_dic), 1) 
            #client.loop_stop() # 비동기 루프 종료
            count=count+1

        #client.loop_start() 
        json_dic={"success":"end", "packet_num":str(entry_size)}
        client.publish('common', json.dumps(json_dic), 1) 
        #client.loop_stop()

        end_time=time.time()
        pub_time= end_time-start_time
        print(str(count)+"회 전송 ("+f"{pub_time: .5f} sec)")
        if pub_time<1.0:
            time.sleep(1.0-pub_time)
    client.loop_stop()
    
    client.disconnect()


main_window = tkinter.Tk()
main_window.title("MQTT Publisher")
main_window.geometry("350x200+200+200")
main_window.resizable(False, False)

#str_text=StringVar()
tkinter.Label(main_window, text="size:", width=10, height=5).grid(row=1, column=0)
size_entry=tkinter.Entry(main_window, width=20)
size_entry.grid(row=1, column= 1, padx=10)
size_entry.insert(0, "1")
tkinter.Label(main_window, text=" * 1 (mb/s)", width=10, height=5).grid(row=1, column=2)

tkinter.Label(main_window, text="time:", width=10).grid(row=2, column=0)
time_entry=tkinter.Entry(main_window, width=20)
time_entry.grid(row=2, column= 1, padx=10)
time_entry.insert(0,"1")
tkinter.Button(main_window, text="send", width=8, command=pub).grid(row = 2, column = 2, padx = 10)

main_label=tkinter.Label(main_window, text = size_entry.get()+"mb/s ("+time_entry.get()+"s)", height=2)
main_label.grid(row = 0, column = 1, padx = 10, pady = 5)
main_window.mainloop()