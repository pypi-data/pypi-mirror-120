import time
import logging
import pulsar

LOGGER = logging.getLogger(__name__)


class PulseSecrets:
    def __init__(self, url, admin_token, api_url, cert_file):
        self.url = url
        self.admin_token = admin_token
        self.api_url = api_url
        self.cert_file = cert_file


def send_message(pulsar_url, token, cert_file, topic, message):
    auth = pulsar.AuthenticationToken(token)
    client = pulsar.Client(pulsar_url, authentication=auth, tls_trust_certs_file_path=cert_file)
    try:
        producer = client.create_producer(topic)
        producer.send(message.encode('utf-8'))
    except Exception as e:
        LOGGER.error(f"Failed to send message: {e}")
    finally:
        client.close()


def consume_messages(pulsar_url, token, cert_file, topic, subscription, num_messages, timeout_seconds, file_path):
    auth = pulsar.AuthenticationToken(token)
    client = pulsar.Client(pulsar_url, authentication=auth, tls_trust_certs_file_path=cert_file)
    start_time = time.time()
    num_messages_received = 0
    consumer = client.subscribe(topic, subscription)
    while num_messages_received < num_messages:
        try:
            msg = consumer.receive(60000)
        except Exception as e:
            print("No message received within timeout: " + str(e))
            continue
        try:
            with open(file_path, 'a') as f:
                f.write(msg.data().decode('utf-8') + '\n')
            consumer.acknowledge(msg)
            num_messages_received += 1
        except Exception as e:
            print("Something went wrong processing message: " + str(e))
            consumer.negative_acknowledge(msg)

        if time.time() - start_time > timeout_seconds:
            break
    consumer.unsubscribe()
