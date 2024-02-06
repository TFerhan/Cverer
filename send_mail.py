import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json
import os
import convertapi

convertapi.api_secret = 'tkHjgzt6QVQJjNSr'

def send_email(to_email, lettre_results ):
    with open('static/uploads/analyse.txt', 'w') as file:
        file.write(json.dumps(lettre_results))
    result = convertapi.convert('pdf', {'File': 'static/uploads/analyse.txt'})
    output_pdf_file = 'static/uploads/lettre_optim.pdf'
    result.file.save(output_pdf_file)
    os.remove('static/uploads/analyse.txt')
    msg = MIMEMultipart()
    msg['From'] = 'carin.satham@gmail.com'
    msg['To'] = to_email
    msg['Subject'] = 'Cverer - Your Optimization Results'
    body = 'Please find attached the optimization results.'
    msg.attach(MIMEText(body, 'plain'))

    # Attach the PDF file
    with open(output_pdf_file, 'rb') as file:
        attach = MIMEBase('application', 'octet-stream')
        attach.set_payload(file.read())
        encoders.encode_base64(attach)
        attach.add_header('Content-Disposition', 'attachment', filename=str(output_pdf_file))
        msg.attach(attach)

    # Send the email
    server = smtplib.SMTP('smtp-relay.brevo.com', 587)
    server.starttls()
    server.login('taha.ferhan@hotmail.com', '52STO3wEm8FWBL6c')
    text = msg.as_string()
    server.sendmail('taha.ferhan@hotmail.com', to_email, text)
    server.quit()


