import csv
import json
import logging
LOG_FORMAT = "%(levelname)s: %(funcName)s; %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


def log():
    return logging.getLogger()

class FuelParser:
    def __init__(self, input_json_file):
        log().debug("Fuel parser Init Start")
        self.vehicles = []
        with open(input_json_file) as in_file:
            data = json.load(in_file)

            for vehicle in data["Vehicles"]:
                self.vehicles.append(Vehicle(vehicle))

            log().debug([print(veh) for veh in self.vehicles])
        log().debug("Fuel parser Init End")

class Vehicle:
    def __init__(self, json_record):
        self.name = json_record["Name"]
        self.entries = []

        for entry in json_record["FuelEntries"]:
            self.entries.append(Entry(entry))

    def __str__(self):
        return "Vehicle name: {} {}".format(self.name, [str(entry) for entry in self.entries])

    def generate_csv(self):
        with open("output/output.csv", 'w') as out_file:
            fieldnames = ["Data", "Odo (km)","Fuel (litres)","Full","Price (optional)","l/100km (optional)","latitude (optional)","longitude (optional)","City (optional)","Notes (optional)","Missed","TankNumber","FuelType","VolumePrice","StationID (optional)","ExcludeDistance","UniqueId","TankCalc"]
            writer = csv.DictWriter(out_file, delimiter=",", fieldnames=fieldnames)
            writer.writeheader()
            for entry in self.entries:
                writer.writerow({"Data": entry.date, "Odo (km)": entry.odometer, "Fuel (litres)": entry.volume})



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



