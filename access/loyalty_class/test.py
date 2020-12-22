import re
def FN_validation_mobile(mobile):
    number = re.compile(r'[^0-9]').sub('', mobile)
    if len(number) != 11:
        return 1

    else:
        if (mobile.startswith('01')):
            print(mobile.startswith('01'))
            return True
        else:
            return 2

print (FN_validation_mobile ('01002890278'))
