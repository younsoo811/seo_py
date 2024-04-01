import sys
import pika
 
queue = 'ys_queue'
message = ' '.join(sys.argv[1:])
 
connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'
                , port=5672
                , virtual_host='/'
                , credentials=pika.PlainCredentials('ys', 'ys')   # username, password
            ))
 
channel = connection.channel()
 
channel.queue_declare(queue=queue)
 
channel.basic_publish(
    exchange=''     
    , routing_key=queue   
    , body=message         
)
print(" [x] Sent " + message )
 
connection.close()