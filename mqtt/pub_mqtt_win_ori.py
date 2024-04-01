import paho.mqtt.client as mqtt
import json

import tkinter
import tkinter.ttk
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
import tkinter.font

count=1
def pub():
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
    client.on_publish = on_publish

    client.connect('localhost', 1883)
    for i in range(0,5):
        # 비동기 루프 시작 (백그라운드에서 브로커와의 연결 상태 유지하고 콜백 함수 처리)
        client.loop_start() 
        #common 이라는 Topic에 json 형식(string타입)의 메시지 발행
        client.publish('common', json.dumps({"success": "ok"+str(count)}), 1) 
        client.loop_stop() # 비동기 루프 종료
        count=count+1

    client.disconnect()

main_window = tkinter.Tk()
main_window.title("MQTT Publisher")
main_window.geometry("350x200+200+200")
main_window.resizable(False, False)

tkinter.Label(main_window, text = "", height=2).grid(row = 0, column = 1, padx = 10, pady = 10)
tkinter.Button(main_window, text="send", width=8, command=pub).grid(row = 2, column = 2, padx = 110, pady = 10)

main_window.mainloop()