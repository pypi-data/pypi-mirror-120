#modpoll

A command line tool to poll modbus registers

### Basic usages

- Poll Modbus RTU device and save to local csv file
```bash
modpoll --config examples/scpm-s6.csv --rtu /dev/ttyUSB0 --rtu-baud 9600 --export export.csv
```
- Poll Modbus TCP device and publish to MQTT broker
```bash
modpoll --config examples/scpm-s6.csv --tcp 192.168.1.10 --tcp-port 502 --mqtt-host localhost
```
