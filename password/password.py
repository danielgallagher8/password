"""
Password Keeper application to store passwords locally
"""

#Import libraries
from PyQt5 import QtWidgets, QtGui
import sys
import os
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

#Define classes
class App(QtWidgets.QMainWindow):
  
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.initial_layout()
  
    def initial_layout(self):
        
        #Set initial formatting
        self.setWindowTitle('Password Keeper')
        self.setWindowIcon(QtGui.QIcon('./static/lock.png'))
        self.setFont(QtGui.QFont('Calibri', 11))
        self.bold_font = QtGui.QFont('Calibri', 11)
        self.bold_font.setBold(True)
      
        #Create the base layer 
        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)
        self.base_layout = QtWidgets.QVBoxLayout(self)
        self.widget.setLayout(self.base_layout)
        
class Login(App):
    
    def __init__(self):
        super().__init__()
        self.main = Main()
        self.login_layout()
        self.actions()
        self.db = Database()
        self.base_layout.addStretch()
    
    def login_layout(self):
        self.setFixedSize(800, 400)
        label = QtWidgets.QLabel('Login')
        label.setFont(self.bold_font)
        self.base_layout.addWidget(label)
        self.username = QtWidgets.QLineEdit(self)
        self.password = QtWidgets.QLineEdit(self)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.base_layout.addWidget(self.username)
        self.base_layout.addWidget(self.password)
        self.submit_button = QtWidgets.QPushButton('Submit', self)
        self.base_layout.addWidget(self.submit_button)
        
    def actions(self):
        self.submit_button.clicked.connect(self.login_click)
    
    def login_click(self):
        user = self.username.text()
        pwd = self.password.text()
        self.username.clear()
        self.password.clear()
        db_check = self.db.check_user(user, pwd)
        if db_check is None: 
            self.current_user = user
            self.main.show()
            self.hide()
        else:
            box = QtWidgets.QMessageBox()
            box.setWindowTitle("Error")
            box.setText(db_check)
            box.exec()

