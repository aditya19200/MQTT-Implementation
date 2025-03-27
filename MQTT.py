import paho.mqtt.client as mqtt
import json
import logging
import time
import random
import threading
from typing import Dict, Any, Optional

class AdvancedMQTTManager:
    def __init__(self, 
                 broker: str = 'localhost', 
                 port: int = 1883, 
                 client_id: Optional[str] = None,
                 username: Optional[str] = None, 
                 password: Optional[str] = None):
        """
        Advanced MQTT Client with comprehensive features
        
        Args:
            broker (str): MQTT broker address
            port (int): Broker port
            client_id (str, optional): Unique client identifier
            username (str, optional): Broker authentication username
            password (str, optional): Broker authentication password
        """
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
        
        # Authentication setup
        self.username = username
        self.password = password
        
        # Create MQTT client
        self.client = mqtt.Client(
            client_id=self.client_id, 
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )
        
        # Set authentication if provided
        if username and password:
            self.client.username_pw_set(username, password)
        
        # Callback configurations
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_publish = self._on_publish
        
        # Message management
        self.message_store: Dict[str, list] = {}
        self.message_lock = threading.Lock()
        
        # Connection status
        self.is_connected = False
    
    def _on_connect(self, client, userdata, flags, rc, properties=None):
        """
        Enhanced connection callback with detailed logging
        """
        if rc == 0:
            self.is_connected = True
            self.logger.info(f"Connected to MQTT Broker: {self.broker}")
            
            # Auto-subscribe to system topics
            self.client.subscribe("system/status")
            self.client.subscribe("system/config")
        else:
            error_messages = {
                1: "Incorrect protocol version",
                2: "Invalid client identifier",
                3: "Server unavailable",
                4: "Bad username or password",
                5: "Not authorized"
            }
            self.logger.error(f"Connection failed: {error_messages.get(rc, 'Unknown error')}")
    
    def _on_message(self, client, userdata, message, properties=None):
        """
        Advanced message handling with storage and processing
        """
        try:
            # Decode and parse payload
            payload = message.payload.decode('utf-8')
            try:
                parsed_payload = json.loads(payload)
            except json.JSONDecodeError:
                parsed_payload = payload
            
            # Thread-safe message storage
            with self.message_lock:
                if message.topic not in self.message_store:
                    self.message_store[message.topic] = []
                self.message_store[message.topic].append({
                    'payload': parsed_payload,
                    'timestamp': time.time()
                })
            
            self.logger.info(f"Received on {message.topic}: {parsed_payload}")
        
        except Exception as e:
            self.logger.error(f"Message processing error: {e}")
    
    def publish(self, 
                topic: str, 
                message: Any, 
                qos: int = 1, 
                retain: bool = False):
        """
        Enhanced message publishing with multiple options
        
        Args:
            topic (str): MQTT topic
            message (Any): Message to publish
            qos (int): Quality of Service level (0, 1, 2)
            retain (bool): Retain message on broker
        """
        try:
            # Convert to JSON if dictionary
            if isinstance(message, dict):
                message = json.dumps(message)
            
            # Publish with enhanced parameters
            result = self.client.publish(
                topic=topic, 
                payload=str(message), 
                qos=qos, 
                retain=retain
            )
            
            # Check publication status
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                self.logger.info(f"Published to {topic}")
            else:
                self.logger.warning(f"Publication to {topic} failed")
        
        except Exception as e:
            self.logger.error(f"Publish error on {topic}: {e}")
    
    def get_messages(self, topic: str, clear: bool = True) -> list:
        """
        Retrieve and optionally clear messages for a topic
        
        Args:
            topic (str): Topic to retrieve messages from
            clear (bool): Clear messages after retrieval
        
        Returns:
            list: Messages received on the topic
        """
        with self.message_lock:
            messages = self.message_store.get(topic, [])
            if clear:
                self.message_store[topic] = []
            return messages

def simulate_advanced_sensor_network():
    """
    Advanced IoT sensor network simulation
    """
    # Create MQTT client
    mqtt_client = AdvancedMQTTManager(
        broker='localhost', 
        username='optional_username', 
        password='optional_password'
    )
    
    # Connection and loop start
    mqtt_client.client.connect(mqtt_client.broker, mqtt_client.port)
    mqtt_client.client.loop_start()
    
    # Sensor configurations
    sensors = {
        'temperature': {
            'topic': 'sensors/climate/temperature',
            'range': (20, 30),
            'unit': '°C'
        },
        'humidity': {
            'topic': 'sensors/climate/humidity',
            'range': (40, 60),
            'unit': '%'
        },
        'pressure': {
            'topic': 'sensors/climate/pressure',
            'range': (990, 1010),
            'unit': 'hPa'
        }
    }
    
    try:
        while True:
            for sensor, config in sensors.items():
                # Generate sensor data
                value = round(random.uniform(config['range'][0], config['range'][1]), 2)
                
                # Create comprehensive payload
                payload = {
                    'sensor': sensor,
                    'value': value,
                    'unit': config['unit'],
                    'timestamp': time.time(),
                    'device_id': f'sensor_{sensor}'
                }
                
                # Publish with variable QoS
                mqtt_client.publish(
                    topic=config['topic'], 
                    message=payload, 
                    qos=random.choice([0, 1, 2])
                )
            
            # Wait between sensor readings
            time.sleep(5)
    
    except KeyboardInterrupt:
        print("Stopping sensor simulation...")
    finally:
        mqtt_client.client.loop_stop()

def main():
    # Run sensor simulation
    simulate_advanced_sensor_network()

if __name__ == "__main__":
    main()
