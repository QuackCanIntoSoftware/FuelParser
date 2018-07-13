import logging
LOG_FORMAT = "%(levelname)s: %(funcName)s; %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


def log():
    return logging.getLogger()


class Vehicle:
    def __init__(self, json_record):
        self.name = json_record["Name"]
        self.entries = []

        for entry in json_record["FuelEntries"]:
            self.entries.append(Entry(entry))

    def __str__(self):
        return "Vehicle name: {} {}".format(self.name, [str(entry) for entry in self.entries])



class Entry:
    def __init__(self, json_record):
        self.date = None
        self.odometer = None
        self.volume = None
        self.price_unit = None
        self.price_full = None
        self.partial = None

        log().debug("Entry input: " + str(json_record))
        self.date       = json_record["UpdatedOn"][:10]
        self.odometer   = int(json_record["Odometer"])
        self.volume     = float(json_record["Units"])
        self.price_unit = float(json_record["UnitCost"])
        self.price_full = self.price_unit * self.volume
        self.partial    = json_record["IsPartial"]
        log().debug("Entry output: " + str(self))

    def __str__(self):
        return "{0:^12}{1:>7}{2:>6.2f}{3:>5.2f}{4:>7.2f}{5:>2}".format(
            self.date,
            self.odometer,
            self.volume,
            self.price_unit,
            self.price_full,
            self.partial)



