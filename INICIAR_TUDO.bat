@echo off
title Servidor de Automacao

echo Garante que o script esta rodando na pasta certa...
cd /d "%~dp0"
echo Pasta atual: %cd%
echo.

echo Iniciando o servidor...

REM Edite a linha abaixo com o caminho que o comando 'where python' retornou!
"C:\Users\Robo01\AppData\Local\Programs\Python\Python311\python.exe" servidor_unico.py

echo.
pause