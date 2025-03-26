# **🚀 Django Ride Management API**

This is a Django-based Ride Management API that allows users to book, update, and track rides.

---

## **📌 Prerequisites**
Make sure you have the following installed before running the project:

- Python (>= 3.8)  
- pip (Package Manager for Python)  
- Virtualenv (Recommended)  
- PostgreSQL or SQLite (as per `DATABASES` settings)  

---

## **🛠 Installation & Setup**

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/romeodancil/drf-rides-api
cd your-repo
```

### **2️⃣ Create and Activate Virtual Environment**
```sh
python -m venv venv
# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **5️⃣ Run Database Migrations**
```sh
python manage.py makemigrations
python manage.py migrate
```
## **🚀 Testing the Application**
```sh
python manage.py runserver
```
Open your postman
---

## **📡 API Endpoints**
| Endpoint                 | Method | Description                    | Authentication |
|--------------------------|--------|--------------------------------|---------------|
| `/user`                  | GET    | List all users                 | Required      |
| `/user`                  | POST   | Create User (User/Admin type)  | Required      |
| `/api/token/`            | POST   | Obtain auth token (DRF Token)  | Required      |
| `/ride`                  | GET    | List all the rides             | Required      |
| `/ride`                  | POST   | Booking a ride                 | Required      |
| `/ride`                  | PUT    | Update my ride                 | Required      |
| `/ride-events`           | GET    | List all ride events           | Required      |
| `/ride-events`           | POST   | Create ride events             | Required      |

---

## **🔑 Authentication**
This API uses **Token Authentication**.  

To authenticate, include the token in the headers:  
```sh
Authorization: Token your-token-here
```

---

## **📄 License**
This project is licensed under the **MIT License**.

