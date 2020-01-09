import math, random


def generateOTP(num_digits):
    digits = "0123456789"
    OTP = ""
    for i in range(num_digits):
        OTP += digits[int(math.floor(random.random() * 10))]
    return OTP