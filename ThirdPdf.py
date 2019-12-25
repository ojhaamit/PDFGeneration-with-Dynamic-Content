import time
from tkinter import messagebox
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import FourthPdf
import sqlite3

def g_letter():
    #Create Database Connection
    conn = sqlite3.connect("letters.db")
    cursor = conn.cursor()

    fdata = []
    cursor.execute("""SELECT * FROM lvariables""")
    fdata = cursor.fetchall()
    #Commit the connection
    conn.commit()

    #Close the connection:
    conn.close()

    print(fdata)
    print(len(fdata))

    for i in range(len(fdata)):

        doc = SimpleDocTemplate("form_letter_%s.pdf" % str(fdata[i][0]), pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        Content = []
        logo = "LogoMakr.png"
        amount_due = fdata[i][9]
        due_date = "01/01/2020"

        formatted_time = time.ctime()
        full_name = str(fdata[i][1]) + " " + str(fdata[i][2])
        address = []
        for add in range(len(fdata)):
            address.append(str(fdata[add][3]) + " " + str(fdata[add][4]) + "," + str(fdata[add][5]) + " " + str(fdata[add][6]) + " " + str(fdata[add][7]))

        print(address)
        my_image = Image(logo, 2*inch, 2*inch)
        Content.append(my_image)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        ptext = '<font size=10>%s</font>' % formatted_time

        Content.append(Paragraph(ptext, styles["Normal"]))
        Content.append(Spacer(1, 10))

        ptext = '<font size=10>%s</font>' % full_name
        Content.append(Paragraph(ptext, styles["Normal"]))
        for part in address:
            ptext = '<font size=10>%s</font>' % part.strip(",")
            Content.append(Paragraph(ptext, styles["Normal"]))

        Content.append(Spacer(1, 10))
        ptext = '<font size=10>Dear %s:</font>' % full_name.split()[0].strip()
        Content.append(Paragraph(ptext, styles["Normal"]))
        Content.append(Spacer(1, 10))

        ptext = '<font size=10>Your bill for current month is due for the amount %s.\
                Please pay by %s for availing uninterrupted services.</font>' % (amount_due, due_date)

        Content.append(Paragraph(ptext, styles["Justify"]))
        Content.append(Spacer(1, 10))

        ptext = '<font size=10>Thank you very much and we look forward to serving you.</font>'
        Content.append(Paragraph(ptext, styles["Justify"]))
        Content.append(Spacer(1, 10))
        ptext = '<font size=10>Sincerely,</font>'
        Content.append(Paragraph(ptext, styles["Normal"]))
        ptext = '<font size=10>Test PDF</font>'
        Content.append(Paragraph(ptext, styles["Normal"]))
        Content.append(Spacer(1, 10))
        doc.build(Content)

    messagebox.showinfo("Alert", "PDF Generated!")