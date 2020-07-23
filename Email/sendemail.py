from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import json
import smtplib


def get_email_from_mail_list(name_co_worker):
    """Return email from coworker"""
    with open('mail_list.json', 'rb') as mailing_list:
        emails = json.load(mailing_list)
    email_co_worker = emails[name_co_worker]
    return email_co_worker


def change_shift_different_day(current_shift, new_shift, current_date, new_date, name_co_worker):
    """Create and send standard email to change shift with a co-worker"""
    mail_co_worker = get_email_from_mail_list(name_co_worker.lower())
    msg = MIMEMultipart()
    msg['To'] = 'thom@live.nl'
    msg['From'] = 'thom@live.nl'
    msg['cc'] = [mail_co_worker]
    password = #enter password
    msg['Subject'] = 'Dienst Ruilen'
    body = '<font face="Consolas, Courier, monospace">' + f"""
    Beste J, <br><br>

    Graag wil ik van dienst ruilen met {name_co_worker} op {current_date}. <br>
    Dit betekent dat ik dienst {new_shift} zal draaien op {new_date} en {name_co_worker} dienst {current_shift} op {new_date}.<br><br>
    Bedankt voor het aanpassen!<br><br><br>

    Met vriendelijke groet,<br>
    T. Suijkerbuijk
    """ + '</font>'

    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


def vacation_day(vacation):
    """Create and send standard email to ask for vacation day(s)"""
    msg = MIMEMultipart()
    msg['To'] = 'thom@live.nl'
    msg['From'] = 'thom@live.nl'
    password = # enter password
    msg['Subject'] = 'Dienst Ruilen'
    body = '<font face="Consolas, Courier, monospace">' + f"""
        Beste J., <br><br>

        Graag wil ik op de volgende dag(en) vrij zijn: {vacation}. <br>
        Graag hoor ik of je akkoord bent met deze dag(en).<br><br><br>

        Met vriendelijke groet,<br>
        T. Suijkerbuijk
        """ + '</font>'

    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
