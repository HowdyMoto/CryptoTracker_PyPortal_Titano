# CryptoTracker_PyPortal_Titano
 This is a simple crypto price tracker for Adafruit's PyPortal Titano.

This tracker shows three crypto asset prices: BTC, ETH, and XMR. It uses CoinCap's API. It's very easy to modify if you want to add other crypto prices.

Instructions:
1. Get yourself an Adafruit PyPortal Titano from https://www.adafruit.com/product/4465
2. Plug the Titano into your computer.
3. Download CircuitPython 7.x UF2 for your Titano: https://circuitpython.org/board/pyportal_titano/
4. Double-click the reset button your Titano, copy this above UF2 to the device.
5. Copy the project files to your device. The program will try to ru, but won't be able to log into your WiFi until you give it credentials.
6. Create a files called 'secrets.py' on your Titano.
7. Paste this into the file:
secrets = {
    'ssid' : 'your_wifi_SSID_name',
    'password' : 'your_wifi_password',
    'api_key' : 'your_coincap_API_key',
    }

8. Replace the above placeholder with your Wifi network credentials.
9. Get an API key here: https://coincap.io/api-key
10. Replace the above placeholder with your API key.
11. Save secrets.py to your Titano. 
12. Get the required CircuitPython 7.x runtime libraries here: https://circuitpython.org/libraries
13. Unzip the libraries on your local machine
14. Create a directory on Titano called /lib
14. When you run the program, it will let you know which libraries are missing. Copy over the needed libraries from the ZIP files /lib folder to the /lib directory on your Titano.
15. Enjoy!
