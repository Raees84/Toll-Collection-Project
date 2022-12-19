import kivymd
import kivy
import mysql.connector
import time

from datetime import datetime

import xml.dom.minidom as minidom
from urllib.error import HTTPError, URLError
from xml.dom.minidom import Document
from xml.etree.ElementTree import Element, SubElement, tostring

from urllib.request import Request, urlopen
import uuid

import http.client
import random
import urllib.error
import urllib.parse
import urllib.request

import json
import requests


BASE_URL = 'https://proxy.momoapi.mtn.com'  # 'https://sandbox.momodeveloper.mtn.com'
SUBSCRIPTION_KEY = '07aed02420e540c6ae00b0b8f7db3c49'  # 'f23c7d41a1494d1ba0020c284f417132'
API_USER = 'f4caae14-44f9-4cab-81db-8966a5603294'
API_KEY = '5df61371f4844cb9aac53e140a5139da'



from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDRaisedButton, MDFloatingActionButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.screen import MDScreen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.theming import ThemeManager
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivymd.uix.gridlayout import MDGridLayout
Window.size = (350, 580)

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

global genderChoice
class Application(MDApp):
	username = ''
	requestToPayID = ''
	requestToPayToken = ''
	depositAmount = ''
	TOKEN = ''
	ID = ''

	def build(self):
		global screen_manager
		screen_manager = ScreenManager()  
		screen_manager.add_widget(Builder.load_file("pre-splash.kv"))
		Clock.schedule_once(self.login, 5)
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
		screen_manager.add_widget(Builder.load_file("account.kv"))
		screen_manager.add_widget(Builder.load_file("deposit.kv"))
		screen_manager.add_widget(Builder.load_file("history.kv"))
		screen_manager.add_widget(Builder.load_file("vehicleSettings.kv"))
		screen_manager.add_widget(Builder.load_file("vehicles.kv"))
		screen_manager.add_widget(Builder.load_file("information.kv"))
		screen_manager.add_widget(Builder.load_file("settings.kv"))
		screen_manager.add_widget(Builder.load_file("transfers.kv"))
		screen_manager.add_widget(Builder.load_file("transactions.kv"))
		screen_manager.add_widget(Builder.load_file("changeUsername.kv"))	
		screen_manager.add_widget(Builder.load_file("changePassword.kv"))	
		screen_manager.add_widget(Builder.load_file("addVehicle.kv"))
		screen_manager.add_widget(Builder.load_file("removeVehicle.kv"))

		return screen_manager

	#def on_start(self):
		#Clock.schedule_once(self.login, 5)


	def login(self, *args):
		screen_manager.current = "login"


	def checkMale(self, checkbox, active):
		global gender
		if active:
			gender = "Male"
	
	def checkFemale(self, checkbox, active):
		global gender
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

		if firstName1.text == '' or lastName1.text == '':
			toast('Enter full details.')
			screen_manager.current = 'name'

		else:
			screen_manager.transition.direction = 'left'
			screen_manager.current = 'gender'
			print(firstName1)
			print({firstName.text})
			qwerty = '{firstName.text}'
			print(qwerty)

	
	def setUsername(self, username):
		global username1

		try:
			db = mysql.connector.connect(
			host = "104.155.170.169",
			user = "root",
			password = "G00dwill",
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
			
			print("length = ", len(result))

			if usernameCheck == '':
				toast('Choose a username.')
				screen_manager.current = 'username'

			else:
				for i in range(len(result)):
					if usernameCheck == result[i][0]:
						print(result[i])
						print("user already exists")
						screen_manager.current = "username"
						#Snackbar(text="Username has already been taken. Choose a different username").open()
						toast("Username has already been taken. Choose a different username")
						break
						
					else:
						username1 = username
						screen_manager.transition.direction = "left"
						screen_manager.current = "password"

			db.close()

		except:
			toast("Check internet connection.")
			screen_manager.current = 'username'



	
	def setContacts(self, mobileNumber, emailAddress):
		global mobileNumber1
		global emailAddress1

		if mobileNumber.text == '' or emailAddress.text == '':
			toast('Enter full contact details.')
			screen_manager.current = 'contacts'

		else:
			mobileNumber1 = mobileNumber
			emailAddress1 = emailAddress
			screen_manager.transition.direction = 'left'
			screen_manager.current = 'username'

	def setPassword(self, userPassword):
		global password1

		if userPassword.text == '':
			toast('Choose your password.')
			screen_manager.current = 'password'

		else:
			password1 = userPassword
			screen_manager.transition.direction = 'left'
			screen_manager.current = 'endOfSignup'


	def send_data(self, *args):
		try:
			db = mysql.connector.connect(
			host = "104.155.170.169",
			user = "root",
			password = "G00dwill",
			database = "tollcollection"
			)
			mycursor = db.cursor()

			global usernameInput
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

			app = MDApp.get_running_app()
			app.username = usernameInput

			mycursor.execute("SELECT * FROM balances")
			result = mycursor.fetchall()
			length = len(result)

			sql = '''INSERT INTO tollcollection.balances(balanceID, username, balance) VALUES(%s,%s,%s)'''
			data = (length + 1, usernameInput, 0)
			mycursor.execute(sql, data)

			db.commit()
			

			screen_manager.transition.direction = 'left'
			screen_manager.current = 'home'
			toast('Welcome.')

		except:
			#db.rollback()
			toast("Check internet connection.")
			screen_manager.current = 'endOfSignup'

	def receive_data(self, usernameLogin, passwordLogin):

		try:
			db = mysql.connector.connect(
			host = "104.155.170.169",
			user = "root",
			password = "G00dwill",
			database = "tollcollection"
			)
			mycursor = db.cursor()

			mycursor.execute("SELECT * FROM motorists")
			result = mycursor.fetchall();

			global usernameInput
			usernameInput = usernameLogin.text
			password = passwordLogin.text

			counter1 = 0
			counter2 = 0
			length = len(result)
			print('length', length)

			if usernameInput == '' or password=='':
				snackbar = Snackbar(text="Enter log in details.", font_size='15sp')
				snackbar.open()
				screen_manager.current = 'login'	

			else:
				try:
					for i in range(len(result)):
						if usernameInput == result[i][0] and password == result[i][7]:
							app = MDApp.get_running_app()
							app.username = usernameInput
							print("Login name = ", app.username)
							print("Successful login")
							print(result[i][0])
							print(result[i][7])
							screen_manager.transition.direction = "left"
							screen_manager.current = 'home'
							Snackbar(text="Successful login").open()
							usernameLogin.text = ""
							passwordLogin.text = ""
							break
								
						if usernameInput != result[i][0] or password != result[i][7]:
							counter1 = counter1 + 1
							counter2 = counter2 + 1
							
					if counter1 == length or counter2 == length:
						print(counter1, counter2)
						print("Failed login")
						toast('Log in failed, enter correct details.')
						screen_manager.transition.direction = "left"
						screen_manager.current = "login"
						#Snackbar(text="Login failed").open()

				except:
					#db.rollback()
					toast('Check if information entered is correct...')
					print('Login failed.')
					screen_manager.current = "login"

				#screen_manager.current = 'home'

			db.close()

		except:
			toast("Check internet connection.")
			screen_manager.current = 'login'

		
		
	def goToAccount(self):
		screen_manager.transition.direction = "left"
		screen_manager.current = "account"

	def goToDeposit(self):
		screen_manager.transition.direction = "left"
		screen_manager.current = "deposit"

	def goToHistory(self):
		screen_manager.transition.direction = "left"
		screen_manager.current = "history"

	def goToVehicleSettings(self):
		screen_manager.transition.direction = "left"
		screen_manager.current = "vehicleSettings"

	def goToVehicles(self):
		screen_manager.transition.direction = "left"
		screen_manager.current = "vehicles"

	def goToInformation(self):
		screen_manager.transition.direction = "left"
		screen_manager.current = "information"

	def goToSettings(self):
		screen_manager.transition.direction = "left"
		screen_manager.current = "settings"

	def goToTransfers(self):
		screen_manager.transition.direction = "left"
		screen_manager.current = "transfers"

	def logoff(self):
		app = MDApp.get_running_app()
		app.username = ""
		screen_manager.transition.direction = "right"
		screen_manager.current = "login"

	def refreshAccount(self, account, balance):
		app = MDApp.get_running_app()
		usernameDisplay = app.username
		#try:
		db = mysql.connector.connect(
		host = "104.155.170.169",
		user = "root",
		password = "G00dwill",
		database = "tollcollection"
		)
		mycursor = db.cursor()

		sql = '''SELECT balance FROM balances WHERE username = %s'''
		#mycursor.execute("SELECT * FROM balances WHERE username = 'usernameInput'")
		data = (usernameDisplay,)
		mycursor.execute(sql, data)
		#mycursor.execute("SELECT balance FROM balances WHERE username = usernameDisplay")
		result = mycursor.fetchone()


		print(result[0])
		print(account.text)
		print(balance.text)

		#usernameInput = pass_data(*args)
		
		print("Username entered ", app.username)
		account.text = "   " + usernameDisplay
		balance.text = str(result[0]) + "   "


		screen_manager.transition.direction = "left"
		screen_manager.current = "account"

	def refreshTransactionHistory(self):
		screen_manager.transition.direction = "left"
		screen_manager.current = "transactions"

	def goToTransactionHistory(self):
		screen_manager.transition.direction = "left"
		screen_manager.current = "transactions"

	def changeAccountLabels(self, account, balance):
		app = MDApp.get_running_app()
		usernameDisplay = app.username

		try:
			db = mysql.connector.connect(
			host = "104.155.170.169",
			user = "root",
			password = "G00dwill",
			database = "tollcollection"
			)
			mycursor = db.cursor()

			sql = '''SELECT balance FROM balances WHERE username = %s'''
			#mycursor.execute("SELECT * FROM balances WHERE username = 'usernameInput'")
			data = (usernameDisplay,)
			print("Account username display = ", usernameDisplay)
			mycursor.execute(sql, data)
			#mycursor.execute("SELECT balance FROM balances WHERE username = usernameDisplay")
			result = mycursor.fetchone()


			print(result[0])
			print(account.text)
			print(balance.text)

			#usernameInput = pass_data(*args)
			
			print("Username entered ", app.username)
			account.text = "   " + usernameDisplay
			balance.text = str(result[0]) + "   "
		except:
			toast("Error")

	def getInformation(self, firstName, lastName, usernameInfo, gender, employmentStatus, phoneNumber, emailAddress):
		app = MDApp.get_running_app()
		usernameDisplay = app.username

		db = mysql.connector.connect(
		host = "104.155.170.169",
		user = "root",
		password = "G00dwill",
		database = "tollcollection"
		)
		mycursor = db.cursor()

		sql = '''SELECT * FROM motorists WHERE username = %s'''
		#mycursor.execute("SELECT * FROM balances WHERE username = 'usernameInput'")
		data = (usernameDisplay,)
		mycursor.execute(sql, data)
		#mycursor.execute("SELECT balance FROM balances WHERE username = usernameDisplay")
		result = mycursor.fetchone()

		firstName.text = result[1]
		lastName.text = result[2]
		usernameInfo.text = usernameDisplay
		gender.text = result[3]
		employmentStatus.text = result[4]
		phoneNumber.text = str(result[6])
		emailAddress.text = result[5]



	def transfer(self, receiverUsername, amount):
		app = MDApp.get_running_app()
		senderUsername = app.username
		receiver = receiverUsername.text

		try:
			db = mysql.connector.connect(
			host = "104.155.170.169",
			user = "root",
			password = "G00dwill",
			database = "tollcollection"
			)
			mycursor = db.cursor(buffered = True)

			sql = '''SELECT balance FROM balances WHERE username = %s'''
			#mycursor.execute("SELECT * FROM balances WHERE username = 'usernameInput'")
			data = (senderUsername,)
			mycursor.execute(sql, data)
			#mycursor.execute("SELECT balance FROM balances WHERE username = usernameDisplay")
			result = mycursor.fetchone()

			availableBalance = result[0]
			print("availableBalance = ", availableBalance)

			if receiverUsername.text == "" or amount.text == "":
				toast("Enter transfer details.")

			try:
				if amount.text != "":
					amountSent = float(amount.text)
					if receiverUsername.text == senderUsername:
						receiverUsername.text = ""
						toast("The receiver cannot be you. Enter a different receiver.")
					else:
						userSQL = '''SELECT * FROM motorists WHERE username = %s'''
						data0 = (receiverUsername.text,)
						mycursor.execute(userSQL, data0)
						receiverResult = mycursor.fetchone()
						#print("receiverResult = ", receiverResult)
						#print("receiverResult[0] = ", receiverResult[0])

						if receiverResult[0] == receiverUsername.text:
							if availableBalance < amountSent:
								toast("Transfer failed.\nYou have insufficient funds.")

							else:
								sql1 = '''UPDATE balances SET balance = balance + %s WHERE username = %s'''
								data1 = (amountSent, receiverUsername.text)

								mycursor.execute(sql1, data1)
								db.commit()

								sql2 = '''UPDATE balances SET balance = balance - %s WHERE username = %s'''
								data2 = (amountSent, senderUsername)

								mycursor.execute(sql2, data2)
								db.commit()

								toast("Transfer successful.")
								receiverUsername.text = ""
								amount.text = ""

								now = datetime.now()
								dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

								mycursor.execute("SELECT * FROM transactionhistory")
								result = mycursor.fetchall()
								transactionHistoryLength = len(result)

								sql = '''INSERT INTO tollcollection.transactionhistory(transactionID, description, username, amount, timestamp) VALUES(%s, %s, %s, %s, %s)'''
								data = (transactionHistoryLength + 1, "Transfer", senderUsername, amountSent, dt_string)
								mycursor.execute(sql, data)

								db.commit()

								sql = '''INSERT INTO tollcollection.transactionhistory(transactionID, description, username, amount, timestamp) VALUES(%s, %s, %s, %s, %s)'''
								data = (transactionHistoryLength + 2, "Receival", receiver, amountSent, dt_string)
								mycursor.execute(sql, data)

								db.commit()

						else:
							toast("The receiver username entered does not exist.")

			except:
				toast("Receiver does not exist.")
	
		except:
			receiverUsername.text = ""
			amount.text = ""
			toast("Database connection failed.")

	def displayCurrentUsername(self, currentUsername):
		app = MDApp.get_running_app()
		currentUsername.text = app.username

	def changeUsername(self, currentUsername, newUsername):
		app = MDApp.get_running_app()
		currentUsername.text = app.username

		try:
			db = mysql.connector.connect(
			host = "104.155.170.169",
			user = "root",
			password = "G00dwill",
			database = "tollcollection"
			)
			mycursor = db.cursor(buffered = True)

			usernameCheck = newUsername.text
			print(usernameCheck)

			mycursor.execute("SELECT * FROM motorists")
			result = mycursor.fetchall();
			#print(result)
			#print(result[0])
			#print(result[0][0])
			
			print(len(result))

			if usernameCheck == '':
				toast('Choose a username.')
				#screen_manager.current = 'username'

			else:
				for i in range(len(result)):
					if usernameCheck == result[i][0]:
						print(result[i])
						print("user already exists")
						#screen_manager.current = "username"
						#Snackbar(text="Username has already been taken. Choose a different username").open()
						toast("Username has already been taken. Choose a different username")
						break
						
					else:
						#username1 = username

						sql1 = '''UPDATE motorists SET username = %s WHERE username = %s'''
						sql2 = '''UPDATE balances SET username = %s WHERE username = %s'''
						sql3 = '''UPDATE transactionhistory SET username = %s WHERE username = %s'''
						sql4 = '''UPDATE tollhistory SET username = %s WHERE username = %s'''
						sql5 = '''UPDATE vehicles SET username = %s WHERE username = %s'''
						data = (newUsername.text, currentUsername.text)

						sql3 = '''UPDATE transactionhistory SET username = %s WHERE username = %s'''

						mycursor.execute(sql1, data)
						mycursor.execute(sql2, data)
						mycursor.execute(sql3, data)
						mycursor.execute(sql4, data)
						mycursor.execute(sql5, data)
						db.commit()

						app.username = newUsername.text

						toast("Username changed successfully.")
						screen_manager.transition.direction = "right"
						screen_manager.current = "settings"

			db.close()

		except:
			toast("Check internet connection.")
			#screen_manager.current = 'username'



	def changePassword(self, oldPassword, newPassword, confirmPassword):
		app = MDApp.get_running_app()
		user = app.username

		try:
			db = mysql.connector.connect(
			host = "104.155.170.169",
			user = "root",
			password = "G00dwill",
			database = "tollcollection"
			)
			mycursor = db.cursor(buffered = True)

			#mycursor.execute("SELECT * FROM motorists")
			sql = '''SELECT userPassword FROM motorists WHERE username = %s'''
			data = (user,)
			mycursor.execute(sql, data)
			result = mycursor.fetchone()
			print("Result = ", result[0])

			if oldPassword.text == "" or newPassword.text == "" or confirmPassword.text == "":
				toast("Enter password details.")

			else:
				if result[0] != oldPassword.text:
					toast("Enter the correct password to be changed.")

				if newPassword.text != confirmPassword.text:
					toast("New password and confirm password do not match.")

				if result[0] == oldPassword.text and newPassword.text == confirmPassword.text:
					sql1 = '''UPDATE motorists SET userPassword = %s WHERE username = %s'''
					data1 = (newPassword.text, user)

					mycursor.execute(sql1, data1)
					db.commit()

					toast("Password changed successfully.")
					screen_manager.transition.direction = "right"
					screen_manager.current = "settings"

					oldPassword.text = ""
					newPassword.text = ""
					confirmPassword.text = ""
			

			db.close()

		except:
			toast("Check internet connection.")
			#screen_manager.current = 'username'


	def displayVehicles(self, gridLayout, registrationNumberLabel1, registrationNumberLabel2, registrationNumberLabel3, registrationNumberLabel4, registrationNumberLabel5, registrationNumberLabel6, registrationNumberLabel7, registrationNumberLabel8, registrationNumberLabel9, registrationNumberLabel10):
		app = MDApp.get_running_app()
		user = app.username

		try:
			db = mysql.connector.connect(
			host = "104.155.170.169",
			user = "root",
			password = "G00dwill",
			database = "tollcollection"
			)
			mycursor = db.cursor(buffered = True)

			#mycursor.execute("SELECT * FROM vehicles")
			sql = '''SELECT * FROM vehicles WHERE username = %s'''
			data = (user,)
			mycursor.execute(sql, data)
			result = mycursor.fetchall()
			print("Result = ", result)

			db.close()

			length = len(result)
			print("length = ", length)
			gridLayout.rows = length

			registrationNumberLabel1.text = result[0][0]
			registrationNumberLabel2.text = result[1][0]
			registrationNumberLabel3.text = result[2][0]
			registrationNumberLabel4.text = result[3][0]
			registrationNumberLabel5.text = result[4][0]
			registrationNumberLabel6.text = result[5][0]
			registrationNumberLabel7.text = result[6][0]
			registrationNumberLabel8.text = result[7][0]
			registrationNumberLabel9.text = result[8][0]
			registrationNumberLabel10.text = result[9][0]
				

			
		except:
			#toast("Check internet connection.")
			#screen_manager.current = 'username'
			1+1




	def addVehicle(self, registrationNumber):
		app = MDApp.get_running_app()
		user = app.username

		if registrationNumber.text == "":
			toast("Enter vehicle registration number.")

		else:
			try:
				db = mysql.connector.connect(
				host = "104.155.170.169",
				user = "root",
				password = "G00dwill",
				database = "tollcollection"
				)
				mycursor = db.cursor(buffered = True)


				mycursor.execute("SELECT * FROM vehicles")
				result = mycursor.fetchall()

				vehicle = registrationNumber.text

				for i in range(len(result)):
					if registrationNumber.text == result[i][0]:
						print(result[i])
						print("vehicle already exists")
						#screen_manager.current = "username"
						#Snackbar(text="Username has already been taken. Choose a different username").open()
						toast("Vehicle is already registered.")
						break

					else:
						sql = '''INSERT INTO vehicles(registrationNumber, username) VALUES(%s,%s)'''
						data = (vehicle, user)
						mycursor.execute(sql, data)

						db.commit()
						
						toast("Vehicle added successfully.")
						
						screen_manager.transition.direction = "right"
						screen_manager.current = "vehicleSettings"

						registrationNumber.text = ""
						
				db.close()		
					
				
			except:
				1
				#toast("Check internet connection.")
				#screen_manager.current = 'username'


	def removeVehicle(self, registrationNumber):
		app = MDApp.get_running_app()
		user = app.username

		if registrationNumber.text == "":
			toast("Enter vehicle registration number.")

		else:
			try:
				db = mysql.connector.connect(
				host = "104.155.170.169",
				user = "root",
				password = "G00dwill",
				database = "tollcollection"
				)
				mycursor = db.cursor(buffered = True)


				mycursor.execute("SELECT * FROM vehicles")
				result = mycursor.fetchall()
				#print(result)

				vehicle = registrationNumber.text
				print("delete veh = ", vehicle)

				print("range = ", range(len(result)))

				counter = 0

				for i in range(len(result)):
					if registrationNumber.text != result[i][0]:
						counter = counter + 1
						#toast("Vehicle is not registered.")
						#registrationNumber.text = ""

				if counter == len(result):
					toast("Vehicle is not registered.")
					registrationNumber.text = ""

				else:
					sql = '''SELECT username FROM vehicles WHERE registrationNumber = %s'''
					data = (registrationNumber.text,)
					mycursor.execute(sql, data)
					result = mycursor.fetchone()
					print("vehicle owner = ", result[0])
					print("user = ", user)

				
					if user == result[0]:
						#print("delete veh = ", result[i][0])
						sql = '''DELETE FROM vehicles WHERE registrationNumber = %s'''
						data = (registrationNumber.text,)
						mycursor.execute(sql, data)

						db.commit()
						
						
						toast("Vehicle removed successfully.")
						screen_manager.transition.direction = "right"
						screen_manager.current = "vehicleSettings"

						registrationNumber.text = ""

					else:
						toast("Vehicle is not registered under your account.")
						

					
						
						
				db.close()		
					
				
			except:
				1
				#toast("Check internet connection.")
				#screen_manager.current = 'username'
				
				
	def displayTransactionHistory(self, gridLayout, transactionHistory1, transactionHistory2, transactionHistory3, transactionHistory4, transactionHistory5, transactionHistory6, transactionHistory7, transactionHistory8, transactionHistory9, transactionHistory10):
		app = MDApp.get_running_app()
		user = app.username

		try:
			db = mysql.connector.connect(
			host = "104.155.170.169",
			user = "root",
			password = "G00dwill",
			database = "tollcollection"
			)
			mycursor = db.cursor(buffered = True)

			#mycursor.execute("SELECT * FROM vehicles")
			sql = '''SELECT * FROM transactionhistory WHERE username = %s'''
			data = (user,)
			mycursor.execute(sql, data)
			result = mycursor.fetchall()
			print("Result = ", result)
			print("qwerty = ", result[0][1])

			db.close()

			length = len(result)
			print("length = ", length)
			gridLayout.rows = length

			a = result[0][1] 
			b = "     "
			c = str(result[0][3])

			d = a + c

			print(d)
			

			transactionHistory1.text = result[0][4] + "     " + result[0][1] + "     Amount: E" + str(result[0][3])
			transactionHistory2.text = result[1][4] + "     " + result[1][1] + "     Amount: E" + str(result[1][3])
			transactionHistory3.text = result[2][4] + "     " + result[2][1] + "     Amount: E" + str(result[2][3])
			transactionHistory4.text = result[3][4] + "     " + result[3][1] + "     Amount: E" + str(result[3][3])
			transactionHistory5.text = result[4][4] + "     " + result[4][1] + "     Amount: E" + str(result[4][3])
			transactionHistory6.text = result[5][4] + "     " + result[5][1] + "     Amount: E" + str(result[5][3])
			transactionHistory7.text = result[6][4] + "     " + result[6][1] + "     Amount: E" + str(result[6][3])
			transactionHistory8.text = result[7][4] + "     " + result[7][1] + "     Amount: E" + str(result[7][3])
			transactionHistory9.text = result[8][4] + "     " + result[8][1] + "     Amount: E" + str(result[8][3])
			transactionHistory10.text = result[9][4] + "     " + result[9][1] + "     Amount: E" + str(result[9][3])
				

			
		except:
			#toast("Check internet connection.")
			#screen_manager.current = 'username'
			1+1


	def displayTollHistory(self, gridLayout, tollHistory1, tollHistory2, tollHistory3, tollHistory4, tollHistory5, tollHistory6, tollHistory7, tollHistory8, tollHistory9, tollHistory10):
		app = MDApp.get_running_app()
		user = app.username

		try:
			db = mysql.connector.connect(
			host = "104.155.170.169",
			user = "root",
			password = "G00dwill",
			database = "tollcollection"
			)
			mycursor = db.cursor(buffered = True)

			#mycursor.execute("SELECT * FROM vehicles")
			sql = '''SELECT * FROM tollhistory WHERE username = %s'''
			data = (user,)
			mycursor.execute(sql, data)
			result = mycursor.fetchall()
			print("Result = ", result)
			print("qwerty = ", result[0][1])

			db.close()

			length = len(result)
			print("length = ", length)
			gridLayout.rows = length

			a = result[0][1] 
			b = "     "
			c = str(result[0][3])

			d = a + c

			print(d)

			print("Timestamp = ", result[0][0])
			

			tollHistory1.text = result[0][0] + "     " + result[0][1] + "     " + result[0][2]
			tollHistory2.text = result[1][0] + "     " + result[1][1] + "     " + result[1][2]
			tollHistory3.text = result[2][0] + "     " + result[2][1] + "     " + result[2][2]
			tollHistory4.text = result[3][0] + "     " + result[3][1] + "     " + result[3][2]
			tollHistory5.text = result[4][0] + "     " + result[4][1] + "     " + result[4][2]
			tollHistory6.text = result[5][0] + "     " + result[5][1] + "     " + result[5][2]
			tollHistory7.text = result[6][0] + "     " + result[6][1] + "     " + result[6][2]
			tollHistory8.text = result[7][0] + "     " + result[7][1] + "     " + result[7][2]
			tollHistory9.text = result[8][0] + "     " + result[8][1] + "     " + result[8][2]
			tollHistory10.text = result[9][0] + "     " + result[9][1] + "     " + result[9][2]
				

			
		except:
			#toast("Check internet connection.")
			#screen_manager.current = 'username'
			1+1




	# -------------------------------------------- MTN MOMO Payment System -------------------------------------------------
	def create_user(self):
	    """Static function that returns a unique uuid for each user"""
	    _id = str(uuid.uuid4())
	    print("UUID = ", _id)

	    headers = {
	        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
	        'X-Reference-Id': _id,
	        'Content-Type': 'application/json'
	    }

	    body = {'providerCallbackHost': 'https://webhook.site/855be9ef-eae0-4547-97a9-88edc949ded7'}

	    url = BASE_URL + '/v1_0/apiuser'

	    req = requests.post(url, json=body, headers=headers)

	    if req.status_code is not 201:
	        print("DONE STEP 1:\t\t" + "FAILURE")
	        return None

	    # request was a success, return the generated uuid
	    print("DONE STEP 1:\t\t" + "SUCCESS")

	    app = MDApp.get_running_app()
	    app.ID = _id

	    return _id


	def create_user_api(self):
	    """Static function to get an apiKey, given a unique uuid4"""
	    app = MDApp.get_running_app()
	    #_id = create_user()
	    _id = app.ID
	    if _id is not None:
	        url = BASE_URL + f"/v1_0/apiuser/{_id}/apikey"

	        headers = {
	            'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
	        }

	        response = requests.post(url, headers=headers)
	        print(response.content)

	        if response.status_code is not 201:
	            print("DONE STEP 2:\t\t" + "FAILURE")
	            return None

	        data = response.json()
	        print("DONE STEP 2:\t\t" + "SUCCESS", "\t\t" + data['apiKey'])
	        return {
	            'id': _id,
	            'apiKey': data['apiKey']
	        }

	    else:
	        return None


	def generate_token(self):
	    """Static function to generate a token for a given uuid, apikey"""
	    # IDS = create_user_api()  uncomment in sandbox development
	    url = BASE_URL + '/collection/token/'
	    headers = {
	        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
	    }

	    auth = (API_USER, API_KEY)

	    response = requests.post(url, headers=headers, auth=auth)

	    if response.status_code is not 200:
	        # print("DONE STEP 3:\t\t" + "FAILURE")
	        #raise Exception(response.status_code)
	        toast("Try again later.")

	    data = response.json()
	    # print("DONE STEP 3:\t\t" + "SUCCESS")

	    app = MDApp.get_running_app()
	    app.TOKEN = {
	        'id': API_USER,
	        'token': data['access_token']
	    }

	    return {
	        'id': API_USER,
	        'token': data['access_token']
	    }


	def requestToPay(self, amount, phoneNumber):
		try:
		    """Static function to request user to authorise payments"""
		    if amount.text == "" or phoneNumber.text == "":
		    	toast("Enter all fields.")

		    else:
			    app = MDApp.get_running_app()

			    url = BASE_URL + '/collection/v1_0/requesttopay'
			    request_to_pay_id = str(uuid.uuid4())

			    currency = "SZL"

			    #TOKEN = generate_token()

			    if app.TOKEN is not None:
			        token = app.TOKEN['token']

			        headers = {
			            'X-Reference-Id': request_to_pay_id,
			            'Authorization': 'Bearer ' + token,
			            'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
			            'X-Target-Environment': 'mtnswaziland',  # 'sandbox',
			            'Content-Type': 'application/json'
			        }

			        body = {
			            "amount": amount.text,
			            "currency": currency,
			            "externalId": "1234",
			            "payer": {
			                "partyIdType": "MSISDN",
			                "partyId": phoneNumber.text
			            },
			            "payerMessage": "Toll Gate account deposit.",
			            "payeeNote": "Deposit money into your Toll Gate account."
			        }

			        response = requests.post(url, json=body, headers=headers)

			        if response.status_code is not 202:
			            # print("DONE STEP 4:\t\t" + "FAILURE")
			            #raise Exception(response.status_code)
			            toast("Try again later.")


			        app.requestToPayID = request_to_pay_id
			        app.requestToPayToken = token
			        app.depositAmount = amount.text

			        # print("DONE STEP 4:\t\t" + "SUCCESS")
			        return request_to_pay_id, token

		except:
			toast("Try again later.")

	def check_payment_status(self):
		try:
			app = MDApp.get_running_app()
			request_to_pay_id = app.requestToPayID
			token = app.requestToPayToken

			url = BASE_URL + f'/collection/v1_0/requesttopay/{request_to_pay_id}'

			headers = {
		        'Authorization': 'Bearer ' + token,
		        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
		        'X-Target-Environment': 'mtnswaziland',
		        'Content-Type': 'application/json'
		    }

			response = requests.get(url, headers=headers)

			if response.status_code is not 200:
				print("ERROR CODE\t", response.status_code)
				#raise Exception("Transaction Failed. Please try again. If error persists, contact us at info@afrishopon.com or "
		                        #"call +268 7691 6994")

			data = response.json()

			status = data['status']
			print(status)

		    
			depositorUsername = app.username
			depositAmount = float(app.depositAmount)

			

			if (status != "SUCCESSFUL") and (status != "FAILED"):
				toast("Transaction is pending. Please wait.")
				if status == "PENDING":
					print(status)
					#status = "Your transaction is pending. Please approve the transaction. Dial *007*2#. If you don't get any"\
		                    # " notifications for approval, check if your MOMO wallet has enough cash. "
		        

				while(status == "PENDING"):
					response = requests.get(url, headers=headers)
					data = response.json()

					status = data['status']
					print(status)

					if status == "SUCCESSFUL":
						break

					if status == "FAILED":
						break

					time.sleep(30)
						

			if status == "FAILED":
				toast("Transaction failed.")
				

			if status == "SUCCESSFUL":
				try:
					db = mysql.connector.connect(
					host = "104.155.170.169",
					user = "root",
					password = "G00dwill",
					database = "tollcollection"
					)
					mycursor = db.cursor()

					sql1 = '''UPDATE balances SET balance = balance + %s WHERE username = %s'''
					data1 = (depositAmount, depositorUsername)

					mycursor.execute(sql1, data1)

					db.commit()

					now = datetime.now()
					dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

					mycursor.execute("SELECT * FROM transactionhistory")
					result = mycursor.fetchall()
					transactionHistoryLength = len(result)

					sql = '''INSERT INTO tollcollection.transactionhistory(transactionID, description, username, amount, timestamp) VALUES(%s, %s, %s, %s, %s)'''
					data = (transactionHistoryLength + 2, "Deposit", depositorUsername, depositAmount, dt_string)
					mycursor.execute(sql, data)

					db.commit()

					toast("Deposit Successful.")
					screen_manager.transition.direction = "right"
					screen_manager.current = "home"
				except:
					toast("Deposit error.")
					#screen_manager.transition.direction = "right"
					screen_manager.current = "deposit"


		    # transaction was successful, should present use with redirect options
			return status

		except:
			1 + 1









if __name__ == '__main__':
	Application().run()
	
	