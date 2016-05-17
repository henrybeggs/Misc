import requests, bs4, itertools, datetime, json, time
from threading import Thread

def site_finder():
    places = {}
    url = "https://www.craigslist.org/about/sites"
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    for i in soup.findAll('a', href=True):
        places[i.string] = "http:" + str(i['href'])
    while True:
        try:
            return places[raw_input("Please enter the area you would like to search: \n").lower()]
        except Exception:
            print "Error: Please enter a valid area"

def conduct_search(base):
    term = raw_input("Please enter a search term: \n").replace(" ", "+")
    url = "{}search/sss?s={}sort=date&query={}".format(base, 0, term)
    return url

def collect_links(link, main):
    print "{} | Now collecting valid links".format(datetime.datetime.now())
    links = []
    link = link.split("s=0")
    for i in itertools.count(step=100):
        nextpage = 's={}'.format(i).join(link)
        try:
            soup = bs4.BeautifulSoup(requests.get(nextpage).text, 'lxml')
            rows = soup.find('div', 'content').find_all('p', 'row')
            if len(rows) == 0:
                break
            for row in rows:
                 links.append(main + row.a['href'][1:])
        except:
            break
    json.dump(links, open('/Users/henrybeggs/Desktop/Scripts/Craigslist/car_links', 'w'))
    print "{} | Links written to file".format(datetime.datetime.now())
    return links

def find_page():
    f = open('/Users/henrybeggs/Desktop/Scripts/Craigslist/car_data', 'w')
    print "{} | Unloading Links...".format(datetime.datetime.now())
    links = set(json.load(open('/Users/henrybeggs/Desktop/Scripts/Craigslist/car_links', 'r')))
    for link in links:
        try:
            response = requests.get(link)
            soup = bs4.BeautifulSoup(response.text, 'lxml')
            post_data = soup.select(".postinginfos , #titletextonly , .price , #postingbody")
        except:
            continue
    f.close()

def main():
    mainpage = site_finder()
    query = conduct_search(mainpage)
    gather_links = Thread(target=collect_links, args=(query, mainpage))
    while True:
        gather_links.start()
        find_page()
        time.sleep(3600)

if __name__ == '__main__':
    main()