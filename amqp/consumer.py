import pika
 
queue = 'ys_queue'

# rabbitmq와 연결 설정
connection  = pika.BlockingConnection(pika.URLParameters('amqp://ys:ys@localhost:5672/'))
 
# 통신을 위한 채널 생성
channel = connection.channel()

# 메시지 큐 생성
channel.queue_declare(queue=queue)
 
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    ch.basic_ack( delivery_tag=method.delivery_tag )
 
channel.basic_consume( queue, callback )
 
print(' [*] 메시지 수신 대기')
channel.start_consuming()
