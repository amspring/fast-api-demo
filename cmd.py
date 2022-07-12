# -*- coding: utf-8 -*-
# Project  : app
# File     : cmd.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-06-17 11:51
# Remarks  :
from app import create_app

app = create_app()

if __name__ == '__main__':
    import uvicorn
    from app import settings

    uvicorn.run(app='cmd:app', host=settings.app.host, port=settings.app.port, reload=True, debug=True)
