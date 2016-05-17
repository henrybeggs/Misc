import requests, bs4, datetime, json, re

base_url = "http://stlouis.craigslist.org/search/cta?s="

fout = open('/Users/henrybeggs/Desktop/posts', 'w+')

today = ' '.join(datetime.datetime.now().ctime().split()[1:3])

def new_listings():
    s = 0
    while True:
        listing = []
        search_url = base_url + str(s)
        response = requests.get(search_url)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        times = soup.select("time")
        rows = soup.findAll('p', 'row')
        for post in range(len(rows)):
            date = times[post].text
            link = search_url + rows[post].a['href']
            if date == today:
                listing.append((date, link))
            elif len(listing) > 0:
                print str(len(listing)) + " new links were found"
                return listing
            else:
                print "No new listings"
                return
        s += 100

def append(new):
    posts = []
    for link in new:
        car = []
        specs = []
        try:
            response = requests.get(link[1])
            soup = bs4.BeautifulSoup(response.text, 'lxml')
            post = soup.select(".attrgroup")
            price = soup.select(".price")
            posted = soup.select(".postinginfo, time")
            for posting in posted:
                reg = re.match("posted: \d\d\d\d-(\d\d-\d\d?)", posting.text)
                if reg is not None:
                    date = reg.group(1).split("-")
                    date = datetime(month=int(date[0]), day=int(date[1]), year=2016)
                    date = ' '.join(date.ctime().split()[1:3])
            for p in price:
                price = p.text
            for j in post[0]:
                line = j.text.split()
                year = line[0]
                vehicle = line[1:]
                make = vehicle[0]
                model = ' '.join(vehicle[1:])
            for k in post[1]:
                specs.append(k.text.split(": "))


        except:
            continue
        car_dict = {'make': make, 'model': model, 'year': year, 'link': link, 'price': price, 'posted': date, 'specs': specs}
        car.append(car_dict)
        posts.append(car)
        print posts[-1]
        json.dump(posts, fout)
        fout.write("\n")

append(new_listings())
