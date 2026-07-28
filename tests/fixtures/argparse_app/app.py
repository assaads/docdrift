import argparse


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="mycli")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("fetch")
    sub.add_parser("purge")
    return p
