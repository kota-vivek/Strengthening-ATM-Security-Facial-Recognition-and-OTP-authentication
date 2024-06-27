import cv2
import face_recognition
import sqlite3
from tkinter import *
from tkinter import ttk
import time
from tkinter import font
from tkinter import messagebox
from twilio.rest import Client
import random
from PIL import ImageTk, Image

# Unknown Face Warning
def warningOTP():
    processing.pack_forget()
    processingText.pack_forget()
    response = messagebox.askquestion("Invalid OTP", "You have inserted wrong OTP!!!\nTry Again?")
    if response == "yes":
        processing.pack_forget()
        processingText.pack_forget()
        start()
    else:
        root.quit()

# Unknown Face Warning
def warningUnkownFace():
    processing.pack_forget()
    processingText.pack_forget()
    fp.pack_forget()

    response = messagebox.askquestion("No Face", "Could not detect any face\nTry Again?")
    if response == "yes":
        start()
    else:
        root.quit()

# Account Number Warning
def warningAccountNumber():
    processing.pack_forget()
    processingText.pack_forget()

    response = messagebox.askquestion("Invalid Account Number", "Invalid Account Number\nTry Again?")
    if response == "yes":
        start()
    else:
        root.quit()

# Pin Warning
def warningPin():
    processing.pack_forget()
    processingText.pack_forget()

    response = messagebox.askquestion("Incorrect Pin", "Incorrect Pin\nTry Again?")
    if response == "yes":
        start()
    else:
        root.quit()

# OTP Verification
def verifyOTP():
    failedText.pack_forget()
    fp.pack_forget()
    OTPText.pack_forget()
    OTPNumInput.pack_forget()
    OTPsubmitButton.pack_forget()

    processingText = Label(root, text="Verifying OTP Code")
    processing = ttk.Progressbar(root, orient=HORIZONTAL, length=300, mode="indeterminate")
    # Showing in the Screen
    processingText.pack(pady=20)
    processing.pack()
    processing.start(10)

    # Matching OTP
    if otp == int(OTPNumInput.get()):
        processingText.pack_forget()
        processing.pack_forget()
        processing.after(100, update)
    else:
        # Set error message to invalid OTP
        processing.after(100, warningOTP)

def readDB():
    connect = sqlite3.connect("bank_database.db")
    c = connect.cursor()
    number = accountNumInput.get()
    sql = "SELECT * FROM accounts WHERE account_number = '{0}'"
    c.execute(sql.format(number))

    data = c.fetchone()
    if data is None:
        data = []
    else:
        with open('baseImage.jpg', 'wb') as f:
            f.write(data[2])
    connect.close()
    return data

def vo11():
    global NP
    global NP1
    global con

    NP = Label(root, text="Enter New PIN")
    NP1 = Entry(root, width=50, borderwidth=2)
    NP.pack(pady = 20)
    NP1.pack(pady = 20)
    def vo12():
        global la
        global ba
        global qu
        NP.pack_forget()
        NP1.pack_forget()
        con.pack_forget()
        o=NP1.get()
        pinupdate(o)
        la = Label(root, text="Your PIN has been Changed Successfully")
        la.pack(pady=10)
        ba=Button(root, text="Continue", width=20, height=2, bg="#2d5cf7", fg="white", command=vo13)
        ba.pack(pady = 20)
        qu=Button(root, text="Quit", width=20, height=2, bg="#ff0000", fg="white", command=quit)
        qu.pack(pady = 20)
    con=Button(root, text="Confirm", width=20, height=2, bg="#2d5cf7", fg="white", command=vo12)
    con.pack(pady = 20)
    def vo13():
            ba.pack_forget()
            qu.pack_forget()
            la.pack_forget()
            start()

