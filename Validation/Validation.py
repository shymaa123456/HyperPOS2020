import re
import datetime

class  CL_validation():
    email_address = "hossam.nabi.cs@gmail.com"
    def FN_valedation_mail(self,email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("address is valid")
        else:
            print("not valid")

    def FN_validation_password(self,password):
        while True:
            if len(password) < 8:
                print("Make sure your password is at lest 8 letters")
                break
            elif re.search('[0-9]', password) is None:
                print("Make sure your password has a number in it")
                break
            elif re.search('[A-Z]', password) is None:
                print("Make sure your password has a capital letter in it")
                break
            else:
                print("Your password seems fine")
                break

    def FN_validation_mobile(self, mobile):
        number = re.compile(r'[^0-9]').sub('', mobile)
        if len(number) == 11:
            print("Done")
        else:
            print("No")

    def FN_validation_formate(self,mobile):
        if(mobile.startswith('01')):
            print(mobile.startswith('01'))
        else:
            print(mobile.startswith('01'))

    def FN_validation_type(self,data):
        print(type(data))

    def FN_isEmpty(self,data):
        if len(data)==0 or data==null:
            return true
        else:
            return false

    def FN_validation_date(self,date):
        start = datetime.datetime.now()
        end = datetime.datetime.strptime("30-11-2030", "%d-%m-%Y")
        entry_date= datetime.datetime.strptime(date, "%d-%m-%Y")
        if start <= entry_date <= end:
            print("PASS!")
        else:
            print("YOU SHALL NOT PASS.")


