import csv
import json
import argparse
import logging
import FuelParser

LOG_FORMAT = "%(levelname)s: %(funcName)s; %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


def log():
    return logging.getLogger()


def main():
    log().info('Started')

    parser = argparse.ArgumentParser()
    parser.add_argument("in_path")
    args = parser.parse_args()
    log().debug('Parsing finished. in_path: ' + str(args.in_path))

    fuel_parser = FuelParser.FuelParser(args.in_path)
    fuel_parser.generate_csv()

    log().info('Finished')
    print("DONE!")

if __name__ == '__main__':
    main()