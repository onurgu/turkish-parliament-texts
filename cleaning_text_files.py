import argparse
import codecs
import os
import sys


from rules import rules

output_extension = "."

def get_files(datafolder):
    for term_name in os.listdir(datafolder):
        if not term_name.startswith("."):
            term_foldername = os.path.join(datafolder, term_name)
            for filename in os.listdir(term_foldername):
                yield (term_name,
                       os.path.splitext(filename)[0],
                       os.path.join(term_foldername, filename))

def main(datafolder,outfolder):
    for term_name, filename, path in get_files(datafolder):
        with open(path) as file:
            text = file.read()
        text = apply_rules(filename, term_name, text)
        outfilename = os.path.join(outfolder, term_name, filename+output_extension)
        os.makedirs(os.path.dirname(outfilename), exist_ok=True)
        with open(outfilename,"w") as outfile:
            print(text, file=outfile)


def apply_rules(filename, term_name, text):
    for name, rule, cond in rules:
        if cond(term_name, filename):
            text = rule(text)
            print("Applied rule %s on %s" % (name, filename))
    return text


def extract_term_name(filename):

    """
    
    :param filename: TXTs/kurucu-meclis/kurucu-meclis-d00/km__00002013/00001.txt
    :return: 
    """

    import re
    m = re.match(r".*/([^/]+)/([^/]+)/(\d+).txt$", filename)
    if m:
        return "/".join([m.group(2), m.group(3)]), "/".join([m.group(1), m.group(2)])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    #parser.add_argument('--sum', dest='accumulate', action='store_const',
    #    const=sum, default=max,help='sum the integers (default: find the max)')
    parser.add_argument("--command",
                        choices=["clean_directories", "clean_stdin"],
                        default="clean_directories")
    parser.add_argument("--filename", default="",
                        help="the filename to extract term_name")
    parser.add_argument("--datafolder", default="data/TXTs/",
                        help="the root folder to read the raw texts from")
    parser.add_argument("--output_folder", default="data/cleaned-txt/",
                        help="the root folder to write cleaned text")

    args = parser.parse_args()

    if args.command == "clean_directories":
        main(args.datafolder, args.output_folder)
    else:
        text = "".join(sys.stdin.readlines())
        filename, term_name = extract_term_name(args.filename)
        cleaned_text = apply_rules(filename, term_name, str(text))
        print(cleaned_text)
