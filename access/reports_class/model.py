import re

from access.reports_class.ReportPDF import body, Text

title = Text()
title.setName("Invoice")
title.setFooter(
    " س ت 36108 ملف  ضريبي 212/306/5 مأموريه  ضرائب الشركات المساهمة رقم التسجيل بضرائب المبيعات 153/846/310 ")
title.setFont('Scheherazade-Regular.ttf')
title.setFontsize(10)
title.setcodeText("15235692356562")
title.setwaterText("hyperone company")
title.settelText("1266533")
title.setbrachText("Entrance 1,EL Sheikh Zayed City")

title.setQuery("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID` JOIN `promotion_group` ON `PROMOTION_GROUP`.`CG_GROUP_ID`=(SELECT `CUSTOMER_GROUP`.`CG_GROUP_ID` FROM `CUSTOMER_GROUP` WHERE `CUSTOMER_GROUP`.`CG_DESC`='Gp11')")

body()
# from access.reports_class.reporting import CL_report
#
# window_two = CL_report()
# window_two.show()


