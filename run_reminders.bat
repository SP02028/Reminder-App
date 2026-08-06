@echo off
cd /d "%~dp0"
"C:\Users\palsh\AppData\Local\Python\pythoncore-3.14-64\python.exe" main.py >> logs\reminder.log 2>&1
