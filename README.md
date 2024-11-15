[![N|Solid](https://i.postimg.cc/TYt0MYZ5/brand-logo-primary-removebg-preview.png)](https://nodesource.com/products/nsolid)

## _SCRAPING d'articles_


**Qu'est ce que ARXIV ?**
Arxiv est un site d'archive sur une multitude de sujets scientifiques. On peut retrouver des articles sur le domaine de la physique, des mathématiques, de l'informatique, de la biologie quantitative, des statistiques, de l'ingénierie électrique, de l'ingénierie des systèmes et de l'économie.

**L'intérêt du programme ?**
Il va nous servir à récupérer des des informations sur des articles dans le domaine de l'informatique et plus précisément de l'intelligence artificielle. Cela nous permettra de faire une correlation avec d'autres données provenant d'autres sites.

### Program's Features 
- Itération dans le site ARXIV 
- Récupération des liens d'articles
- Récupération des titres, dates d'articles

### Bibliothèques 
```python
import requests
from bs4 import BeautifoulSoup
import json
import datetime
```
### Functions
```python
def get_page_content(start_index, start_date, end_date):
```
```python
def get_total_results(html_content):
```
```python
def save_to_json(data, filename="ARXIV_DATA.json"):
```
```python
def get_next_year(year, month):
```
```python
def fetch_articles_for_period(start_date, end_date):
```
```python
def search_by_monthly_segments(start_year, end_year):
```
```python
def search_by_monthly_segments(start_year, end_year):
```
```python
def main(start_year, end_year):
```

### Donnés voulues : 

```python
[
    {
        "title": "Titre de l'article",
        "link": "Lien de l'article",
        "date_epoch": "Date format EPOCH"
    }
]    
```

### Rendue Finale 

![N|Solid](https://i.postimg.cc/Fsbtjck5/Capture-d-cran-2024-11-15-105532.png)

##### **See Ya! ️👾**
