# Library Management System

This is a simple library management system built with Django.

## Features

- Book management
- User management
- Loan management
- Basic reporting

## Setup

1. Clone the repository
2. Install Docker and Docker Compose
3. Run `docker-compose up --build`
4. Access the application at http://localhost:8000

## Running Tests

Run `docker-compose run web python manage.py test`

## Deployment

This project is configured for deployment with Docker, Gunicorn, and Whitenoise for static files.
