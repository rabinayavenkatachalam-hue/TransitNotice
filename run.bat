@echo off
title TransitNotice - Tamil Nadu Public Transport Tracker
echo ========================================================
echo   TransitNotice - Tamil Nadu Public Transport Tracker
echo   All 38 Districts Official Advisory Aggregator
echo ========================================================
echo.
echo Starting Flask web server...
set FLASK_SKIP_DOTENV=1
python app.py
pause
