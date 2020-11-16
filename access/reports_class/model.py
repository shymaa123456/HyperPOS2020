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

body()