class Main(App):
    
    def __init__(self):
        super().__init__()
        self.create_actions()
        self.main_layout()
        self.actions()
        self.db = Database()
        self.display_home()
    
    def main_layout(self):
        #Create the scrollable area
        self.scroll = QtWidgets.QScrollArea()
        self.base_layout.addWidget(self.scroll)
        
        #Create the top layer
        self.top_widget = QtWidgets.QWidget()
        self.top_layout = QtWidgets.QVBoxLayout()
        
        #Add formatting
        self.resize(1800, 1500)
        self.top_layout.addStretch()
        self.top_layout.setSpacing(40)
        
        #Create menu bar
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(self.newAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.homeAction)
        fileMenu.addAction(self.exitAction)
        settingsMenu = menuBar.addMenu("&Settings")
        settingsMenu.addAction(self.pwdAction)
    
    def create_actions(self):
        self.newAction = QtWidgets.QAction("&New", self)
        self.homeAction = QtWidgets.QAction("&Home", self)
        self.exitAction = QtWidgets.QAction("&Exit", self)
        self.pwdAction = QtWidgets.QAction("&Change Password", self)
    
    def actions(self):
        self.exitAction.triggered.connect(self.close)
        self.newAction.triggered.connect(self.display_new)
        self.homeAction.triggered.connect(self.display_home)
        self.pwdAction.triggered.connect(self.display_change_pwd)
    
    def display_new(self):
        self.reset_layout()
        label = QtWidgets.QLabel('New')
        label.setFont(self.bold_font)
        self.top_layout.addWidget(label)
        self.pwd_name = QtWidgets.QLineEdit()
        self.pwd_username = QtWidgets.QLineEdit()
        self.pwd_password = QtWidgets.QLineEdit()
        self.pwd_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.top_layout.addWidget(QtWidgets.QLabel('Name:'))
        self.top_layout.addWidget(self.pwd_name)
        self.top_layout.addWidget(QtWidgets.QLabel('Username:'))
        self.top_layout.addWidget(self.pwd_username)
        self.top_layout.addWidget(QtWidgets.QLabel('Password:'))
        self.top_layout.addWidget(self.pwd_password)
        self.add_pwd_button = QtWidgets.QPushButton('Submit')
        self.top_layout.addWidget(self.add_pwd_button)
        self.add_pwd_button.clicked.connect(self.add_pwd)
        self.reassign_layout()
    
    def display_home(self):
        self.reset_layout()
        label = QtWidgets.QLabel('Home')
        label.setFont(self.bold_font)
        self.top_layout.addWidget(label)
        for pwd in self.get_pwds():
            pass_button = QtWidgets.QPushButton(pwd['name'])
            pass_button.setObjectName(pwd['name'])
            pass_button.clicked.connect(self.display_pwd)
            self.top_layout.addWidget(pass_button)
        self.reassign_layout()
        
    def display_change_pwd(self):
        self.reset_layout()
        label = QtWidgets.QLabel('Change Password')
        label.setFont(self.bold_font)
        self.top_layout.addWidget(label)
        self.old_password = QtWidgets.QLineEdit()
        self.new_password = QtWidgets.QLineEdit()
        self.confirm_password = QtWidgets.QLineEdit()
        self.old_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.new_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.top_layout.addWidget(QtWidgets.QLabel('Old Password:'))
        self.top_layout.addWidget(self.old_password)
        self.top_layout.addWidget(QtWidgets.QLabel('New Password:'))
        self.top_layout.addWidget(self.new_password)
        self.top_layout.addWidget(QtWidgets.QLabel('Confirm Password:'))
        self.top_layout.addWidget(self.confirm_password)
        self.change_pwd_button = QtWidgets.QPushButton('Submit')
        self.top_layout.addWidget(self.change_pwd_button)
        self.change_pwd_button.clicked.connect(self.new_pwd)
        self.reassign_layout()
    
    def display_pwd(self):
        self.reset_layout()
        sending_button = self.sender().objectName()
        pwd = self.get_pass(sending_button)
        self.name_label = QtWidgets.QLabel(pwd['name'])
        self.top_layout.addWidget(self.name_label)
        label = QtWidgets.QLabel('Username:')
        label.setFont(self.bold_font)
        self.top_layout.addWidget(label)
        self.username_label = QtWidgets.QLabel(pwd['username'])
        self.top_layout.addWidget(self.username_label)
        label = QtWidgets.QLabel('Password:')
        label.setFont(self.bold_font)
        self.top_layout.addWidget(label)
        self.password_label = QtWidgets.QLabel(pwd['password'])
        #self.password_label.setHidden(True)
        self.top_layout.addWidget(self.password_label)
        self.edit_button = QtWidgets.QPushButton('Edit', self)
        self.edit_button.clicked.connect(lambda: self.display_edit_pass(pwd))
        self.top_layout.addWidget(self.edit_button)
        self.delete_button = QtWidgets.QPushButton('Delete', self)
        self.delete_button.clicked.connect(lambda: self.delete_pass(pwd))
        self.top_layout.addWidget(self.delete_button)
        self.reassign_layout()
    
    def reset_layout(self):
        self.top_widget = QtWidgets.QWidget()
        self.top_layout = QtWidgets.QVBoxLayout()

    def reassign_layout(self):
        self.space_stretch()
        self.top_widget.setLayout(self.top_layout)
        self.scroll.setWidget(self.top_widget)
    
    def space_stretch(self):
        self.top_layout.addStretch()
        self.top_layout.setSpacing(40)
    
    def new_pwd(self):
        old_pwd = self.old_password.text()
        new_pwd = self.new_password.text()
        conf_pwd = self.confirm_password.text()
        self.old_password.clear()
        self.new_password.clear()
        self.confirm_password.clear()
        #self.current_user = LoginWin().current_user
        update_pwd = self.db.update_pwd('admin', old_pwd, new_pwd, conf_pwd)
        if update_pwd is None:
            box = QtWidgets.QMessageBox()
            box.setWindowTitle("Change Password")
            box.setText("Password has been updated")
            box.exec()
        else:
            box = QtWidgets.QMessageBox()
            box.setWindowTitle("Error")
            box.setText(update_pwd)
            box.exec()
    
    def add_pwd(self):
        name = self.pwd_name.text()
        username = self.pwd_username.text()
        password = self.pwd_password.text()
        self.pwd_name.clear()
        self.pwd_username.clear()
        self.pwd_password.clear()
        add_pwd = self.db.add_pwd(name, username, password)
        if add_pwd is None:
            box = QtWidgets.QMessageBox()
            box.setWindowTitle("Password Added")
            box.setText("Your new password has been added")
            box.exec()
        else:
            box = QtWidgets.QMessageBox()
            box.setWindowTitle("Error")
            box.setText(add_pwd)
            box.exec()
    
    def get_pwds(self):
        pwds = self.db.get_db().execute(
                "SELECT * FROM passwords ORDER BY name ASC"
                ).fetchall()
        return pwds
    
    def get_pass(self, name):
        pwd = self.db.get_db().execute(
                "SELECT * FROM passwords WHERE name = ?", (name,)
                ).fetchone()
        return pwd
    
    def display_edit_pass(self, pwd):
        self.reset_layout()
        label = QtWidgets.QLabel("Edit: {}".format(pwd['name']))
        label.setFont(self.bold_font)
        self.top_layout.addWidget(label)
        self.save_name = pwd['name']
        self.save_username = QtWidgets.QLineEdit(pwd['username'])
        self.top_layout.addWidget(self.save_username)
        self.save_password = QtWidgets.QLineEdit(pwd['password'])
        self.top_layout.addWidget(self.save_password)
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.clicked.connect(self.edit_pass)
        self.top_layout.addWidget(self.save_button)
        self.reassign_layout()
    
    def edit_pass(self):
        username = self.save_username.text()
        password = self.save_password.text()
        self.db.edit_pwd(self.save_name, username, password)
        box = QtWidgets.QMessageBox()
        box.setWindowTitle("Password Keeper")
        box.setText("Password Updated")
        box.exec()
        self.display_home()
    
    def delete_pass(self, pwd):
        self.db.delete_pwd(pwd['name'])
        box = QtWidgets.QMessageBox()
        box.setWindowTitle("Password Keeper")
        box.setText("Password Deleted")
        box.exec()
        self.display_home()
    
