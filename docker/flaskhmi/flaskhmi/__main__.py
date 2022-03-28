#!/usr/bin/env python3

"""Web application to emulate the HMI control

   Displays:
   - Current Temperature
   - Temperature Settings

   Controls:
   - Increase Temperature
   - Decrease Temperature

   TODO
   - Use React or VueJS to make it slicker?
   - Clean up modbus.py
   - Make the UI prettier
   - Provide command line arguments for IP and port
"""

from flask import Flask, jsonify, redirect, render_template, request

from flaskhmi.modbus import ModbusClient

app = Flask(__name__)

modbus_client = None


@app.route('/')
def main_page():
    return render_template('index.html', title='HMI Emulator')


@app.route('/set_client', methods=['POST'])
def set_client():
    global modbus_client
    client_ip = request.form.get('client_ip')
    modbus_client = ModbusClient(ip=client_ip, port=502)
    return redirect("/")


@app.route('/temperature/', methods=['GET'])
def temperature():
    if modbus_client:
        temp, setting = modbus_client.get_temperature()
    else:
        temp, setting = (0, 0)
    return jsonify({'temp': temp, 'setting': setting})


@app.route('/raise/', methods=['GET'])
def raisetemp():
    if modbus_client:
        modbus_client.raise_temperature_1c()
    return redirect("/temperature")


@app.route('/lower/', methods=['GET'])
def lowertemp():
    if modbus_client:
        modbus_client.lower_temperature_1c()
    return redirect("/temperature")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8800, debug=True)
