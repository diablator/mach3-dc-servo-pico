
import network
import socket
import time
import machine

# Motor kontrol pinleri
pwm = machine.PWM(machine.Pin(16))
pwm.freq(1000)
dir_pin = machine.Pin(17, machine.Pin.OUT)

# PID değerleri
Kp = 1.0
Ki = 0.0
Kd = 0.0
target_position = 0
current_position = 0
running = False

# WiFi ayarları
ssid = 'YOUR_WIFI_SSID'
password = 'YOUR_WIFI_PASSWORD'

# WiFi bağlantısı
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

print("WiFi bağlanıyor...")
while not wlan.isconnected():
    time.sleep(1)
print("Bağlandı. IP:", wlan.ifconfig()[0])

# HTML arayüz
def web_page():
    html = f"""<!DOCTYPE html>
    <html>
    <head>
      <title>PID Servo Kontrol</title>
      <style>
        body {{ font-family: sans-serif; text-align:center; }}
        input {{ margin: 5px; padding: 5px; width: 80px; }}
      </style>
    </head>
    <body>
      <h2>Web PID Servo Kontrol</h2>
      <form>
        Kp: <input name="Kp" type="number" step="0.1" value="{Kp}"><br>
        Ki: <input name="Ki" type="number" step="0.1" value="{Ki}"><br>
        Kd: <input name="Kd" type="number" step="0.1" value="{Kd}"><br>
        Hedef: <input name="target" type="number" value="{target_position}"><br>
        <input type="submit" name="run" value="Baslat">
        <input type="submit" name="stop" value="Durdur">
      </form>
      <p>Mevcut Pozisyon: {current_position}</p>
    </body>
    </html>
    """.replace('
', '')
    return html

# Soket sunucusu başlat
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Web sunucu çalışıyor...')

# PID döngüsü
integral = 0
last_error = 0

def update_motor():
    global integral, last_error, current_position
    error = target_position - current_position
    integral += error
    derivative = error - last_error
    last_error = error
    output = (Kp * error) + (Ki * integral) + (Kd * derivative)
    pwm_val = min(max(abs(int(output)), 0), 65535)
    dir_pin.value(1 if output > 0 else 0)
    pwm.duty_u16(pwm_val)
    current_position += 1 if output > 0 else -1

# Ana döngü
while True:
    if running:
        update_motor()
    try:
        conn, addr = s.accept()
        print('Yeni istemci:', addr)
        request = conn.recv(1024)
        request = str(request)
        if '/?run=' in request:
            running = True
        if '/?stop=' in request:
            running = False
        if 'Kp=' in request:
            try:
                Kp = float(request.split('Kp=')[1].split('&')[0])
                Ki = float(request.split('Ki=')[1].split('&')[0])
                Kd = float(request.split('Kd=')[1].split('&')[0])
                target_position = int(request.split('target=')[1].split('&')[0])
            except:
                pass
        response = web_page()
        conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
        conn.send(response)
        conn.close()
    except Exception as e:
        print("Hata:", e)
        pass
    time.sleep(0.1)
