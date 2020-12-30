import datetime
def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d-%m.%Y')
        print("suc")
    except ValueError:
        raise ValueError("Incorrect data format, should be DD-MM-YYYY")

validate('23.12.2020')
#validate('2003-12-32')