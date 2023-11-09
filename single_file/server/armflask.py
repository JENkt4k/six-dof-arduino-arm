from flask import Flask, request
import serial
import serial.tools.list_ports

app = Flask(__name__)
available_ports = [port.device for port in serial.tools.list_ports.comports()]
print(available_ports)
print(available_ports[0])
arduino_serial = serial.Serial(available_ports[0], 9600)  # Update to your Arduino's serial port

@app.route('/move_servo', methods=['POST'])
def move_servo():
    data = request.json
    servo_id = data['servo_id']
    position = data['position']
    command = f"S{servo_id},{position}\n"
    arduino_serial.write(command.encode())
    return {'status': 'OK'}

@app.route('/move_servos', methods=['POST'])
def move_servos():
    data = request.json
    servo_positions = data['servo_positions']
    print(servo_positions)
    
    allcommands = ""
    for servo in servo_positions:
        print(servo)
        servo_id = servo['servo_id']
        position = servo['position']
        command = f"S{servo_id},{position}\n"
        allcommands += command

    print(allcommands)
        
    arduino_serial.write(allcommands.encode())
        
    return {'status': 'OK'} #return jsonify({"status": "success", "message": "Servos moved"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=59780)

