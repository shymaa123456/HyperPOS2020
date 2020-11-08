import re
import datetime
from PyQt5 import QtWidgets
class  CL_validation():
    email_address = "hossam.nabi.cs@gmail.com"

    @staticmethod
    def FN_valedation_mail(email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            QtWidgets.QMessageBox.warning(  "Error", "address is valid" )

            print("")
        else:
            print("not valid")

    @staticmethod
    def FN_validation_password(password):
        while True:
            if len(password) < 8:
                QtWidgets.QMessageBox.warning( "Error", "Make sure your password is at lest 8 letters" )

                break
            elif re.search('[0-9]', password) is None:
                QtWidgets.QMessageBox.warning(  "Error", "Make sure your password has a number in it" )

                break
            elif re.search('[A-Z]', password) is None:
                QtWidgets.QMessageBox.warning( "Error", "Make sure your password has a capital letter in it" )

                break
            else:
                print("Your password seems fine")
                break

    @staticmethod
    def FN_validation_mobile( mobile):
        number = re.compile(r'[^0-9]').sub('', mobile)
        if len(number) != 11:
            QtWidgets.QMessageBox.warning(  "Error", "Invalid mobile n0,len must be = 11" )
        else:
            if (mobile.startswith( '01' )):
                print( mobile.startswith( '01' ) )
            else:
                QtWidgets.QMessageBox.warning( "Error", "Invalid mobile no,no must start with '01'" )



    def FN_validation_type(self,data):
        print(type(data))

    def FN_isEmpty(self,data):
        if len(data)==0 or data is None:
            return True
        else:
            return False

    def FN_validation_date(date):
        start = datetime.datetime.now()
        end = datetime.datetime.strptime("30-11-2030", "%d-%m-%Y")
        entry_date= datetime.datetime.strptime(date, "%d-%m-%Y")
        if start <= entry_date <= end:
            print("PASS!")
        else:
            QtWidgets.QMessageBox.warning(  "Error", "Invalid date format" )


if __name__ == '__main__':

    CL_validation.FN_valedation_mail("ttt@gg.com")


