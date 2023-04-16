
@rem
@echo off

setlocal

"%~dp0/../runtime/python.exe" -m awscli %*
