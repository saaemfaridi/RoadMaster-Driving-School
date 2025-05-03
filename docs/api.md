# RoadMaster API Documentation

This document outlines the API endpoints available in the RoadMaster application.

## Authentication

All API endpoints require authentication. Authentication is done via JWT tokens.

To obtain a token, make a POST request to the `/api/auth/login` endpoint with your credentials:

```
POST /api/auth/login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

The response will include a token that should be included in the `Authorization` header for all subsequent requests:

```
Authorization: Bearer <your_token>
```

## API Endpoints

### Status

```
GET /api/status
```

Returns the current status of the API.

**Response:**
```json
{
  "status": "online"
}
```

### Bookings

#### Get All Bookings

```
GET /api/bookings
```

Returns a list of all bookings.

**Response:**
```json
{
  "bookings": [
    {
      "id": 1,
      "name": "John Doe",
      "phone": "+1234567890",
      "lesson_type": "Standard Driving Lesson",
      "slot_datetime": "2023-12-01 10:00:00",
      "created_at": "2023-11-15 10:30:00"
    }
  ]
}
```

#### Get a Specific Booking

```
GET /api/bookings/:id
```

Returns details for a specific booking.

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "phone": "+1234567890",
  "lesson_type": "Standard Driving Lesson",
  "slot_datetime": "2023-12-01 10:00:00",
  "created_at": "2023-11-15 10:30:00"
}
```

#### Create a Booking

```
POST /api/bookings
Content-Type: application/json

{
  "name": "Jane Smith",
  "phone": "+1987654321",
  "lesson_type": "Advanced Driving Lesson",
  "slot_datetime": "2023-12-05 14:00:00"
}
```

Creates a new booking.

**Response:**
```json
{
  "id": 2,
  "name": "Jane Smith",
  "phone": "+1987654321",
  "lesson_type": "Advanced Driving Lesson",
  "slot_datetime": "2023-12-05 14:00:00",
  "created_at": "2023-11-16 09:45:00"
}
```

#### Update a Booking

```
PUT /api/bookings/:id
Content-Type: application/json

{
  "lesson_type": "Emergency Driving Lesson",
  "slot_datetime": "2023-12-05 16:00:00"
}
```

Updates an existing booking. Only include the fields you want to update.

**Response:**
```json
{
  "id": 2,
  "name": "Jane Smith",
  "phone": "+1987654321",
  "lesson_type": "Emergency Driving Lesson",
  "slot_datetime": "2023-12-05 16:00:00",
  "created_at": "2023-11-16 09:45:00"
}
```

#### Delete a Booking

```
DELETE /api/bookings/:id
```

Deletes a booking.

**Response:**
```json
{
  "message": "Booking deleted successfully"
}
```

### Tasks

#### Get All Tasks

```
GET /api/tasks
```

Returns a list of all tasks for the authenticated user.

**Response:**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Task title",
      "description": "Task description",
      "due_date": "2023-12-31T23:59:59",
      "completed": false,
      "priority": 1,
      "created_at": "2023-11-15T10:30:00"
    }
  ]
}
```

#### Get a Specific Task

```
GET /api/tasks/:id
```

Returns details for a specific task.

**Response:**
```json
{
  "id": 1,
  "title": "Task title",
  "description": "Task description",
  "due_date": "2023-12-31T23:59:59",
  "completed": false,
  "priority": 1,
  "created_at": "2023-11-15T10:30:00"
}
```

#### Create a Task

```
POST /api/tasks
Content-Type: application/json

{
  "title": "New task",
  "description": "Task description",
  "due_date": "2023-12-31T23:59:59",
  "priority": 2
}
```

Creates a new task.

**Response:**
```json
{
  "id": 2,
  "title": "New task",
  "description": "Task description",
  "due_date": "2023-12-31T23:59:59",
  "completed": false,
  "priority": 2,
  "created_at": "2023-11-16T14:20:00"
}
```

#### Update a Task

```
PUT /api/tasks/:id
Content-Type: application/json

{
  "title": "Updated task title",
  "completed": true
}
```

Updates an existing task. Only include the fields you want to update.

**Response:**
```json
{
  "id": 2,
  "title": "Updated task title",
  "description": "Task description",
  "due_date": "2023-12-31T23:59:59",
  "completed": true,
  "priority": 2,
  "created_at": "2023-11-16T14:20:00"
}
```

#### Delete a Task

```
DELETE /api/tasks/:id
```

Deletes a task.

**Response:**
```json
{
  "message": "Task deleted successfully"
}
```

### Users

#### Get User Profile

```
GET /api/users/profile
```

Returns the profile of the authenticated user.

**Response:**
```json
{
  "id": 1,
  "username": "user123",
  "email": "user@example.com",
  "phone_number": "+1234567890",
  "created_at": "2023-10-01T08:00:00"
}
```

#### Update User Profile

```
PUT /api/users/profile
Content-Type: application/json

{
  "email": "newemail@example.com",
  "phone_number": "+9876543210"
}
```

Updates the profile of the authenticated user.

**Response:**
```json
{
  "id": 1,
  "username": "user123",
  "email": "newemail@example.com",
  "phone_number": "+9876543210",
  "created_at": "2023-10-01T08:00:00"
}
```

## Error Responses

All API endpoints return standard HTTP status codes to indicate success or failure.

In case of an error, the response body will include an error message:

```json
{
  "error": "Error message"
}
```

Common error codes:
- 400: Bad Request - The request was invalid
- 401: Unauthorized - Authentication is required
- 403: Forbidden - The user does not have permission
- 404: Not Found - The requested resource was not found
- 500: Internal Server Error - An unexpected error occurred

## Rate Limiting

API requests are limited to 100 requests per minute per user. If you exceed this limit, you'll receive a 429 Too Many Requests response. 