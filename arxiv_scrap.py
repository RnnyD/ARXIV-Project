import requests                 #APPORT DE LA LIBRAIRIE REQUESTS
from bs4 import BeautifulSoup   #APPORT DE LA LIBRAIRIE BEAUTIFOULSOUP, PERMET D'INTERAGIR SUR LA PARTIE HTML
import json                     #APPORT DE LA LIBRAIRIE JSON, PERMETTANT DE FAIRE DES SAUVEGARDES DE FICHIER
import datetime                 #APPORT DE LA LIBRAIRIE DATETIME, PERMETTANT D'APPORTER DES FORMATS DE DATES ET FONCTIONS
import time                     #APPORT DE LA LIBRAIRIE TIME, PERMET DE POUVOIR FAIRE DES PAUSES ENTRE LES REQUETES


## PERMET DE SET LES PARAMETRE DE BASES NECESSAIRE A NOTRE CODE (PROVIENT DU SITE)
def get_page_content(start_index, start_date, end_date):
    url = "https://arxiv.org/search/advanced"
    params = {
        'advanced': '',
        'terms-0-operator': 'AND',
        'terms-0-term': 'artificial intelligence',
        'terms-0-field': 'all',
        'classification-physics_archives': 'all',
        'classification-include_cross_list': 'include',
        'date-filter_by': 'date_range',
        'date-from_date': start_date,   #PERMET DE FORMER LA DATE POUR NOTRE PLAGE DE RECHERCHE 
        'date-to_date': end_date,       #PERMET DE FORMER LA DATE POUR NOTRE PLAGE DE RECHERCHE 
        'date-date_type': 'submitted_date',
        'abstracts': 'show',
        'size': '200',          
        'order': '-announced_date_first',
        'start': start_index    #PERMET DE RENDRE L'INDEX DE PAGE DYNAMIQUE ET DONC PAGINER 
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, comme Gecko) Chrome/130.0.0.0 Safari/537.36'
    }

    response = requests.get(url, params=params, headers=headers)
    return response.content

## NOUS PERMET D'AVOIR LE NOMBRE TOTAL DE RESULTATS DE LA RECHERCHE FAITE 
def get_total_results(html_content):
    soup = BeautifulSoup(html_content, 'html.parser') #ANALYSE DE DU CONTENU HTML
    try:
        total_results_text = soup.find("h1", class_="title is-clearfix").get_text(strip=True)
        total_results = int(total_results_text.split()[3].replace(',', '')) 
        return total_results
    except (AttributeError, IndexError, ValueError):
        return 0  #LE 0 EST RETOURNER SI LE NOMBRE NE PEUT ETRE EXTRAIT (GESTION D'ERREURS)
    

## VA NOUS PERMETTRE D'EXTRAIRE TITRES, DATES, POUR EN SUITE FORMER UNE LISTE PUIS DICO
def extract_article_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all("li", class_="arxiv-result") #PERMET D'ALLER CHERCHER DANS LA BALISE(ENDROIT OU SE SITUE LES INFOS)
    
    extracted_data = []
    for article in articles:
        title_tag = article.find("p", class_="title is-5 mathjax")
        title = title_tag.get_text(strip=True) if title_tag else "No Title"

        link_tag = article.find("p", class_="list-title").a
        link = link_tag["href"] if link_tag else "No Link"

        date_text = article.find("p", class_="is-size-7").get_text().replace(",", "").strip().split(";")[0]
        date_text = date_text.replace("Submitted ", "")
        try:
            date_epoch = datetime.datetime.strptime(date_text, "%d %B %Y").timestamp()
        except ValueError:
            date_epoch = None 

        extracted_data.append({
            "title": title,
            "link": link,
            "date_epoch": date_epoch
        })

    return extracted_data

## PERMET DE SAUVEGARDER 
def save_to_json(data, filename="ARXIV_DATA.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Données sauvegardées dans {filename}")
    

##PERMET DE PASSER A L'ANNEE SUIVANTE LORSQU'ON ARRIVE A DECEMBRE
def get_next_year(year, month):
    if month == 12:
        return year + 1, 1
    return year, month + 1


## PERMET DE RECUPERER TOUT LES ARTICLES SUR UNE PERIODE ET GERER LA PAGINATION
def fetch_articles_for_period(start_date, end_date):
    start_index = 0
    all_articles = []

    first_page_content = get_page_content(start_index, start_date, end_date)
    total_results = get_total_results(first_page_content)
    print(f"Nombre total d'articles pour la période {start_date} à {end_date} : {total_results}")

    while start_index < total_results and start_index < 10000: #GESTION DE LA CONTRAINTE DES 10K ARTICLES
        print(f"Extraction des articles à partir de l'index {start_index}...")

        html_content = get_page_content(start_index, start_date, end_date)
        articles = extract_article_info(html_content)
        all_articles.extend(articles)

        start_index += 200  #POUR ALLER A LA PAGE SUIVANTE ON AJOUTE 200 A LA VARIABLE
        #time.sleep(1.5)    #AU CAS OU PERMET DE RALLONGER LE TEMPS ENTRE REQUETE POUR EVITER UN BANISSEMENT A NOUVEAU 😒

    return all_articles


## PERMET DE RECHERCHER LESS ARTICLES PAR MOIS DU 1ER AU 1ER 
def search_by_monthly_segments(start_year, end_year):
    all_articles = []
    
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            start_date = f"{year}-{month:02d}-01"
            next_year, next_month = get_next_year(year, month)
            end_date = f"{next_year}-{next_month:02d}-01"
            
            monthly_articles = fetch_articles_for_period(start_date, end_date)
            all_articles.extend(monthly_articles)

    save_to_json(all_articles)


## FONCTION PRINCIPALE 
def main(start_year, end_year):
    search_by_monthly_segments(start_year, end_year)