def verifyOTP1():
    OTPText.pack_forget()
    OTPNumInput.pack_forget()
    OTPsubmitButton.pack_forget()
    global processing
    global processingText
    processingText = Label(root, text="Verifying OTP Code")
    processing = ttk.Progressbar(root, orient=HORIZONTAL, length=300, mode="indeterminate")
    # Showing in the Screen
    processingText.pack(pady=20)
    processing.pack()
    processing.start(10)
    # Matching OTP
    if otp == int(OTPNumInput.get()):
        processingText.pack_forget()
        processing.pack_forget()
        processing.after(1000,vo11) 

    else:
        # Set error message to invalid OTP
        processing.after(1000, warningOTP)

# Asking for OTP
def callOTP():
    processing.pack_forget()
    processingText.pack_forget()
    fp.pack_forget()

    global failedText
    global OTPText
    global OTPNumInput
    global OTPsubmitButton
    global otp

    # Generate and Send OTP
    D=readDB()
    account_sid = D[4] # SID is being removed for security
    auth_token = D[5] # Token is being removed for security
    client = Client(account_sid, auth_token)
    otp = random.randint(100000, 999999)
    #mobile = '+88017xxxxxxxxx' # Number is being removed for security
    sms = client.messages.create(
        body='Please enter this OTP to continue Log in. Your OTP is - ' + str(otp),
        from_=D[6],
        to= "+91"+str(contactNumber)
    )
    sms.sid
    failedText=Label(root,text="Face Recognition Failed", fg="red")
    OTPText = Label(root, text="Enter Your OTP Code")
    OTPNumInput = Entry(root, width=50, borderwidth=2)
    OTPsubmitButton = Button(root, text="Log In", width=20, height=2, bg="#2d5cf7", fg="white", command=verifyOTP)
    # failedText.pack(pady=10)
    OTPText.pack(pady=10)
    OTPNumInput.pack()
    OTPsubmitButton.pack(pady=10)

#Face Authentication
def callOTP1():
    accountNumInput.pack_forget()
    loginButton.pack_forget()
    enter.pack_forget()

    global OTPText
    global OTPNumInput
    global OTPsubmitButton
    global otp

    # Generate and Send OTP
    D=readDB()
    account_sid = D[4] # SID is being removed for security
    auth_token = D[5] # Token is being removed for security
    client = Client(account_sid, auth_token)
    otp = random.randint(100000, 999999)
    #mobile = '+88017xxxxxxxxx' # Number is being removed for security
    sms = client.messages.create(
        body='Please enter this OTP to continue pin change. Your OTP is - ' + str(otp),
        from_=D[6],
        to= "+91"+str(D[3])
    )
    sms.sid
    OTPText = Label(root, text="Enter Your OTP Code")
    OTPNumInput = Entry(root, width=50, borderwidth=2)
    OTPsubmitButton = Button(root, text="Log In", width=20, height=2, bg="#2d5cf7", fg="white", command=verifyOTP1)
    OTPText.pack(pady=10)
    OTPNumInput.pack()
    OTPsubmitButton.pack(pady=10)

def faceAuthentication():

    # Get video footage
    global faceFramesEncoded
    faceFramesEncoded = []
    totalDist = []
    face1 = []
    video = cv2.VideoCapture(0)

    # set footage length to 5 seconds
    endTime = time.time() + 15
    while time.time() < endTime:
        status, frame = video.read()
        # Converting resized original image into RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Encode image frame
        frameEncode = face_recognition.face_encodings(frame)
        # Get face location(top, right, bottom, left)
        faceLoc = face_recognition.face_locations(frame)

        for ef, fl in zip( frameEncode, faceLoc):
            if len(face1) == 0:
                face1.append(ef)
            dist = face_recognition.face_distance(face1, ef)

            # if any human face found, get the distance from base image
            if len(dist) > 0:
                totalDist.append(dist[0])
                faceFramesEncoded.append(ef)

                top, right, bottom, left = fl
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 4)
            # Show the video
            cv2.imshow('Live Video', frame)
            cv2.waitKey(1)

    video.release()
    cv2.destroyAllWindows()

    if len(totalDist)<1:
        return False
    distance = sum(totalDist) / len(totalDist)
    if distance < 0.16:
        return False
    else:
        return True

