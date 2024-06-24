from flask import Flask, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
from constantes import *
import json


mqtt_client = mqtt.Client()
app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("semaforo.html")

def conectar_mqtt(client, userdata, flags, rc):
    print("Estou conectado ao MQTT")
    client.subscribe(TOPICO_STATUS_SEMAFORO)

@socketio.on("status")
def receber_mensagem(client, userdata, msg):
    json_data = json.loads(msg.payload)
    print("Mensagem recebida: ", json_data)

    socketio.emit("status_semaforo", json_data)

if __name__ == "__main__":
    mqtt_client.on_connect = conectar_mqtt
    mqtt_client.on_message = receber_mensagem

    mqtt_client.username_pw_set(MQTT_USUARIO, MQTT_SENHA)
    mqtt_client.connect(MQTT_HOST, MQTT_PORT, MQTT_TEMPO)
    mqtt_client.loop_start()

    socketio.run(app, debug=True, log_output=True, use_reloader=True)