from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import LETTER, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from datetime import datetime
from bidi.algorithm import get_display

foot = "text".encode('utf-8')
fontname = ''
fontsize = 0
name = "done"
code = ""
watermark = ""
branch = ""
tel = ""


class Foo():
    def foo_func(self, title):
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


class FooterCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_canvas(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_canvas(self, page_count):
        foo = Foo()  # init Foo class and call its function

        pdfmetrics.registerFont(TTFont('Scheherazade', foo.getFont()))
        self.setFont('Scheherazade', foo.getFontsize())
        page = "Page %s of %s" % (self._pageNumber, page_count)
        x = 128
        z = 550
        self.saveState()
        self.setStrokeColorRGB(0, 0, 0)
        self.setLineWidth(2)
        self.line(66, 60, LETTER[0] - 66, 60)

        self.drawString(LETTER[0] - x, 30, page)
        arabic_text = foo.getFooter()  ##" س ت 36108 ملف  ضريبي 212/306/5 مأموريه  ضرائب الشركات المساهمة رقم التسجيل بضرائب المبيعات 153/846/310 "
        arabic_text = arabic_reshaper.reshape(arabic_text)
        arabic_text = get_display(arabic_text)
        self.drawString(LETTER[0] - z, 45, arabic_text.encode('utf-8'))

        self.drawString(265, 810, str(foo.getName()))
        today = datetime.now()
        self.drawString(40, 790, today.strftime('%Y-%m-%d'))
        self.drawString(40, 780, foo.getbrachText())
        self.drawString(40, 770, "Tel : " + foo.gettelText())
        self.drawString(260, 770, foo.getcodeText())
        self.drawString(270, 760, "Copy")
        self.drawImage('hypertwo.png', 490, 800)
        self.drawString(480, 795, "Hyperone Company")
        self.drawString(490, 785, "Mehwar 26")
        self.drawString(450, 775, "Entrance 1,EL Sheikh Zayed City")
        self.line(50, 750, LETTER[0] - 66, 750)

        self.setFont("Courier", 50)
        self.setFillColorRGB(230 / 256, 230 / 256, 230 / 256)
        self.translate(500, 100)
        self.rotate(90)
        self.drawCentredString(420, 350, foo.getwaterText())
        self.drawCentredString(420, 150, foo.getwaterText())
        self.drawCentredString(420, 20, foo.getwaterText())

        self.restoreState()
