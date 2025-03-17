# Tax Collection System

The **Tax Collection System** is a FastAPI-based application designed to manage tax records, user assignments, and authentication for a tax collection service. It provides a robust API for managing houses, tax records, user roles, and assignments, with secure authentication and role-based access control.

---

## Features

- **Authentication**: Implements JWT-based authentication with access and refresh tokens.
- **Role-Based Access Control**: Supports roles such as `ADMIN` and `COLLECTOR` for secure access to endpoints.
- **House Management**: Create, retrieve, and manage house records.
- **Tax Record Management**: Insert, retrieve, and update tax records.
- **User Management**: Register users with role-based permissions.
- **Assignment Management**: Assign collectors to houses for tax collection.
- **Database Integration**: Uses SQLModel for ORM and SQLite for database management.
- **Unit Tests**: Comprehensive test coverage for all major functionalities.

---

## Project Structure

├── auth/ # Authentication utilities
├── controller/ # Business logic for various modules
├── db.py # Database setup and session management
├── main.py # Entry point for the FastAPI application
├── objects/ # Data models for houses, users, tax records, etc.
├── service/ # API routes and handlers
├── tests/ # Unit tests for the application
├── requirements.txt # Python dependencies
├── pyproject.toml # Configuration for code formatting and linting
└── README.md # Project documentation

---

## Installation

1. Clone the repository:

   ```
   bash
   git clone https://github.com/krishnakarthikperi/TaxCollectionSystem-Backend.git
   cd Tax-Collection
   ```

2. Create a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   uvicorn main:app --reload
   ```

---

## Endpoints

#### Authentication

- `POST /token`: Authenticate a user and return access and refresh tokens.
- `POST /token/refresh`: Refresh an expired access token.
- `POST /logout`: Log out the currently authenticated user.

#### User Management

- `POST /register`: Register a new user (Admin-only).

#### House Management

- `POST /house`: Create new house records.
- `GET /households`: Retrieve all house records.
- `GET /households/{household_id}`: Retrieve house records by household ID.

#### Tax Record Management

- `POST /recordcollections`: Insert multiple tax records.
- `GET /gettaxrecords`: Retrieve all tax records.
- `GET /tax-records/{houseNumber}`: Retrieve tax records for a specific house.
- `PUT /tax-record/{recordId}`: Update a specific tax record.

#### Assignment Management

- `POST /assign-collector`: Assign a collector to a house (Admin-only).
- `GET /assignments/{collector_id}`: Retrieve assignments for a specific user.

---

## Testing

Run the unit tests using pytest:
```pytest```

---

## Configuration

#### Database

The application uses SQLite as the database. The database file is located at taxcollection1.db. To initialize the database and create tables, run:
`python db.py`

#### Code Formatting and Linting

- **Black**: Code formatter configured in pyproject.toml.
- **Ruff**: Linter configured in pyproject.toml.

---

## JWT Configuration

The application uses JWT for authentication. Key configurations include:

- **Access Token Expiry**: 30 minutes
- **Refresh Token Expiry**: 7 days
- **Algorithm**: HS256
- **Keys**: Update ACCESS_SECRET_KEY and REFRESH_SECRET_KEY in auth/authconstants.py before deployment.

---

## To-Do

- <input disabled="" type="checkbox"> Explore alternate methods for dependency injection in non-route paths.
- <input disabled="" type="checkbox"> Add more granular role-based permissions for endpoints.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contributors

- **Krishna Karthik Peri** - Developer
