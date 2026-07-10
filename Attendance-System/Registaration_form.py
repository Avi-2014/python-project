import sys
import os    # directory banane ke liye
import shutil  # system me photo folder me photos ko permanently save karne ke liye ya copy karne ke liye use
import mysql.connector
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QPixmap
import face_recognition   
import pickle
import cv2
import tempfile


class StudentForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Registration")
        self.setGeometry(100, 100, 400, 400)

        # UI Elements
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Name")

        self.roll_input = QLineEdit()
        self.roll_input.setPlaceholderText("Enter Roll Number")
        
        self.branch_input = QLineEdit()
        self.branch_input.setPlaceholderText("Enter Branch")

        self.photo_display = QLabel()
        self.photo_display.setFixedSize(150, 150)

        self.upload_btn = QPushButton("Upload Photo")
        self.upload_btn.clicked.connect(self.upload_photo)
        
        self.live_btn = QPushButton("Live Capture")
        self.live_btn.clicked.connect(self.live_cap)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.submit_data)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Roll Number:"))
        layout.addWidget(self.roll_input)
        layout.addWidget(QLabel("Branch:"))
        layout.addWidget(self.branch_input)
        layout.addWidget(QLabel("Photo:"))
        layout.addWidget(self.photo_display)
        layout.addWidget(self.upload_btn)
        layout.addWidget(self.live_btn)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)
        self.photo_path = None

        # Ensure photo directory exists
        self.photo_dir = "photo"
        os.makedirs(self.photo_dir, exist_ok=True)

    def upload_photo(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Photo", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            self.photo_path = file_name
            pixmap = QPixmap(file_name).scaled(self.photo_display.size())
            self.photo_display.setPixmap(pixmap)

    
    def live_cap(self):
        cap = cv2.VideoCapture(0)  # Webcam open karo
        if not cap.isOpened():
            print("Error: Cannot access the webcam.")
            return

        print("Press 's' to capture the photo, 'q' to quit.")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Cannot read frame from webcam.")
                break

            cv2.imshow("Webcam", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                # Jab 's' press ho, tab photo capture karo
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
                cv2.imwrite(temp_file.name, frame)
                print(f"Photo captured and saved at: {temp_file.name}")
                self.photo_path = temp_file.name
                pixmap = QPixmap(temp_file.name).scaled(self.photo_display.size())
                self.photo_display.setPixmap(pixmap)
                # temp_file.close()
                break
            elif key == ord('q'):
                # Jab 'q' press ho, tab quit karo
                print("Quitting without capturing.")
                break

        cap.release()
        cv2.destroyAllWindows()
    
    
    def submit_data(self):
        name = self.name_input.text()
        roll = self.roll_input.text()
        branch = self.branch_input.text()

        if not name or not roll or not branch or not self.photo_path:
            QMessageBox.warning(self, "Missing Info", "Please fill all fields and upload a photo.")
            return

        try:
            # Load and encode face
            image = face_recognition.load_image_file(self.photo_path)
            encoding = face_recognition.face_encodings(image)

            if not encoding:
                QMessageBox.warning(self, "Face Not Found", "No face detected in the image.")
                return

            encoding_blob = pickle.dumps(encoding[0])  # Convert face encoding to binary

            # Save photo in the photo directory with roll number as file name
            ext = os.path.splitext(self.photo_path)[1]
            saved_photo_path = os.path.join(self.photo_dir, f"{roll}{ext}")
            shutil.copy(self.photo_path, saved_photo_path)

            # MySQL Connection
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="attendance_system"
            )
            cursor = conn.cursor()

            sql = "INSERT INTO students (name, roll_number, branch, face_encoding, photo) VALUES (%s,%s, %s, %s, %s)"
            val = (name, roll, branch, encoding_blob, saved_photo_path)
            cursor.execute(sql, val)
            conn.commit()

            QMessageBox.information(self, "Success", "Student data saved successfully.")
            self.name_input.setText('')
            self.roll_input.setText('')
            self.branch_input.setText('')
            
            
            cursor.close()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Something went wrong:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = StudentForm()
    form.show()
    sys.exit(app.exec_())
