import csv
import json
import argparse
import logging

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

    with open(args.in_path) as in_file:
        data = json.load(in_file)
        print(data)
        [print(veh) for veh in data["Vehicles"]]

    log().info('Finished')
    print("DONE!")

if __name__ == '__main__':
    main()