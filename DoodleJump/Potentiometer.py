import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

#Creating the I2C Bus
i2c = busio.I2C(board.SCL, board.SDA)

#Creating theADC object using i2C bus
ads = ADS.ADS1015(i2c)

#creat single ended input on channel 0
chan0 = AnalogIn(ads, ADS.P0) # center position potentiometer
chan1 = AnalogIn(ads, ADS.P1) # left position pot
chan2 = AnalogIn(ads, ADS.P2) # right position pot

#create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

print("{:>5}\t{:>5}".format('raw','v'))

while True:
    print("Centre: {:>5}\t{:>5.3f}".format(chan0.value, chan0.voltage))
    print("Right: {:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage))
    print("Left: {:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage))
    time.sleep(1)
#   x = input()
#    if x == '1':
#        break