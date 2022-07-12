#!/bin/bash
if [ -f .env ]; then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

typeset -l ENV
ENV=$PROJECT_ENV
cp "config/config.${ENV}.yml" config.yml

echo "remove all log..."
rm -rf *log*

echo "install requirements"
/opt/python3.9.7/bin/python3.9 -m pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

echo "copy api.ini to /home/mooc/supervisord.d"
cp api.ini /home/mooc/supervisord.d

echo "start service"
supervisorctl update && supervisorctl restart api

echo "enjoy!"