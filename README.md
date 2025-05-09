# Ce-Su Servo: Raspberry Pi Pico PID Servo Sistemi

Bu proje, Mach3 uyumlu STEP/DIR sinyallerinden PID kontrollü servo DC motor sistemi üretmek için geliştirilmiştir.

## İçerik

- `main_menu_v2.py`: OLED ekran ve rotary encoder üzerinden PID parametrelerini ayarlama.
- `web_pid_server.py`: Pico W kullanarak Wi-Fi üzerinden PID kontrolü sağlayan web arayüzü.

## Kullanım

### OLED Menü Sistemi (Pico):
- GP8/GP9: OLED ekran (I2C)
- GP6/GP7: Encoder A/B
- GP10: Encoder buton
- GP16/GP17: PWM ve yön çıkışı (IBT-2 sürücü için)

### Web Arayüz (Pico W):
- WiFi bilgilerini `web_pid_server.py` içine girin
- Pico W açıldığında IP adresi üzerinden kontrol ekranına erişin
- PID ayarlarını, hedef pozisyonu ve motor durumunu kontrol edin

## Lisans
MIT Lisansı – Suat + GPT işbirliği ile
