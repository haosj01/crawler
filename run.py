#!/usr/bin/python
# -*- coding: UTF-8 -*-

from setting import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050,threaded=True)