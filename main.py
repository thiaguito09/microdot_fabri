def connect_to(ssid: str, passwd: str):
    import network
    ssid = 'Red Profesores'
    passwd ='Profes_IMPA_2022'
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(ssid, passwd)
        while not sta_if.isconnected():
            pass
    return sta_if.ifconfig()[0]
        
from microdot import Microdot, send_file
app = Microdot()

@app.route("/")
def index(request):
    return send_file("index.html")

@app.route("/assets/<dir>/<file>")
def assets(request,dir, file):
    return send_file('/assets/'+ dir+ '/'+ file)

@app.route("/data/update")
def data_update(request):
    from machine import ADC, Pin
    sensor_temp = ADC(Pin(22))
    lectura = sensor_temp.read_u16() * 3.3 / (1 << 16)
    temperatura_cpu = lectura * 100
    return { "cpu_temp" : temperatura_cpu }

if __name__ == "__main__": 
    try:
        ip = connect_to("Red Profesores", "Profes_IMPA_2022")
        print("IP: " + ip + ":5000")
        app.run()
    except KeyboardInterrupt:
        print("MEASUREMENT OFF")
