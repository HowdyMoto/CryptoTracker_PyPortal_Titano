import time
import board
import busio
import displayio
import terminalio
from digitalio import DigitalInOut

from adafruit_display_text import label
from adafruit_display_shapes.triangle import Triangle
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
btc_price = 0.0
eth_price = 0.0
xmr_price = 0.0
BTC_URL = "http://api.coincap.io/v2/assets/bitcoin"
ETH_URL = "http://api.coincap.io/v2/assets/ethereum"
XMR_URL = "http://api.coincap.io/v2/assets/monero"
num_requests = 0
num_loops = 0

########### Set up display ###############################################################################
display = board.DISPLAY

########## UI setup ##########################################################################################
font = bitmap_font.load_font("fonts/Nunito-Regular-75.bdf")
loadscreen_group = displayio.Group()
wait_label = label.Label(font, text="Connecting to WiFi...", scale=1, color=WHITE, x=80, y=150)
loadscreen_group.append(wait_label)
display.show(loadscreen_group)

indent_label = 32
indent_price = 140
indent_change = 360
indent_indicator = 400
indent_top = 64
vert_spacing = 96
triangle_width = 32

pricedata_group = displayio.Group()
btc_label = label.Label(font, text="BTC", color=WHITE, x=indent_label, y=indent_top )
eth_label = label.Label(font, text="ETH", color=WHITE, x=indent_label, y=(indent_top + vert_spacing) )
xmr_label = label.Label(font, text="XMR", color=WHITE, x=indent_label, y=(indent_top + vert_spacing*2) )
btc_price_label = label.Label(font, text="wait...", scale=1, color=WHITE, x=indent_price, y=indent_top)
eth_price_label = label.Label(font, text="wait...", scale=1, color=WHITE, x=indent_price, y=(indent_top + vert_spacing))
xmr_price_label = label.Label(font, text="wait...", scale=1, color=WHITE, x=indent_price, y=(indent_top + vert_spacing*2) )
btc_change_label = label.Label(font, text=str(""), scale=1, color=WHITE, x=indent_change, y=indent_top)
eth_change_label = label.Label(font, text=str(""), scale=1, color=WHITE, x=indent_change, y=(indent_top + vert_spacing))
xmr_change_label = label.Label(font, text=str(""), scale=1, color=WHITE, x=indent_change, y=(indent_top + vert_spacing*2) )

pricedata_group.append(btc_label)
pricedata_group.append(eth_label)
pricedata_group.append(xmr_label)
pricedata_group.append(btc_price_label)
pricedata_group.append(eth_price_label)
pricedata_group.append(xmr_price_label)
pricedata_group.append(btc_change_label)
pricedata_group.append(eth_change_label)
pricedata_group.append(xmr_change_label)

######## Wi-Fi setup ########################################################################################
try:
    from secrets import secrets
except ImportError:
    print("WiFi SSID and password are kept in secrets.py, please add them there!")
    raise

# If you are using a board with pre-defined ESP32 Pins:
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

######## MAIN LOOP ###########################################################################################
while True:


    ######## BTC prices
    response = requests.get(BTC_URL, headers=header)
    num_requests += 1
    try:
        response_json = response.json()
        btc_price = float(response_json["data"]["priceUsd"])
        btc_price_label.text = "%.2f" % btc_price
        btc_price_delta_unformatted = float(response_json["data"]["changePercent24Hr"])
        btc_price_delta = round(btc_price_delta_unformatted, 1)
        if btc_price_delta >= 0:
            btc_price_label.color = GREEN
            btc_change_label.color = GREEN
            btc_change_label.text = str(btc_price_delta) + "%"
        else:
            btc_price_label.color = RED
            btc_change_label.color = RED
            btc_change_label.text = str(btc_price_delta) + "%"
    except (ValueError, RuntimeError) as e:
        print(str(response))
        print("Server not responding, retrying in 60 seconds. -", e)
        time.sleep(60)


    ######## ETH prices
    response = requests.get(ETH_URL, headers=header)
    num_requests += 1
    try:
        response_json = response.json()
        eth_price = float(response_json["data"]["priceUsd"])
        eth_price_label.text = "%.2f" % eth_price
        eth_price_delta_unformatted = float(response_json["data"]["changePercent24Hr"])
        eth_price_delta = round(eth_price_delta_unformatted, 1)
        if eth_price_delta >= 0.0:
            eth_price_label.color = GREEN
            eth_change_label.color = GREEN
            eth_change_label.text = str(eth_price_delta) + "%"
        else:
            eth_price_label.color = RED
            eth_change_label.color = RED
            eth_change_label.text = str(eth_price_delta) + "%"
    except (ValueError, RuntimeError) as e:
        print(str(response))
        print("Server not responding, retrying in 60 seconds. -", e)
        time.sleep(60)


    ######## XMR prices
    response = requests.get(XMR_URL, headers=header)
    num_requests += 1
    try:
        response_json = response.json()
        xmr_price = float(response_json["data"]["priceUsd"])
        xmr_price_label.text = "%.2f" % xmr_price
        xmr_price_delta_unformatted = float(response_json["data"]["changePercent24Hr"])
        xmr_price_delta = round(xmr_price_delta_unformatted, 1)
        if xmr_price_delta >= 0.0:
            xmr_price_label.color = GREEN
            xmr_change_label.color = GREEN
            xmr_change_label.text = str(xmr_price_delta) + "%"
        else:
            xmr_price_label.color = RED
            xmr_change_label.color = RED
            xmr_change_label.text = str(xmr_price_delta) + "%"
    except (ValueError, RuntimeError) as e:
        print(str(response))
        print("Server not responding, retrying in 60 seconds. -", e)
        time.sleep(60)

    num_loops += 1
    print("Loops=" + str(num_loops) + " Requests=" + str(num_requests) )
    time.sleep(180)