#Face Recognition
def matchFace():

    img = cv2.imread('baseImage.jpg')
    # Change color to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Encode base image
    imgEncode = face_recognition.face_encodings(img)[0]

    # Compare with video footage
    totalDist = []
    for ef in faceFramesEncoded:
        dist = face_recognition.face_distance([imgEncode], ef)
        # if any human face found, get the distance from base image
        if len(dist) > 0:
            totalDist.append(dist[0])

    if len(totalDist)<1:
        return False
    distance = sum(totalDist) / len(totalDist)

    if distance > 0.6:
        return False
    else:
        return True

# Function to read data from DB
def readDB():
    connect = sqlite3.connect("bank_database.db")
    c = connect.cursor()
    number = accountNumInput.get()
    sql = "SELECT * FROM accounts WHERE account_number = '{0}'"
    c.execute(sql.format(number))

    data = c.fetchone()
    if data is None:
        data = []
    else:
        with open('baseImage.jpg', 'wb') as f:
            f.write(data[2])
    connect.close()
    return data
def pinupdate(n):
     # Function to update the balance in the SQLite database
    connection = sqlite3.connect("bank_database.db")
    cursor = connection.cursor()
    A=readDB()
    # Replace 'account_id' with the actual primary key or unique identifier for the account
    account_id =  A[0]# Replace this with the actual account ID
    s=str(n)
    # Update the balance for the specific account
    cursor.execute("UPDATE accounts SET account_pin = ? WHERE account_number like ?", (s, account_id))
    connection.commit()
    connection.close()

#checkbalanceback
def back():
    balance.pack_forget()
    Showbalance.pack_forget()
    backButton.pack_forget()
    exitButton.pack_forget()
    update()

#depositback
def back2():
    AmountInput.pack_forget()
    Amount.pack_forget()
    nextButton.pack_forget()
    backButton.pack_forget()
    exitButton.pack_forget()
    update()

#withdrawback
def back3():
    AmountInput.pack_forget()
    Amount.pack_forget()
    nextButton.pack_forget()
    backButton.pack_forget()
    exitButton.pack_forget()
    update()

#deposit
def f():
    global Amount
    global AmountInput
    global nextButton
    global backButton
    global exitButton
    D=readDB()
    def g():
        UpdateBalance(D[7]+int(AmountInput.get()))
        G=readDB()
        response = messagebox.askquestion("Deposit Successfull", "Your Current Balance is: "+str(G[7])+"\nContinue?")
        if response == "yes":
            Amount.pack_forget()
            AmountInput.pack_forget()
            nextButton.pack_forget()
            exitButton.pack_forget()
            backButton.pack_forget()
            update()
        else:
            root.quit()
    chcekAcount.pack_forget()
    balanceButton.pack_forget()
    pinchangeButton.pack_forget()
    withdrawButton.pack_forget()
    depositButton.pack_forget()
    exitButton.pack_forget()
    Amount=Label(root,text="Enter the Amount",fg="black")
    AmountInput=Entry(root,width=20,borderwidth=2)
    Amount.pack(pady=15)
    AmountInput.pack(pady=10)
    nextButton = Button(root, text="Deposit", width=10, height=2, bg="#ffffff", fg="#000000",command=g)
    nextButton.pack(pady=10)
    backButton = Button(root, text="Back", width=10, height=2, bg="#ffffff", fg="#000000", command=back2)
    exitButton = Button(root, text="Exit", width=10, height=2, bg="#e3242b", fg="#000000", command=d)
    backButton.pack(side="left",padx=15,pady=15,anchor="sw")
    exitButton.pack(side="right",padx=15,pady=15,anchor="se")
    #deposit update
    
