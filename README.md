# LostAndFound
this is analitic dashbord
# 🎒 Lost & Found Web Application

A simple and efficient **Lost & Found Management System** built using
**Python (Flask)** and **SQLite**.\
This application allows users to report lost items, post found items,
and search for items easily.

------------------------------------------------------------------------

## 🚀 Features

-   🔐 User Authentication (Signup / Login)
-   📝 Post Lost Items
-   📦 Post Found Items
-   🔍 Search Items
-   📊 Dashboard for managing posts
-   🗂 SQLite Database Integration
-   🎨 Clean UI with HTML & CSS
-   📁 Image Upload Support

------------------------------------------------------------------------

## 🛠 Tech Stack

-   **Backend:** Python, Flask
-   **Database:** SQLite
-   **Frontend:** HTML, CSS
-   **Templating Engine:** Jinja2
-   **File Uploads:** Local Upload Folder

------------------------------------------------------------------------

## 📁 Project Structure

    LostAndFound/
    │
    ├── main.py                # Main Flask application
    ├── models.py              # Database models
    ├── database.py            # Database connection & setup
    ├── lostandfound.db        # SQLite database
    │
    ├── templates/             # HTML templates
    │   ├── base.html
    │   ├── home.html
    │   ├── login.html
    │   ├── signup.html
    │   ├── dashboard.html
    │   ├── postlost.html
    │   ├── postfound.html
    │   ├── search.html
    │   └── index.html
    │
    ├── static/
    │   └── style.css          # CSS Styling
    │
    ├── uploads/               # Uploaded item images
    │
    └── README.md

------------------------------------------------------------------------

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

    git clone https://github.com/your-username/LostAndFound.git
    cd LostAndFound

### 2️⃣ Create Virtual Environment (Recommended)

    python -m venv venv

Activate it:

**Windows:**

    venv\Scripts\activate

**Mac/Linux:**

    source venv/bin/activate

### 3️⃣ Install Dependencies

    pip install flask

(Optional) Create requirements file:

    pip freeze > requirements.txt

### 4️⃣ Run the Application

    python main.py

### 5️⃣ Open in Browser

    http://127.0.0.1:5000

------------------------------------------------------------------------

## 🗄 Database

-   Uses SQLite database
-   File: `lostandfound.db`
-   Automatically created if not exists (depending on configuration)

------------------------------------------------------------------------

## 🔐 Production Notes

-   Disable debug mode before deployment
-   Use environment variables for secret keys
-   Consider using PostgreSQL/MySQL for production
-   Deploy on Render / Railway / VPS / AWS

------------------------------------------------------------------------

## 🧑‍💻 Author

Muskan Singh\
Software Developer

------------------------------------------------------------------------

## 📜 License

This project is open-source and available under the MIT License.

------------------------------------------------------------------------

⭐ If you like this project, don't forget to give it a star on GitHub!
