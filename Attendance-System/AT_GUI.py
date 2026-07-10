
import cv2
import face_recognition
import mysql.connector
import pickle       # binary code ko stor karne k liye

import sys
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
import keyboard
import time
from datetime import datetime

from Registaration_form import StudentForm 

cam = None


# MySQL Connection Setup
db = mysql.connector.connect(host="localhost", user="root", passwd="",  database="attendance_system")
cursor = db.cursor()   
        # .........................................  


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1004, 655)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.titel_label = QtWidgets.QLabel(self.centralwidget)
        self.titel_label.setGeometry(QtCore.QRect(0, 30, 421, 71))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.titel_label.setFont(font)
        self.titel_label.setStyleSheet("background-color:#8d0aff; color:white; border-top-right-radius: 30px; border-bottom-right-radius: 30px; border-top-left-radius: 0px; border-bottom-left-radius: 0px;")
        self.titel_label.setObjectName("titel_label")
        
        
        self.cam_status = QtWidgets.QLabel(self.centralwidget)
        self.cam_status.setGeometry(QtCore.QRect(40, 100, 590, 50))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(40)
        self.cam_status.setFont(font)
        self.cam_status.setText("")
        self.cam_status.setObjectName("cam_status")
        
        
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(670, 30, 311, 501))
        self.frame_2.setStyleSheet("border: 10px solid #8d0aff; border-radius: 30px;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        
        self.photo = QtWidgets.QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(750, 85, 141, 150))
        self.photo.setStyleSheet("border:3px solid black ; border-radius:10px")
        
        # file_path = 'photo/avi.jpg'
        self.photo.setPixmap(QtGui.QPixmap('resource\cap2.png'))
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")
        
        self.name_label = QtWidgets.QLabel(self.centralwidget)
        self.name_label.setGeometry(QtCore.QRect(710, 260, 141, 50))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(50)
        self.name_label.setFont(font)
        self.name_label.setText("Name: ")
        self.name_label.setObjectName("name_label")
        
        self.name = QtWidgets.QLabel(self.centralwidget)
        self.name.setGeometry(QtCore.QRect(780, 260, 190, 50))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(40)
        self.name.setFont(font)
        self.name.setText("")
        self.name.setObjectName("name")
        
        
        self.branch_label = QtWidgets.QLabel(self.centralwidget)
        self.branch_label.setGeometry(QtCore.QRect(710, 290, 141, 50))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(40)
        self.branch_label.setFont(font)
        self.branch_label.setText("Branch: ")
        self.branch_label.setObjectName("branch_label")
        
        
        self.branch = QtWidgets.QLabel(self.centralwidget)
        self.branch.setGeometry(QtCore.QRect(790, 290, 177, 50))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(40)
        self.branch.setFont(font)
        self.branch.setText("")
        self.branch.setObjectName("branch")
        
        
        self.roll_N_label= QtWidgets.QLabel(self.centralwidget)
        self.roll_N_label.setGeometry(QtCore.QRect(710, 320, 141, 50))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(50)
        self.roll_N_label.setFont(font)
        self.roll_N_label.setText("Roll No. :")
        self.roll_N_label.setObjectName("roll_N_label")
        
        self.roll_N= QtWidgets.QLabel(self.centralwidget)
        self.roll_N.setGeometry(QtCore.QRect(805, 320, 165, 50))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(40)
        self.roll_N.setFont(font)
        self.roll_N.setText("")
        self.roll_N.setObjectName("roll_N")
        
        self.status= QtWidgets.QLabel(self.centralwidget)
        self.status.setGeometry(QtCore.QRect(700, 400, 250, 60))
        self.status.setStyleSheet("background-color: limegreen; border-radius:20px; color:white;")
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(40)
        self.status.setFont(font)
        self.status.setText("   Status")
        self.status.setAlignment(Qt.AlignCenter) 
        self.status.setObjectName("status")
        # self.status.hide()
        
        
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(0, 30, 71, 71))
        self.logo.setStyleSheet("COLOR:WHITE;")
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("resource\logo.png"))
        self.logo.setObjectName("logo")
        
        
        self.register_B = QtWidgets.QPushButton(self.centralwidget)
        self.register_B.setGeometry(QtCore.QRect(720, 560, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        self.register_B.setFont(font)
        self.register_B.setStyleSheet("background-color:#8903ff; border-radius: 20px; color: white;")
        self.register_B.setObjectName("register_B")
        self.register_B.clicked.connect(self.register_student)
        
        
        self.attendance_B = QtWidgets.QPushButton(self.centralwidget)
        self.attendance_B.setGeometry(QtCore.QRect(220, 560, 201, 61))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        self.attendance_B.setFont(font)
        self.attendance_B.setStyleSheet("background-color:#8903ff; border-radius: 20px; color: white;")
        self.attendance_B.setObjectName("attendance_B")
        # self.attendance_B.clicked.connect(self.mark_attendance)
        self.attendance_B.clicked.connect(self.mark_attendance2)
        
        
# ............................................
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(30, 140, 591, 391))
        self.image_label.setStyleSheet("border: 10px solid red; border-radius: 20px;")
        self.logo.setText("")
        self.image_label.setPixmap(QtGui.QPixmap("resource\cap2.png"))
        self.image_label.setScaledContents(True)
        self.image_label.setObjectName("image_label")
       
       
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Attendance System"))
        self.titel_label.setText(_translate("MainWindow", "       ATTENDANCE SYSTEM"))
        self.register_B.setText(_translate("MainWindow", "Register Student"))
        self.attendance_B.setText(_translate("MainWindow", "Start Attendance"))
        self.image_label.setText(_translate("MainWindow", ""))
        
        
    def register_student(self):
        self.second_window = StudentForm()
        self.second_window.show()
        

    # final code
    def mark_attendance2(self):
        global cam
        cam = cv2.VideoCapture(0)  # Camera start karein
        cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Lag avoid karne ke liye buffer set karein
        # print("Attendance System Started... Press 'q' to exit.")
        
        
        while True:
            ret, frame = cam.read()  # Frame capture karein
            # self.cam_status.setText("Look at the camera..")
            
            # this code for showing video in label
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
             # Get image height, width, channel
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w

            # Convert to QImage
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Convert QImage to QPixmap and set to QLabel
            self.image_label.setPixmap(QPixmap.fromImage(qt_image))
            # ...........................................
            if not ret:
                print("Camera issue! Restarting...")
                continue
            if keyboard.is_pressed('s'):
                face_locations = face_recognition.face_locations(frame)  # Face detect karein
                face_encodings = face_recognition.face_encodings(frame, face_locations)

                student_found = False  # Default maan lein ki student register nahi hai

                cursor.execute("SELECT name, roll_number, branch, face_encoding FROM students")
                students = cursor.fetchall()

                for student in students:
                    name, roll_number, branch, stored_encoding = student
                    stored_encoding = pickle.loads(stored_encoding)

                    for face_encoding in face_encodings:
                        match = face_recognition.compare_faces([stored_encoding], face_encoding)[0]

                        if match:
                            student_found = True
                            today_date = datetime.now().date()
                            current_time = datetime.now().strftime("%H:%M:%S")

                            cursor.execute("SELECT * FROM attendance WHERE roll_number=%s AND date=%s", (roll_number, today_date))
                            result = cursor.fetchone()

                            if result:
                                Image_file ='photo/'+roll_number+'.jpg'
                                self.photo.setPixmap(QtGui.QPixmap(Image_file))
                                self.name.setText(name)
                                self.branch.setText(branch)
                                self.roll_N.setText(roll_number)
                                self.status.setStyleSheet(" border-radius:20px; background-color:yellow; color: black")
                                self.status.setText("Attendance already \n marked for today!")
                                self.status.show()
                                
                            else:
                                cursor.execute("INSERT INTO attendance (roll_number,name, date, time) VALUES (%s, %s,%s, %s)", 
                                            (roll_number,name, today_date, current_time))
                                db.commit()
                                Image_file ='photo/'+roll_number+'.jpg'
                                self.photo.setPixmap(QtGui.QPixmap(Image_file))
                                self.name.setText(name)
                                self.branch.setText(branch)
                                self.roll_N.setText(roll_number)
                                self.status.setStyleSheet(" border-radius:20px; background-color: limegreen; color: white")
                                self.status.setText("Attendance marked.")
                                
                        elif(student_found == False):
                            # print("Not found")
                            # print("Student not registered! Please register first.")
                            self.photo.setPixmap(QtGui.QPixmap('resource\cap2.png'))
                            self.image_label.setPixmap(QtGui.QPixmap('resource\cap2.png'))
                            self.name.setText('')
                            self.branch.setText('')
                            self.roll_N.setText('')
                            self.status.setStyleSheet(" border-radius:20px; background-color:red; color: black")
                            self.status.setText("Student not registered! \n Please register first.")
                            
                        
                            
            # if not student_found and face_locations:
            #     print("Student not registered! Please register first.")
        
            # cv2.imshow("Face Attendance System", frame)  # Camera ka live feed show karein

            if cv2.waitKey(1) & keyboard.is_pressed('q'):  # 'q' dabaane par system exit karein
                self.photo.setPixmap(QtGui.QPixmap('resource\cap2.png'))
                self.image_label.setPixmap(QtGui.QPixmap('resource\cap2.png'))
                self.name.setText('')
                self.branch.setText('')
                self.roll_N.setText('')
                self.status.setStyleSheet("background-color: limegreen; border-radius:20px; color:white;")
                self.status.setText("Status")
                break
            
                
        cam.release()
        cv2.destroyAllWindows()
        print("Attendance System Closed.")
        
         
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
