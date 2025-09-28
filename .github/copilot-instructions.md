# FastAPI Authentication System - Copilot Instructions

## Project Overview

This is a **FastAPI-based RESTful authentication system** designed as a production-ready authentication service with comprehensive security features. The system implements JWT-based authentication with refresh tokens, email verification, and Redis-backed session management.

## Architecture & Technology Stack

### Core Technologies
- **Backend Framework**: FastAPI (Python 3.12+)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens (access + refresh) using python-jose
- **Caching/Session**: Redis for email verification codes and TTL management
- **Password Security**: bcrypt for password hashing via passlib
- **API Documentation**: Auto-generated Swagger UI via FastAPI

### Project Structure
```
app/
├── main.py          # FastAPI application entry point
├── auth.py          # Authentication routes and JWT handling
├── crud.py          # Database CRUD operations
├── models.py        # SQLAlchemy database models
├── schemas.py       # Pydantic models for request/response validation
├── database.py      # Database connection and session management
├── utils.py         # Utility functions for token creation
└── routers/
    └── users.py     # User management routes
```

## Development Guidelines

### Security Best Practices
1. **Password Security**: Always use bcrypt hashing for passwords, never store plaintext
2. **JWT Management**: 
   - Use short-lived access tokens (30 min default)
   - Implement secure refresh token rotation
   - Store refresh tokens in database with expiration tracking
3. **Input Validation**: Use Pydantic models for all request/response validation
4. **Environment Variables**: Store sensitive data (SECRET_KEY, database URLs) in environment variables
5. **CORS**: Configure CORS properly for production deployments

### Code Style & Patterns
1. **FastAPI Patterns**: 
   - Use dependency injection for database sessions and authentication
   - Implement proper status codes and error responses
   - Follow FastAPI's response model patterns
2. **Database Operations**:
   - Use SQLAlchemy sessions properly with try/except/finally blocks
   - Implement proper transaction handling
   - Use database indexes for frequently queried fields
3. **Error Handling**: Use FastAPI's HTTPException with appropriate status codes

### Key Features Implementation
1. **Email Verification Flow**:
   - Generate 6-character random codes
   - Store in Redis with 5-minute TTL
   - Validate codes before user registration/login
2. **Authentication Flow**:
   - Email/password login returns access + refresh tokens
   - Protected routes require valid access token
   - Refresh endpoint allows token renewal
3. **User Management**:
   - CRUD operations for user profiles
   - Secure password updates
   - Account deletion with proper cleanup

### Development Environment
- **Local Setup**: Requires Redis server running locally
- **Database**: SQLite for development, easily configurable for PostgreSQL in production
- **Testing**: Use FastAPI's TestClient for endpoint testing
- **Documentation**: Access Swagger UI at `/docs` when server is running

### Common Pitfalls to Avoid
1. Don't expose sensitive information in error messages
2. Always validate JWT tokens in protected routes
3. Handle Redis connection failures gracefully
4. Don't forget to close database sessions
5. Implement proper CORS for frontend integration

### Future Enhancements
- SMTP integration for real email sending
- Docker containerization
- GitHub Actions CI/CD pipeline
- Rate limiting and security monitoring
- User role-based access control

## When Contributing
- Follow the existing code structure and naming conventions
- Add proper error handling and logging
- Update documentation for new endpoints
- Test authentication flows thoroughly
- Consider security implications of any changes