import requests
import psycopg2
import os
from bs4 import BeautifulSoup

def html_table_to_python(url):

    page_content = requests.get(url).text
    soup = BeautifulSoup(page_content, 'html.parser')

    page_table = soup.find('table')

    # Make a list of the keys from header to be zipped with dict
    keys = []
    for th in page_table.find_all('th'):
        keys.append(th.text)

    table = []
    for row in page_table.find_all('tr'):
        vals = []
        for td in row.find_all('td'):
            vals.append(td.text)
        row_dict = dict(zip(keys, vals))
        if row_dict:
            table.append(row_dict)

    return table

def refactor_table(table, verbose=False):
    """takes the star trek table and modifies it to my liking"""
    new_table = []

    #Fill series value
    for row in table:
        match row['series']:
            case 'TOS':
                series = 1
            case 'TNG':
                series = 2
            case 'DS9':
                series = 3
            case 'VGR':
                series = 4
            case 'ENT':
                series = 5
            case _:
                series = 0  #Should only be the movies

        season = row['ep. ID'][1:-2]
        if season == '-':
            season = 0
        else:
            season = int(season)

        new_row_dict = dict([
            ('series', series),
            ('season', season),
            ('episode', int(row['ep. ID'][2:])),
            ('julianDate', row['date']),
            ('stardate', row['stardate']),
            ('title', row['title']),
            ('airDate', None),
        ])
        new_table.append(new_row_dict)
    if verbose:
        for row in new_table:
            for k, v in row.items():
                print(k + ': ' + str(v))
            print()

    return new_table

def python_to_psql(table, recreate_table=False):
    conn = psycopg2.connect(
        host='localhost',
        database='startrekdb',
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
        )
    cur = conn.cursor()

    if recreate_table:
        cur.execute('DROP TABLE IF EXISTS trektable')
        cur.execute(
            'CREATE TABLE trektable ('
            'id serial PRIMARY KEY,'
            'series integer NOT NULL,'
            'season integer NOT NULL,'
            'episode integer NOT NULL,'
            'juliandate varchar (16),'
            'stardate varchar (16),'
            'title varchar (150),'
            'airdate varchar (16)'
            ')'
            )
    
    for row in table:
        cur.execute('INSERT INTO trektable (series, season, episode, juliandate, stardate, title, airDate)'
        'VALUES (%s, %s, %s, %s, %s, %s, %s)',
        (row['series'], row['season'], row['episode'], row['julianDate'], row['stardate'], row['title'], row['airDate'])
        )
    conn.commit()
    cur.close()
    conn.close()


url = 'https://www.johnstonsarchive.net/startrek/st-episodes-1.html'
table = html_table_to_python(url)
table = refactor_table(table)
python_to_psql(table, True)