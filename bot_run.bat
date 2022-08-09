@echo off

call %~dp0WOK_restaurant\venv\Scripts\activate

cd %~dp0WOK_restaurant

set TOKEN=5528805122:AAECuRWAWKMbMtHemV5jzKHISZjMwEbCv5A

python bot_tg.py

pause