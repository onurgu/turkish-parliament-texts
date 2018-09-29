import logging
import os, glob
from subprocess import Popen, PIPE

import codecs

def parse_oturum_dosyasi(oturum_html_str):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(oturum_html_str, 'html.parser')

    paragraphs = soup.find_all("p", attrs={"class": "GENELKURUL"})

    return [p.text for p in paragraphs]


def main():
    txt_root = '/home/kerata/TPTDataSet/TXTs'
    pdf_root = '/home/kerata/TPTDataSet/PDFs'

    loggingLevel = logging.DEBUG
    logger = logging.getLogger()
    formatter = logging.Formatter('%(message)s')
    logger.setLevel(loggingLevel)

    file_handler = logging.FileHandler('/home/kerata/pdftotext.log', mode='w')
    file_handler.setLevel(loggingLevel)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    folder_names = [folder_name for folder_name in os.listdir(pdf_root)
                    if folder_name == 'tbmm' and os.path.isdir(os.path.join(pdf_root, folder_name))]

    # cs  kapali-oturum  kurucu-meclis  mgk  millet-meclisi  tbt
    for folder_name in sorted(folder_names):
        pdf_holder_path = os.path.join(pdf_root, folder_name)
        txt_holder_path = os.path.join(txt_root, folder_name)
        os.makedirs(txt_holder_path, exist_ok=True)

        # cs-ty01  cs-ty02  ...
        for pdf_folder in os.listdir(pdf_holder_path):
            pdf_folder_path = os.path.join(pdf_holder_path, pdf_folder)
            txt_folder_path = os.path.join(txt_holder_path, pdf_folder)
            os.makedirs(txt_folder_path, exist_ok=True)

            if os.path.isdir(pdf_folder_path) and not pdf_folder.startswith('.'):
                # cs__01001001.pdf cs__01001002.pdf ...
                for pdf_file in os.listdir(pdf_folder_path):
                    if pdf_file.endswith('.pdf'):
                        file_name = pdf_file[:-4]

                        pdf_path = os.path.join(pdf_folder_path, pdf_file)
                        txt_path = os.path.join(txt_folder_path, file_name) # + '.txt'
                        if os.path.exists(txt_path):
                            continue

                        os.makedirs(txt_path, exist_ok=True)

                        logging.debug(pdf_path, txt_path)

                        # TODO: exceeding numbers gives error
                        page_count = 1
                        while True:
                            output_file = '{}/{:05d}.txt'.format(txt_path, page_count)
                            with Popen(['pdftotext', '-f', str(page_count), '-l', str(page_count), pdf_path, output_file], stdout=PIPE, stderr=PIPE) as proc:
                                err = proc.stderr.read()
                                if len(err) == 0:
                                    logging.debug(proc.stdout.read())
                                else:
                                    logging.error(proc.stderr.read())
                                    break
                            page_count += 1


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--command", default="main", choices=["main", "parse_oturum_dosyasi"], required=True)
    parser.add_argument("--input_file")

    args = parser.parse_args()

    if args.command == "main":
        main()
    elif args.command == "parse_oturum_dosyasi":
        assert args.input_file, "You should supply input_file argument with this command"
        with open(args.input_file, "r", encoding="utf-8") as f:
            paragraphs = parse_oturum_dosyasi("\n".join(f.readlines()))
            print(paragraphs)