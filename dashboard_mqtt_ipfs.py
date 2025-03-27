import tkinter as tk
from tkinter import scrolledtext
import paho.mqtt.client as mqtt
import requests

# Configurações MQTT
MQTT_BROKER = "localhost"
MQTT_TOPIC = "sensores/#"

# Configurações IPFS
IPFS_API_URL = "http://127.0.0.1:5001/api/v0"

# Interface Gráfica
class MQTTIPFSDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor MQTT + IPFS")
        
        # Área de logs
        self.log_area = scrolledtext.ScrolledText(root, width=60, height=20)
        self.log_area.pack(padx=10, pady=10)
        
        # Botão para abrir a WebUI do IPFS
        self.webui_btn = tk.Button(root, text="Abrir IPFS WebUI", command=self.open_webui)
        self.webui_btn.pack(pady=5)
        
        # Iniciar cliente MQTT
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(MQTT_BROKER, 1883, 60)
        self.mqtt_client.subscribe(MQTT_TOPIC)
        self.mqtt_client.loop_start()
    
    def on_message(self, client, userdata, msg):
        # Exibir mensagem MQTT
        log_msg = f"[MQTT] {msg.topic}: {msg.payload.decode()}\n"
        self.log_area.insert(tk.END, log_msg)
        self.log_area.see(tk.END)
        
        # Adicionar ao IPFS (opcional)
        cid = self.add_to_ipfs(log_msg)
        if cid:
            self.log_area.insert(tk.END, f"[IPFS] Arquivo salvo com CID: {cid}\n\n")
    
    def add_to_ipfs(self, data):
        try:
            response = requests.post(f"{IPFS_API_URL}/add", files={"file": ("log.txt", data)})
            return response.json()["Hash"]
        except Exception as e:
            self.log_area.insert(tk.END, f"[ERRO IPFS] {str(e)}\n")
            return None
    
    def open_webui(self):
        import webbrowser
        webbrowser.open("http://localhost:5001/webui")

# Iniciar a interface
root = tk.Tk()
app = MQTTIPFSDashboard(root)
root.mainloop()
