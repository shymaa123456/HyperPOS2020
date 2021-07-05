import re
import datetime
from PyQt5 import QtWidgets
from data_connection.h1pos import db1

class CL_validation():
    email_address = "hossam.nabi.cs@gmail.com"


    @staticmethod
    def FN_valedation_mail(email):
        if re.match(r"[^@]+@[^@]+\.[^@]", email):
            return True;
        else:
            return False;

    @staticmethod
    def FN_validation_password(self, password):
        mes = 0

        if len(password) < 8:
            mes = 1
            QtWidgets.QMessageBox.warning(self, "Error", "Make sure your password is at lest 8 letters")

        elif re.search('[0-9]', password) is None:
            QtWidgets.QMessageBox.warning(self, "Error", "Make sure your password has a number in it")
            mes = 1

        elif re.search('[A-Z]', password) is None:
            QtWidgets.QMessageBox.warning(self, "Error", "Make sure your password has a capital letter in it")
            mes = 1

        else:
            print("Your password seems fine")
        if mes == 1:
            return True
        else:
            return False

    @staticmethod
    def FN_validation_mobile(mobile):
        try:
            number = re.compile(r'[^0-9]').sub('', mobile)
            if len(number) != 11:
                return 3
            else:
                if (mobile.startswith('01')):
                    print(mobile.startswith('01'))
                    return True
                else:
                    return 2
        except Exception as err:
            print(err)
    @staticmethod
    def FN_validation_nationalID(nationalID):
        try:
            if len(nationalID) != 14:
                return False
            else:
                return True
        except Exception as err:
            print(err)
    @staticmethod
    def FN_validation_str(self, data, field_name):
        if type(data) is str:
            print(type(data) is str)
            return True
        else:
            message = "Make sure your that " + field_name + "is string"
            QtWidgets.QMessageBox.warning(self, "Error", message)

        return (type(data) is str)
    @staticmethod
    def FN_validation_int(data):
        if any(c.isalpha() for c in data)==False:
            return True
        else:
            return False

    @staticmethod
    def FN_isEmpty(data):
        if len(data) == 0 or data is None:
            return True
        else:
            return False

    def FN_validation_date(date):
        start = datetime.datetime.now()
        end = datetime.datetime.strptime("30-11-2030", "%d-%m-%Y")
        entry_date = datetime.datetime.strptime(date, "%d-%m-%Y")
        if start <= entry_date <= end:
            print("PASS!")
            return True
        else:
            QtWidgets.QMessageBox.warning("Error", "Invalid date format")

    def FN_validate_date1(date_text):
        try:
            datetime.datetime.strptime(date_text, '%d.%m.%Y')
            return  True
        except ValueError:
            raise ValueError("Incorrect data format, should be DD.MM.YYYY")

if __name__ == '__main__':
    data=CL_validation()
    print(data.FN_valedation_mail("shymaa.helal@gmail.com123"))