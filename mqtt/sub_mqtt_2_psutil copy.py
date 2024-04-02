import paho.mqtt.client as mqtt
import json
import psutil

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)

# 연결 정상적으로 끊어짐 (rc=0)
def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))

# 토픽에 성공적으로 구독 (메시지 id와 Qos레벨 출력)
def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + "qos: " + str(granted_qos))

count_num=0
p_num=0
cpu_p=0.0
mem_p=0.0
tot=0
tot_count=0
# 새로운 메시지 도착했을때 호출됨 (메시지 본문 문자열로 디코딩하고, dic 타입으로 가져옴 )
def on_message(client, userdata, msg):
    global count_num
    global p_num
    global cpu_p
    global mem_p
    global tot
    global tot_count

    json_dic=json.loads(str(msg.payload.decode("utf-8")))
    #print(json_dic["success"])
    #print("=", end="")
    if json_dic["success"]=="end":
        p_num=int(json_dic["packet_num"])
        print(str(count_num)+"=="+str(p_num)+"==============================\n")
        print("CPU - MAX: "+str(cpu_p))
        print("CPU - AVG: "+str(tot/tot_count))
        print("RAM - MAX: ", f"{mem_p:.1f}")
        count_num=0
        cpu_p=0.0
        mem_p=0.0
        tot=0
    else:
        count_num=count_num+1
        print(count_num)
        cpu_live=psutil.cpu_percent()
        if cpu_live>0.0:
            print("=",cpu_live)
            tot=tot+cpu_live
            tot_count=tot_count+1
            if cpu_p<cpu_live:
                cpu_p=cpu_live
    mem_live=(psutil.virtual_memory().used*100)/psutil.virtual_memory().total
    if mem_p<mem_live:
        mem_p=mem_live
    

# 새로운 클라이언트 생성
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
#client.on_subscribe = on_subscribe
client.on_message = on_message

client.connect('localhost', 1883)

# common 이라는 Topic 구독, Qos 1
client.subscribe('common', 1)
client.loop_forever()