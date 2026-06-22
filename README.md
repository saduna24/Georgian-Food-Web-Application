# 🇬🇪 Georgian Food Web Application

A clean, modern, and fully responsive e-commerce web application built using Python (Flask) and SQLite3, featuring premium styles and local Georgian typography.

---

## ✨ Features

- **Dynamic Menu Showcase**: Displays traditional Georgian dishes inside beautifully styled layout cards.
- **AJAX Shopping Cart**: Adds items to the cart instantly without page reloads for a seamless user experience.
- **Admin Authentication**: Secure login and logout system for managers to control the active menu.
- **Product Management**: Intuitive interface for administrators to create and delete menu items dynamically.
- **Order Dispatch System**: Built-in checkout module configured with table allocations to organize customer orders.
- **Sophisticated Aesthetics**: Custom dark/minimalist design themes, integrated local `DM Constitution` font tracking, and localized Georgian Lari (`₾`) currency formats.

---

## 🛠️ Tech Stack

- **Back-End**: Python, Flask, SQLite3
- **Front-End**: HTML5, CSS3, Bootstrap 5, JavaScript (Fetch API)
- **Database**: relational SQLite management (`food.db`)

---

## 🚀 Getting Started

Follow these steps to run the project locally on your machine.

### 1. Clone the repository
```bash
git clone https://github.com
cd your-repo-name
```

### 2. Install Flask
Make sure you have Python installed, then run:
```bash
pip install Flask
```

### 3. File Directory Structure
Ensure your assets and typography paths match the local template layouts:
```text
├── app.py
├── food.db
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── create_product.html
│   └── checkout.html
└── static/
    ├── style.css
    └── DM-Constitution.ttf
```

### 4. Run the application
```bash
python app.py
```
Open your browser and visit: `http://127.0.0`

---

## 🔑 Default Credentials
To access the Admin dashboard to add or delete dishes:
- **Username**: `admin`
- **Password**: `password123`