#Check Balance
def a():
    global balance
    global Showbalance
    global backButton
    global exitButton
    D=readDB()
    chcekAcount.pack_forget()
    balanceButton.pack_forget()
    pinchangeButton.pack_forget()
    withdrawButton.pack_forget()
    depositButton.pack_forget()
    exitButton.pack_forget()
    balance=Label(root,text="Your Account Balance",fg="black")
    custom_font = font.Font(family="Yu Mincho", size=12)
    Showbalance=Label(root, font=custom_font, text=str(D[7]))
    Showbalance.config(font=("Yu Mincho",14))
    backButton = Button(root, text="Back", width=10, height=2, bg="#ffffff", fg="#000000", command=back)
    exitButton = Button(root, text="Exit", width=10, height=2, bg="#e3242b", fg="#000000", command=d)
    backButton.pack(side="left",padx=15,pady=15,anchor="sw")
    exitButton.pack(side="right",padx=15,pady=15,anchor="se")
    balance.pack(pady=15)
    Showbalance.pack(pady=15)

#otp change
def z():
    D=readDB()
    global cpinlabel
    global cpinInput
    global npinlabel
    global npinInput
    global  backbButton
    global exitbButton
    global changeButton
    chcekAcount.pack_forget()
    balanceButton.pack_forget()
    pinchangeButton.pack_forget()
    withdrawButton.pack_forget()
    depositButton.pack_forget()
    exitButton.pack_forget()
    cpinlabel=Label(root, text="Enter Your current pin", fg="Black")
    cpinInput=Entry(root, width=20, borderwidth=2)
    npinlabel=Label(root,text="Enter Your New pin", fg="Black")
    npinInput=Entry(root, width=20, borderwidth=2)
    cpinlabel.pack(pady=10)
    cpinInput.pack(pady=10)
    npinlabel.pack(pady=10)
    npinInput.pack(pady=10)
    def y():
        if cpinInput.get()==str(D[1]) and npinInput.get()!="":
            pinupdate(npinInput.get())
            response = messagebox.askquestion("pin change", "pin change is successful\nContinue?")
            if response == "yes":
                cpinlabel.pack_forget()
                cpinInput.pack_forget()
                npinlabel.pack_forget()
                npinInput.pack_forget()
                changeButton.pack_forget()
                backbButton.pack_forget()
                exitbButton.pack_forget()
                update()
            else:
                root.quit()
        else:
            response = messagebox.askquestion("pin change", "Your current pin is wrong or new pin is invalid \nRetry?")
            if response == "yes":
                cpinlabel.pack_forget()
                cpinInput.pack_forget()
                npinlabel.pack_forget()
                npinInput.pack_forget()
                changeButton.pack_forget()
                backbButton.pack_forget()
                exitbButton.pack_forget()
                z()
            else:
                cpinlabel.pack_forget()
                cpinInput.pack_forget()
                npinlabel.pack_forget()
                npinInput.pack_forget()
                changeButton.pack_forget()
                backbButton.pack_forget()
                exitbButton.pack_forget()
                update()
    changeButton=Button(root,text="Change",width=10,height=2,bg="#ffffff",fg="#000000",command=y)
    changeButton.pack(pady=10)
    backbButton = Button(root, text="Back", width=10, height=2, bg="#ffffff", fg="#000000", command=back4)
    exitbButton = Button(root, text="Exit", width=10, height=2, bg="#e3242b", fg="#000000", command=d)
    backbButton.pack(side="left",padx=15,pady=15,anchor="sw")
    exitbButton.pack(side="right",padx=15,pady=15,anchor="se")

def back4():
    cpinlabel.pack_forget()
    cpinInput.pack_forget()
    npinlabel.pack_forget()
    npinInput.pack_forget()
    backbButton.pack_forget()
    exitbButton.pack_forget()
    changeButton.pack_forget()
    update()

