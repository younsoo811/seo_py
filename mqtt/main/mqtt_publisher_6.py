import paho.mqtt.client as mqtt
import json
import time

import tkinter
import tkinter.ttk
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
import tkinter.font

# 백업 데이터 가져오기
entry_list=[]
with open('_internal/data/entry_data.txt', 'r') as file:
    for i in file:
        entry_list.append(i.strip())

# json 파일 읽어오기
with open('framedata.json', 'r') as json_file:
    framedata_json=json.load(json_file)
with open('event.json', 'r') as json_file:
    event_json=json.load(json_file)

count=1 # object id 값 순차적으로 증가시키기 위한 변수
check_connect=False # 서버와 연결 확인하는 변수
check_disconnect=False  # 전송이 완료되었음(서버와 정상적으로 연결이 끊어졌음)을 확인하는 변수

def pub():
    global check_connect
    global check_disconnect
    global entry_list   # 백업 데이터 저장 리스트

    # frame 관련 입력 값 가져오기
    entry_pf=profile_entry.get()
    entry_cam=camera_id_entry.get()
    # event 관련 입력 값 가져오기
    entry_pfid=profile_id_entry.get()
    entry_add=address_entry.get()
    # 전송 설정 입력 값 가져오기
    entry_time = time_entry.get()
    entry_size = size_entry.get()

    # (수정 예정)나중에 entry 값 리스트로 저장시 for문으로 돌리기
    entry_list[0]=entry_pf
    entry_list[1]=entry_cam
    entry_list[2]=entry_pfid
    entry_list[3]=entry_add
    entry_list[4]=entry_size
    entry_list[5]=entry_time
    entry_list[6]=str(check1.get())
    entry_list[7]=str(check2.get())

    # 엔트리 내용 백업
    with open('_internal/data/entry_data.txt', 'w+') as f:
        f.write('\n'.join(entry_list))


    main_label['text']="topic당 "+str(entry_size)+"개 전송 ("+str(entry_time)+"s)"

    if entry_pf=="":
        entry_pf="profile"
    if entry_cam=="":
        entry_cam="camera_id"
    if entry_pfid==None:
        entry_pfid=2
    if entry_add=="":
        entry_add="address"

    def on_connect(client, userdata, flags, rc):
        global check_connect
        if rc == 0:
            print("connected OK")
            check_connect=True
        else:
            print("Bad connection Returned code=", rc)
            check_connect=False

    # 연결 정상적으로 끊어짐 (rc=0)
    def on_disconnect(client, userdata, flags, rc=0):
        global check_disconnect
        print("disconnect: "+str(rc))
        check_disconnect=True


    # 새로운 클라이언트 생성
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    # 연결 설정 관리============================================================
    client.username_pw_set("seo_ai", "qrqvud3")
    client.connect('localhost', 1883)

    time_save=str(time.strftime("%H: %M: %S", time.localtime(time.time())))  

    client.loop_start()

    global count
    for j in range(0,int(entry_time)):  # 1초마다 설정한 횟수만큼 전송시킴 (총 전송 시간을 의미)
        start_time=time.time()
        frame_count=0
        event_count=0
        for i in range(0, int(entry_size)): # 설정한 횟수만큼 frame 또는 event를 한쌍씩 전송시킴
            if frame_count==len(framedata_json):
                frame_count=0
            if event_count==len(framedata_json):
                event_count=0
            
            # frame 1개 전송
            if check1.get()==1:
                # frame num 갱신 (1씩 증가)
                framedata_json[frame_count]["frame_num"]=count
                live_t=int(time.time())
                # event
                framedata_json[frame_count]["cam_dt"]=live_t
                framedata_json[frame_count]["ed_dt"]=live_t
                # framedata
                framedata_json[frame_count]["ntp_ts"]=live_t
                framedata_json[frame_count]["creator_ntp_ts"]=live_t
                # senders
                framedata_json[frame_count]["senders"][0]=entry_pf
                framedata_json[frame_count]["senders"][1]=entry_cam

                # 몇 개의 objects 가 들어있는지 확인
                len_dic=len(framedata_json[frame_count]["objects"])
                # 각 objects 마다 고유 id 부여
                for index in range(0, len_dic):                    
                    framedata_json[frame_count]["objects"][index]["object_id"]=str(time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())))+"_"+str(count)
                    count+=1

                print("detection 전송")
                client.publish('detection', json.dumps(framedata_json[frame_count]), 1)                
            # event 1개 전송
            if check2.get()==1:
                # event json              
                event_json[event_count]["profile_id"]=entry_pfid
                event_json[event_count]["address"]=entry_add
                event_json[event_count]["token"]=entry_pf
                event_json[event_count]["camera_id"]=entry_cam
                #전송
                print("event 전송")
                client.publish('event', json.dumps(event_json[event_count]), 1) 

            frame_count+=1
            event_count+=1


        end_time=time.time()
        pub_time= end_time-start_time
        print(str(entry_size)+"번 전송 ("+f"{pub_time: .5f} sec)")
        if pub_time<1.0:
            time.sleep(1.0-pub_time)    # 전송 시간이 1초 미만인 경우 남은 시간만큼 대기
    client.loop_stop()
    
    client.disconnect()

    # 로그 기록 변경
    if check_connect==True: # 연결 성공시
        check_label['text']="success"  
        check_time_label['text']=time_save
        check_connect=False

    if check_disconnect==True:  # 전송 성공시
        pub_label['text']="finish"
        pub_time_label['text']=str(time.strftime("%H: %M: %S", time.localtime(time.time())))
        check_disconnect=False



