# Capstone-Project: ClassroomBooker
The idea of this project is to create an web application that will allow MGSU students/faculties to freely share information regarding available classrooms for use in real-time basis, and further let them book any empty classrooms not in use for various activities such as group meetings, team projects, hanging out for fun, etc.

# Setup
This project is created in Python with Flask microframework, JS, and HTML/CSS. You will first need to install Python (v3.6 or newer), and then the following modules as well using pip:
1. Clone this project repository to your local machine (PC), open cmd and navigate to the cloned folder. For example, **C:\Capstone**.
2. Activate your virtual environment, then enter the following *pip command* to install python modules:
  > (YourVirtualEnvironment)C:\Capstone> pip install -U [NameOfModule]
* List of required modules:
  - flask
  - Flask-SQLAlchemy
  - Flask-WTF
  - flask-bcrypt
  - flask-login
  - Pillow
  
3. Once these modules are installed, enter the following command in command line prompt to run:
  > (YourVirtualEnvironment)C:\Capstone> python run.py
  
  You may need to set some environment variables if you receive a "KeyError: 'EMAIL_USER' ". 
  You'll want to copy and paste the following two lines commands into your CLI and executes:
  
  set EMAIL_USER=YourGoogleEmailAddress@gmail.com
  
  set EMAIL_PASSWORD=YourGoogleAppPassword
  
4. You will see the flask app is running now. Open your browser, and go to the URL displayed in your command prompt or
  > localhost:5000
