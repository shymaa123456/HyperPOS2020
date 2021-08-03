# import urllib.request
# def connect():
#     try:
#         urllib.request.urlopen('http://google.com') #Python 3.x
#         return True
#     except:
#         return False
# print( 'connected' if connect() else 'no internet!' )



# from pythonping import ping
#
# ping('192.168.1.2', verbose=True)


# import os
# from time import sleep
#
# def add():
#     print("in add function")
#
# def sub():
#     print("in subtract function")
#
# def ping():
#     online = os.system("ping -n 1 192.168.1.86")
#     if(online == 0):
#          print("Avilabe with ",online)
#          return True
#     else:
#          print("Ofline with ",online)
#          return False
#
# while True:
#    add()
#    sleep(0.5)
#    if( ping()):
#          sub()
#    sleep(0.5)


import os
ping = os.system('ping 192.168.1.86')
if ping == 0:
 print ('up')
else:
 print('down')