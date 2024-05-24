import argparse
import json
import logging
import os
import traceback
from typing import Iterator, TextIO

logging.basicConfig(level=logging.INFO)


def readchars(filename: str) -> Iterator[int]:
    """Iterates all characters in file."""
    with open(filename, "rb") as fp:
        while buffer := fp.read(1_000_000):
            yield from buffer


def try_decode(buffer: list[int], lineno: int) -> str:
    """Try to decode given byte sequenes into string."""
    try:
        return bytes(buffer).decode("euc_jis_2004")
    except Exception as ex:
        logging.error(f"Error at line {lineno}: {ex}")
        return ""


def readlines(filename: str) -> Iterator[str]:
    """Iterates over all (non-UTF-8) sentences."""
    buffer = []
    lineno = 1
    nlchar = ord("\n")
    
    for c in readchars(filename):
        if c == nlchar:
            yield try_decode(buffer, lineno)
            buffer = []
            lineno += 1
        else:
            buffer.append(c)
    
    if buffer:
        yield try_decode(buffer, lineno)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("fi", type=str, help="Input file")
    p.add_argument("fo_prefix", type=str, help="Prefix of output files")
    args = p.parse_args()
    
    keys = ["url", "title", "date", "site", "category", "text"]

    files: dict[str, TextIO] = {}

    fo_dirname = os.path.dirname(args.fo_prefix)
    os.makedirs(fo_dirname, mode=0o755, exist_ok=True)

    try:
        for line in readlines(args.fi):
            if not line:
                continue
            values = line.strip().split("\t", 5)
            data = {k: v for k, v in zip(keys, values)}

            month = data["date"][:6]
            if month not in files:
                fo_name = f"{args.fo_prefix}_{month}.jsonl"
                logging.info(f"Open: {fo_name}")
                files[month] = open(fo_name, "w")
            fo = files[month]

            fo.write(json.dumps(data, ensure_ascii=False))
            fo.write("\n")
    except (Exception, KeyboardInterrupt) as ex:
        error_str = traceback.format_exception(ex)
        logging.error("".join(error_str))
        pass

    for fo_name, fo in files.items():
        logging.info(f"Close: {fo_name}")
        fo.close()


if __name__ == "__main__":
    main()
