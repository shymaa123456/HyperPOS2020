from IPython.external.qt_for_kernel import QtGui
from appdirs import unicode
from pandas.tests.io.excel.test_xlrd import xlrd, xlwt

from access.reports_class.ReportPDF import body,Text
from Validation.Validation import CL_validation
title=Text()
title.setName("Invoice")
title.setFooter(" س ت 36108 ملف  ضريبي 212/306/5 مأموريه  ضرائب الشركات المساهمة رقم التسجيل بضرائب المبيعات 153/846/310 ")
title.setFont('Scheherazade-Regular.ttf')
title.setFontsize(10)
title.setcodeText("15235692356562")
title.setwaterText("hyperone company")
title.settelText("1266533")
title.setbrachText("Entrance 1,EL Sheikh Zayed City")

import xlwings as xw
import pandas as pd
import numpy as np

# Open a template file
wb = xw.Book('mytemplate.xlsx')

# Sample DataFrame
df = pd.DataFrame(np.random.randn(5, 4), columns=['one', 'two', 'three', 'four'],
                  index=['a', 'b', 'c', 'd', 'e'])

# Assign data to cells
wb.sheets[0]['A1'].value = 'My Report'
wb.sheets[0]['A3'].value = df

# Save under a new file name
wb.save('myreport.xlsx')


body()