# Function for authorized screen
def update():
    # Removing Elements from Screen after 3sec
    processing.pack_forget()
    fp.pack_forget()
    processingText.pack_forget()

    global chcekAcount
    global balanceButton
    global pinchangeButton
    global withdrawButton
    global depositButton
    global exitButton

    # Calling UI Elements for account Options
    chcekAcount = Label(root, text="Choose Your Option", fg="black")
    balanceButton = Button(root, text="Check Balance", width=20, height=2, bg="#2d5cf7", fg="white",command=a)
    pinchangeButton=Button(root, text="Pin change", width=20, height=2, bg="#2d5df7", fg="white",command=z)
    withdrawButton = Button(root, text="Withdraw Amount", width=20, height=2, bg="#2d5cf7", fg="white",command=b)
    depositButton = Button(root, text="Deposit Amount", width=20, height=2, bg="#2d5cf7", fg="white",command=f)
    exitButton=Button(root,text="Exit Session", width=20, height=2, bg="#e3242b", fg="white", command=d)
    # Showing in the Screen
    chcekAcount.pack(pady=15)
    balanceButton.pack(pady=10)
    pinchangeButton.pack(pady=10)
    withdrawButton.pack(pady=10)
    depositButton.pack(pady=10)
    exitButton.pack(pady=10)

#withdraw
def b():
    D=readDB()
    global Amount
    global AmountInput
    global nextButton
    global backButton
    global exitButton
    chcekAcount.pack_forget()
    balanceButton.pack_forget()
    pinchangeButton.pack_forget()
    withdrawButton.pack_forget()
    depositButton.pack_forget()
    exitButton.pack_forget()
    Amount=Label(root,text="Enter the Amount",fg="black")
    AmountInput=Entry(root,width=20,borderwidth=2)
    Amount.pack(pady=15)
    AmountInput.pack(pady=10)
    #vlc
    def e():
        D=readDB()
        if int(D[7])<int(AmountInput.get()):
            response = messagebox.askquestion("Insufficient Balance", "Insufficient Balance\nTry Again?")
            if response == "yes":
                Amount.pack_forget()
                AmountInput.pack_forget()
                nextButton.pack_forget()
                backButton.pack_forget()
                exitButton.pack_forget()
                b()
            else:
                root.quit()
        else:
            newbalance=int(D[7])-int(AmountInput.get())
            UpdateBalance(newbalance)
            S=readDB()
            response = messagebox.askquestion("Withdraw Successful", "Your Remaining Balance is: "+str(D[7]-int(AmountInput.get()))+" \nContinue?")
            if response == "yes":
                Amount.pack_forget()
                AmountInput.pack_forget()
                nextButton.pack_forget()
                exitButton.pack_forget()
                backButton.pack_forget()
                update()
            else:
                root.quit()
    nextButton = Button(root, text="Withdraw", width=10, height=2, bg="#ffffff", fg="#000000",command=e)
    nextButton.pack(pady=10)
    backButton = Button(root, text="Back", width=10, height=2, bg="#ffffff", fg="#000000", command=back3)
    exitButton = Button(root, text="Exit", width=10, height=2, bg="#e3242b", fg="#000000", command=d)
    backButton.pack(side="left",padx=15,pady=15,anchor="sw")
    exitButton.pack(side="right",padx=15,pady=15,anchor="se")

#UpdateBalance
def UpdateBalance(n):
     # Function to update the balance in the SQLite database
    connection = sqlite3.connect("bank_database.db")
    cursor = connection.cursor()
    A=readDB()
    # Replace 'account_id' with the actual primary key or unique identifier for the account
    account_id =  A[0]# Replace this with the actual account ID
    
    # Update the balance for the specific account
    cursor.execute("UPDATE accounts SET balance = ? WHERE account_number like ?", (n, account_id))
    connection.commit()
    connection.close()

#Quit
def d():
    root.quit()
