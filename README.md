# Introdcution to wongnok-recipes
เว็บแอปพลิเคชันรวบรวมสูตรอาหาร หรือ "Wongnok recipes" เปิดให้ผู้เยี่ยมชมทั่วไปสามารถ
เข้ามาสืบค้นสูตรอาหารผ่านชื่อเมนูหรือวัตถุดิขได้  หากยังไม่รู้ชื่อเมนูหรือวัตถุดิบสามารถสืบคั้นได้จาก
เงื่อนไข "ระยะเวลาที่ใช้ในการปรุงอาหาร" และ "ความยากง่ายของเมนู" ได้ โดยระบบจะแสดงผลลัพธ์ที่
ตรงกับเงื่อนไขมาให้ นอกจากนี้ยังมีระบบสมาชิกที่สามารถสมัครเพื่อสร้าง, แก้ไข หรือลบสูตรของตัว
เอง รวมถึงให้คะแนนสูตรอาหารของเพื่อนสมาชิกคนอื่นได้

ขั้นตอนการรัน web application และ การใช้งานเบื้องต้น

first time: ................................
create new environment
> cd 505330-wongnok-recipes 
> conda create --name wk-be python=3.11
> conda activate wk-be
> pip install -r reqiurement.txt
create database - Prerequire:sqlite is installed
> python database.py
> python models.py 

Run Project
> uvicon main:app --reload

Workspace Directory Detail
wongnok_recipes/
│
├── backend/             # All backend-related files
│   ├── app/             # Main application package
│   │   ├── __init__.py  # Initializes the Python package
│   │   ├── main.py      # FastAPI application instance and routes
│   │   ├── models.py    # Database models
│   │   ├── schemas.py   # Pydantic models for request/response validation
│   │   ├── crud.py      # CRUD operations (interaction with the database)
│   │   └── database.py  # Database session management and engine
│   │
│   ├── tests/           # Test modules for the backend
│   │   └── test_api.py  # Test cases for API endpoints
│   │
│   └── requirements.txt # Project dependencies
│
├── frontend/            # Frontend-related files (Streamlit app)
│   ├── app.py           # Streamlit application
│   └── requirements.txt # Frontend dependencies
│
├── scripts/             # Utility scripts, e.g., for setting up the database
│   └── init_db.py       # Script for initializing the database
│
└── README.md            # Project overview and setup instructions


.
├── README.md
├── database.py            # Database session management and engine
├── images                 # Static folder for image collection 
├── main.py                # main app
├── models.py              # Data table model
├── requirtements.txt      # Library that use in this project
├── routers                # API Service
│   ├── auth.py
│   |__ recipes.py
│   
├── static
│   └── wongnok            # Static file for rendoring
│       ├── css
│       │   ├── base.css
│       │   └── bootstrap.css
│       └── js
│           ├── bootstrap.js
│           ├── jquery-slim.js
│           └── popper.js
├── templates              # Template for UI
│   ├── add-recipe.html
│   ├── add-todo.html
│   ├── edit-todo.html
│   ├── home.html
│   ├── layout.html
│   ├── login.html
│   ├── navbar.html
│   └── register.html
└── wongnok_recipes.db    # Data Base that use for this app - sqlite

API Document 
locallhost
http://locallhost:8000/docs

**ยังทำ Fornt-End ไม่เสร็จ**