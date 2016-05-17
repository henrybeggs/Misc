import json, requests, bs4



def car_finder():
    links = json.load(open('/Users/henrybeggs/Desktop/carlinks', 'r'))
    fout = open('/Users/henrybeggs/Desktop/car', 'a')
    for link in links:
        details = {}
        response = requests.get(link)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        specs = soup.select(".attrgroup")
        try:
            vehicle = specs[0].text
            for i in specs[1]:
                spec = i.text.split(": ")
                if len(spec) > 1:
                    details[spec[0]] = spec[1]
            price = soup.select(".price")[0].text
            post = soup.select("#postingbody")[0].text
            make = vehicle.split()[1].lower()
            year = vehicle.split()[0]
            title = soup.select("#titletextonly")[0].text
            postinginfo = soup.select(".postinginfo")
            postid = postinginfo[1].text.split(": ")[1]
            postdate = postinginfo[2].text.split(": ")[1].split()[0]
        except:
            continue
        car = {"title": title, "make": make, "specs": details, "price": price, "post": post, "year": year, "id": postid, "date": postdate, "link": link}
        print car['make'], car['price']
        json.dump(car, fout)
        fout.write("\n")
    return
car_finder()

