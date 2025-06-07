# 🧘 Omnify Booking System

This project was developed as part of the initial technical round for **Omnify**.

---

## 📌 Description

A backend service built with **Django** and **SQLite** for managing and booking fitness classes. It supports:

- User registration and class booking  
- Class time adjustments based on selected timezones  
- Validation for slot availability and duplicate bookings  
- Clean and modular Django project structure

---

## 🚀 Tech Stack

- **Python** (v3.10+)
- **Django** (v4.x recommended)
- **SQLite** (in-memory DB or file-based)

---

## 🛠️ Features
ALl api endpoints images are given in images folder
- `POST /book`  
  Accepts a class booking request with `user_id` and `class_id`.  
  Validates:
  - Whether the class exists
  - Whether the user already booked
  - If class has available slots  
  Creates a new booking and reduces the available slot count if valid.

- `GET /bookings?user_id=1`  
  Returns all class bookings made by a user, with class time in the user's timezone (supports only `Asia/Kolkata` and `America/New_York`).

- `GET /classes`  
  Returns all available classes with remaining slots and class time formatted in IST and UTC.

---
You can hit the /PrePopulateData endpoint (mapped to views.populate) to seed the database with:
2 TimeZones
2 Users
3 Classes (with 5, 2, 3 slots respectively)
5 Bookings
