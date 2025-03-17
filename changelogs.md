#### 2025-03-06:

Setting up project.

- Setup python virtual environment
- Install FastAPI module and dependecies

#### 2025-03-07

- Setting up DB
- Installed sqlite3 module and dependecies
- Created python objects for house, user, taxrecord and assignment to be used by SQLModel to create DB tables
- Created db.py to interact with db and carry out table creation opeartions

- Setting up authentication
- Implemented JWT token based authentication system
- Access token, refresh token and delete

- Setting up methods for serving the endpoints
- Method neet to be refactored
- Routing yet to be done

#### 2025-03-08

- Restructed the project with MVC architecture
- Added routes

- Updated authentication dependencies for routes
- Removed redundancies in the method callings

#### 2025-03-09

- Resolved dependecy issue in non-route paths by injecting at endpoint

#### 2025-03-15

- Added tests for authentication
- Refactored code following best practices

#### 2025-03-16

- Added tests for houses
- Bulkified house's service class

#### 2025-03-17

- Updated existing tests with pyfixtures

- Added tests for taxRecord
- Bulkified taxRecord's service class

- Added tests for assignment and db

- Documented and formatted the project

### JWT

`iss` (issuer): identifies the principal that issued the JWT.
`sub` (subject): identifies the principal that is the subject of the JWT. Must be unique
`aud` (audience): identifies the recipients that the JWT is intended for (array of strings/uri)
`exp` (expiration time): identifies the expiration time (UTC Unix) after which you must no longer accept this token. It should be after the issued-at time.
`nbf`(not before): identifies the UTC Unix time before which the JWT must not be accepted
`iat` (issued at): identifies the UTC Unix time at which the JWT was issued
`jti` (JWT ID): provides a unique identifier for the JWT.

# To-D0

Check alternate method for dependency injection in non-route path
