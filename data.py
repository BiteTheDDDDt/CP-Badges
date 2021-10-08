import re
import json
import requests

from bs4 import BeautifulSoup as bs


def get_info(handle, website):
    website = website.lower()
    if website == 'codechef':
        return get_cc(handle)
    elif website == 'codeforces':
        return get_cf(handle)
    elif website == 'atcoder':
        return get_at(handle)
    elif website == 'topcoder':
        return get_top(handle)
    elif website == 'yukicoder':
        return get_yuki(handle)
    elif website == 'uri':
        return get_uri(handle)
    elif website == 'leetcode':
        return get_leetcode(handle, false)
    elif website == 'leetcode':
        return get_leetcode(handle, true)
    else:
        raise ValueError('wrong platform website name')


def get_cf(user):
    r = requests.get(f"https://codeforces.com/profile/{user}").text
    soup = bs(r, 'lxml')
    s = soup.find('span', class_='smaller')
    s = s.text
    rating = (re.findall(r'\d+', s)[0])
    col = 'red'
    y = int(rating)
    if (y <= 1199):
        col = '#cec8c1'
    elif (y > 1199 and y <= 1399):
        col = '#43A217'
    elif (y > 1399 and y <= 1599):
        col = "#22C4AE"
    elif (y > 1599 and y <= 1899):
        col = "#1427B2"
    elif (y > 1899 and y <= 2099):
        col = "#700CB0"
    elif (y > 2099 and y <= 2299):
        col = "#F9A908"
    elif(y > 2299 and y <= 2399):
        col = "#FBB948"
    else:
        col = "#FF0000"
    return [rating, col]


def get_cc(user):
    url = f'https://www.codechef.com/users/{user}'
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    rating = soup.find_all('small')
    rating = (re.findall(r'\d+', rating[-1].text))
    col = 'red'
    y = int(rating[0])
    if (y <= 1399):
        col = '#6A6860'
    elif (y > 1399 and y <= 1599):
        col = '#3D8C0B'
    elif (y > 1599 and y <= 1799):
        col = "#347FBD"
    elif (y > 1799 and y <= 1999):
        col = "#7A4AAF"
    elif (y > 1999 and y <= 2199):
        col = "#FFC300"
    elif (y > 2199 and y <= 2499):
        col = "#FF9E1B"
    else:
        col = "#FF1B1B"
    return [rating[0], col]


def get_at(user):
    url = f'https://atcoder.jp/users/{user}'
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    x = soup.find_all('table', class_='dl-table')
    y = x[1].find_all('span')
    y = [i.text for i in y]
    val = y[y.index('―') - 1]
    col = 'red'
    a = int(val)
    if (a <= 399):
        col = '#8E8E81'
    elif (a > 399 and a <= 799):
        col = '#81501B'
    elif (a > 799 and a <= 1199):
        col = '#5CB01E'
    elif (a > 1199 and a <= 1599):
        col = '#16E5D8'
    elif (a > 1599 and a <= 1999):
        col = '#1642E5'
    elif (a > 1999 and a <= 2399):
        col = '#CFE115'
    elif (a > 2399 and a <= 2799):
        col = '#FF8700'
    else:
        col = '#FF0000'
    return [val, col]


def get_top(user):
    url = f'http://api.topcoder.com/v2/users/{user}'
    json_data = requests.get(url).json()
    rating = None
    for kind in json_data['ratingSummary']:
        if kind['name'] == 'Algorithm':
            rating = kind['rating']
    color = None
    if rating < 900:
        color = "#8E8E81"
    elif rating < 1200:
        color = "#5CB01E"
    elif rating < 1500:
        color = "#1642E5"
    elif rating < 2200:
        color = "#CFE115"
    else:
        color = "#FF0000"
    return [rating, color]


def get_yuki(user):
    url = f'https://yukicoder.me/api/v1/user/name/{user}'
    json_data = requests.get(url).json()
    level = str(json_data['Level'])
    color = '#2ecc71'
    return [level, color]


def get_uri(user_id):
    url = f'https://www.urionlinejudge.com.br/judge/pt/profile/{user_id}'
    r = requests.get(url).text

    soup = bs(r, 'html.parser')
    s = soup.find('ul', class_='pb-information')
    s = [word.lower() for word in s.text.split()]

    points = 0
    if 'pontos:' in s:
        strpoints = s[s.index('pontos:')+1].replace('.', '')
        points = int(strpoints[:strpoints.index(',')])
    elif 'points:' in s:
        strpoints = s[s.index('points:')+1].replace('.', '')
        points = int(strpoints[:strpoints.index(',')])

    return [points, '#F9A908']


def get_leetcode(username, cn = False):
    if cn:
        url = 'http://leetcode-cn.com/graphql'
    else:
        url = 'http://leetcode.com/graphql'
    queryString = '''query getContestRankingData($username: String!) {
                        userContestRankingHistory(username: $username) {
                                rating
                            }
                    }'''
    variables = {
        "username": username,
    }
    r = requests.get(url, json={'query': queryString, 'variables': variables})
    json_data = r.json()
    rankings = max([d['rating']
                    for d in json_data['data']['userContestRankingHistory']])
    rankings = int(rankings)
    return [rankings, '#FFA116']
