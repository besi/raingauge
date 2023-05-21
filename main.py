from machine import Pin
import time

start = time.time()

def callback(p):
    if p.value() == 0:
        t = str(time.time() - start)
        print(f"tick {t}")

pin = 4
p = machine.Pin(pin, Pin.IN, Pin.PULL_UP)
p.irq(trigger=Pin.IRQ_FALLING, handler=callback)
