from machine import Pin
from utime import sleep

def test_infrared():
    
    # print(i2c_bus.scan())  # Get the address (nb 41=0x29, 82=0x52)
    
    # Setup vl53l0 object
    


    
    

        # Start device
    sensor = Pin(28, Pin.IN)

        # Read ten samples
    for _ in range(100):
        strength = sensor.value()
        print(f"strength = {strength}")  # Check calibration!
        sleep(0.5)
        
        # Stop device
 


if __name__ == "__main__":
    test_infrared()
