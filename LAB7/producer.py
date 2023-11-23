from utils.products_crawler import scrape_links
import pika
import requests
import sys

url = input("Write the URL to be scrapped: ")


connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()

channel.queue_declare(queue='links')

for product in scrape_links(url,[],3):
    channel.basic_publish(exchange='',
                        routing_key='links',
                        body=product,
                         properties=pika.BasicProperties(
                                       delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                                   ))
    print(f" [x] Sent product: {product}")
