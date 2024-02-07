## Introduction
Cverer is a Web based solution, developped to help candidates to optimize their resume or cover letters and also analyse Job market trends based on a Job role search query.
The Web app compare data from scraping the Job listing of the website https://www.rekrute.com/ and extracted of the user resume as Pdf, to give it finally as input to the OpenAI API to generate insights, optimizations and suggestions to send it to the user as an attachement file via his mail inbox.

## Installation
For the local direct installation:

1-Install the libraries included in the requirements.txt file 
```bash
pip install -r requirements.txt
```
2- If you're using Windows, ensure that you have WSL installed and configured on your system. You can find instructions for installing WSL here: [WSL Installation Guide](https://docs.microsoft.com/en-us/windows/wsl/install) Or go to the Microsoft Store and install Ubuntu 

3- Run the rq worker on the wsl
```bash
rq worker
```

4- You Need Three APIs, two for free and one paid:\n
Free:
-[ConvertApi](https://www.convertapi.com/) to convert the generated text analysis to a PDF file. It is used in the main app.py and api_cv.py files.
-[Brevo](https://www.brevo.com/fr/lp/smtp/) (Optional) to send results by mail, you can always send it by login to your user mail by password and use the default port 597. It is used in app.py and api_cv.py file.
Paid:
-[OpenAI](https://openai.com/) to analyse and generate text use the GPT 4 TURBO Model. It is used in the api_cv.py file.



5- Run the app.py
```bash
python app.py
```






