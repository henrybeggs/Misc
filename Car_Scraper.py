import requests, bs4, itertools, datetime, json, time
from threading import Thread

def search_terms():
    items = []
    print "Please enter search terms: "
    while True:
        item = raw_input()
        if len(item) > 0:
            items.append(item)
        else:
            break
    return '+'.join(items)

def results(trms):
    links = []
    print "Collecting valid links " + str(datetime.datetime.now()) + "\n"
    for s in itertools.count(start=0, step=100):
        try:
            response = requests.get("https://stlouis.craigslist.org/search/cta?s={}&query={}".format(s, trms))
            soup = bs4.BeautifulSoup(response.text, 'lxml')
            rows = soup.find('div', 'content').find_all('p', 'row')
            if len(rows) == 0:
                break
            for row in rows:
                link = "http://craigslist.com/" + row.a['href'][1:]
                if link not in links:
                    links.append("http://craigslist.com/" + row.a['href'][1:])
                else:
                    continue
        except:
            break
    json.dump(links, open('/Users/henrybeggs/Desktop/Scripts/Craigslist/car_links', 'w'))
    print "Links written " + str(datetime.datetime.now()) + "\n"

def data_extractor():
    links = json.load(open('/Users/henrybeggs/Desktop/Scripts/Craigslist/car_links'))
    for i in links:
        response = requests.get(i)
        soup = bs4.BeautifulSoup(response.text, 'lxml')


def main():
    terms = search_terms()
    while True:
        # Write valid links
        results(terms)
        data_extractor()
        time.sleep(3600)

if __name__ == '__main__':
    main()