import sys
import typing
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import cv2
import sqlite3
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QLineEdit, QLabel, QPushButton, QListWidget, QFileDialog, QListWidgetItem, QCheckBox, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QIcon,QFont


class ThirdWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Third Window')
        self.setGeometry(100, 100, 600, 500)
        layout = QVBoxLayout()
        self.setLayout(layout)
        label = QLabel(self)
        label.setText("Persons Data Page")
        label.setGeometry(100, 20, 200, 30)


        self.Person_name_box = QLineEdit(self)
        self.Person_name_box.setGeometry(105, 200, 100, 30)
        self.Person_name_label = QLabel('Person Name:', self)
        self.Person_name_label.setGeometry(20, 200, 100, 30)
        self.Person_Info_box = QLineEdit(self)
        self.Person_Info_box.setGeometry(145, 250, 100, 30)
        self.Person_Info_label = QLabel('Preson Information:', self)
        self.Person_Info_label.setGeometry(20, 250, 100, 30)


        #self.picture_label = QLabel('Picture:', self)
        #self.picture_label.setGeometry(20, 300, 200, 30)
        self.picture_box = QLineEdit(self)
        self.picture_box.setGeometry(180, 300, 140, 30)
        self.picture_button = QPushButton('Select Person Photo', self)
        self.picture_button.setGeometry(10, 300, 150, 30)
        self.picture_button.setStyleSheet("background-color: white;")
        self.picture_button.clicked.connect(self.select_Photo)

        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(20, 20, 550, 120)
        self.list_widget.itemSelectionChanged.connect(self.enable_delete_button)
        self.Add_button = QPushButton('Add', self)
        self.Add_button.setGeometry(20, 150, 100, 30)
        self.Add_button.setStyleSheet("background-color: white;")
        self.Add_button.clicked.connect(self.Add_person)
        self.update_button = QPushButton('Update', self)
        self.update_button.setGeometry(230, 150, 100, 30)
        self.update_button.setStyleSheet("background-color: white;")
        self.update_button.clicked.connect(self.update_Person)
        self.delete_button = QPushButton('Delete', self)
        self.delete_button.setGeometry(450, 150, 100, 30)
        self.delete_button.setStyleSheet("background-color: white;")
        self.delete_button.clicked.connect(self.delete_Person)
        self.load_Persons()
        self.show()
    def select_Photo(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select Picture', '', 'Image Files (*.png *.jpg *.bmp)')
        if file_path:
            self.picture_box.setText(file_path)

    def Add_person(self):
        Person_name = self.Person_name_box.text().strip()
        Person_Info = self.Person_Info_box.text().strip()
        picture_path = self.picture_box.text().strip()
        if not picture_path:
            picture_data = None
        else:
            with open(picture_path, 'rb') as f:
                picture_data = f.read()
        if not Person_name or not Person_Info:
            QMessageBox.warning(
                self, 'Error', 'Make Sure that you fill all boxes.')
            return
        connection = sqlite3.connect('PersonsData.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO PersonsData (Person_name, Person_Info, picture) VALUES (?, ?, ?)',
                       (Person_name, Person_Info, picture_data))
        connection.commit()
        connection.close()
        self.Person_name_box.clear()
        self.Person_Info_box.clear()
        self.picture_box.clear()
        self.load_Persons()
    def update_Person(self):
        selected_item = self.list_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(
                self, 'Error', 'Please select a Person from list of records to edit and enter name and information.')
            return
        Person_ID = int(selected_item.text().split(':')[0])
        Person_name = self.Person_name_box.text().strip()
        Person_Info = self.Person_Info_box.text().strip()
        if not Person_name or not Person_Info:
            QMessageBox.warning(
                self, 'Error', 'Please enter a Person name, Person_Info')
            return
        connection = sqlite3.connect('PersonsData.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE PersonsData SET Person_name=?, Person_Info=? WHERE ID=?',
                       (Person_name, Person_Info, Person_ID))
        connection.commit()
        connection.close()
        self.Person_name_box.clear()
        self.Person_Info_box.clear()
        self.load_Persons()
    def enable_delete_button(self):
        if len(self.list_widget.selectedItems()) > 0:
            self.delete_button.setEnabled(True)
        else:
            self.delete_button.setEnabled(False)
    def delete_Person(self):
        selected_item = self.list_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(
                self, 'Error', 'Select a Person to delete.')
            return
        selected_text = selected_item.text()
        Person_ID= selected_text.split(':')[0]
        confirm = QMessageBox.question(self, 'Deletion assurance', f"this person will be deleted from data permanently --> {Person_ID}?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            connection = sqlite3.connect('PersonsData.db')
            cursor = connection.cursor()
            cursor.execute('DELETE FROM PersonsData WHERE id=?', (Person_ID,))
            connection.commit()
            connection.close()
            self.load_Persons()
    def load_Persons(self):
        self.list_widget.clear()
        connection = sqlite3.connect('PersonsData.db')
        cursor = connection.cursor()
        cursor.execute('SELECT ID, Person_name, Person_Info, picture FROM PersonsData')
        Persons = cursor.fetchall()
        for Person in Persons:
            Person_ID, Person_name, Person_Info,picture_data,= Person
            item_text = f'{Person_ID}: {Person_name} ---- {Person_Info}'
            item = QListWidgetItem(item_text, self.list_widget)
            if picture_data:
                pixmap = QPixmap()
                pixmap.loadFromData(picture_data)
                item.setIcon(QIcon(pixmap))
        connection.close()

class SecondWindow(QDialog):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle('Second Window')
        self.setGeometry(100, 100, 600, 200)
        layout = QVBoxLayout()
        self.setLayout(layout)
        label = QLabel(self)
        label.setText("Persons Data Page")
        label.setGeometry(100, 20, 200, 30)


        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        label.setFont(font)
        label.setStyleSheet("color: black;")
        label.setAlignment(Qt.AlignCenter)
        label.adjustSize()
        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(20, 20, 550, 120)
        self.load_Persons()
    def load_Persons(self):
        self.list_widget.clear()
        connection = sqlite3.connect('PersonsData.db')
        cursor = connection.cursor()
        cursor.execute('SELECT ID, Person_name, Person_Info, picture FROM PersonsData')
        Persons = cursor.fetchall()
        for Person in Persons:
            Person_ID, Person_name, Person_Info,picture_data,= Person
            item_text = f'{Person_ID}: {Person_name} ---- {Person_Info}'
            item = QListWidgetItem(item_text, self.list_widget)
            if picture_data:
                pixmap = QPixmap()
                pixmap.loadFromData(picture_data)
                item.setIcon(QIcon(pixmap))
        connection.close()
        self.show()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Home Page')
        self.setGeometry(100, 100, 400, 300)
        label = QLabel(self)
        label.setText("Welcome to the Home Page")
        label.setGeometry(60, 20, 200, 30)


        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        label.setFont(font)
        label.setStyleSheet("color: black;")
        label.setAlignment(Qt.AlignCenter)
        label.adjustSize()

        button1 = QPushButton(self)
        button1.setText('View Data')
        button1.setGeometry(110, 80, 150, 40)
        button1.setStyleSheet("background-color: white;")
        button1.clicked.connect(self.openSecondWindow)


        # Create the second QPushButton
        button2 = QPushButton(self)
        button2.setText('Edit Data')
        button2.setGeometry(110, 130, 150, 40)
        button2.setStyleSheet("background-color: white;")
        button2.clicked.connect(self.openThirdWindow)
        
        



    def openSecondWindow(self):
        secondWindow = SecondWindow()
        secondWindow.exec_()

    def openThirdWindow(self):
        ThirdWindowww = ThirdWindow()
        ThirdWindowww.exec_()
   
 
if __name__ == '__main__':
    connection = sqlite3.connect('PersonsData.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS PersonsData (ID INTEGER PRIMARY KEY, Person_name TEXT NOT NULL, Person_Info TEXT NOT NULL, picture BLOB)')
    connection.commit()
    connection.close()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())