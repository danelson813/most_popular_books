import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import sqlite3

def get_url(i):
        url = f"https://books.toscrape.com/catalogue/page-{i+1}.html"
        return url

def fix_title(str):
    return str.replace(',', '-')


def get_connection(url):
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    books = soup.find_all('article')
    return books


def get_info(books: list):
    base = 'https://books.toscrape.com/catalogue/'
    for book in books:
        link = base + book.find('h3').a['href']
        title = book.find('h3').a['title']
        price = book.find('p', class_='price_color').text[2:]
        result_ = f"{fix_title(title)},{price},{link}"
        print_to_disk(result_)

       
def print_to_disk(result):
    with open('data.csv', 'a') as f:
        f.write(str(result)+ '\n')

def save_to_db(data):
    conn = sqlite3.connect(r'books.db')
    curr = conn.cursor()
    data.to_sql('books', conn, if_exists='replace', index=False)
   

def read_csvfile():
    return pd.read_csv('data.csv', names=['title', 'price', 'link'])


def main():
    results = []
    for i in range(50):
        url = get_url(i)
        books = get_connection(url)
        get_info(books)
    data = read_csvfile()
    data.to_csv('df.csv', index=False)
    save_to_db(data)  

if __name__ == '__main__':
    main()
