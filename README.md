# Advanced MQTT Communication Demo

## Overview
This project demonstrates a comprehensive MQTT (Message Queuing Telemetry Transport) implementation in Python, designed to showcase the protocol's key features and provide a robust framework for IoT and messaging applications.

## Features

### MQTT Protocol Implementation
- Full pub/sub communication model
- Support for multiple QoS (Quality of Service) levels
- Flexible topic management
- Secure connection with authentication support

### Key Capabilities
- Automatic message queuing
- Comprehensive logging
- Error handling
- IoT sensor data simulation
- Flexible configuration options

## Prerequisites

### System Requirements
- Python 3.7+
- Linux/macOS/Windows

### Dependencies
- paho-mqtt
- json
- logging
- threading

## Installation

1. Clone the Repository
```bash
git clone https://github.com/yourusername/mqtt-demo.git
cd mqtt-demo
```

2. Create Virtual Environment (Optional but Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Configuration

### MQTT Broker Setup
- Supports localhost and remote broker configurations
- Configurable port and authentication
- Clean session options

### Connection Parameters
- Broker Address
- Port Number
- Client ID
- Username/Password (Optional)

## Usage Examples

### Basic Publishing
```python
from mqtt_manager import MQTTManager

# Create MQTT Client
client = MQTTManager(broker='localhost')
client.connect()

# Publish Message
client.publish('home/living-room/temperature', {'value': 22.5})
```

### Subscribing to Topics
```python
# Subscribe to Topic
client.subscribe('home/sensors/#')

# Retrieve Messages
messages = client.get_messages('home/sensors/temperature')
```

## Simulation Modes

### Sensor Data Simulation
- Generates random sensor data
- Supports multiple sensor types
- Configurable data ranges
- Randomized QoS levels

## Error Handling
- Detailed logging
- Connection status tracking
- Exception management
- Configurable error reporting

## Best Practices

### MQTT Protocol Considerations
- Use appropriate QoS levels
- Implement proper error handling
- Manage connection states
- Use retained messages when necessary

### Performance Tips
- Keep payloads small
- Use clean sessions judiciously
- Monitor connection keepalive

## Troubleshooting

### Common Issues
- Broker Connection Failures
- Authentication Problems
- Network Instability

### Debugging
- Check broker logs
- Verify network connectivity
- Review client configuration

## Contributing
1. Fork the Repository
2. Create Feature Branch
3. Commit Changes
4. Push to Branch
5. Create Pull Request

## Author
Aditya
GitHub: aditya19200

## References
- MQTT Specification
- IoT Communication Protocols
## installation of Mosquitto for windows
winget install Mosquitto 

```

### Recommended `requirements.txt` Content:
```
paho-mqtt==1.6.1
```

