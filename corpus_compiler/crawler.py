import configparser
import datetime
import os
import sys
import wget
import re
import requests
import sqlite3
import time

config_parser = configparser.ConfigParser()
config_parser.read("config.ini")
config = config_parser['default']


def gather_new_html_documents():
    file_based_storage_dir = config['file_based_storage_dir']
    conn = sqlite3.connect(os.path.join(file_based_storage_dir, "metadb.sqlite"))
    cursor = conn.cursor()
    session = requests.session()
    session.proxies = {}
    all_donem_url = config["all_donem_url"]
    # encoding ISO-8859-1
    all_donem_page = download_page(session, all_donem_url)
    donem_pages = {}

    p = re.compile(r'"(https://www.tbmm.gov.tr/tutanak/donem[^"]*)?"')
    for m in p.finditer(all_donem_page):
        url = m.group(1)
        split = url.split('/')
        year = split[-1].split('.')[0][-1]
        donem_name = split[-2]

        file_links = []

        p_sub = re.compile(r'"(https://www.tbmm.gov.tr/tutanak/{}/yil{}/ham/[^"]*)?"'.format(donem_name, year))
        for m_1 in p_sub.finditer(download_page(session, url)):
            file_link = m_1.group(1)
            if 'oylama' not in file_link:
                file_links.append(file_link)

        for file_link in file_links:
            tutanak_content_response = session.get(file_link)
            if tutanak_content_response.ok:
                tutanak_content = tutanak_content_response.content.decode("iso-8859-9")
                file_path = os.path.join(file_based_storage_dir, url.replace("https://www.tbmm.gov.tr/tutanak/", '').replace("/", "_"))
                with open(file_path, "w") as f:
                    f.write(tutanak_content)
                cursor.execute(f"INSERT INTO files (file_type, file_url, referring_url, file_path, created_at) "
                             f"VALUES ('html', '{file_link}', '{url}', '{file_path}', '{datetime.datetime.now()}')")

        donem_pages[url] = file_links

    # print(donem_pages)
    return donem_pages


def get_last_session_id():
    return 0


def download_page(session, url):
    print(url)
    response = session.get(url, timeout=10)
    time.sleep(3)
    return response.text


def file_name_from_url(url):
    return url[url.rfind('/')+1:]


def get_links(file):
    links = {}
    with open(file, 'r', errors='replace') as f:
        for line in f.readlines():
            url, name = line.split(',')
            if '.pdf' in url:
                links[name.strip()] = str(url.strip('"'))
    return links


def download_session_pdfs():
    project_root = '/home/kerata/TPT'
    pdf_folder = '/home/kerata/TPTDataSet/PDFs/'
    csv_folder = '/home/kerata/turkish-parliament-texts'
    folder_names = [folder_name for folder_name in os.listdir(csv_folder) if
                    os.path.isdir(os.path.join(csv_folder, folder_name))]

    for folder_name in folder_names:
        csv_files = [file_name for file_name in os.listdir(os.path.join(csv_folder, folder_name)) if file_name.endswith('.csv')]
        if len(csv_files) > 1 and folder_name != 'tbmm':
            print(folder_name, csv_files)
            holder_folder = os.path.join(pdf_folder, folder_name)
            os.makedirs(holder_folder, exist_ok=True)

            for csv_file in sorted(csv_files):
                section_folder = os.path.join(holder_folder, csv_file[:-4])
                if os.path.isdir(section_folder):
                    contents = [file_name for file_name in os.listdir(section_folder) if file_name.endswith('.pdf')]
                    for url in get_links(os.path.join(os.path.join(csv_folder, folder_name), csv_file)).values():
                        file_name = file_name_from_url(url)
                        if file_name not in contents:
                            if not file_name.startswith('ehtt'):
                                try:
                                    wget.download(url, out=section_folder)
                                except:
                                    print(section_folder, url)
                    continue
                else:
                    os.makedirs(section_folder)

                for desc, url in get_links(os.path.join(os.path.join(csv_folder, folder_name), csv_file)).items():
                    file_name = file_name_from_url(url)
                    if not os.path.isfile(os.path.join(section_folder, file_name)):
                        if not file_name.startswith('ehtt'):
                            try:
                                wget.download(url, out=section_folder)
                            except:
                                print(section_folder, url)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--command", default="main", choices=["download_session_pdfs", "update_session_htmls_from_web", "init_db"],
                        required=True)
    parser.add_argument("--input_file")

    args = parser.parse_args()

    if args.command == "download_session_pdfs":
        download_session_pdfs()
    elif args.command == "update_session_htmls_from_web":
        print(gather_new_html_documents())
    elif args.command == "init_db":
        file_based_storage_dir = config['file_based_storage_dir']

        conn = sqlite3.connect(os.path.join(file_based_storage_dir, "metadb.sqlite"))

        cursor = conn.cursor()

        cursor.execute("DROP TABLE files")
        cursor.execute("CREATE TABLE files (id integer primary key, file_type text, file_url text, referring_url text, file_path text, created_at date)")



