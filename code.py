import time
import board
import busio
import displayio
from digitalio import DigitalInOut
import microcontroller

from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_bitmap_font import bitmap_font

import adafruit_requests as requests
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

COIN1_BMP = displayio.OnDiskBitmap("bitmaps/BTC.bmp")
COIN2_BMP = displayio.OnDiskBitmap("bitmaps/ETH.bmp")
COIN3_BMP = displayio.OnDiskBitmap("bitmaps/XMR.bmp")
WIFI_BMP = displayio.OnDiskBitmap("bitmaps/WiFi.bmp")

INDENT_LABEL = 32
INDENT_PRICE = 140
INDENT_CHANGE = 360
INDENT_TOP = 64
VERTICAL_SPACING = 96

icon_tilegrid1 = displayio.TileGrid(COIN1_BMP, pixel_shader=COIN1_BMP.pixel_shader, x=INDENT_LABEL, y=32)
icon_tilegrid2 = displayio.TileGrid(COIN2_BMP, pixel_shader=COIN2_BMP.pixel_shader, x=INDENT_LABEL, y=128)
icon_tilegrid3 = displayio.TileGrid(COIN3_BMP, pixel_shader=COIN3_BMP.pixel_shader, x=INDENT_LABEL, y=224)

FONT = bitmap_font.load_font("fonts/Nunito-Regular-75.bdf")


######## Get info from secrets.py ######################################################
try:
    from secrets import secrets
except ImportError:
    print("WiFi credentials, API keys, and assets tracked are kept in secrets.py, please add them there!")
    raise

########### Set up display and load screen UI ################################################################
display = board.DISPLAY
loadscreen_group = displayio.Group()
wait_label = label.Label(FONT, text="Connecting to WiFi...", scale=1, color=WHITE, x=80, y=150)
tile_grid_wifi = displayio.TileGrid(WIFI_BMP, pixel_shader=WIFI_BMP.pixel_shader, x=200, y=192)

loadscreen_group.append(wait_label)
loadscreen_group.append(tile_grid_wifi)

display.show(loadscreen_group)

########## Main UI setup ##########################################################################################

rect_background = Rect(0, 0, display.width, display.height, fill=BLACK) # If we detect an error, we turn the background red.

icon_group = displayio.Group()
name_group = displayio.Group()
price_group = displayio.Group()
change_group = displayio.Group()
main_group = displayio.Group()

label_coin1 = label.Label(FONT, text=secrets["coin1label"], color=WHITE, x=INDENT_LABEL, y=INDENT_TOP )
label_coin2 = label.Label(FONT, text=secrets["coin2label"], color=WHITE, x=INDENT_LABEL, y=(INDENT_TOP + VERTICAL_SPACING) )
label_coin3 = label.Label(FONT, text=secrets["coin3label"], color=WHITE, x=INDENT_LABEL, y=(INDENT_TOP + VERTICAL_SPACING*2) )
label_coin1_price = label.Label(FONT, text="wait...", scale=1, color=WHITE, x=INDENT_PRICE, y=INDENT_TOP)
label_coin2_price = label.Label(FONT, text="wait...", scale=1, color=WHITE, x=INDENT_PRICE, y=(INDENT_TOP + VERTICAL_SPACING))
label_coin3_price = label.Label(FONT, text="wait...", scale=1, color=WHITE, x=INDENT_PRICE, y=(INDENT_TOP + VERTICAL_SPACING*2) )
label_coin1_change = label.Label(FONT, text=str(""), scale=1, color=WHITE, x=INDENT_CHANGE, y=INDENT_TOP)
label_coin2_change = label.Label(FONT, text=str(""), scale=1, color=WHITE, x=INDENT_CHANGE, y=(INDENT_TOP + VERTICAL_SPACING))
label_coin3_change = label.Label(FONT, text=str(""), scale=1, color=WHITE, x=INDENT_CHANGE, y=(INDENT_TOP + VERTICAL_SPACING*2) )

icon_group.append(icon_tilegrid1)
icon_group.append(icon_tilegrid2)
icon_group.append(icon_tilegrid3)
name_group.append(label_coin1)
name_group.append(label_coin2)
name_group.append(label_coin3)
price_group.append(label_coin1_price)
price_group.append(label_coin2_price)
price_group.append(label_coin3_price)
change_group.append(label_coin1_change)
change_group.append(label_coin2_change)
change_group.append(label_coin3_change)

main_group.append(rect_background)
main_group.append(icon_group)
#main_group.append(name_group)
main_group.append(price_group)
main_group.append(change_group)


######## Wi-Fi setup ########################################################################################

esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

requests.set_socket(socket, esp)

if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
    print("ESP32 found in idle mode")

while not esp.is_connected:
    try:
        print("Attempting authentication with WiFi...")
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e:
        print("Could not connect to WiFi. Retrying: ", e)
        continue
print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)
print("My IP address is", esp.pretty_ip(esp.ip_address))

api_key = secrets['coincap_api_key']
header = {'Authorization': 'Bearer ' + api_key}

display.show(main_group)   # Only show once the bootup sequence is done and data is requested.

######### Get the price of a coin ########################################################################
def getprice(asset, pricelabel, changelabel):
    try:
        response = requests.get(URL + asset, headers=header)
        if response.status_code == 200:
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
        else:
            return

    except (ValueError, RuntimeError) as e:
        print("Error: ", e)
        rect_background.fill = (160,0,0)
        time.sleep(10)
        microcontroller.reset()

######## MAIN LOOP ########### ##############################################################################
while True:
    getprice(secrets["coin1"], label_coin1_price, label_coin1_change)
    getprice(secrets["coin2"], label_coin2_price, label_coin2_change)
    getprice(secrets["coin3"], label_coin3_price, label_coin3_change)

    NUM_LOOPS += 1
    print("Loops=" + str(NUM_LOOPS) )
    time.sleep(30)