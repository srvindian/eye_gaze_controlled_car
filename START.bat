@echo off
del /f "C:\Users\Sourav\AppData\Local\Google\Chrome\User Data\chrome_debug.log"
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" E:\GMIT\EyeGaze\WebGazer-master\www\calibration.html --enable-logging --v=1
