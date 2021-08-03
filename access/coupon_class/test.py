# import win32ui
# import win32print
# import win32con
#
# INCH =500
#
# hDC = win32ui.CreateDC ()
# hDC.CreatePrinterDC (win32print.GetDefaultPrinter ())
# hDC.StartDoc ("Test doc")
# hDC.StartPage ()
# hDC.SetMapMode (win32con.MM_TWIPS)
# hDC.DrawText ("TEST", (0, INCH * -1, INCH * 8, INCH * -2), win32con.DT_CENTER)
# hDC.EndPage ()
# hDC.EndDoc ()


############################
import barcode
from barcode.writer import ImageWriter

def testEan():
    EAN = barcode.get_barcode_class('code128')
    ean = EAN(u'hp-123456789011', writer=ImageWriter())
    fullname = ean.save('my_ean13_barcode')

if __name__ == '__main__':
    testEan()

import win32print
import win32ui
from PIL import Image, ImageWin

#
# Constants for GetDeviceCaps
#
#
# HORZRES / VERTRES = printable area
#
HORZRES = 8
VERTRES = 10
#
# LOGPIXELS = dots per inch
#
LOGPIXELSX = 88
LOGPIXELSY = 90
#
# PHYSICALWIDTH/HEIGHT = total area
#
PHYSICALWIDTH = 50
PHYSICALHEIGHT = 40
#
# PHYSICALOFFSETX/Y = left / top margin
#
PHYSICALOFFSETX = 20
PHYSICALOFFSETY = 20

printer_name = win32print.GetDefaultPrinter ()
file_name = "my_ean13_barcode.png"

#
# You can only write a Device-independent bitmap
#  directly to a Windows device context; therefore
#  we need (for ease) to use the Python Imaging
#  Library to manipulate the image.
#
# Create a device context from a named printer
#  and assess the printable size of the paper.
#
hDC = win32ui.CreateDC ()
hDC.CreatePrinterDC (printer_name)
printable_area = hDC.GetDeviceCaps (HORZRES), hDC.GetDeviceCaps (VERTRES)
printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)
printer_margins = hDC.GetDeviceCaps (PHYSICALOFFSETX), hDC.GetDeviceCaps (PHYSICALOFFSETY)

#
# Open the image, rotate it if it's wider than
#  it is high, and work out how much to multiply
#  each pixel by to get it as big as possible on
#  the page without distorting.
#
bmp = Image.open (file_name)
if bmp.size[0] > bmp.size[1]:
  bmp = bmp.rotate (0)

ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
scale = min (ratios)

#
# Start the print job, and draw the bitmap to
#  the printer device at the scaled size.
#
hDC.StartDoc (file_name)
hDC.StartPage ()

dib = ImageWin.Dib (bmp)
scaled_width, scaled_height = [int (scale * i) for i in bmp.size]
x1 = int ((printer_size[0] - scaled_width) / 15)

y1 = int ((printer_size[1] - scaled_height) / 10)
x2 = x1 + scaled_width
y2 = y1 + scaled_height
dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))

hDC.EndPage ()
hDC.EndDoc ()
hDC.DeleteDC ()