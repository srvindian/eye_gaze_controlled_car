@echo off
del /f "C:\Users\*** USER NAME ***\AppData\Local\Google\Chrome\User Data\chrome_debug.log"
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" DRIVE:\*** DIRECTORY TO WEBGAZER's ***\calibration.html --enable-logging --v=1
