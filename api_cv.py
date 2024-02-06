from openai import OpenAI
import re
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import convertapi
from rekrute import get_results, get_details, extract_text_from_csv

convertapi.api_secret = 'tkHjgzt6QVQJjNSr'


def compare_data(resume_data, keyword, to_email):
    links, titles = get_results(keyword) 
    if len(links) > 10:
        links = links[:10]
    job_details = get_details(links)
    job_details = extract_text_from_csv(job_details)
    client = OpenAI(api_key= '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')

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": "You are an RH manager your manager will provide you by job listings details in first input and follow it by a candidate resume data, you need to tell him if the candidate is fit for the job or no like a score on 10,  what the candidate must optimize in his resume so that it meets the requirements and job details input to enhace his chances to land those jobs, give certifications to add or any other useful suggestions. Make sure to do you analytics on the average of the job listings and not on a specific job title."
            },
            {
                "role": "user",
                "content": "Job details are : " + ', '.join(map(str, job_details)) + "\n\n\n Resume data are : " + ', '.join(map(str, resume_data))
            },
        ],
        temperature=0.7,
        max_tokens=4096,
        top_p=0.9,
        frequency_penalty=0.2,
        presence_penalty=0.1
    )
    
    with open('static/uploads/analyse.txt', 'w') as file:
        file.write(response.choices[0].message.content)

    
    result = convertapi.convert('pdf', {'File': 'static/uploads/analyse.txt'})
    output_pdf_file = 'static/uploads/cv_optimz.pdf'
    result.file.save(output_pdf_file)
    os.remove('static/uploads/analyse.txt')

    
    msg = MIMEMultipart()
    msg['From'] = 'taha.ferhan@hotmail.com'
    msg['To'] = to_email
    msg['Subject'] = 'Cverer - Resume Optimization'
    body = 'Please find attached the Resume optimization.'
    msg.attach(MIMEText(body, 'plain'))

    with open(output_pdf_file, 'rb') as file:
        attach = MIMEBase('application', 'octet-stream')
        attach.set_payload(file.read())
        encoders.encode_base64(attach)
        attach.add_header('Content-Disposition', 'attachment', filename=str(output_pdf_file))
        msg.attach(attach)
    
    server = smtplib.SMTP('smtp-relay.brevo.com', 587)
    server.starttls()
    server.login('taha.ferhan@hotmail.com', '52STO3wEm8FWBL6c')
    text = msg.as_string()
    server.sendmail('taha.ferhan@hotmail.com', to_email, text)
    server.quit()

def parse_string(input_string):
    
    sections = re.split(r'\*\*(.*?)\*\*', input_string)

    parsed_string = {}

    for i in range(1, len(sections), 2):
        # The title is the current section and the content is the next section
        title = sections[i].strip()
        content = sections[i+1].strip()

        # Add the title and content to the dictionary
        parsed_string[title] = content

    return parsed_string


def job_market_resumer(keyword, to_email):
    links, titles = get_results(keyword) 
    if len(links) > 10:
        links = links[:10]
    job_details = get_details(links)
    job_details = extract_text_from_csv(job_details)
    client = OpenAI(api_key= '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')

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages= [
            {
            "role": "system",
            "content": "You are the best RH manager in town, they have organized a championship that involve best 100RH managers in the world, you are the only one who can win this championship, you need to provide a job market summary to your manager, the summary must include the average of the job listings and not on a specific job title, give certifications that is required on the jobs listing and be unique because those 99 other RH managers will provide the same summary, you need to be the best and win this championship."},
            {
            "role": "user",
            "content": "Job details are : " + ', '.join(map(str, job_details))
            }
        ],
        temperature=0.7,
        max_tokens=3000,
        top_p=0.9,
        frequency_penalty=0.2,
        presence_penalty=0.1
    )
    with open('static/uploads/analyse.txt', 'w') as file:
        file.write(response.choices[0].message.content)

    
    result = convertapi.convert('pdf', {'File': 'static/uploads/analyse.txt'})
    output_pdf_file = 'static/uploads/summary.pdf'
    result.file.save(output_pdf_file)
    os.remove('static/uploads/analyse.txt')

    
    msg = MIMEMultipart()
    msg['From'] = 'taha.ferhan@hotmail.com'
    msg['To'] = to_email
    msg['Subject'] = 'Cverer - Job Market Summary'
    body = 'Please find attached the job market summary.'
    msg.attach(MIMEText(body, 'plain'))

    with open(output_pdf_file, 'rb') as file:
        attach = MIMEBase('application', 'octet-stream')
        attach.set_payload(file.read())
        encoders.encode_base64(attach)
        attach.add_header('Content-Disposition', 'attachment', filename=str(output_pdf_file))
        msg.attach(attach)
    
    server = smtplib.SMTP('smtp-relay.brevo.com', 587)
    server.starttls()
    server.login('taha.ferhan@hotmail.com', '52STO3wEm8FWBL6c')
    text = msg.as_string()
    server.sendmail('taha.ferhan@hotmail.com', to_email, text)
    server.quit()


def compare_data_let(lettre_data, keyword, to_email):
    links, titles = get_results(keyword) 
    if len(links) > 10:
        links = links[:10]
    job_details = get_details(links)
    job_details = extract_text_from_csv(job_details)
    client = OpenAI(api_key= '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')

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": "You are an RH manager your manager will provide you by job listings details in first input and follow it by a candidate cover letter data, you need to tell him if the candidate is fit for the job or no like a score on 10,  what the candidate must optimize in his cover letter so that it meets the requirements and job details input to enhace his chances to land those jobs, give advices on the langage used and what to focus on, and any experiences and motivations to include to add or any other useful suggestions. Make sure to do you analytics on the average of the job listings and not on a specific job title."
            },
            {
                "role": "user",
                "content": "Job details are : " + ', '.join(map(str, job_details)) + "\n\n\n Cover Letter data are : " + ', '.join(map(str, lettre_data))
            },
        ],
        temperature=0.7,
        max_tokens=4096,
        top_p=0.9,
        frequency_penalty=0.2,
        presence_penalty=0.1
    )
    
    with open('static/uploads/analyse.txt', 'w') as file:
        file.write(response.choices[0].message.content)

    
    result = convertapi.convert('pdf', {'File': 'static/uploads/analyse.txt'})
    output_pdf_file = 'static/uploads/let_optimz.pdf'
    result.file.save(output_pdf_file)
    os.remove('static/uploads/analyse.txt')

    
    msg = MIMEMultipart()
    msg['From'] = 'taha.ferhan@hotmail.com'
    msg['To'] = to_email
    msg['Subject'] = 'Cverer - Cover Letter Optimization'
    body = 'Please find attached the Cover letter optimization suggestions.'
    msg.attach(MIMEText(body, 'plain'))

    with open(output_pdf_file, 'rb') as file:
        attach = MIMEBase('application', 'octet-stream')
        attach.set_payload(file.read())
        encoders.encode_base64(attach)
        attach.add_header('Content-Disposition', 'attachment', filename=str(output_pdf_file))
        msg.attach(attach)
    
    server = smtplib.SMTP('smtp-relay.brevo.com', 587)
    server.starttls()
    server.login('taha.ferhan@hotmail.com', '52STO3wEm8FWBL6c')
    text = msg.as_string()
    server.sendmail('taha.ferhan@hotmail.com', to_email, text)
    server.quit()