# Function of start screen
def next():
    global processing
    global processingText
    global contactNumber

    # Removing Elements from Screen after Button Clicked
    titleText.pack_forget()
    accountNumInput.pack_forget()
    accountPassInput.pack_forget()
    loginButton.pack_forget()
    fp.pack_forget()

    # Calling UI Elements for Verifying Notice
    processingText = Label(root, text="Verifying Your Inputs")
    processing = ttk.Progressbar(root, orient=HORIZONTAL, length=300, mode="indeterminate")
    # Showing in the Screen
    processingText.pack(pady=20)
    processing.pack()
    processing.start(10)

    # read data from db
    data = readDB()
    

    if len(data) > 0:
        contactNumber = data[3]
        pinDB = data[1]
        # Check if pin matched
        if pinDB == accountPassInput.get():
            # Process image
            check = faceAuthentication()
            if check:
                result = matchFace()
                if result:
                    processing.after(1000, update)
                else:
                    # Set error message to face not matched
                    processing.after(1000, callOTP)
            else:
                # Set error message to face not matched
                processing.after(100, warningUnkownFace)
        else:
            # Set error message to pin not matched
            processing.after(100, warningPin)
    else:
        # Set error message to account not found
        processing.after(100, warningAccountNumber)

# Functions to start authorization
def start():
    # Removing Elements from Screen after 3sec
    processing.pack_forget()
    processingText.pack_forget()

    global accountNumInput
    global accountPassInput
    global titleText
    global loginButton
    global fp

    # Calling UI Elements
    titleText = Label(root, text="Enter Your Account Number & Password")
    accountNumInput = Entry(root, width=50, borderwidth=2)
    accountPassInput = Entry(root, width=50, borderwidth=2, show="*")
    loginButton = Button(root, text="NEXT", width=20, height=2, bg="#2d5cf7", fg="white", command=next)
    custom_font = font.Font(family="Helvetica", size=12, underline=True)
    fp = Button(root, text="Forgot PIN?",font = custom_font, width=20, height=1,fg = "blue", bd =0,command = fp1)

    # Showing in the Screen
    titleText.pack(pady=30)
    accountNumInput.pack(pady=10)
    accountPassInput.pack(pady=10)
    loginButton.pack(pady=20)
    fp.pack(pady=10)
    accountNumInput.focus()

def fp1():
    global accountNumInput
    global loginButton
    global enter
    titleText.pack_forget()
    accountNumInput.pack_forget()
    accountPassInput.pack_forget()
    loginButton.pack_forget()
    fp.pack_forget()

    enter = Label(root, text="Enter Account Number", fg="black")
    accountNumInput = Entry(root, width=50, borderwidth=2)

    def fp2():
        global data
        data = readDB()
        if(data != []):
            callOTP1()
        else:
            # processingText.pack_forget()
            # processing.pack_forget()
            response = messagebox.askquestion("Invalid Account number", "Invalid Account number\nTry Again?")
            if response == "yes":
                start()
            else:
                root.quit()
    loginButton = Button(root, text="Next", width=20, height=2, bg="#2d5cf7", fg="white", command=fp2)
    enter.pack(pady = 20)
    accountNumInput.pack(pady = 20)
    loginButton.pack(pady=20)
# Start the User Interface
root = Tk()
root.title("ATM Facial Recognition")
root.iconbitmap("Source.ico")
root.geometry("600x600")
# Calling UI Elements
logo = ImageTk.PhotoImage(Image.open("logo.png"))
my_img = Label(image=logo)
titleText = Label(root, text="Enter Your Account Number & Password")
accountNumInput = Entry(root, width=50, borderwidth=2)
accountPassInput = Entry(root, width=50, borderwidth=2, show="*")
loginButton = Button(root, text="NEXT", width=20, height=2, bg="#009B4B", fg="white", command=next)
custom_font = font.Font(family="Helvetica", size=12, underline=True)
fp = Button(root, text="Forgot PIN?",font = custom_font, width=20, height=1,fg = "blue", bd =0,command = fp1)

# Showing in the Screen
my_img.pack(pady=30)
titleText.pack(pady=10)
accountNumInput.pack(pady=10)
accountPassInput.pack(pady=10)
loginButton.pack(pady=20)
fp.pack(pady=10)

accountNumInput.focus()
root.mainloop()
