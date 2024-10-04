# Inventory Management System

## Overview

The Inventory Management System is a backend application built using Django and Django Rest Framework (DRF). This API allows businesses to efficiently manage their stock of products, providing secure access through JWT-based authentication.

## Features

- **CRUD Operations**: Create, read, update, and delete inventory items.
- **JWT Authentication**: Secure endpoints with JWT-based authentication.
- **Caching**: Improve performance with Redis caching for frequently accessed items.
- **Logging**: Comprehensive logging for monitoring API usage and errors.
- **Testing**: Via Postman.

## Technologies Used

- Django
- Django Rest Framework
- PostgreSQL
- Redis
- Python

## Requirements

- Python 3.x
- PostgreSQL
- Redis

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Ananthu303/Inventory-Management-API.git


2. Navigate to the project directory:

        cd inventory_management 

    ## Create a virtual environment:

        python -m venv venv

    ## Activate the virtual environment:

    ## On Windows:
        venv\Scripts\activate

    ## On macOS/Linux:
        source venv/bin/activate


3. Install the required packages:

    pip install -r requirements.txt


4. Install Redis (if not installed on your system):

    Since Redis does not support Windows directly, download the Redis executable from this link.
    ## https://sourceforge.net/projects/redis-for-windows.mirror/
    
        Download --> Open & Extract files --> Redis-x64-5.0.14.1 --> redis-server

        Redis server starts...


5. Set up the database (Current setup - PostgreSQL):

    Rename the `.env_sample` file to `.env` and fill in the required database values for your setup.

    Run the migrations:

    python manage.py makemigrations
    python manage.py migrate


6. Run the development server:

    python manage.py runserver

7. Testing:
   
    To test the API endpoints, you can use the provided Postman collection located in the root directory: `Inventory API.postman_collection.json`. 

    ### Steps to Test:
    1. Open Postman.
    2. Click on "Import" at the top left.
    3. Select the `Inventory API.postman_collection.json` file from the project root directory.
    4. Once imported, you will see all the API endpoints listed.
    5. Test the endpoints using Postman by sending requests to the API.

    ## Endpoints
        User Registration: POST /register/
        User Login: POST /login/
        Create Item: POST /items/
        Read Item: GET /items/{item_id}/
        Update Item: PUT /items/{item_id}/
        Delete Item: DELETE /items/{item_id}/


8. Logging
    Logs are stored in the logs directory under the name `inventory.log`.