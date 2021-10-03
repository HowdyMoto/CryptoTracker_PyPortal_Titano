# CryptoTracker_PyPortal_Titano
 Crypto price tracker for Adafruit's PyPortal Titano

This tracker shows three crypto asset prices: BTC, ETH, and XMR. It uses CoinCap's API.

Instructions:
Get yourself an Adafruit PyPortal Titano from https://www.adafruit.com/product/4465
Plug the Titano into your computer.
Download CircuitPython 7 UF2 for your Titano: https://circuitpython.org/board/pyportal_titano/
Double-click the reset button your Titano, copy this above UF2 to the device.
Copy the project files to your device. The program will try to ru, but won't be able to log into your WiFi until you give it credentials.
Create a files called 'secrets.py' on your Titano.
Paste this into the file:
secrets = {
    'ssid' : 'your_wifi_SSID_name',
    'password' : 'your_wifi_password',
    'api_key' : 'your_coincap_API_key',
    }

Replace the above placeholder with your Wifi network credentials.
Get an API key here: https://coincap.io/api-key
Replace the above placeholder with your API key.

Save secrets.py to your Titano. 
Enjoy!