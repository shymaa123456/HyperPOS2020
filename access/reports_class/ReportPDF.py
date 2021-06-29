
from access.reports_class.WeasypayPDFFile import FooterCanvas,Foo

from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle,Spacer
from reportlab.platypus import Table,LongTable
from reportlab.lib.units import inch,cm,mm
from reportlab.lib.pagesizes import LETTER,A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pandas as pd
from data_connection.h1pos import db1

from reportlab.lib import colors

from reportlab.graphics.shapes import Drawing,Line
import arabic_reshaper

from bidi.algorithm import get_display
from Validation.Validation import CL_validation

name="done"
foot="text"
fontname=''
fontsize=0
code=""
watermark=""
branch=""
tel=""
query=""
cursortest=0
field_names = []

class Text():
    def setCursor(self,cursor):
        global cursortest
        cursortest=cursor
    def getcursor(self):
        return cursortest
    def setName(self,title):
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

    def setCursor(self, col_names):
        global field_names
        field_names = col_names
    def getCursor(self):
        return field_names

class body():
    def __init__(self):
        title=Text()
        val= CL_validation()
        pdfmetrics.registerFont(TTFont('Scheherazade', 'Scheherazade-Regular.ttf'))
        data = [['Nubmber reset:', '248361 5/1/2018', '                                      ', 'Client Data', ''],
                ['phone number:', title.gettelText(), '                           ', 'Customer Code', title.getcodeText()],
                ['mobile number', title.gettelText(), '                             ', 'Customer Name', 'TEST'],
                ['', '', '                                ', 'City', 'Giza']]
        f = Table(data, repeatRows=1, repeatCols=1, hAlign='CENTER')
        d = Drawing(100, 5)
        d.add(Line(16, 6, 500, 6))
        connection = db1.connect()
        frame = pd.read_sql(str(title.getQuery()), connection)

        df = pd.DataFrame(frame, columns= field_names)
        # ['PROM_ID', 'PROM_TYPE_ID', 'PROM_CREATED_BY', 'PROM_CREATED_BY', 'PROM_CREATED_ON','PROM_LINE_NO'])
        df = df.reset_index()
        df = df.rename(columns={"index": "ID"})

        z = df.size
        print(z)
        row, col = df.shape
       # df['PROM_ID'] = df['PROM_ID'].str.wrap(60)
        total = 0
        # numCount = 0
        for y in range(col):
            for x in range(row):
                val = df.iloc[:, y].values[x]
                print(type(val))
                if type(val) == str:

                    arabic_text = arabic_reshaper.reshape(val)
                    arabic_text = get_display(arabic_text)
                    df.iloc[x, y] = arabic_text
        #     numCount += 1
        num = 0
        for x in range(row):
            val = df[field_names[0]].values[x]
            total += int(val)
            num = x
        df.sort_values(by=field_names[0], inplace=True)
        df.at[num + 2, field_names[0]] = str(total)

        col_lst = df.columns.to_list()
        for i in range(1, len(col_lst)):
            arabic_text = arabic_reshaper.reshape(col_lst[i])
            arabic_text = get_display(arabic_text)
            col_lst[i] = arabic_text
        data = [col_lst] + df.values.tolist()

        # data = [df.columns.to_list()] + df.values.tolist()
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
            ('FONT', (0, 0), (-1, 0), 'Scheherazade'),
            ('FONTSIZE', (0, 0), (-1, 0), 6),
            ('FONT', (0,-1), (-1,-1), 'Scheherazade'),
            ('FONTSIZE', (0,-1), (-1,-1), 10)

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

        foo = Foo()
        foo.foo_func(title.getName())
        foo.setFooter(title.getFooter())
        foo.setFont(title.getFont())
        foo.setFontsize(title.getFontsize())
        foo.setcodeText(title.getcodeText())
        foo.setwaterText(title.getwaterText())
        foo.settelText(title.gettelText())
        foo.setbrachText(title.getbrachText())
        p = FooterCanvas
        size=210/len(field_names)
        print(len(field_names))
        print(size)
        doc = SimpleDocTemplate("my_file.pdf", pagesize=A4, rightMargin=50, leftMargin=50, topMargin=100)
        doc.multiBuild(elements, canvasmaker=p)
