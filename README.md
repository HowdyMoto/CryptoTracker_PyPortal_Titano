# PyPortal Titano Cryptocurrency Tracker
#### A crypto price tracker for Adafruit's PyPortal Titano
 This is a simple crypto price tracker for Adafruit's PyPortal Titano. It uses CoinCap's API.

This tracker shows three crypto asset prices, which the user can specify.

### Instructions:
1. Get yourself an Adafruit PyPortal Titano from https://www.adafruit.com/product/4465
2. Plug the Titano into your computer
3. Download CircuitPython 7.x UF2 for your Titano: https://circuitpython.org/board/pyportal_titano/
4. Double-click the reset button your Titano, copy the CircuitPython UF2 to the device
5. Copy the project files to your device. The program will try to run, but it won't until we do a few more things
6. Get the required CircuitPython 7.x runtime libraries here: https://circuitpython.org/libraries
7. Unzip the libraries on your local machine
8. Create a directory on your Titano called /lib
9. When you run the program, it will let you know which libraries are missing. Copy over the needed libraries from the ZIP files /lib folder to the /lib directory on your Titano.
10. Create a file called 'secrets.py' on your Titano
11. Paste this into secrets.py:
```
secrets = {
 'ssid' : 'your_wifi_SSID_name',
 'password' : 'your_wifi_password',
 'coincap_api_key' : 'your_coincap_API_key',
 
 'coin1' : 'bitcoin',
 'coin2' : 'ethereum',
 'coin3' : 'monero',
 'coin1label' : 'BTC',
 'coin2label' : 'ETH',
 'coin3label' : 'XMR',
 }
```
12. Replace the above placeholder WiFi credentials with your Wifi network credentials
13. Replace 'coin1' etc with the names of the coins you want to track
14. Replqace 'coin1label' etc with the abbreviations you want to show for each coin on the tracker (there's not enough room to show long names)
15. Get a CoinCap API key here: https://coincap.io/api-key
16. Replace the above placeholder with your CoinCap API key
17. Save secrets.py to your Titano

### ESP32 crashes
I have tested two boards, and both of them always crash after an unpredictable amount of time with this error in the esp32 libraries.
```
RuntimeError: ESP32 timed out on SPI select
```
After combing the Adafruit forums, seems like there no solution to this issue out there. So, there is code in the app that tries to detect this error and reboot the device.


