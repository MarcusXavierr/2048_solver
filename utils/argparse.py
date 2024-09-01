import argparse

def init_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--delay', type=int, default=100)
    return parser
