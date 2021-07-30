import requests
from bs4 import BeautifulSoup


def getBio(name):
    name = name.lower().replace(' ', '-')
    page = requests.get(f"https://teams.gg/share/{name}")
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find(class_="listing-header-v2__bio").text.replace('\n', '').replace('  ', '')
    return(div)

def getInfo(name):
    name = name.lower().replace(' ', '-')
    page = requests.get(f"https://teams.gg/share/{name}")
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find(class_="listing-header-v2__meta").text
    age = str([int(x) for x in div.split() if x.isnumeric()]).replace('[', '').replace(']', '')
    lang = ''.join((item for item in div if not item.isdigit())).replace(' ', '').replace('\n', '').replace(',', ', ')
    location = soup.find(class_="listing-header-v2__country").text
    gender = soup.find(class_="tgg-icon__gender-male")
    if gender != None:
        gender = 'Male'
    else:
        gender = soup.find(class_="tgg-icon__gender-nonbinary")
        if gender != None:
            gender = 'Nonbinary'
        else:
            gender = soup.find(class_="tgg-icon__gender-female")
            if gender != None:
                gender = 'Female'
            else:
                gender = 'Not Specified'

    x = dict(lang = lang, age = age, gender = gender, location = location)
    return(x)

def getRank(name):
    name = name.lower().replace(' ', '-')
    page = requests.get(f"https://teams.gg/share/{name}")
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find(class_="listing-header-v2__rank").img['src'].replace('/images/site/valorant-ranks/', '').replace('.png', '').replace('_', ' ')
    return(div)

def getAgents(name):
    name = name.lower().replace(' ', '-')
    page = requests.get(f"https://teams.gg/share/{name}")
    soup = BeautifulSoup(page.content, 'html.parser')
    main = soup.find(class_="listing-characters__character listing-characters__character--primary").p.text.replace(' ', '').replace('\n', '')
    second = soup.find(class_="listing-characters__character listing-characters__character--secondary").p.text.replace(' ', '').replace('\n', '')
    x = dict(main = main, second = second)
    return(x)

def getPfp(name):
    name = name.lower().replace(' ', '-')
    page = requests.get(f"https://teams.gg/share/{name}")
    soup = BeautifulSoup(page.content, 'html.parser')
    pfp = soup.find(class_="profile-image__image")['src']
    return(pfp)

def getRoles(name):
    name = name.lower().replace(' ', '-')
    page = requests.get(f"https://teams.gg/share/{name}")
    soup = BeautifulSoup(page.content, 'html.parser')
    primary = soup.find(class_="listing-roles-v2__role listing-roles-v2__role--primary").find(class_="listing-roles-v2__roles").text.replace('\n', '').replace('\t', '')
    secondary = soup.find(class_="listing-roles-v2__role listing-roles-v2__role--secondary").find(class_="listing-roles-v2__roles").text.replace('\n', '').replace('\t', '')
    return dict(primary = primary, secondary = secondary)

def getCommitment(name):
    name = name.lower().replace(' ', '-')
    page = requests.get(f"https://teams.gg/share/{name}")
    soup = BeautifulSoup(page.content, 'html.parser')
    times = soup.find(class_="listing-commitment-v2__list")
    for item in times:
        try:
            if 'Hours' in item.text:
                hours = int(item.find(class_="listing-commitment-v2__value").text.replace('Hours', ''))
            else:
                if 'Days' in item.text:
                    days = int(item.find(class_="listing-commitment-v2__value").text.replace('Days', ''))
        except:
            pass

    return dict(hours = hours, days = days)


def getAll(name):
    return dict(agents = getAgents(name), rank = getRank(name), bio = getBio(name), info = getInfo(name), pfp = getPfp(name), commitment = getCommitment(name))
