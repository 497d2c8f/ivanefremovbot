from python:3
workdir /aiogram/
copy requirements .
run pip install --upgrade pip && pip install -r requirements
copy . .
entrypoint python3 main.py
