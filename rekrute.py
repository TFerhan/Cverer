import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_results(keyword):
    headers = {
    'Content-Type': 'text/html; charset=UTF-8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'http://www.rekrute.com',}
    link = f'https://www.rekrute.com/offres.html?s=1&p=1&o=1&query={keyword}&keyword={keyword}&st=d&jobLocation=RK'
    res = requests.get(link, headers = headers)
    
    if res.status_code == 200:
        print(link)
        
        nor = BeautifulSoup(res.text, features = 'lxml')
        links = []
        titres = []
        sections = nor.find('div', class_ = 'pagination').find('div', class_ = 'section').find('span', class_ = 'jobs').find_all('option')
        for i in range(len(sections)):
            response = requests.get(f'https://www.rekrute.com/offres.html?s=1&p={i+1}&o=1&query={keyword}&keyword={keyword}&st=d&jobLocation=RK', headers = headers)
            print(response.status_code)
            if response.status_code == 200:
                bs = BeautifulSoup(response.text, features = 'lxml')
                offers = bs.find('ul', class_ = 'job-list job-list2').find_all('li', class_ = 'post-id')
                for offer in offers:
                    n = offer.find('a', class_ = 'titreJob')
                    j = n.attrs['href']
                    links.append(f'https://www.rekrute.com{j}')
                    titres.append(n.get_text().strip())
        return links, titres
    else:
        print(res.status_code)
        return 0, 0
    

def get_details(links):
    headers = {
    'Content-Type': 'text/html; charset=UTF-8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'http://www.rekrute.com',}
    dfs = []  # List to store individual DataFrames for each iteration
    require = pd.DataFrame(columns=['Job Title', 'Fields', 'Experience', 'Region', 'Diplome', 'Traits', 'Contrats', 'Date Pub', 'Deadline', 'Enteprise', 'Poste', 'Profil'])
    for link in links:
        response = requests.get(link, headers = headers)
        if response.status_code == 200:
            ts = BeautifulSoup(response.text, features = 'lxml')
            details = ts.find('div', class_ = 'listWrpService jobdetail')
            if details:
                job_title = job_title = details.find('h1').get_text().strip()
                job_sector = details.find('h2').get_text().strip()
                sectors_list = [sector.strip() for sector in job_sector.split('-')]
                sectors_list = [sector for sector in sectors_list if sector]
                sectors_list = ', '.join(sectors_list)
                det_v = details.find_all('ul', class_ ='featureInfo')[0].find_all('li')
                forp = []
                for det in det_v:
                    exp = det.get_text().split()
                    forp.append(exp)
                forp = [' '.join(item) for item in forp]
                person = details.find('div', class_ = 'col-md-12 blc').find_all('span')
                person = [p.get_text().split() for p in person]
                person = [' '.join(item) for item in person]
                person = ', '.join(person)
                det_j = details.find_all('ul', class_ ='featureInfo')[1].find_all('li')
                contrats = []
                for contr in det_j:
                    con = contr.get_text().split()
                    contrats.append(con)
                contrats = [' '.join(item) for item in contrats]
                contrats = ', '.join(contrats)
                pub = ts.find('span', class_ = 'newjob')
                posting_date = pub.find('i', class_='fa-calendar').next_sibling.strip()
                deadline = pub.find('b').get_text(strip=True)
            recru_details = ts.find('div', id = 'recruiterDescription')
            paragraphs = recru_details.find_all('p')
            intro = ' '.join([paragraph.get_text(strip=True) for paragraph in paragraphs])
            poste = ts.find_all('div', class_ = 'col-md-12 blc')
            for p in poste:
                h2 = p.find('h2')
                if h2 and h2.get_text() == 'Poste :' :
                    parags = p.find_all('p')
                    pos = ' '.join([parag.get_text(strip = True) for parag in parags])
                    break
            profil = ts.find_all('div', class_ = 'col-md-12 blc')
            for m in profil:
                h2 = m.find('h2')
                if h2 and h2.get_text() == 'Profil recherché :' :
                    parags = m.find_all('p')
                    prof = ' '.join([parag.get_text(strip = True) for parag in parags])
                    break
            job_data = pd.DataFrame({'Job Title': [job_title], 'Fields': [sectors_list], 'Experience': [forp[0]],
                                      'Region': [forp[1]], 'Diplome': [forp[2]], 'Traits': [person], 'Contrats': [contrats],
                                      'Date Pub': [posting_date], 'Deadline': [deadline], 'Enteprise': [intro],
                                      'Poste': [pos], 'Profil': [prof]})
            dfs.append(job_data)
        else:
            print(response.status_code)
    require = pd.concat(dfs, ignore_index=True)
    return require
        
def extract_text_from_csv(df):
    job_descriptions = []
    for index, row in df.iterrows():
        row_text = ', '.join(f"{column}: {value}" for column, value in row.items())
        job_descriptions.append(row_text)

    return job_descriptions




