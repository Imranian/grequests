import grequests
import pandas as pd
from bs4 import BeautifulSoup
import time

def links():
    urls = []
    for i in range(1, 5):
        urls.append(f'https://www.chess.com/players?page={i}')
    return urls
        
def response(urls):
    responses = grequests.map(grequests.get(url) for url in urls)
    return responses

def data(responses):
    player_names = []
    player_ratings = []
    player_countries = []
    # player_urls = []
    for i, response in enumerate(responses):
        if response.status_code == 200:
            print(i+1, 'success')
            soup = BeautifulSoup(response.text, "lxml")
            names = soup.find_all('span', class_="post-author-name")
            ratings = soup.find_all('a', class_="master-players-world-stats")
            countries = soup.find_all('div', class_="post-author-meta")
                # links = soup.find_all('a', class_='master-players-player-name')
            for name in names:
                n = name.text.strip()
                player_names.append(n)
            for rating in ratings:
                r = rating.text.split('|')[0].strip()
                player_ratings.append(int(r))
            while len(player_names)>len(player_ratings):
                player_ratings.append(1)

            for country in countries:
                c = country.text.strip()
                player_countries.append(c)
                # for link in links:
                #     l = link['href']
                #     player_urls.append(l)
        else:
            print(i+1, response)
        
    return player_names, player_ratings, player_countries

def dataset(player_names, player_ratings, player_countries):
    df = pd.DataFrame({'Name': player_names, 'Ratings': player_ratings, 'Country': player_countries})
    df.to_csv("Chess_ratings.csv", index=False, header=True)


if __name__ == '__main__':
    start = time.perf_counter()
    urls = links()
    res = response(urls)
    n, r, c = data(res)
    set = dataset(n,r,c)
    end = time.perf_counter() - start
    print(end)
    



