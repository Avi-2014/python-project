# python-project
# 🎓 Face Recognition Attendance System

A Python-based Face Recognition Attendance System that automatically recognizes students using a webcam and marks attendance in a MySQL database.

---

## 📌 Features

- Student Registration
- Face Detection & Recognition
- Automatic Attendance Marking
- Attendance only once per day
- Live Camera Preview
- MySQL Database Integration
- PyQt5 Graphical User Interface

---

## 🛠️ Technologies Used

- Python 3.x
- OpenCV
- face_recognition
- PyQt5
- MySQL (XAMPP)
- mysql-connector-python
- NumPy

---

## 📂 Project Structure

```
Attendance-System/
│
├── AT_GUI.py
├── Registaration_form.py
├── attendance_system.sql
├── requirements.txt
├── README.md
│
├── photo/
│
├── resource/
│   ├── logo.png
│   └── cap2.png
│
└── haarcascade_frontalface_default.xml
```

---

## 📋 Requirements

Install Python packages:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install opencv-python
pip install face-recognition
pip install PyQt5
pip install mysql-connector-python
pip install numpy
pip install keyboard
```

---

## 🗄️ Database Setup

1. Install XAMPP.
2. Start Apache and MySQL.
3. Open phpMyAdmin.
4. Create a database named:

```
attendance_system
```

5. Import the file:

```
attendance_system.sql
```

---

## ▶️ Run the Project

Register Student

```bash
python Registaration_form.py
```

Start Attendance System

```bash
python AT_GUI.py
```

---

## 📷 How it Works

1. Register a student with Name, Roll Number, Branch and Photo.
2. Face Encoding is generated and stored in MySQL.
3. Camera captures the student's face.
4. Face is matched with stored encoding.
5. Attendance is marked automatically.
6. Duplicate attendance on the same day is prevented.


## 📦 Database Tables

### students

- id
- name
- roll_number
- branch
- face_encoding
- photo

### attendance

- id
- roll_number
- name
- date
- time

---

## 👨‍💻 Author

**Laloo Prasad(Avi)**

Bachelor of Technology (B.Tech)

Face Recognition Attendance System Project

---

## 📄 License

This project is developed for educational purposes.