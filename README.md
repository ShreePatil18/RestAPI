# 📞 Spam Caller API

This is a Flask-based API that provides functionality for user registration, login, user search, and marking phone numbers as spam. It also includes JWT-based authentication and password hashing using Flask-Bcrypt.

---

## 🚀 Features

- 📝 **User Registration**: Register a user with name, email, phone number, and password.
- 🔒 **User Login**: Authenticate users using phone number and password.
- 🔍 **Search User**: Find users by their phone number and view spam reports against them.
- 🚫 **Mark as Spam**: Allow logged-in users to mark phone numbers as spam.
- 🔐 **JWT Authentication**: Secure endpoints with token-based authentication.
- 🔑 **Password Hashing**: Safely store user passwords.

---

## 🛠️ Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set Up MySQL Database**:
   Create a database named `caller` and execute the following schema:
   ```sql
   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100),
       password VARCHAR(255),
       email VARCHAR(100),
       phone_no VARCHAR(15) UNIQUE
   );

   CREATE TABLE SpamRecord (
       id VARCHAR(36) PRIMARY KEY,
       phone_number VARCHAR(15),
       marked_by VARCHAR(255)
   );
   ```

4. **Update Database Configuration**:
   Modify the `db_config` variable in the code with your MySQL credentials:
   ```python
   db_config = {
       'host': '127.0.0.1',
       'port': '3306',
       'user': 'root',
       'password': '<your-password>',
       'database': 'caller'
   }
   ```

5. **Run the Application**:
   ```bash
   python app.py
   ```

---

## 🔗 API Endpoints

### 1. **User Registration**
- **Endpoint**: `/users/register`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "1234567890",
      "password": "password123"
  }
  ```
- **Response**:
  - Success: `201 - User registered successfully`
  - Error: `400 - Phone number and password are required`
  - Conflict: `409 - Phone number already exists`

### 2. **User Login**
- **Endpoint**: `/users/login`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
      "phone": "1234567890",
      "password": "password123"
  }
  ```
- **Response**:
  - Success: `200 - {"access_token": "<token>"}`
  - Error: `400 - Phone number and password are required`
  - Unauthorized: `401 - Invalid username or password`

### 3. **Search User**
- **Endpoint**: `/users/search`
- **Method**: `GET`
- **Headers**:
  ```
  Authorization: Bearer <token>
  ```
- **Request Body**:
  ```json
  {
      "phone": "1234567890"
  }
  ```
- **Response**:
  - Success: `200 - {"id": 1, "name": "John Doe", "phone_no": "1234567890", "marked_as_spam_by": 5}`
  - Not Found: `404 - User not found`

### 4. **Mark as Spam**
- **Endpoint**: `/users/addspam`
- **Method**: `POST`
- **Headers**:
  ```
  Authorization: Bearer <token>
  ```
- **Request Body**:
  ```json
  {
      "phone": "1234567890"
  }
  ```
- **Response**:
  - Success: `201 - Phone number marked as spam successfully`

---

## 🛡️ Security

- **JWT Tokens** are used to secure endpoints.
- **Hashed Passwords** ensure password security.
- **Input Validation** prevents SQL injection.

---

## 📂 Directory Structure

```plaintext
/
├── app.py                # Main application file
├── requirements.txt      # Dependencies
└── README.md             # Documentation (this file)
```

---

## 📋 Dependencies

- Flask
- Flask-RESTful
- Flask-Bcrypt
- Flask-JWT-Extended
- mysql-connector-python

Install all dependencies with:
```bash
pip install -r requirements.txt
```

---

## 🛠️ Configuration

- Update `JWT_SECRET_KEY` for enhanced security.
- Customize `db_config` for your database.

---

## 🎉 How to Use

1. Register a user using `/users/register`.
2. Log in to get a JWT token.
3. Use the token to access protected endpoints like `/users/search` and `/users/addspam`.


