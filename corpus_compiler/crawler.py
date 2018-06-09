import os, sys
import wget

project_root = '/home/kerata/TPT'
pdf_folder = '/home/kerata/TPTDataSet/PDFs/'
csv_folder = '/home/kerata/turkish-parliament-texts'
folder_names = [folder_name for folder_name in os.listdir(csv_folder) if os.path.isdir(os.path.join(csv_folder, folder_name))]

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

