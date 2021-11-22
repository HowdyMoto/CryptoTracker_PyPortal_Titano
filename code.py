import time
import board
import busio
import displayio
from digitalio import DigitalInOut

from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_bitmap_font import bitmap_font

import adafruit_requests as requests
#from adafruit_pyportal import PyPortal
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi

################### Global vars ##############################################################################
WHITE = 0xFFFFFF
BLACK = 0x000000
GREEN = 0x00FF00
RED =   0xFF0000
DARKRED =   0xCC0000
URL = "http://api.coincap.io/v2/assets/"
BTC_URL = "http://api.coincap.io/v2/assets/bitcoin"
ETH_URL = "http://api.coincap.io/v2/assets/ethereum"
XMR_URL = "http://api.coincap.io/v2/assets/monero"
NUM_LOOPS = 0

######## Get info from secrets.py ######################################################
try:
    from secrets import secrets
except ImportError:
    print("WiFi credentials, API keys, and assets tracked are kept in secrets.py, please add them there!")
    raise

########### Set up display and load screen UI ################################################################
display = board.DISPLAY
font = bitmap_font.load_font("fonts/Nunito-Regular-75.bdf")
loadscreen_group = displayio.Group()
wait_label = label.Label(font, text="Connecting to WiFi...", scale=1, color=WHITE, x=80, y=150)
loadscreen_group.append(wait_label)
display.show(loadscreen_group)

########## UI setup ##########################################################################################
indent_label = 32
indent_price = 140
indent_change = 360
indent_indicator = 400
indent_top = 64
vert_spacing = 96

rect_background = Rect(0, 0, display.width, display.height, fill=BLACK) # If we detect an error, we turn the background red.

pricedata_group = displayio.Group()
label_coin1 = label.Label(font, text=secrets["coin1label"], color=WHITE, x=indent_label, y=indent_top )
label_coin2 = label.Label(font, text=secrets["coin2label"], color=WHITE, x=indent_label, y=(indent_top + vert_spacing) )
label_coin3 = label.Label(font, text=secrets["coin3label"], color=WHITE, x=indent_label, y=(indent_top + vert_spacing*2) )
label_coin1_price = label.Label(font, text="wait...", scale=1, color=WHITE, x=indent_price, y=indent_top)
label_coin2_price = label.Label(font, text="wait...", scale=1, color=WHITE, x=indent_price, y=(indent_top + vert_spacing))
label_coin3_price = label.Label(font, text="wait...", scale=1, color=WHITE, x=indent_price, y=(indent_top + vert_spacing*2) )
label_coin1_change = label.Label(font, text=str(""), scale=1, color=WHITE, x=indent_change, y=indent_top)
label_coin2_change = label.Label(font, text=str(""), scale=1, color=WHITE, x=indent_change, y=(indent_top + vert_spacing))
label_coin3_change = label.Label(font, text=str(""), scale=1, color=WHITE, x=indent_change, y=(indent_top + vert_spacing*2) )

pricedata_group.append(rect_background)
pricedata_group.append(label_coin1)
pricedata_group.append(label_coin2)
pricedata_group.append(label_coin3)
pricedata_group.append(label_coin1_price)
pricedata_group.append(label_coin2_price)
pricedata_group.append(label_coin3_price)
pricedata_group.append(label_coin1_change)
pricedata_group.append(label_coin2_change)
pricedata_group.append(label_coin3_change)

######## Wi-Fi setup ########################################################################################

esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

requests.set_socket(socket, esp)

if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
    print("ESP32 found and in idle mode")

print("Authenticating with WiFi...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e:
        print("could not connect to WiFi, retrying: ", e)
        continue
print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)
print("My IP address is", esp.pretty_ip(esp.ip_address))

api_key = secrets['coincap_api_key']
header = {'Authorization': 'Bearer ' + api_key}

display.show(pricedata_group)   # Only show once the bootup sequence is done and data is requested.

######### Get the price of a coin ########################################################################
def getprice(asset, pricelabel, changelabel):
    try:
        response = requests.get(URL + asset, headers=header)
        response_json = response.json()

        price_unformatted = float(response_json["data"]["priceUsd"])
        price_delta_unformatted = float(response_json["data"]["changePercent24Hr"])    # get the percentage change, which can be many decimal places

        price = "%.2f" % price_unformatted                            # Create a string from a float and round the price to 2 decimal places
        price_delta = "%.1f" % price_delta_unformatted                # Round the price to 1 decimal place 

        if price_delta_unformatted >= 0:
            pricelabel.color = GREEN
            changelabel.color = GREEN
        else:
            pricelabel.color = RED
            changelabel.color = RED

        pricelabel.text = price
        changelabel.text = price_delta + "%"

    except (ValueError, RuntimeError) as e:
        print("Error: ", e)
        rect_background.fill = (128,0,0)

######## MAIN LOOP #########################################################################################
while True:

    getprice("bitcoin", label_coin1_price, label_coin1_change)
    getprice("ethereum", label_coin2_price, label_coin2_change)
    getprice("monero", label_coin3_price, label_coin3_change)

    NUM_LOOPS += 1
    print("Loops=" + str(NUM_LOOPS) )
    time.sleep(180)