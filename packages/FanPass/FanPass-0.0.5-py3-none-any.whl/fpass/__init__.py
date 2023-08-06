import string,random

class check_type:
    def ck(char):
        if(char in string.digits):
            return "Number"
        elif(char in string.ascii_lowercase):
            return "Lower"
        elif(char in string.ascii_uppercase):
            return "Upper"
        return "Special"
    
class classing_the_type:
    def ctp(string):
        au = {"Number":0, "Lower":0, "Upper":0, "Special":0}
        for char in string:
            b = check_type.ck(char)
            au[b] += 1
        return au

class check_pass_level:
    def cpl(passw):
        if len(passw) < 8:
            return ""
        asu = classing_the_type.ctp(passw)
        level = 0
        for i in asu.values():
            if i > 0:
                level += 1
        return level

def password_generator(level_password):
    while True:
        pass_list = [random.choice("""AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz123456789@#$%^&*""") for i in range(8)]
        new_pass = "".join(pass_list)
        if check_pass_level.cpl(new_pass) == level_password:
            return new_pass