import argparse, os
from rules import rules

def get_files(datafolder):
    for term_name in os.listdir(datafolder):
        if not term_name.startswith("."):
            term_foldername = os.path.join(datafolder,term_name)
            for filename in os.listdir(term_foldername):
                yield(term_name,os.path.splitext(filename)[0],os.path.join(term_foldername,filename))

def main(datafolder,outfolder):
    for term_name, filename, path in get_files(datafolder):
        with open(path) as file:
            text = file.read()
        for name,rule,cond in rules:
            if cond(term_name,filename):
                text = rule(text)
                print("Applied rule %s on %s" %(name,filename))
        outfilename = os.path.join(outfolder,term_name,filename+".txt")
        os.makedirs(os.path.dirname(outfilename), exist_ok=True)
        with open(outfilename,"w") as outfile:
            print(text,file=outfile)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    #parser.add_argument('--sum', dest='accumulate', action='store_const',
    #    const=sum, default=max,help='sum the integers (default: find the max)')
    parser.add_argument("--datafolder", default="data/raw-txt/",
                        help="the root folder to read the raw texts from")
    parser.add_argument("--output_folder", default="data/cleaned-txt/",
                        help="the root folder to write cleaned text")

    args = parser.parse_args()
    main(args.datafolder,args.output_folder)
