import re

from access.reports_class.ReportPDF import body, Text

# title = Text()
# title.setName("Invoice")
# title.setFooter(
#     " س ت 36108 ملف  ضريبي 212/306/5 مأموريه  ضرائب الشركات المساهمة رقم التسجيل بضرائب المبيعات 153/846/310 ")
# title.setFont('Scheherazade-Regular.ttf')
# title.setFontsize(10)
# title.setcodeText("15235692356562")
# title.setwaterText("hyperone company")
# title.settelText("1266533")
# title.setbrachText("Entrance 1,EL Sheikh Zayed City")
#
# title.setQuery("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID` JOIN `promotion_group` ON `PROMOTION_GROUP`.`CG_GROUP_ID`=(SELECT `CUSTOMER_GROUP`.`CG_GROUP_ID` FROM `CUSTOMER_GROUP` WHERE `CUSTOMER_GROUP`.`CG_DESC`='Gp11')")
#
# body()
# from access.reports_class.reporting import CL_report
#
# window_two = CL_report()
# window_two.show()
from data_connection.h1pos import db1

conn = db1.connect()

mycursor = conn.cursor()
sql = "update COUPON set COP_STATUS='"+str(0)+"' where COP_ID='"+str(1256)+"'"


mycursor.execute(sql)
db1.connectionCommit(conn)
mycursor.close()


#INSERT INTO COUPON (COP_ID, COP_DESC, COP_DISCOUNT_VAL, COP_DISCOUNT_PERCENT, COP_SERIAL_COUNT, COP_MULTI_USE, COP_MULTI_USE_COUNT, COP_CREATED_BY, COP_CREAED_ON, COP_CHANGED_BY, COP_CHANGED_ON, COP_VALID_FROM, COP_VALID_TO, COP_STATUS) VALUES ( %s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s)  ('2', 'd', 'd', 'd', 'd', '1', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd')
#INSERT INTO COUPON (COP_ID, COP_DESC, COP_DISCOUNT_VAL, COP_MULTI_USE, COP_MULTI_USE_COUNT, COP_CREATED_BY, COP_CREAED_ON, COP_CHANGED_BY, COP_CHANGED_ON, COP_VALID_FROM, COP_VALID_TO, COP_STATUS) VALUES ( %s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s )  ('55', 'kol', '5', '', '', '1', 'kol', 'admin', '2021-01-10-17:00-14', 'kol', 'kol', '2021-01-10-17:00-14', '2021-01-10-17:00-14', None)
#INSERT INTO COUPON (COP_ID, COP_DESC, COP_DISCOUNT_VAL, COP_MULTI_USE, COP_MULTI_USE_COUNT, COP_CREATED_BY, COP_CREAED_ON, COP_CHANGED_BY, COP_CHANGED_ON, COP_VALID_FROM, COP_VALID_TO, COP_STATUS) VALUES ( %s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s )  ('9333', 'do', '10', '', '', '1', '10', 'admin', '2021-01-10', 'do', 'do', '2021-01-10', '2021-01-10', None)
#INSERT INTO COUPON (COP_ID, COP_DESC, COP_DISCOUNT_VAL, COP_MULTI_USE, COP_MULTI_USE_COUNT, COP_CREATED_BY, COP_CREAED_ON, COP_CHANGED_BY, COP_CHANGED_ON, COP_VALID_FROM, COP_VALID_TO, COP_STATUS) VALUES ( %s, %s, %s, %s,%s, %s, %s,%s, %s, %s )  ('556', 'hoss', '5', '1', '10', 'admin', '2021-01-10', 'hoss', 'hoss', '2021-01-10', '2021-01-10', None)



#INSERT INTO COUPON (COP_ID, COP_DESC, , COP_SERIAL_COUNT,COP_MULTI_USE, COP_MULTI_USE_COUNT, COP_CREATED_BY, COP_CREAED_ON, COP_VALID_FROM, COP_VALID_TO, COP_STATUS) VALUES ( %s, %s, %s, %s,%s, %s, %s, %s, %s, %s , %s)  ('123456', 'edition', '1', '1', '1', '0', 'admin', '2021-01-10', '2021-01-10', '2021-01-10', 0)
