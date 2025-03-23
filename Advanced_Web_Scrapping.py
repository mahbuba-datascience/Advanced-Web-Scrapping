import asyncio
import aiohttp
from bs4 import BeautifulSoup
import mysql.connector
from collections import Counter
from urllib.parse import urlparse, unquote
import json
import nest_asyncio
nest_asyncio.apply()

# Define search engines
engines = {
    'Google': 'http://google.com/search?q=',
    'Bing': 'https://www.bing.com/search?q=',
    'Yahoo': 'https://search.yahoo.com/search?p=',
    'DuckDuckGo': 'https://html.duckduckgo.com/html?q='
}

# Adjusted block lists
block_list = ['https://www.bing.com/new/termsofuse','https://privacy.microsoft.com/en-us/privacystatement',
              'https://account.microsoft.com/account/privacy','https://creativecommons.org/licenses/by-sa/3.0',
              'http://go.microsoft.com/fwlink/','https://go.microsoft.com/fwlink','https://support.microsoft.com',
              'http://support.google.com','http://policies.google.com','https://accounts.google.com',
              'http://www.google.com/preferences','setprefs?hl=en&prev=','https://search.yahoo.com/preferences',
              'https://mail.yahoo.com/','https://www.yahoo.com/news','https://finance.yahoo.com',
              'https://sports.yahoo.com/fantasy','https://sports.yahoo.com','https://shopping.yahoo.com',
              'https://www.yahoo.com/news/weathe','https://www.yahoo.com/lifestyle','https://help.yahoo.com/kb/search-for-desktop',
              'http://maps.google.com/maps','https://login.yahoo.com?.src=search','https://images.search.yahoo.com/search',
              'https://video.search.yahoo.com/search','https://search.yahoo.com/search?ei=UTF-8&','https://yahoo.uservoice.com/forums',
              'https://legal.yahoo.com/','https://guce.yahoo.com/privacy-dashboard','https://help.yahoo.com',
              'https://www.yahoo.com','https://www.google.com/imgres','https://www.google.com/maps','//duckduckgo.com/feedback.html'
             ]

#list of urls pertaining to ads to exclude from search engine results
ad_block_list = ['http://www.google.com/aclk','help.ads.microsoft',
                 'https://help.ads.microsoft.com','https://advertising.yahoo.com',
                 'https://help.duckduckgo.com/duckduckgo-help-pages/company/ads-by-microsoft-on-duckduckgo-private-search',
                 'https://duckduckgo.com/y.js?ad_domain','https://mobile.mail.yahoo.com/apps/affiliateRouter?brandUrl'
                ]

# MySQL connection parameters
mySQLparams = {'host': 'localhost', 'user': 'root', 'database': 'MY_CUSTOM_BOT', 'password': '1234'}

# SQL queries
add_search = 'INSERT INTO searches(query, engine) VALUES (%s, %s)'
add_search_results = 'INSERT IGNORE INTO search_results(url, search_id, word_counts) VALUES (%s, %s, %s)'

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def clean_url(url):
    if url.startswith('/url?q='):
        url = unquote(url.split('=')[1].split('&')[0])
    if not urlparse(url).scheme:
        url = 'http://' + url
    return url

# Fetch page content
async def fetch_page(session, url):
    try:
        async with session.get(url) as response:
            return await response.text(), url
    except Exception as e:
        return "", url

# Populate database
async def populate_database(input_query, engine):
    headers = {'user-agent': 'my-app/0.0.1'}
    async with aiohttp.ClientSession() as session:
        response = await session.get(engines[engine] + input_query, headers=headers)
        soup = BeautifulSoup(await response.text(), 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        links = [clean_url(link) for link in links if is_valid_url(clean_url(link)) and not any(ad in link for ad in ad_block_list)]

        connection = mysql.connector.connect(**mySQLparams)
        cursor = connection.cursor()
        cursor.execute(add_search, (input_query, engine))
        search_id = cursor.lastrowid

        tasks = [fetch_page(session, link) for link in links]
        pages = await asyncio.gather(*tasks)

        for text, url in pages:
            word_count = Counter(text.split())
            term_frequency = {word: word_count[word] for word in input_query.split() if word_count[word] > 0}
            if term_frequency:
                json_data = json.dumps(term_frequency)
                cursor.execute(add_search_results, (url, search_id, json_data))

        connection.commit()
        cursor.close()
        connection.close()

# Main function to manage tasks
async def main(search_term):
    tasks = [populate_database(search_term, engine) for engine in engines]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    search_term = "Childhood cancer early diagnosis methods"
    asyncio.run(main(search_term))
