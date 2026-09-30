@echo off
cd /d "%~dp0"
py animation_viewer.py
if errorlevel 1 pause
