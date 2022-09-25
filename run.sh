#!/bin/bash

export TELEGRAM_TOKEN='your telegram bot token'

export MOS_LOGIN='your mos.ru login'
export MOS_PASSWORD='your mos.ru password'

pip install --ignore-installed -r requires.txt

python main.py