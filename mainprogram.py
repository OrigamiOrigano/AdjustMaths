#import tkinter as tk
import customtkinter as ctk
import sqlite3

conn = sqlite3.connect('AdjustMaths.db')
cursor = conn.cursor()

create_students_table = '''
CREATE TABLE IF NOT EXISTS Students (
    StudentID INTEGER PRIMARY KEY,
    ClassID INTEGER,
    FirstName TEXT,
    LastName TEXT,
    DoB Date,
    Username TEXT,
    Password TEXT,
    FOREIGN KEY (ClassID) REFERENCES Class(ClassID)
)
'''

create_teachers_table = '''
CREATE TABLE IF NOT EXISTS Teachers (
    TeacherID INTEGER PRIMARY KEY,
    Title TEXT,
    FirstName TEXT,
    LastName TEXT,
    Username TEXT,
    Password TEXT,
    DoB Date
)
'''

create_class_table = '''
CREATE TABLE IF NOT EXISTS Class (
    ClassID INTEGER PRIMARY KEY,
    TeacherID INTEGER,
    ClassName TEXT,
    FOREIGN KEY (TeacherID) REFERENCES Teachers(TeacherID)
)
'''

create_topic_table = '''
CREATE TABLE IF NOT EXISTS Topic (
    TopicID INTEGER PRIMARY KEY,
    TopicName TEXT
)
'''

create_result_table = '''
CREATE TABLE IF NOT EXISTS Result (
    ResultID INTEGER PRIMARY KEY,
    QuestionID INTEGER,
    StudentID INTEGER,
    TopicID INTEGER,
    ChosenOption TEXT,
    CorrectOption TEXT,
    Correct INTEGER,
    FOREIGN KEY (QuestionID) REFERENCES Question(QuestionID),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (TopicID) REFERENCES Topic(TopicID)
)
'''

create_leaderboard_table = '''
CREATE TABLE IF NOT EXISTS Leaderboard (
    LeaderboardID INTEGER PRIMARY KEY,
    ResultID INTEGER,
    FOREIGN KEY (ResultID) REFERENCES Result(ResultID)
)
'''

create_question_table = '''
CREATE TABLE IF NOT EXISTS Question (
    QuestionID INTEGER PRIMARY KEY,
    TopicID INTEGER,
    StudentID INTEGER,
    ResultID INTEGER,
    QuestionText TEXT,
    OptionA TEXT,
    OptionB TEXT,
    OptionC TEXT,
    OptionD TEXT,
    CorrectOption TEXT,
    Date TEXT,
    FOREIGN KEY (TopicID) REFERENCES Topic(TopicID),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (ResultID) REFERENCES Result(ResultID)
)
'''

cursor.execute(create_students_table)
cursor.execute(create_teachers_table)
cursor.execute(create_class_table)
cursor.execute(create_topic_table)
cursor.execute(create_result_table)
cursor.execute(create_leaderboard_table)
cursor.execute(create_question_table)





def StudentInsertion():
    insertion = '''
    INSERT INTO Students (FirstName, LastName, DoB, Username, Password) VALUES (?, ?, ?, ?, ?)
    '''

    sample_students = [
        ('Moosa', 'Islam', '2007-04-11', '18MIslam', 'Moosa'),
        ('Rowan', 'Gilchrist', '2006-11-15', '06RGilchrist', 'Rowan'),
        ('Owen', 'Klapkowski', '2006-09-21', '06OKlapkowski', 'Owen'),
        ('Melanie', 'Pritchard', '2007-03-11', '07MPritchard', 'Melanie'),
        ('Riveen', 'Kumanayaka', '2007-02-13', '07RKumanayaka', 'Riveen')
    ]

    t_insertion = '''
    INSERT INTO Teachers (Title, FirstName, LastName, Username, Password, DoB) VALUES (?, ?, ?, ?, ?, ?)
    '''

    sample_teachers = [
        ("Mrs.", 'Joanna', 'Hill', 'JHill', 'Hill', '1999-02-11'),
        ("Mr.", 'Peter', 'Severn', 'PSevern', 'Severn', '1997-03-12')
    ]

    cursor.executemany(insertion, sample_students)
    cursor.executemany(t_insertion, sample_teachers)

