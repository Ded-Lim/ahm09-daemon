#!/usr/bin/env python3
import usb.core
import usb.util
import os
import time
import signal
import sys

# Настройки устройства
VENDOR_ID = 0x4c4a
PRODUCT_ID = 0x4155
INTERFACE = 3
ENDPOINT = 0x82

def main():
    print("Запуск AHM09 Daemon...")
    
    while True:
        try:
            # Находим устройство
            dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
            if dev is None:
                print("Устройство не найдено. Ожидание...")
                time.sleep(5)
                continue
            
            print("Устройство найдено. Слушаем кнопки...")
            
            # Основной цикл чтения
            while True:
                try:
                    # Читаем данные
                    data = dev.read(ENDPOINT, 16, timeout=1000)
                    
                    # Обрабатываем кнопки
                    if data[0] == 1:    # Volume Up
                        os.system("pactl set-sink-volume @DEFAULT_SINK@ +2%")
                        print("🔊 Громкость +")
                    elif data[0] == 2:  # Volume Down
                        os.system("pactl set-sink-volume @DEFAULT_SINK@ -2%")
                        print("🔉 Громкость -")
                    elif data[0] == 8:  # Play/Pause
                        os.system("playerctl play-pause 2>/dev/null")
                        print("⏯️ Play/Pause")
                    elif data[0] == 16: # Next Track
                        os.system("playerctl next 2>/dev/null")
                        print("⏭️ Следующий трек")
                    elif data[0] == 32: # Previous Track
                        os.system("playerctl previous 2>/dev/null")
                        print("⏮️ Предыдущий трек")
                        
                except usb.core.USBError as e:
                    if e.errno != 110:  # Игнорируем таймауты
                        print(f"USB ошибка: {e}")
                        break
                except Exception as e:
                    print(f"Ошибка: {e}")
                    break
                    
        except Exception as e:
            print(f"Критическая ошибка: {e}")
            time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nДемон остановлен")