main_window = tkinter.Tk()
main_window.title("MQTT Publisher")
main_window.geometry("350x600+200+200")
main_window.resizable(False, False)

# 여백
main_label=tkinter.Label(main_window, text = "", height=2)
main_label.pack(side="top", expand=True, padx=5, pady=5)


sender_frame=LabelFrame(main_window, text="FrameData.json")
sender_frame.pack(side="top", expand=True, padx=5, pady=5)
tkinter.Label(sender_frame, text="senders:", width=10).grid(row=1, column=0)
# profile
profile_entry=tkinter.Entry(sender_frame, width=20)
profile_entry.grid(row=1, column= 1, padx=10)
profile_entry.insert(0, entry_list[0])
tkinter.Label(sender_frame, text="profile(token)", width=10,anchor=W).grid(row=1, column=2)
# camera_id
camera_id_entry=tkinter.Entry(sender_frame, width=20)
camera_id_entry.grid(row=2, column= 1, padx=10, pady=5)
camera_id_entry.insert(0, entry_list[1])
tkinter.Label(sender_frame, text="camera_id", width=10,anchor=W).grid(row=2, column=2)


event_frame=LabelFrame(main_window, text="event.json")
event_frame.pack(side="top", expand=True, padx=5, pady=5)
# profile_id
tkinter.Label(event_frame, text="profile_id:", width=10).grid(row=4, column=0)
profile_id_entry=tkinter.Entry(event_frame, width=20)
profile_id_entry.grid(row=4, column= 1, padx=10, pady=15)
profile_id_entry.insert(0, entry_list[2])
tkinter.Label(event_frame, text="(type->int)", width=10,anchor=W).grid(row=4, column=2)
# address
tkinter.Label(event_frame, text="address:", width=10).grid(row=5, column=0)
address_entry=tkinter.Entry(event_frame, width=20)
address_entry.grid(row=5, column= 1, padx=10, pady=15)
address_entry.insert(0, entry_list[3])

# 전송 설정 정보 출력
info_frame=LabelFrame(main_window, text="setting")
info_frame.pack(side="top", expand=True, padx=5, pady=5)

set_frame=LabelFrame(main_window, text="setting")
set_frame.pack(side="top", expand=True, padx=5, pady=5)
# 전송할 json 파일 선택
check1=IntVar()
check2=IntVar()
tkinter.Label(set_frame, text="topic:", width=10).grid(row=6, column=0)
detec_check=tkinter.Checkbutton(set_frame, text="detection", variable=check1)
detec_check.grid(row=6, column= 1, padx=10, pady=10)
event_check=tkinter.Checkbutton(set_frame, text="event", variable=check2, anchor=W)
event_check.grid(row=6, column= 2, pady=10)
# 체크 버튼 저장값 기반 설정
if int(entry_list[6])==1:
    detec_check.toggle()
if int(entry_list[7])==1:
    event_check.toggle()

# 초당 전송 수
tkinter.Label(set_frame, text="size:", width=10).grid(row=7, column=0)
size_entry=tkinter.Entry(set_frame, width=20)
size_entry.grid(row=7, column= 1, padx=10, pady=10)
size_entry.insert(0, entry_list[4])
tkinter.Label(set_frame, text="번 전송", width=10,anchor=W).grid(row=7, column=2)
# 전송 시간 설정
tkinter.Label(set_frame, text="time:", width=10).grid(row=8, column=0)
time_entry=tkinter.Entry(set_frame, width=20)
time_entry.grid(row=8, column= 1, padx=10)
time_entry.insert(0,entry_list[5])
# 전송 버튼
tkinter.Button(set_frame, text="send", width=8, command=pub).grid(row = 8, column = 2, padx = 10)

# 전송 설정 정보 출력
tkinter.Label(info_frame, text="", width=10).grid(row=6, column=0)
main_label=tkinter.Label(info_frame, text = "topic당 "+size_entry.get()+"개 전송 ("+time_entry.get()+"s)", width=20, height=2)
main_label.grid(row = 6, column = 1, padx = 10, pady = 5)
tkinter.Label(info_frame, text="", width=10,anchor=W).grid(row=6, column=2)

# 로그
log_frame=LabelFrame(main_window, text="log")
log_frame.pack(side="top", expand=True, padx=5, pady=5)
# 연결 성공 여부
tkinter.Label(log_frame, text="connect:", width=10, anchor=E, padx=10, pady=5).grid(row=0, column=0)
check_label=tkinter.Label(log_frame, text="Fail", width=15, anchor=W)
check_label.grid(row=0, column=1)
check_time_label=tkinter.Label(log_frame, text="(time)", width=20, anchor=W)
check_time_label.grid(row=0, column=2)
# 전송 성공 여부
tkinter.Label(log_frame, text="publish:", width=10, anchor=E).grid(row=1, column=0)
pub_label=tkinter.Label(log_frame, text="None", width=15, anchor=W)
pub_label.grid(row=1, column=1)
pub_time_label=tkinter.Label(log_frame, text="(time)", width=20, anchor=W)
pub_time_label.grid(row=1, column=2)

# 여백
b_label=tkinter.Label(main_window, text = "", height=2)
b_label.pack(side="top", expand=True, padx=5, pady=5)

main_window.mainloop()