StudentInsertion()


conn.commit()


class AdjustMaths:
    def __init__(self):
        self.conn = sqlite3.connect('AdjustMaths.db')
        self.cursor = self.conn.cursor()

        ctk.set_default_color_theme("green") # dark-blue, blue, green

        self.window = ctk.CTk() # making a window to put all the information on
        self.window.geometry("1280x720") # setting a window size, this is adjustable.

        self.window.title("Welcome to AdjustMaths!")
        self.font_settings = ("Times", 24, 'bold')



        self.login_page() # calling the first method, the login page.

    def login_page(self):

        self.window.geometry("500x410") 

        self.allframe = ctk.CTkFrame(self.window)
        self.allframe.pack(pady = 50)

        welcome = ctk.CTkLabel(self.allframe, text="AdjustMaths!", font = ("Times", 30, 'bold'), text_color="green") # setting a large title
        welcome.pack(pady = 30, padx = 15) # 250 padding on top, 175 below


        self.u_enter = ctk.CTkEntry(self.allframe, placeholder_text="Username") # username entry.
        self.u_enter.pack(pady=3)  # sticky goes ew, meaning east west expansion for when the window is expanded.

        self.P_enter = ctk.CTkEntry(self.allframe, placeholder_text="Password", show = "*") # Password entry, show "*" will display characters input as * for privacy. self for "global" variable for .get
        self.P_enter.pack(pady = 10) # sticky goes ew, meaning east west expansion for when the window is expanded.


        login = ctk.CTkButton(self.allframe, text="Login",  command=self.login_check) # making the login button, when clicked will link to the login_check method
        #login.grid(column = 0, row = 0, padx = 5, pady = 7) # putting it in the middle of the buttons
        login.pack(pady = 7)

        t_sign_upbutton = ctk.CTkButton(self.allframe, text = "Teacher Sign up", command = self.teacher_signup)
        t_sign_upbutton.pack(side = "left", pady = (15, 20), padx = (25,5))

        s_sign_upbutton = ctk.CTkButton(self.allframe, text = "Student Sign up", command = self.student_signup)
        s_sign_upbutton.pack(side = "right", pady = 15, padx = (5, 25))


    def page_clearer(self, window):
        for widget in window.winfo_children():
            widget.destroy()

    def login_check(self): # checking all the input information to ensure a login can occur
        
        username = "" # setting the default values to nothing so a presence check can be done
        password = ""
        username = self.u_enter.get() # retrieving the username and password from the input boxes 18MIslam or JHill
        password = self.P_enter.get() # Moosa or Hill

        print (username, password)

        if username != "":
            if username[0].isdigit() == True: # if the first symbol of the username is a digit, then it is a student, otherwise it will be a teacher
                user_search = "SELECT Password FROM Students WHERE Username = ?"
                self.cursor.execute(user_search , (username,))
                password_from_table = self.cursor.fetchone()
                student = True

            else:
                teacher_search = "SELECT Password FROM Teachers WHERE Username = ?"
                self.cursor.execute(teacher_search, (username,))
                password_from_table = self.cursor.fetchone()
                student = False



            if password_from_table != None:
                if password == password_from_table[0] and student == True: # queries from the database returned as tuples, so using indexes is required.
                    self.student_home_screen(username)
                
                elif password == password_from_table[0] and student == False:
                    self.teacher_home_screen(username)

                else:
                    self.wrong_info("Incorrect Password")

            else:
                self.wrong_info("Incorrect Username")

        else:
            self.wrong_info("No username entered.")

    


    def student_home_screen(self, username):
        self.page_clearer(self.window)
        self.window.title(f"Welcome {username}")


    def teacher_home_screen(self, username):
        self.page_clearer(self.window)
        self.window.title(f"Welcome {username}")


    def wrong_info(self, Text): # makes a popup that the wrong password has been entered
        popup = ctk.CTkToplevel() # will show up above the current window
        popup.title(f"{Text}") 

        popup.configure(bg = "#000000", pady = 20) # setting some coloours
        popup.geometry("300x120") #] size of the window
        label = ctk.CTkLabel(popup, text=f"{Text}" ) # text for popup
        label.pack()

        close_button = ctk.CTkButton(popup, text="Close" , command=popup.destroy) # button to close the popup
        close_button.pack(pady=10) 


    def student_signup(self): # needs code

        self.page_clearer(self.window)

        
        welcome = ctk.CTkLabel(self.window, text="Student Sign Up Page", font = (("Times"), 26, 'bold', "underline") , width=30, height=3, text_color = "green") # setting a large title
        welcome.pack(pady=25)

        input_frame = ctk.CTkFrame(self.window) # making a frame in which the username and password can be placed
        input_frame.pack(pady=20)


        self.fname_enter = ctk.CTkEntry(input_frame ,  width=200, placeholder_text = "First Name") 
        self.fname_enter.grid(row=0, column=1, padx = (20,5) ,pady = (20,10), sticky = "ew") # sticky goes ew, meaning east west expansion for when the window is expanded.


        self.lname_enter = ctk.CTkEntry(input_frame ,  width=200, placeholder_text = "Last Name") 
        self.lname_enter.grid(row=0, column=2, padx = (5,20) ,pady = (20,10), sticky = "ew") # sticky goes ew, meaning east west expansion for when the window is expanded.


        self.dob_enter = ctk.CTkEntry(input_frame ,  width=200, placeholder_text = "Date of Birth") 
        self.dob_enter.grid(row=1, column=1, padx = (20,5) ,pady = 10, sticky = "ew",) # sticky goes ew, meaning east west expansion for when the window is expanded.

        self.class_enter = ctk.CTkEntry(input_frame ,  width=200, placeholder_text = "Class Name") 
        self.class_enter.grid(row=1, column=2, padx = (5,20) ,pady = 10, sticky = "ew", ) # sticky goes ew, meaning east west expansion for when the window is expanded.


        self.pass_enter = ctk.CTkEntry(input_frame ,  width=200,  placeholder_text = "Password", show = "*") 
        self.pass_enter.grid(row=2, column=1, padx = (20,5) ,pady = 10, sticky = "ew") # sticky goes ew, meaning east west expansion for when the window is expanded.#


        self.repass_enter = ctk.CTkEntry(input_frame ,  width=200, placeholder_text = "Re-enter" , show = "*") 
        self.repass_enter.grid(row=2, column=2, padx = (5,20) ,pady = 10, sticky = "ew") # sticky goes ew, meaning east west expansion for when the window is expanded.

        signup_button = ctk.CTkButton(input_frame, text="Sign Up!",  command=self.signupchecks)
        signup_button.grid(row=3, columnspan=4, pady=20)

    def signup_check(self):
        firstname = self.fname_enter.get()
        lastname = self.lname_enter.get()

        dob = self.dob_enter.get()
        password = self.pass_enter.get()
        reentry = self.repass_enter.get()
    
        alreadyexists = "SELECT * FROM Students WHERE FirstName = ? and LastName = ? AND DoB = ?"

        self.cursor.execute(alreadyexists, (firstname,lastname, dob))
        result = self.cursor.fetchone()

        print (result)

        if result != None: # if a result is returned, it means that the student already exists
            self.wrong_info("User already exists!")
            self.page_clearer(self.window)
            self.login_page()

        # need to make statement checking if the Class that is input exists, but first need to make signup for teacher, so the teacherID exists for each Class. Development of student stuff must come after that's done.

        else:
            if password != reentry:
                self.wrong_info("Passwords are not the same")

            else:
                print ("User does not exist, add to database")
                create_account = '''INSERT INTO Students (FirstName, LastName, DoB, )'''
                



    def teacher_signup(self): # needs code
        self.page_clearer(self.window)
        print ("Teacher signing up here...")


    def run(self):
        self.window.mainloop() # actually runs everything..

app = AdjustMaths()
app.run()
