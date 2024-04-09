import paho.mqtt.client as mqtt
import json

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


# 새로운 메시지 도착했을때 호출됨 (메시지 본문 문자열로 디코딩하고, dic 타입으로 가져옴 )
def on_message(client, userdata, msg):
    json_dic=json.loads(str(msg.payload.decode("utf-8")))
    if "senders" in json_dic:
        print("==========FrameData============")
        # print("frame_num    :",json_dic[0]["frame_num"])
        # print("senders      : "+json_dic[0]["senders"][0]+", "+json_dic[0]["senders"][1])
        # print("ntp_ts       :",json_dic[0]["ntp_ts"])
        # print("create_ntp_ts:",json_dic[0]["creator_ntp_ts"])
        # print("objects1     :",json_dic[0]["objects"][0]["object_id"])
        print(json_dic)
    if "event_id" in json_dic:
        print("============event==============")
        # print("token        :",json_dic["token"])
        # print("camera_id    :",json_dic["camera_id"])
        # print("profile_id   :",json_dic["profile_id"])
        # print("address      :",json_dic["address"]+"\n")
        print(json_dic)
        print("\n")


# 새로운 클라이언트 생성
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
#client.on_subscribe = on_subscribe
client.on_message = on_message

client.connect('localhost', 1883)

# common 이라는 Topic 구독, Qos 1
client.subscribe('detection', 1)
client.subscribe('event', 1)
client.loop_forever()