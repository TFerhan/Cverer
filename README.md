## Introduction
Cverer is a web-based solution developed to assist candidates in optimizing their resumes and cover letters. Additionally, it provides insights into job market trends based on job role search queries. The web app compares data scraped from job listings on [Rekrute](https://www.rekrute.com/) with information extracted from the user's resume PDF. This data is then used as input for the OpenAI API, which generates insights, optimizations, and suggestions. These are delivered to the user as an attachment via email.

## Installation

1-Install the libraries included in the requirements.txt file 
```bash
pip install -r requirements.txt
```
2- If you're using Windows, ensure that you have WSL installed and configured on your system. You can find instructions for installing WSL here: [WSL Installation Guide](https://docs.microsoft.com/en-us/windows/wsl/install) Or go to the Microsoft Store and install Ubuntu.

3- Run the rq worker on the wsl
```bash
rq worker
```

4- You Need Three APIs, two for free and one paid:

Free:

-[ConvertApi](https://www.convertapi.com/) to convert the generated text analysis to a PDF file. It is used in the main app.py and api_cv.py files.

-[Brevo](https://www.brevo.com/fr/lp/smtp/) (Optional) to send results by mail, you can always send it by login to your user mail by password and use the default port 597. It is used in app.py and api_cv.py file.

Paid:

-[OpenAI](https://openai.com/) to analyse and generate text use the GPT 4 TURBO Model. It is used in the api_cv.py file.

5- Run the app.py
```bash
python app.py
```

## Usage
1- Navigate to the main page (typically localhost:5000)

2- In the main page, scroll down and their will be a form to fill, where there is three fields, the first is for the search query , you can enter any keyword representing a Job role or a domain field (eq. Data analyst, cyber...). Second choose an option , to optimize your resume , cover lettter or analyse the job market. Finally, enter your email address to receive the results.

3- Your resume or cover letter must be in a PDF file format.

## Features
Redis is used with rq worker on the back-end to execute open ai functions, because this last one take >30s to be completed so the web browser will take too long to respond and the user may close or lost his connection and lost the results. I encoutered this solution while trying to deploy my app on Heroku and the browser took >30s to respond and the app crashed. I tried to work with celery but i encoutered difficulties.

Fine tunning the Open Ai API parameters (e.g temperature, top p...) was essential to return the best results after using some prompt engineering.

BeautifulSoup was used to scrap the Data and stored in panda's DataFrame.

Flask and Redis for the back-end.

Bootstrap, HTML, CSS for the front-end.


## Contact 
This project was created by :

- **Ferhan Taha**
  - LinkedIn: [Ferhan Taha on LinkedIn](https://www.linkedin.com/in/tferhan/)
  - Email: taha.ferhan@hotmail.com


Feel free to connect with us on LinkedIn to learn more about our skills and experiences!






