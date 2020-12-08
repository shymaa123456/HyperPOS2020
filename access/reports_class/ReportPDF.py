import mysql

from access.reports_class.WeasypayPDFFile import FooterCanvas, Foo

from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Spacer
from reportlab.platypus import Table, LongTable
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.pagesizes import LETTER, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pandas as pd

from mysql.connector import Error

import mysql.connector

from reportlab.lib import colors

from reportlab.graphics.shapes import Drawing, Line
import arabic_reshaper

from bidi.algorithm import get_display
from Validation.Validation import CL_validation

name = "done"
foot = "text"
fontname = ''
fontsize = 0
code = ""
watermark = ""
branch = ""
tel = ""
query = ""
cursortest = 0


class Text():
    def setCursor(self, cursor):
        global cursortest
        cursortest = cursor

    def getcursor(self):
        return cursortest

    def setName(self, title):
        global name
        name = title

    def getName(self):
        return name

    def setFooter(self, footer):
        global foot
        foot = footer

    def getFooter(self):
        return foot

    def setFont(self, font):
        global fontname
        fontname = font

    def getFont(self):
        return fontname

    def setFontsize(self, font):
        global fontsize
        fontsize = font

    def getFontsize(self):
        return fontsize

    def setcodeText(self, codeText):
        global code
        code = codeText

    def getcodeText(self):
        return code

    def setwaterText(self, waterText):
        global watermark
        watermark = waterText

    def getwaterText(self):
        return watermark

    def setbrachText(self, waterText):
        global branch
        branch = waterText

    def getbrachText(self):
        return branch

    def settelText(self, waterText):
        global tel
        tel = waterText

    def gettelText(self):
        return tel

    def setQuery(self, waterText):
        global query
        query = waterText

    def getQuery(self):
        return query


class body():
    def __init__(self):
        title = Text()
        val = CL_validation()
        pdfmetrics.registerFont(TTFont('Scheherazade', 'Scheherazade-Regular.ttf'))
        data = [['Nubmber reset:', '248361 5/1/2018', '                                      ', '', 'Client Data'],
                ['phone number:', title.gettelText(), '                           ', title.getcodeText(),
                 'Customer Code'],
                ['mobile number', title.gettelText(), '                             ', 'TEST', 'Customer Name'],
                ['', '', '                                ', 'Giza', 'City']]
        f = Table(data, repeatRows=1, repeatCols=1, hAlign='CENTER')

        d = Drawing(100, 5)
        d.add(Line(16, 6, 500, 6))

        # sqlEngine = create_engine('mysql+pymysql://root:@127.0.0.1', pool_recycle=3600)
        # dbConnection = sqlEngine.connect()
        connection = mysql.connector.connect(host='localhost', database='Hyper1_Retail'
                                             , user='root', port='3306')
        # frame = pd.read_sql("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID` AND `PROMOTION_DETAIL`.`PROM_STATUS`='3' JOIN `PROM_BRANCH` ON `PROM_BRANCH`.`BRANCH_NO`=(SELECT `BRANCH`.`BRANCH_NO` FROM `BRANCH` WHERE `BRANCH`.`BRANCH_DESC_A`='zayed')", connection)
        frame = pd.read_sql(str(title.getQuery()), connection)
        df = pd.DataFrame(frame,
                          columns=['PROM_ID', 'PROM_TYPE_ID', 'PROM_CREATED_BY', 'PROM_CREATED_BY', 'PROM_CREATED_ON',
                                   'PROM_LINE_NO'])

        # df = pd.DataFrame(cursortest.fetchall())
        # df.columns = cursortest.keys()

        df = df.reset_index()
        df = df.rename(columns={"index": ""})

        z = df.size
        print(z)
        row, col = df.shape
        df['PROM_ID'] = df['PROM_ID'].str.wrap(60)
        total = 0
        numCount = 0
        for x in range(row):
            val = df['PROM_ID'].values[x]
            arabic_text = arabic_reshaper.reshape(val)
            arabic_text = get_display(arabic_text)
            df.at[x, 'PROM_ID'] = arabic_text
            numCount += 1
        num = 0
        for x in range(row):
            val = df['PROM_ID'].values[x]
            total += int(val)
            num = x

        df.sort_values(by=['PROM_ID'], inplace=True)

        df.at[num + 2, 'PROM_ID'] = str(total)
        df.at[num + 2, 'PROM_ID'] = str(numCount)
        df.at[num + 2, 'PROM_ID'] = str(numCount)

        data = [df.columns.to_list()] + df.values.tolist()

        table = Table(data, repeatRows=1, repeatCols=1,
                      rowHeights=20, hAlign='CENTER')

        table.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.2, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.2, colors.black),
            ('LINEBELOW', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Scheherazade'),
            ('GRID', (0, 0), (-1, -1), 0.01 * inch, (0, 0, 0,)),
            ('FONTSIZE', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONT', (0, 0), (-1, 0), 'Times-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 6),
            ('FONT', (0, -1), (-1, -1), 'Times-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 10)

        ]))
        genStr = "Total LienceNumber: " + str(total)

        styles = getSampleStyleSheet()
        elements = []
        elements.append(f)
        elements.append(d)
        elements.append(table)
        elements.append(Spacer(20, 20))
        elements.append(Paragraph(genStr))

        elements.append(PageBreak())
        # elements.append(Paragraph("", styles["Normal"]))
        # Build
        foo = Foo()  # init Foo class and call its function
        foo.foo_func(title.getName())
        foo.setFooter(title.getFooter())
        foo.setFont(title.getFont())
        foo.setFontsize(title.getFontsize())
        foo.setcodeText(title.getcodeText())
        foo.setwaterText(title.getwaterText())
        foo.settelText(title.gettelText())
        foo.setbrachText(title.getbrachText())
        p = FooterCanvas
        doc = SimpleDocTemplate("my_file.pdf", pagesize=A4, rightMargin=30, leftMargin=30, topMargin=100)
        doc.multiBuild(elements, canvasmaker=p)
