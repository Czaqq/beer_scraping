#zrobic osobny projekt który zadziala jak niezalezny program i na gita projekt

from making_soup import openLinkAndReturnSoup
import json

def get_cities(root_link):
    cities_with_taps = []
    cities_with_shps = []
    soup = openLinkAndReturnSoup(root_link)
    panel_body = soup.findAll("div", {"class": "panel-body"})
    for panel in panel_body:
        anchors = panel.findAll("a")
        for anch in anchors:
            if anch['href'].endswith("multitaps"):
                cities_with_taps.append({"city": anch.text.rsplit(" ", 1)[0].strip(), "link": anch['href']})
            elif anch['href'].endswith("shops"):
                cities_with_shps.append({"city": anch.text.rsplit(" ", 1)[0].strip(), "link": anch['href']})
    return cities_with_taps, cities_with_shps

def get_pubs_from_city(city_link):
    pubs = []
    soup = openLinkAndReturnSoup(city_link)
    pub_soups = soup.findAll("div", {"class": "panel-body"})[1:]

    for pub_soup in pub_soups:
        try:
            pub = dict()
            pub["Pub Name"] = pub_soup.text.replace("\t", "").replace(" taps", "").strip()[:-2].strip()
            pub["Link"] = pub_soup.findAll("a")[0]["href"]
            pubs.append(pub)
        except IndexError:
            print("Wrong format")
    return pubs

def get_beers_in_pubs(pub_link):
    beers = []
    soup = openLinkAndReturnSoup(pub_link)
    beer_names = soup.findAll("h4", {"class": "cml_shadow"})
    beer_kinds = soup.findAll("span", {"class": "cml_shadow"})
    beer_volts = soup.findAll("h4", {"class": "cml_shadow"})

    for beer_name, beer_kind, beer_volt in zip(beer_names, beer_kinds, beer_volts):    #działa do momentu gdy ilość argumentów jest równa pomiędzy przeszukiwanymi listami
        try:
            beer = dict()
            beer["Beer Name"] = beer_name.contents[1].contents[4].strip()
            beer["Beer Kind"] = beer_kind.text
            beer["Beer Voltage"] = beer_volt.contents[1].contents[8].strip()
            beers.append(beer)
        except IndexError:
            print("Wrong format")
    return beers

def collect(root_link):
    cities_with_taps, cities_with_shps = get_cities(root_link)
    maderfaker_dict = dict()
    for pub_city in cities_with_taps:
        city_name = pub_city["city"]
        city_link = pub_city.get("link")
        maderfaker_dict[city_name] = dict()
        pubs_in_city = get_pubs_from_city(city_link)

        for pub in pubs_in_city:
            pub_name = pub.get("Pub Name")
            pub_link = pub.get("Link")
            beers_in_pub = get_beers_in_pubs(pub_link)
            maderfaker_dict.get(city_name)[pub_name] = beers_in_pub

            for beer in beers_in_pub:
                beer_name = beer.get("Beer Name")
                beer_kind = beer.get("Beer Kind")
                beer_voltage = beer.get("Beer Voltage")
                print(city_name)
    return maderfaker_dict

master_dict = collect("https://ontap.pl")
print(master_dict)

def write_beers_to_jsonfile(json_file, my_dict):
    with open (json_file, "w", encoding="UTF-8") as jsonfile:
        json.dump(my_dict, jsonfile, ensure_ascii=False, indent=4)

print(write_beers_to_jsonfile("write_beers_to_jsonfile.json", master_dict))
