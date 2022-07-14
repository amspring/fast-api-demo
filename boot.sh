#!/bin/bash
if [ -f .env ]; then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

typeset -l ENV
ENV=$PROJECT_ENV
cp "config/config.${ENV}.yml" config.yml

echo "install requirements"
/opt/python3.10.2/bin/python3.10 -m pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

echo "copy api.ini to /var/app/conf/supervisord.d"
cp config/api.ini /var/app/conf/supervisord.d

echo "update and restart service"
supervisorctl update && supervisorctl restart api

echo "Success!"