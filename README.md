# PyPortal Titano Cryptocurrency Tracker
#### A crypto price tracker for Adafruit's PyPortal Titano
 This is a simple crypto price tracker for Adafruit's PyPortal Titano.

This tracker shows three crypto asset prices: BTC, ETH, and XMR. It uses CoinCap's API. It's very easy to modify if you want to add other crypto prices.

### Instructions:
1. Get yourself an Adafruit PyPortal Titano from https://www.adafruit.com/product/4465
2. Plug the Titano into your computer.
3. Download CircuitPython 7.x UF2 for your Titano: https://circuitpython.org/board/pyportal_titano/
4. Double-click the reset button your Titano, copy the CircuitPython UF2 to the device. 
5. Copy the project files to your device. The program will try to run, but it won't until we do a few more things.
6. Get the required CircuitPython 7.x runtime libraries here: https://circuitpython.org/libraries
7. Unzip the libraries on your local machine
8. Create a directory on your Titano called /lib
9. When you run the program, it will let you know which libraries are missing. Copy over the needed libraries from the ZIP files /lib folder to the /lib directory on your Titano.
10. Create a file called 'secrets.py' on your Titano.
11. Paste this into secrets.py:

```
secrets = {
 'ssid' : 'your_wifi_SSID_name',
 'password' : 'your_wifi_password',
 'api_key' : 'your_coincap_API_key',
 }
```


12. Replace the above placeholder WiFi credentials with your Wifi network credentials.
13. Get a CoinCap API key here: https://coincap.io/api-key
14. Replace the above placeholder with your CoinCap API key.
15. Save secrets.py to your Titano. 

Enjoy!