class Database:
    
    def __init__(self):
        self.path = os.path.dirname(sys.argv[0])
        self.name = os.path.join(self.path, 'pass.sqlite')
        
    def get_db(self):
        db = sqlite3.connect(
                self.name,
                detect_types=sqlite3.PARSE_DECLTYPES
                )
        db.row_factory = sqlite3.Row
        return db
    
    def close_db(self):
        db = sqlite3.connect(
                self.name
                )
        db.close()
    
    def run_script(self):
        db = self.get_db()
        db.execute(
                'CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL,password TEXT NOT NULL)'
                )
        db.commit()
        db.execute(
                'CREATE TABLE  passwords (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL)'
                )
        db.commit()
        db.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)', ('admin', generate_password_hash('admin'))
                )
        db.commit()
    
    def check_user(self, user, password):
        db = self.get_db()
        get_user = db.execute(
                "SELECT * FROM users WHERE username = ?", (user,)
                ).fetchone()
        error = None
        if get_user is None:
            error = 'Unknown user'
        elif not check_password_hash(get_user['password'], password):
            error = 'Incorrect password'
        
        return error
    
    def update_pwd(self, user, old_pwd, new_pwd, conf_pwd):
        db = self.get_db()
        get_user = db.execute(
                "SELECT * FROM users WHERE username = ?", (user,)
                ).fetchone()
        error = None
        if old_pwd == new_pwd:
            error = "New password is the same as old password"
        elif not check_password_hash(get_user['password'], old_pwd):
            error = "Incorrect password"
        elif new_pwd != conf_pwd:
            error = "New password does not match when confirmed"
        
        if error is None:
            db.execute(
                    "UPDATE users SET password = ? WHERE username = ?", (generate_password_hash(new_pwd), user)
                    )
            db.commit()
        
        return error
    
    def add_pwd(self, name, username, password):
        db = self.get_db()
        get_name = db.execute(
                "SELECT * FROM passwords WHERE name = ?",(name,)
                ).fetchone()
        error = None
        if get_name is not None:
            error = "Name already exists"
        
        if error is None:
            db.execute(
                    "INSERT INTO passwords (name, username, password) VALUES (?, ?, ?)", (name, username, password,)
                    )
            db.commit()
        
        return error
    
    def edit_pwd(self, name, username, password):
        db = self.get_db()
        db.execute(
                "UPDATE passwords SET username = ?, password = ? WHERE name = ?", (username, password, name,)
                )
        db.commit()
    
    def delete_pwd(self, name):
        db = self.get_db()
        db.execute(
                "DELETE FROM passwords WHERE name = ?", (name,)
                )
        db.commit()

class RunApp:
    
    def __init__(self, *args, **kwargs):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setStyle('Breeze')
        self.db = Database()
    
    def run(self):
        if not os.path.isfile(self.db.name):
            self.db.run_script()
        win = Login()
        win.show()
        sys.exit(self.app.exec_())

"""
if __name__ == '__main__':
    r = RunApp()
    r.run()
"""
