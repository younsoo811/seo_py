import paho.mqtt.client as mqtt
import json
import base64
import time

import tkinter
import tkinter.ttk
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
import tkinter.font


with open("test_2.png", "rb") as  image_file:
    img_bin = image_file.read()
    encoded_str=base64.b64encode(img_bin)

    img_dic={
        "test_img":encoded_str.decode()
    }

    img_json= json.dumps(img_dic)

count=1
def pub():
    entry_time = time_entry.get()
    entry_size = size_entry.get()
    main_label['text']=str(entry_size)+"mb/s ("+str(entry_time)+"s)"

    global count
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("connected OK")
        else:
            print("Bad connection Returned code=", rc)

    # MQTT 메시지 발행 콜백 함수 (클라이언트 id, 데이터, 메시지 id)
    def on_publish(client, userdata, mid):
        print("mid= ", mid)

    # 연결 정상적으로 끊어짐 (rc=0)
    def on_disconnect(client, userdata, flags, rc=0):
        print(str(rc))


    # 새로운 클라이언트 생성
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    #client.on_publish = on_publish

    client.connect('localhost', 1883)

    for j in range(0,int(entry_time)):
        for i in range(0,3*int(entry_size)):
            # 비동기 루프 시작 (백그라운드에서 브로커와의 연결 상태 유지하고 콜백 함수 처리)
            client.loop_start() 
            #common 이라는 Topic에 json 형식(string타입)의 메시지 발행
            #client.publish('common', json.dumps({"success": "ok"+str(count)}), 1) 
            client.publish('common', img_json, 1)
            client.loop_stop() # 비동기 루프 종료
            count=count+1
        time.sleep(1)

    print(entry_size+"mb/s ("+entry_time+"s)")
    
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