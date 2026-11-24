@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
echo ========================================================
echo   Запуск персонального Web-тренажера English Feedback
echo ========================================================
cd /d "%~dp0"
start http://127.0.0.1:5000
python app.py
pause
