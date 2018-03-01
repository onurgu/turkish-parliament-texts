import requests
import datetime
import time
import re

base = 'https://www.tbmm.gov.tr/develop/owa/'

session = requests.session()
def download_page(url):
    response = session.get(url)
    time.sleep(0.1)
    return response.text


# tbmm pages
term_pages = {}
base_term = base + 'tutanak_dergisi_pdfler.yasama_yillari?v_meclis=1&v_donem={}'
for i in range(1, 26):
    url = base_term.format(i)
    term_pages[url] = download_page(url)
    print(term_pages[url])

year_pages = {}
p = re.compile('<TD target=_blank><A HREF="(.*)"')
for path, html in term_pages.items():
    for m in p.finditer(html):
        url = base + m.group(1)
        print(url)
        year_pages[url] = download_page(url)
        print(year_pages[url])


date_mappings = {}
p = re.compile('<TD ALIGN="right"><A HREF="(.*)".*\n<TD ALIGN="right">(.*)</TD>')
p2 = re.compile('<TD ALIGN="right"><A HREF="(.*)".*\n.*\n<TD ALIGN="right">(.*)</TD>')
for path, html in year_pages.items():
    temp = {}

    # This part take care of the publications with old alphabet which are not included
    # in the dataset but present anyway
    # Excluded documents are until
    # third term, second year, first of December... 01 December 1928
    if path[91:93] == '01' or path[91:93] == '02':
        for m in p2.finditer(html):
            temp[m.group(1)] = m.group(2)
    elif path[91:93] == '03' and path[108:109] == '1':
        for m in p2.finditer(html):
            temp[m.group(1)] = m.group(2)
    elif path[91:93] == '03' and path[108:109] == '2':
        counter = 0
        for m in p2.finditer(html):
            counter += 1
            temp[m.group(1)] = m.group(2)
            if counter == 9:
                start_from = m.end()
                break

        for m in p.finditer(html[start_from:]):
            temp[m.group(1)] = m.group(2)
    else:
        for m in p.finditer(html):
            temp[m.group(1)] = m.group(2)

    date_mappings[path[90:93] + '-y' + path[108:109]] = temp



root = download_page(base + 'tutanak_dergisi_pdfler.meclis_donemleri?v_meclisdonem=0')

# pages in the root
root_pages = []
p = re.compile('<TD ALIGN="right" target=_blank ><A HREF="(.*)"')
for m in p.finditer(root):
    root_pages.append(m.group(1))

# tbmm and ko pages
temp_pages = []
p = re.compile('<TD ALIGN="right" target=_blank><A HREF="(.*)"')
for m in p.finditer(root):
    temp_pages.append(m.group(1))

root_pages = root_pages[:-5] + temp_pages[-7:] + root_pages[-5:]

# downloading everything but tbmm
root_pages = [[url, download_page(base + url)] for url in root_pages]

# Our naming convetions by order, may become absolete in time...
def naming(i, url):
    if i < 19:
        return 'tbt-ty{}'.format(url[-2:])
    elif i < 38:
        return 'cs-ty{}'.format(url[-2:])
    elif i < 43:
        return 'mm-{}'.format(url[-3:])
    elif i < 46:
        return 'ko-{}'.format(url[-2:])
    elif i < 50:
        return 'ko-0{}'.format(url[-1:])
    elif i < 51:
        return 'danisma-meclisi-{}'.format(url[-3:])
    elif i < 52:
        return 'mgk-{}'.format(url[-3:])
    elif i < 53:
        return 'kurucu-meclis-{}'.format(url[-3:])
    elif i < 54:
        return 'temsilciler-meclisi-{}'.format(url[-3:])
    else:
        return 'milli-birlik-komitesi-{}'.format(url[-3:])

p = re.compile('<TD ALIGN="right"><A HREF="(.*)".*\n<TD ALIGN="right" width=110>(.*)</TD>')
for i, [url, html] in enumerate(root_pages):
    temp = {}
    for m in p.finditer(html):
        temp[m.group(1)] = m.group(2)
    date_mappings[naming(i, url)] = temp

# Incorrect in the site!!!
# cs-ty09 https://www.tbmm.gov.tr/tutanaklar/TUTANAK/CS__/t09/c059/cs__09059079.pdf 11 Haziran 0190

date_mappings['cs-ty09']['https://www.tbmm.gov.tr/tutanaklar/TUTANAK/CS__/t09/c059/cs__09059079.pdf'] = '11 Haziran 1970'

tr_date_map = {
    'Ocak': '1',
    'Şubat': '2',
    'Mart': '3',
    'Nisan': '4',
    'Mayıs': '5',
    'Haziran': '6',
    'Temmuz': '7',
    'Ağustos': '8',
    'Eylül': '9',
    'Ekim': '10',
    'Kasım': '11',
    'Aralık': '12'
 }

# for debugging purposes
tr_date_map_rev = {
    1: 'Ocak',
    2: 'Şubat',
    3: 'Mart',
    4: 'Nisan',
    5: 'Mayıs',
    6: 'Haziran',
    7: 'Temmuz',
    8: 'Ağustos',
    9: 'Eylül',
    10: 'Ekim',
    11: 'Kasım',
    12: 'Aralık'
 }
def reformat_tr_date(str):
    parts = str.split()
    return '-'.join([parts[0], tr_date_map[parts[1]], parts[2]])

n_date_mappings = {}
for k, v in date_mappings.items():
    temp_v = {}
    for addr, str_date in v.items():
        # interval part was present in the previous version...
        if addr != 'interval':
            temp_v[addr] = datetime.datetime.strptime(reformat_tr_date(str_date), '%d-%m-%Y').date()
            # for debugging purposes
            if str_date != '{:02} {:8}{}'.format(temp_v[addr].day, tr_date_map_rev[temp_v[addr].month], temp_v[addr].year):
                print(k, addr, str_date)
                raise Exception(str_date, '{:02} {:8}{}'.format(temp_v[addr].day, tr_date_map_rev[temp_v[addr].month], temp_v[addr].year))
        else:
            temp_v[addr] = [
                datetime.datetime.strptime(reformat_tr_date(str_date[0]), '%d-%m-%Y').date(),
                datetime.datetime.strptime(reformat_tr_date(str_date[1]), '%d-%m-%Y').date()
            ]
    n_date_mappings[k] = temp_v
n_date_mappings

