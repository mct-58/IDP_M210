from machine import Pin
from utime import sleep

def test_infrared():

    sensor = Pin(28, Pin.IN)

        # Read ten samples
    for _ in range(1000):
        strength = sensor.value()
        print(f"strength = {strength}")  # Check calibration!
        sleep(0.01)
        
        # Stop device
 


if __name__ == "__main__":
    test_infrared()
