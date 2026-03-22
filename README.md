# Task Manager API
## Overview
The Task Manager API is a RESTful API designed to manage tasks and users. It provides endpoints for creating, reading, updating, and deleting tasks and users.

## Application Information
* **App Name:** task-manager
* **App Description:** A REST API for managing tasks
* **App Version:** 1.0.0

## Dependencies
The Task Manager API depends on the following libraries:
* fastapi
* uvicorn
* sqlalchemy
* pydantic
* python-jose
* passlib

## Usage
To run the Task Manager API, follow these steps:
1. Clone the repository using `git clone`
2. Create a virtual environment using `python -m venv venv`
3. Activate the virtual environment using `source venv/bin/activate` (on Linux/Mac) or `venv\Scripts\activate` (on Windows)
4. Install the dependencies using `pip install -r requirements.txt`
5. Create a `.env` file with the required environment variables (see `.env.example` for an example)
6. Run the API using `uvicorn main:app --host 0.0.0.0 --port 8000`

## API Endpoints
The Task Manager API provides the following endpoints:
### Tasks
* **GET /tasks**: Retrieve a list of all tasks
* **POST /tasks**: Create a new task
* **GET /tasks/{task_id}**: Retrieve a task by ID
* **PUT /tasks/{task_id}**: Update a task
* **DELETE /tasks/{task_id}**: Delete a task

### Users
* **GET /users**: Retrieve a list of all users
* **POST /users**: Create a new user
* **GET /users/{user_id}**: Retrieve a user by ID
* **PUT /users/{user_id}**: Update a user
* **DELETE /users/{user_id}**: Delete a user

## API Documentation
For more information about the API endpoints, including request and response formats, please refer to the API documentation at `/docs`.