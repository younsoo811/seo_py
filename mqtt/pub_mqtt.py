import paho.mqtt.client as mqtt
import json


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)

# MQTT 메시지 발행 콜백 함수 (클라이언트 id, 데이터, 메시지 id)
def on_publish(client, userdata, mid):
    print("In on_pub callback mid= ", mid)

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

    client.loop_start() # 비동기 루프 시작 (백그라운드에서 브로커와의 연결 상태 유지하고 콜백 함수 처리)

    client.publish('common', json.dumps({"success": "ok"}), 1) #common 이라는 Topic에 json 형식(string타입)의 메시지 발행
    client.loop_stop() # 비동기 루프 종료

client.disconnect()