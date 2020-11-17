
from WeasypayPDFFile import FooterCanvas,Foo

from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle,Spacer
from reportlab.platypus import Table,LongTable
from reportlab.lib.units import inch,cm,mm
from reportlab.lib.pagesizes import LETTER,A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pandas as pd
import numpy as np
import textwrap
import sys
from reportlab.lib import colors
from sqlalchemy import create_engine
import pymysql
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.eanbc import Ean13BarcodeWidget
from reportlab.graphics.shapes import Drawing,Line
from reportlab.platypus import Flowable
import arabic_reshaper
from fpdf import FPDF
from datetime import datetime
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
class Text():
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
class body():
    def __init__(self):
        title=Text()
        val= CL_validation()
        pdfmetrics.registerFont(TTFont('Scheherazade', 'Scheherazade-Regular.ttf'))
        data = [['Nubmber reset:', '248361 5/1/2018', '                                      ', '', 'Client Data'],
                ['phone number:', title.gettelText(), '                           ', title.getcodeText(), 'Customer Code'],
                ['mobile number', title.gettelText(), '                             ', 'TEST', 'Customer Name'],
                ['', '', '                                ', 'Giza', 'City']]
        f = Table(data, repeatRows=1, repeatCols=1, hAlign='CENTER')

        d = Drawing(100, 5)
        d.add(Line(16, 6, 500, 6))

        sqlEngine = create_engine('mysql+pymysql://habdelnaby:123P@ssword@10.2.1.190', pool_recycle=3600)
        dbConnection = sqlEngine.connect()
        frame = pd.read_sql("select * from Hyper1_Retail.PROMOTIONAL_VOUCHER", dbConnection)
        df = pd.DataFrame(frame, columns=['PROMV_VOUCHER_ID', 'PROMV_VOUCHER_DESC', 'PROMV_VOUCHER_VAL', 'PROMV_SERIAL_ID', 'PROMV_CREATED_BY','PrROMV_CHANGED_ON'])

        df = df.reset_index()
        df = df.rename(columns={"index": ""})

        z = df.size
        print(z)
        row, col = df.shape
        df['PROMV_SERIAL_ID'] = df['PROMV_SERIAL_ID'].str.wrap(60)
        total = 0
        numCount = 0
        for x in range(row):
            val = df['PROMV_SERIAL_ID'].values[x]
            arabic_text = arabic_reshaper.reshape(val)
            arabic_text = get_display(arabic_text)
            df.at[x, 'PROMV_SERIAL_ID'] = arabic_text
            numCount += 1
        num = 0
        for x in range(row):
            val = df['PROMV_SERIAL_ID'].values[x]
            total += int(val)
            num = x

        df.sort_values(by=['PROMV_SERIAL_ID'], inplace=True)

        df.at[num + 2, 'PROMV_SERIAL_ID'] = str(total)
        df.at[num + 2, 'PROMV_SERIAL_ID'] = str(numCount)
        df.at[num + 2, 'PROMV_SERIAL_ID'] = str(numCount)

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
            ('FONT', (0,-1), (-1,-1), 'Times-Bold'),
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
        # elements.append(Paragraph("", styles["Normal"]))
        # Build
        foo = Foo()# init Foo class and call its function
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
