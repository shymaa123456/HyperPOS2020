import xlwt


# ----------------------------------------------------------------------
def main():
    """"""
    book = xlwt.Workbook()
    sheet1 = book.add_sheet("PySheet1")

    cols = ["A", "B", "C", "D", "E"]
    txt = "Row %s, Col %s"

    for num in range(5):
        #row = sheet1.row(num)
        for index, col in enumerate(cols):
            value = txt % (num + 1, col)
            #row.write(index, value)
            sheet1.write(num, index, value)
    book.save("test.xls")


# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()