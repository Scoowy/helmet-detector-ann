#!/bin/env python
from app import createApp, socketio

app = createApp(debug=False)

if __name__ == '__main__':
    print('Starting server...')
    socketio.run(app, host='127.0.0.1', port=8000)
    print(f'Server started! Listening on port 8000')
