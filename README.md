# DjangoChat

This is a simple Backend API for a Chat App built using Django Rest Framework.

## To run the project

1. Setup the virtual environment.
2. Install `django`, `restframework`, `channels` and other requirements.
3. Run `python manage.py runserver` to start the server.

## API Endpoints

- User registration: POST `/api/register/`
- User login: POST `/api/login/`
- Start a chat: POST `/api/chat/start/`
- Send a message: WEBSOCKET `/api/chat/send/`