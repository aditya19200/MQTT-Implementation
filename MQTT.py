import paho.mqtt.client as mqtt
import json
import logging
import time
import random
import threading
from typing import Dict, Any

class MQTTManager:
   
    def __init__(self, broker: str = 'localhost', port: int = 1883, 
                 client_id: str = None, username: str = None, password: str = None):
       
        # Logging configuration
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # Connection parameters
        self.broker = broker
        self.port = port
        self.client_id = client_id or f'mqtt-client-{random.randint(0, 1000)}'
        
        # Create MQTT client
        self.client = mqtt.Client(self.client_id)
        
        # Authentication setup
        if username and password:
            self.client.username_pw_set(username, password)
        
        # Callback function registrations
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_publish = self._on_publish
        self.client.on_subscribe = self._on_subscribe
        
        # Message tracking
        self.message_queue: Dict[str, list] = {}
        
        # Connection status
        self.is_connected = False

    def _on_connect(self, client, userdata, flags, rc):
       
        if rc == 0:
            self.logger.info(f"Connected to MQTT Broker: {self.broker}")
            self.is_connected = True
        else:
            error_messages = {
                1: "Incorrect protocol version",
                2: "Invalid client identifier",
                3: "Server unavailable",
                4: "Bad username or password",
                5: "Not authorized"
            }
            self.logger.error(f"Connection failed: {error_messages.get(rc, 'Unknown error')}")

    def _on_message(self, client, userdata, message):
       
        try:
            # Decode payload with error handling
            payload = message.payload.decode('utf-8')
            
            # Parse JSON if possible
            try:
                parsed_payload = json.loads(payload)
            except json.JSONDecodeError:
                parsed_payload = payload
            
            # Log received message
            self.logger.info(f"Received on {message.topic}: {parsed_payload}")
            
            # Store message in queue
            if message.topic not in self.message_queue:
                self.message_queue[message.topic] = []
            self.message_queue[message.topic].append(parsed_payload)
        
        except Exception as e:
            self.logger.error(f"Message processing error: {e}")

    def _on_publish(self, client, userdata, mid):
       
        self.logger.info(f"Message published successfully (Message ID: {mid})")

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        
        self.logger.info(f"Subscribed successfully (Message ID: {mid}, QoS: {granted_qos})")

    def connect(self, clean_session: bool = True):
       
        try:
            # Configure clean session
            self.client.clean_session = clean_session
            
            # Attempt connection
            self.client.connect(
                host=self.broker, 
                port=self.port, 
                keepalive=60
            )
            
            # Start network loop in a separate thread
            self.client.loop_start()
            
            # Wait for connection
            start_time = time.time()
            while not self.is_connected and time.time() - start_time < 10:
                time.sleep(0.1)
            
            if not self.is_connected:
                raise ConnectionError("Connection timeout")
        
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            raise

    def publish(self, topic: str, message: Any, qos: int = 0, retain: bool = False):
      
        try:
            # Convert message to JSON if it's a dictionary
            if isinstance(message, dict):
                message = json.dumps(message)
            
            # Publish with specified parameters
            self.client.publish(
                topic=topic, 
                payload=str(message), 
                qos=qos, 
                retain=retain
            )
        except Exception as e:
            self.logger.error(f"Publish error on topic {topic}: {e}")

    def subscribe(self, topic: str, qos: int = 0):
        
        try:
            self.client.subscribe(topic, qos)
        except Exception as e:
            self.logger.error(f"Subscription error for topic {topic}: {e}")

    def get_messages(self, topic: str, clear: bool = True) -> list:
       
        messages = self.message_queue.get(topic, [])
        if clear:
            self.message_queue[topic] = []
        return messages

    def disconnect(self):
        
        try:
            self.client.loop_stop()
            self.client.disconnect()
            self.logger.info("Disconnected from MQTT broker")
        except Exception as e:
            self.logger.error(f"Disconnection error: {e}")

def simulate_sensor_data():
   
    # Create MQTT client
    mqtt_client = MQTTManager(broker='localhost')
    mqtt_client.connect()

    # Simulate multiple sensors
    sensors = {
        'temperature': {'topic': 'home/sensors/temperature', 'range': (20, 30)},
        'humidity': {'topic': 'home/sensors/humidity', 'range': (40, 60)},
        'pressure': {'topic': 'home/sensors/pressure', 'range': (990, 1010)}
    }

    try:
        while True:
            for sensor, config in sensors.items():
                # Generate random sensor value
                value = round(random.uniform(config['range'][0], config['range'][1]), 2)
                
                # Create sensor data payload
                payload = {
                    'sensor': sensor,
                    'value': value,
                    'timestamp': time.time()
                }
                
                # Publish with different QoS levels
                mqtt_client.publish(
                    topic=config['topic'], 
                    message=payload, 
                    qos=random.choice([0, 1, 2])
                )
            
            # Wait before next data generation
            time.sleep(5)

    except KeyboardInterrupt:
        print("Stopping sensor simulation...")
    finally:
        mqtt_client.disconnect()

def main():
   
    # Create MQTT client
    mqtt_client = MQTTManager(broker='localhost')
    
    try:
        # Connect to broker
        mqtt_client.connect()
        
        # Subscribe to multiple topics
        mqtt_client.subscribe('home/sensors/#')
        
        # Start sensor data simulation in a separate thread
        sensor_thread = threading.Thread(target=simulate_sensor_data)
        sensor_thread.start()
        
        # Wait and periodically check received messages
        try:
            while True:
                for topic in ['home/sensors/temperature', 'home/sensors/humidity', 'home/sensors/pressure']:
                    messages = mqtt_client.get_messages(topic)
                    if messages:
                        print(f"Messages for {topic}: {messages}")
                time.sleep(10)
        
        except KeyboardInterrupt:
            print("Stopping MQTT client...")
    
    finally:
        mqtt_client.disconnect()

if __name__ == "__main__":
    main()
