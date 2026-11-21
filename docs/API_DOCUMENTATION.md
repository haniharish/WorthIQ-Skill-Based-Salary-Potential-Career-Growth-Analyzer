# WorthIQ Phase 1 API Documentation

Base URL: `http://localhost:8000/api`

---

## 1. Authentication Endpoints (`/api/auth/`)

### A. Register User
- **Endpoint**: `POST /api/auth/register/`
- **Permissions**: `AllowAny`
- **Request Body**:
  ```json
  {
    "full_name": "Rohan Sharma",
    "email": "rohan.sharma@example.com",
    "password": "Password123!",
    "confirm_password": "Password123!"
  }
  ```
- **Response** (`201 Created`):
  ```json
  {
    "message": "Account registered successfully.",
    "user": {
      "id": 1,
      "full_name": "Rohan Sharma",
      "email": "rohan.sharma@example.com",
      "date_joined": "2026-11-21T07:44:00Z",
      "is_active": true,
      "has_profile": false
    },
    "tokens": {
      "refresh": "eyJhbGciOi...",
      "access": "eyJhbGciOi..."
    }
  }
  ```

### B. User Login
- **Endpoint**: `POST /api/auth/login/`
- **Permissions**: `AllowAny`
- **Request Body**:
  ```json
  {
    "email": "rohan.sharma@example.com",
    "password": "Password123!"
  }
  ```
- **Response** (`200 OK`):
  ```json
  {
    "message": "Logged in successfully.",
    "user": {
      "id": 1,
      "full_name": "Rohan Sharma",
      "email": "rohan.sharma@example.com",
      "date_joined": "2026-11-21T07:44:00Z",
      "is_active": true,
      "has_profile": true
    },
    "tokens": {
      "refresh": "eyJhbGciOi...",
      "access": "eyJhbGciOi..."
    }
  }
  ```

### C. Refresh JWT Token
- **Endpoint**: `POST /api/auth/token/refresh/`
- **Permissions**: `AllowAny`
- **Request Body**:
  ```json
  {
    "refresh": "eyJhbGciOi..."
  }
  ```
- **Response** (`200 OK`):
  ```json
  {
    "access": "eyJhbGciOi...",
    "refresh": "eyJhbGciOi..."
  }
  ```

### D. Logout & Token Blacklist
- **Endpoint**: `POST /api/auth/logout/`
- **Permissions**: `IsAuthenticated` (Bearer `<access_token>`)
- **Request Body**:
  ```json
  {
    "refresh": "eyJhbGciOi..."
  }
  ```
- **Response** (`200 OK`):
  ```json
  {
    "message": "Logged out successfully."
  }
  ```

### E. Current User Details
- **Endpoint**: `GET /api/auth/me/`
- **Permissions**: `IsAuthenticated` (Bearer `<access_token>`)
- **Response** (`200 OK`):
  ```json
  {
    "id": 1,
    "full_name": "Rohan Sharma",
    "email": "rohan.sharma@example.com",
    "date_joined": "2026-11-21T07:44:00Z",
    "is_active": true,
    "has_profile": true
  }
  ```

---

## 2. Profile Management Endpoints (`/api/profile/`)

All profile endpoints require the `Authorization: Bearer <access_token>` header.

### A. Retrieve Profile
- **Endpoint**: `GET /api/profile/`
- **Permissions**: `IsAuthenticated`
- **Response** (`200 OK`):
  ```json
  {
    "id": 1,
    "user": {
      "id": 1,
      "full_name": "Rohan Sharma",
      "email": "rohan.sharma@example.com",
      "date_joined": "2026-11-21T07:44:00Z",
      "is_active": true,
      "has_profile": true
    },
    "job_role": "Full Stack Developer",
    "years_of_experience": "3.5",
    "location": "Bengaluru, India",
    "education": "B.Tech in Computer Science",
    "current_salary": "14.50",
    "skills": [
      { "id": 1, "name": "Python", "created_at": "..." },
      { "id": 2, "name": "Django", "created_at": "..." },
      { "id": 3, "name": "React.js", "created_at": "..." }
    ],
    "created_at": "2026-11-21T07:45:00Z",
    "updated_at": "2026-11-21T07:45:00Z"
  }
  ```
- **Response if Profile Not Found** (`404 Not Found`):
  ```json
  {
    "detail": "Profile not found. Please complete profile setup.",
    "has_profile": false
  }
  ```

### B. Create Profile
- **Endpoint**: `POST /api/profile/`
- **Permissions**: `IsAuthenticated`
- **Request Body**:
  ```json
  {
    "job_role": "Full Stack Developer",
    "years_of_experience": 3.5,
    "location": "Bengaluru, India",
    "education": "B.Tech in Computer Science",
    "current_salary": 14.5,
    "skills_input": ["Python", "Django", "React.js", "PostgreSQL", "Docker"]
  }
  ```
- **Response** (`201 Created`): Returns created `UserProfile` object.

### C. Update Profile (Full / PUT)
- **Endpoint**: `PUT /api/profile/`
- **Permissions**: `IsAuthenticated`
- **Request Body**: All fields required.
- **Response** (`200 OK`): Returns updated `UserProfile` object.

### D. Update Profile (Partial / PATCH)
- **Endpoint**: `PATCH /api/profile/`
- **Permissions**: `IsAuthenticated`
- **Request Body**: Any subset of fields:
  ```json
  {
    "years_of_experience": 4.5,
    "current_salary": 16.0
  }
  ```
- **Response** (`200 OK`): Returns updated `UserProfile` object.

### E. Skills Catalog
- **Endpoint**: `GET /api/profile/skills/?search=react`
- **Permissions**: `AllowAny`
- **Response** (`200 OK`):
  ```json
  [
    { "id": 3, "name": "React.js", "created_at": "..." }
  ]
  ```
