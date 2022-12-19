import kivymd
import mysql.connector
import re

from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
Window.size = (350, 580)

class Application(MDApp):

	regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


	def build(self):
		global screen_manager
		screen_manager = ScreenManager()  
		screen_manager.add_widget(Builder.load_file("pre-splash.kv"))
		screen_manager.add_widget(Builder.load_file("login.kv"))
		screen_manager.add_widget(Builder.load_file("signup.kv"))
		screen_manager.add_widget(Builder.load_file("name.kv"))
		screen_manager.add_widget(Builder.load_file("gender.kv"))
		screen_manager.add_widget(Builder.load_file("employmentStatus.kv"))
		screen_manager.add_widget(Builder.load_file("contacts.kv"))
		screen_manager.add_widget(Builder.load_file("username.kv"))
		screen_manager.add_widget(Builder.load_file("password.kv"))
		screen_manager.add_widget(Builder.load_file("endOfSignup.kv"))
		screen_manager.add_widget(Builder.load_file("home.kv"))
		return screen_manager

	def on_start(self):
		Clock.schedule_once(self.login, 5)

	def login(self, *args):
		screen_manager.current = "login"


	def showUsernameAlert(self):
		self.dialog = MDDialog(font_name =  "Poppins-Medium.ttf",
			title = "Username has already been taken.",
			text = "Choose a different username.",

			buttons = [MDFlatButton(font_name = "Poppins-Regular.ttf",
				text = "OKAY",
				on_release =  self.dialog.close()
				),

			],
			)
		self.dialog.open()

	def checkMale(self, checkbox, active):
		global gender
		if active:
			gender = "Male"

	def checkFemale(self, checkbox, active):
		if active:
			gender = "Female"

	def checkEmployed(self, checkbox, active):
		global employmentStatus
		if active:
			employmentStatus = "Employed"

	def checkNotEmployed(self, checkbox, active):
		global employmentStatus
		if active:
			employmentStatus = "Unemployed"

	def setName(self, firstName, lastName):
		global firstName1
		global lastName1
		firstName1 = firstName
		lastName1 = lastName
		print(firstName1)
		print({firstName.text})
		qwerty = '{firstName.text}'
		print(qwerty)

	
	def setUsername(self, username):
		global username1

		db = mysql.connector.connect(
		host = "35.202.185.144",
		user = "root",
		password = "injamsira98",
		database = "tollcollection"
		)
		mycursor = db.cursor()

		usernameCheck = username.text
		print(usernameCheck)

		mycursor.execute("SELECT * FROM motorists")
		result = mycursor.fetchall();
		#print(result)
		#print(result[0])
		#print(result[0][0])
		
		print(len(result))

		for i in range(len(result)):
			if usernameCheck == result[i][0]:
				print(result[i])
				print("user already exists")
				Snackbar(text="Username has already been taken.").open()
				screen_manager.current = "username"
				
			else:
				username1 = username
				screen_manager.transition.direction = "left"
				screen_manager.current = "password"


	
	def setContacts(self, mobileNumber, emailAddress):
		global mobileNumber1
		global emailAddress1
		mobileNumber1 = mobileNumber
		emailAddress1 = emailAddress

	def setPassword(self, userPassword):
		global password1
		password1 = userPassword

	

	def send_data(self, *args):
		db = mysql.connector.connect(
		host = "35.202.185.144",
		user = "root",
		password = "injamsira98",
		database = "tollcollection"
		)
		mycursor = db.cursor()

		usernameInput = username1.text
		firstNameInput = firstName1.text
		lastNameInput = lastName1.text
		emailAddressInput = emailAddress1.text
		mobileNumberInput = mobileNumber1.text
		userPasswordInput = password1.text
		genderInput = gender
		employmentStatusInput = employmentStatus

		sql = '''INSERT INTO tollcollection.motorists(username, firstName, lastName, gender, employmentStatus, emailAddress, mobileNumber, userPassword) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'''
                     
		data = (usernameInput, firstNameInput, lastNameInput, genderInput, employmentStatusInput, emailAddressInput, mobileNumberInput, userPasswordInput)
		

		mycursor.execute(sql, data)

		db.commit()

	def receive_data(self, usernameLogin, passwordLogin):
		db = mysql.connector.connect(
		host = "35.202.185.144",
		user = "root",
		password = "injamsira98",
		database = "tollcollection"
		)
		mycursor = db.cursor()

		mycursor.execute("SELECT * FROM motorists")
		result = mycursor.fetchall();

		usernameInput = usernameLogin.text
		password = passwordLogin.text

		for i in range(len(result)):
			if usernameInput == result[i][0] and password == result[i][7]:
				print("Successful login")
				print(result[i][0])
				print(result[i][7])
				screen_manager.transition.direction = "left"
				Snackbar(text="Successful login").open()
				screen_manager.current = "home"
				break
					
			if usernameInput != result[i][0]:
				print("Failed login")
				screen_manager.transition.direction = "left"
				screen_manager.current = "login"
				#Snackbar(text="Login failed").open()


		




		

if __name__ == "__main__":
	Application().run()