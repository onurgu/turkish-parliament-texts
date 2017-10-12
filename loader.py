
import argparse
import re

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", default="sentences", required=True,
                        choices=["sentences"])
    parser.add_argument("--txt_filepath", required=True)
    parser.add_argument("--pdf_filepath", required=False)

    return parser


if __name__ == "__main__":

    parser = create_parser()

    args = parser.parse_args()

    with open(args.txt_filepath, "r") as f:

        current_sentence = ""

        line = f.readline()
        while line:
            if line.strip() == "":
                print(current_sentence + "\n")
                current_sentence = ""
            else:
                m = re.match(".+\xc2\xad\n$", line)
                if m:
                    line = line[:-3]
                else:
                    m = re.match(".+\n\n$", line)
                    if m:
                        line = line[:-2] + " "
                    else:
                        m = re.match(".+[^\n]\n$", line)
                        if m:
                            line = line[:-1] + " "

                if line[-1] in [".", ",", "?"]:
                    line += " "
                current_sentence += line
            line = f.readline()
