
import machine
import utime
import ssd1306

# === OLED I2C Ayarları ===
i2c = machine.I2C(0, scl=machine.Pin(9), sda=machine.Pin(8))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# === Rotary Encoder ve Buton ===
enc_a = machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_UP)
enc_b = machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_UP)
button = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_UP)

# === EEPROM benzeri flash saklama (RAM taklidi) ===
# (Gerçek flash yazımı için 'flashbdev' gibi kütüphaneler gerekir)
# Basit tutmak için sabit değişken kullanıyoruz
Kp = 1.0
Ki = 0.0
Kd = 0.0
target_pos = 0

# === Menü Yönetimi ===
menu_index = 0
menu_items = ["Kp", "Ki", "Kd", "Target", "Test Motor"]
params = [Kp, Ki, Kd, target_pos]
last_a = enc_a.value()

# === PID Motor Test Sinyalleri ===
pwm = machine.PWM(machine.Pin(16))
pwm.freq(1000)
dir_pin = machine.Pin(17, machine.Pin.OUT)

# Encoder simülasyonu için sayıcı
encoder_value = 0

def read_encoder():
    global last_a, params, menu_index
    current_a = enc_a.value()
    current_b = enc_b.value()
    if last_a == 0 and current_a == 1:
        if current_b == 0:
            if menu_index < 4:
                params[menu_index] += 0.1
            else:
                pass
        else:
            if menu_index < 4:
                params[menu_index] -= 0.1
            else:
                pass
        if menu_index < 4:
            params[menu_index] = round(params[menu_index], 2)
    last_a = current_a

def draw_menu():
    oled.fill(0)
    oled.text("PID MENUSU:", 0, 0)
    for i in range(len(menu_items)):
        prefix = ">" if i == menu_index else " "
        if i < 4:
            oled.text(f"{prefix}{menu_items[i]}: {params[i]:.2f}", 0, 12 + i*10)
        else:
            oled.text(f"{prefix}{menu_items[i]}", 0, 12 + i*10)
    oled.show()

def test_motor(target):
    global encoder_value
    error = target - encoder_value
    pwm_val = min(max(abs(int(error * 100)), 0), 65535)
    dir_pin.value(1 if error > 0 else 0)
    pwm.duty_u16(pwm_val)
    encoder_value += 1 if error > 0 else -1

def button_handler(pin):
    global menu_index
    menu_index = (menu_index + 1) % len(menu_items)

button.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_handler)

# === Ana Döngü ===
while True:
    read_encoder()
    draw_menu()
    if menu_index == 4:
        test_motor(params[3])
    utime.sleep_ms(100)
