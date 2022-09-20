
# Import Python System Libraries
import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import pycubed_rfm9x as adafruit_rfm9x

#RxEN and TxEN
RxEN = DigitalInOut(board.D22)
RxEN.direction = Direction.OUTPUT
RxEN.value = True

TxEN = DigitalInOut(board.D27)
TxEN.direction = Direction.OUTPUT
TxEN.value = False

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 401.0)
rfm9x.tx_power = 23
prev_packet = None
rfm9x.node = 0xBA
rfm9x.destination = 0xAB

#mode = False for Rx and True for Tx
def SwitchPins(mode):
    if(not mode):
        RxEN.value = True
        TxEN.value = False
    else:
        RxEN.value = False
        TxEN.value = True

while True:
    SwitchPins(False)
    packet = None
    # draw a box to clear the image
    display.fill(0)
    display.text('RasPi LoRa', 35, 0, 1)

    # check for packet rx
    packet = rfm9x.receive(with_ack = True)
    print(packet)
    if packet is None:
        display.show()
        display.text('- Waiting for PKT -', 15, 20, 1)
    else:
        # Display the packet text and rssi
        display.fill(0)
        prev_packet = packet
        packet_text = str([hex(c) for c in prev_packet])
        
        #packet_text = str(prev_packet, "utf8")
        display.text('RX RECIEVED: ', 0, 0, 1)
        display.text(packet_text, 25, 0, 1)
        time.sleep(3)

    # Send Test
#     virtualButton = input()
#     if(virtualButton == "s"):
#         SwitchPins(True)
#         display.fill(0)
#         button_c_data = bytes("SpicySpaceCraft","utf-8")
#         rfm9x.send(button_c_data)
#         display.text('SpicySpaceCraft', 25, 15, 1)


    display.show()
    time.sleep(0.1)

