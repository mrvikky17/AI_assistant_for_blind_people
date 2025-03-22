import random
import smtplib

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(email, otp):
    print(f"OTP sent to {email}: {otp}")
    # Uncomment and configure SMTP for production use
    # server = smtplib.SMTP("smtp.gmail.com", 587)
    # server.starttls()
    # server.login("youremail@gmail.com", "yourpassword")
    # server.sendmail("youremail@gmail.com", email, f"Your OTP is {otp}")
    # server.quit()
