import argparse
import json
import logging
import pathlib

logging.basicConfig(level=logging.INFO)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("in_dir", type=pathlib.Path, help="Input directory containing JSONL files")
    p.add_argument("out_file", type=pathlib.Path, help="Output file")
    args = p.parse_args()

    in_dir: pathlib.Path = args.in_dir
    out_file: pathlib.Path = args.out_file

    in_filenames = sorted(in_dir.glob("*.jsonl"))

    with out_file.open("w") as fo:
        for ifn in in_filenames:
            logging.info(ifn)
            with ifn.open() as fi:
                for line in fi:
                    j = json.loads(line)
                    print(j["url"], file=fo)



if __name__ == "__main__":
    main()