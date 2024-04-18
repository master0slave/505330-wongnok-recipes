# Introdcution to wongnok-recipes
เว็บแอปพลิเคชันรวบรวมสูตรอาหาร หรือ "Wongnok recipes" เปิดให้ผู้เยี่ยมชมทั่วไปสามารถ
เข้ามาสืบค้นสูตรอาหารผ่านชื่อเมนูหรือวัตถุดิขได้  หากยังไม่รู้ชื่อเมนูหรือวัตถุดิบสามารถสืบคั้นได้จาก
เงื่อนไข "ระยะเวลาที่ใช้ในการปรุงอาหาร" และ "ความยากง่ายของเมนู" ได้ โดยระบบจะแสดงผลลัพธ์ที่
ตรงกับเงื่อนไขมาให้ นอกจากนี้ยังมีระบบสมาชิกที่สามารถสมัครเพื่อสร้าง, แก้ไข หรือลบสูตรของตัว
เอง รวมถึงให้คะแนนสูตรอาหารของเพื่อนสมาชิกคนอื่นได้

ขั้นตอนการรัน web application และ การใช้งานเบื้องต้น

### Init Prroject
#### Create new environment
```
> cd 505330-wongnok-recipes 
> conda create --name wk-be python=3.11
> conda activate wk-be
> pip install -r reqiurement.txt
```
#### Create database - Prerequire:sqlite is installed
```
> python database.py
> python models.py 
```
### Run Project
> uvicon main:app --reload

### Workspace Directory Detail
```
wongnok_recipes/
.
|── README.md
|
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
│   ├── edit-recipe.html
│   ├── home.html
│   ├── layout.html
│   ├── login.html
│   ├── navbar.html
│   └── register.html
└── wongnok_recipes.db    # Data Base that use for this app - sqlite
```
### Example

![alt text](<images/Screenshot 2567-04-19 at 00.17.52.png>)
![alt text](<images/Screenshot 2567-04-19 at 00.21.22.png>)

![alt text](<images/Screenshot 2567-04-19 at 00.06.40.png>)

### API Document
http://locallhost:8000/docs

![alt text](<images/Screenshot 2567-04-18 at 20.05.01.png>)