import logging
import os, glob
from subprocess import Popen, PIPE

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

