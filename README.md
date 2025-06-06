# Community Help Platform

A web application that connects people requesting assistance with volunteers in their local area. The platform supports posting and browsing help requests, applying to assist, and communicating through real-time messaging.

## Features

- User registration and authentication (JWT-based)
- Role-based access: Requesters and Volunteers
- Create and manage help posts with optional file uploads
- Browse and apply for available help requests
- Geolocation-based prioritization of posts
- Real-time messaging using WebSockets
- Scalable backend with API-based architecture

## Tech Stack

**Frontend**  
- Vue.js  
- Axios (for API communication)

**Backend**  
- Django  
- Django REST Framework  
- Django Channels
- JWT Authentication

**Real-Time Messaging**  
- **WebSockets** via **Django Channels**
- Enables chat between users involved in a help post
- Optional future support for group chat or status updates

**Database**  
- PostgreSQL  
- Firebase (planned for real-time communication and file storage)

## Project Structure




## Setup Instructions

### Backend (Django)

```bash
cd backend
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


cd frontend
npm install
npm run dev

