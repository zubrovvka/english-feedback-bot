@echo off
chcp 65001 > nul
echo ========================================================
echo   Запуск персонального English Feedback & ReWord Bot
echo ========================================================
cd /d "%~dp0"
python bot.py
pause
