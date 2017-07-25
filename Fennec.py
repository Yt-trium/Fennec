import requests;
from bs4 import BeautifulSoup;
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

# func : addOffer
# syno : add offer to the database
# args : url
# retu : nothing
def addOffer(url):
    url = 'https:' + url;
    r = requests.get(url)
    print("[ ADD ]", r, url);
    soup = BeautifulSoup(r.text, 'html.parser')

    # print(soup.find('h2', {'class':'item_price clearfix'})["content"]);

    '''
    idOffer     = soup.find('span',{'class':'flat-horizontal saveAd link-like'})['data-savead-id'];
    pseudo      = soup.find('a', {'class':'uppercase bold trackable'}).string.strip();
    name        = soup.find("meta",  property="og:title")["content"];
    description = soup.find(itemprop="description").contents
    price       =
    address     =
    addDate     =
    phone       =
    '''

    #sqlite.execute('INSERT INTO Offers (`idOffer`,`pseudo`,`name`,`description`,`price`,`address`,`addDate`,`phone`) VALUES (0,"a","b","c",0,"d","e",0)');
    #sqlite.commit();
    #print("[ ADD ]", idOffer, psedo, name, description, price, address, addDate, phone);
    return;


print("-", SOFT, VERSION, "by", AUTHOR, "-");

sqlite = sqlite3.connect('main.db')
scan('https://www.leboncoin.fr/annonces/offres/ile_de_france/');

sqlite.commit();
sqlite.close();
