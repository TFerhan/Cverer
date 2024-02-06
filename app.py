from flask import Flask, render_template,request, flash, make_response, redirect, url_for
from forms import UploadPDFForm,KeywordAndActionForm
from random import sample
import json
from rekrute import get_results
from pdf_scp import extract_pdf_text
from api_cv import compare_data, job_market_resumer, compare_data_let
import convertapi
from redis import Redis
from rq import Queue
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib



app = Flask(__name__)
app.config['SECRET_KEY'] = 'WlUrPgXjHOL9OquLGcQ96yfoZOyNLfCYFV05NUQN9DE3Fb4tUcWW02s4pYySzeDj'

convertapi.api_secret = 'tkHjgzt6QVQJjNSr'

#r = Redis.from_url('<your-Redis-connection-url>')
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
q = Queue(connection=r)

@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    form = KeywordAndActionForm()
    
    if form.validate_on_submit():
        keyword = form.keyword.data
        action = form.action.data
        email = form.email.data
        if action == 'choose':
            flash('Please choose an action')
            return render_template('index.html', form=form)
        links, titles = get_results(keyword)
        if len(links) == 0:
            flash('No jobs found for this keyword. Please try another keyword.')
            return render_template('index.html', form=form)
        if len(titles) >= 5:
            titles = sample(titles, 5)
        if action == 'optimize':
            resp = make_response(redirect(url_for('upload_pdf', keyword=keyword)))
            resp.set_cookie('email', json.dumps(email), max_age=60*60*24*365*2)
            resp.set_cookie('titles', json.dumps(titles), max_age=60*60*24*365*2)
            return resp
        elif action == 'analyze':
            email = form.email.data
            q.empty()
            q.enqueue(job_market_resumer, keyword, email)
            return render_template('sent.html')
        elif action == 'lettre':
            resp = make_response(redirect(url_for('lettre', keyword=keyword)))
            resp.set_cookie('titles', json.dumps(titles), max_age=60*60*24*365*2)
            resp.set_cookie('email', json.dumps(email), max_age=60*60*24*365*2)
            return resp
    return render_template('index.html', form=form)



@app.route('/upload_pdf', methods=['GET', 'POST'])
def upload_pdf():
    form = UploadPDFForm()
    email = json.loads(request.cookies.get('email'))
    titles = json.loads(request.cookies.get('titles', '[])'))
    keyword = request.args.get('keyword')
    if form.validate_on_submit():
        file = form.file.data
        resume_data = extract_pdf_text(file)
        print(keyword)
        # cache.set('resume', resume_data, timeout=60*30) 
        file.save('static/uploads/' + file.filename)
        q.empty()
        q.enqueue(compare_data, resume_data, keyword, email)
        return render_template('sent.html')
    return render_template('resume.html', keyword=keyword, form = form, titles = titles)
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/lettre', methods=['GET', 'POST'])
def lettre():
    form = UploadPDFForm()
    email = json.loads(request.cookies.get('email'))
    titles = json.loads(request.cookies.get('titles', '[]'))
    keyword = request.args.get('keyword')
    if form.validate_on_submit():
        file = form.file.data
        lettre_data = extract_pdf_text(file)
        file.save('static/uploads/' + file.filename)
        q.empty()
        q.enqueue(compare_data_let, lettre_data, keyword, email)
        return render_template('sent.html')
    return render_template('lettre.html', keyword=keyword, form = form, titles=titles)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form.get('email')
        message = request.form.get('msg')

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = 'taha.ferhan@hotmail.com'
        msg['Subject'] = 'Cverer Contact'
        msg.attach(MIMEText(message, 'plain'))

        try:
            server = smtplib.SMTP('smtp-relay.brevo.com', 587)
            server.starttls()
            server.login('taha.ferhan@hotmail.com', '52STO3wEm8FWBL6c')
            text = msg.as_string()
            server.sendmail(email, 'taha.ferhan@hotmail.com', text)
            server.quit()

            flash('Your message has been sent successfully!')
        except Exception as e:
            flash('Error: ' + str(e))

        return redirect(url_for('contact'))

    return render_template('contact_us.html')


if __name__ == '__main__':

    app.run()
