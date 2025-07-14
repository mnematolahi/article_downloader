@echo off
title Poweren.ir Downloader - Mostafa
echo Checking Python and required packages...
python -m pip install --upgrade pip
pip install selenium undetected-chromedriver tqdm

echo.
echo Running downloader script...
python main.py

pause
