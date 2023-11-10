import pika
from tinydb import TinyDB, Query
import sys 
import threading
from utils.info_crawler import scrap_info

consumers = int(input("input number of consumers: "))
host = 'localhost'

lock = threading.Lock()

def handle_consumer(consumer_index):
    connection = pika.BlockingConnection(
            pika.ConnectionParameters(host = host))

    channel = connection.channel()
    channel.queue_declare(queue='links', durable=False)
    
    def callback(ch, method, properties, body):
        product = str(body.decode())
        print(f'Consumer no.{consumer_index} received product: {product}')


        #adding to the database:
        db = TinyDB('database.json')
        Product = Query()


        info = scrap_info(product)
        
        with lock:
            exists = db.get(Product['url'] == product)
            if exists is None:
                    db.insert(info)
            else:
                db.update(info, doc_ids=[exists.doc_id])

            print(f" [consumer no.  {consumer_index}] has finished")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            


    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='links', on_message_callback=callback)

    channel.start_consuming()

try:
    print(' [*] Waiting for messages. To exit press CTRL+C')

    for i in range(consumers):
        consumer_thread = threading.Thread(target = handle_consumer, args = (i + 1,))
        consumer_thread.start()

except KeyboardInterrupt:
    try:
        sys.exit(0)
    except SystemExit:
        exit()

