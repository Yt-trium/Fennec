import time
import requests;
from bs4 import BeautifulSoup;
from fake_useragent import UserAgent
import sqlite3;

SOFT    = "Fennec"
AUTHOR  = "Yt-trium"
VERSION = "1.0";

# func : scan
# syno : scan leboncoin and add all offer
# args : url
# retu : nothing
def scan(url):
    r = requests.get(url)
    print("[SCAN ]", r, url);
    soup = BeautifulSoup(r.text, 'html.parser')
    for offers in soup.find_all(itemtype='http://schema.org/Offer'):
        for offer in offers.find_all('a', href=True):
            addOffer(offer['href'])
    return;

# func : getPhone
# syno : get phone number
# args : url and if from offer
# retu : phone number
def getPhone(url, id):
    phone_payload = "list_id=" + str(id) + "&app_id=leboncoin_web_utils&key=YOURKEY&text=1"
    phone_headers = {
        'accept': "*/*",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "fr,en-US;q=0.8,en;q=0.6,es;q=0.4",
        'connection': "keep-alive",
        'content-length': "89",
        'content-type': "application/x-www-form-urlencoded",
        'host': "api.leboncoin.fr",
        'origin': "https://www.leboncoin.fr",
        'referer': str(url),
        'user-agent': str(ua.random),
        'cache-control': "no-cache",
    }

    phoneReq = requests.request("POST", "https://api.leboncoin.fr/api/utils/phonenumber.json", data=phone_payload, headers=phone_headers).json()["utils"];
    phone       = (phoneReq["phonenumber"] if phoneReq["status"] == 'OK' else 1);

    return phone;

# func : addOffer
# syno : add offer to the database
# args : url
# retu : nothing
def addOffer(url):
    url = 'https:' + url;
    r = requests.get(url)
    print("[ ADD ]", r, url);
    soup = BeautifulSoup(r.text, 'html.parser')

    idOffer     = soup.find('span',{'class':'flat-horizontal saveAd link-like'})['data-savead-id'];
    pseudo      = soup.find('a', {'class':'uppercase bold trackable'}).string.strip();
    name        = soup.find("meta",  property="og:title")["content"];
    description = soup.find(itemprop="description").contents;
    tmp         = soup.find('h2', {'class':'item_price clearfix'});
    price       = (0 if tmp == None else tmp["content"]);
    address     = soup.find(itemprop="address").contents;
    addDate     = soup.find(itemprop="availabilityStarts")["content"];

    isPhone     = soup.find('button', {'class':'button-orange phoneNumber skip_interstitial mw trackable'});
    phone       = 0 if isPhone == 'None' else getPhone(url, idOffer);

    print("[ ADD ]", idOffer, pseudo, name, description, price, address, addDate, phone);

    exit(0xF001) if isPhone and phone == 1 else 0;

    #sqlite.execute('INSERT INTO Offers (`idOffer`,`pseudo`,`name`,`description`,`price`,`address`,`addDate`,`phone`) VALUES (0,"a","b","c",0,"d","e",0)');
    #sqlite.commit();

    time.sleep(10) if isPhone else 0;
    return;

print("-", SOFT, VERSION, "by", AUTHOR, "-");

ua = UserAgent()
sqlite = sqlite3.connect('main.db')
scan('https://www.leboncoin.fr/annonces/offres/ile_de_france/');

sqlite.commit();
sqlite.close();
