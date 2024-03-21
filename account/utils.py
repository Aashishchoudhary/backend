import random

# it will genrate 4 digit otp

def otp_generator():
    otp = random.randint(0000, 9999)
    return otp

def six_digit_otp_genrator():
    otp = random.randint(000000 , 999999)
    return otp