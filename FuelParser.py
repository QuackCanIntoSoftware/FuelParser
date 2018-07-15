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

        log().debug("Fuel parser Init End")

    def generate_csv(self, output_file="output/vehicle-{0}-sync.csv"):
        for i, vehicle in enumerate(self.vehicles, 1):
            with open(output_file.format(i), 'w') as out_file:
                self._save_vehicle(out_file, vehicle)
                self._save_log(out_file, vehicle)

            # fieldnames = ["Data", "Odo (km)","Fuel (litres)","Full","Price (optional)","l/100km (optional)","latitude (optional)","longitude (optional)","City (optional)","Notes (optional)","Missed","TankNumber","FuelType","VolumePrice","StationID (optional)","ExcludeDistance","UniqueId","TankCalc"]
            # writer = csv.DictWriter(out_file, delimiter=",", fieldnames=fieldnames)
            # writer.writeheader()
            # for entry in self.entries:
            #     writer.writerow({"Data": entry.date, "Odo (km)": entry.odometer, "Fuel (litres)": entry.volume})

    def _save_vehicle(self, output_file, vehicle):
        log().debug("Writing Vehicle {} data to CSV".format(vehicle.name))
        output_file.write('"## Vehicle"\x0A')
        lines = [
            '"## Vehicle"',
            '"Name","Description","DistUnit","FuelUnit","ConsumptionUnit","ImportCSVDateFormat","VIN","Insurance","Plate","Make","Model","Year","TankCount","Tank1Type","Tank2Type","Active","Tank1Capacity","Tank2Capacity"',
        ]
        lines.append('"{0}","","0","0","0","yyyy-MM-dd","","","","","","","1","100","0","1","60.0","0.0"'.format(vehicle.name))
        output_file.writelines(lines)

    def _save_log(self, output_file, vehicle):
        log().debug("Writing {} Log data to CSV".format(vehicle.name))
        lines = [
            '"## Log"',
            '"Data","Odo (km)","Fuel (litres)","Full","Price (optional)","l/100km (optional)","latitude (optional)","longitude (optional)","City (optional)","Notes (optional)","Missed","TankNumber","FuelType","VolumePrice","StationID (optional)","ExcludeDistance","UniqueId","TankCalc"'
        ]
        entries = []
        last_odo = None
        for id, entry in enumerate(vehicle.entries, 1):
            if last_odo is None:
                average = 0.0
            else:
                average = (entry.odometer - last_odo) / entry.volume
            last_odo = entry.odometer
            entries.append('"{date}","{odometer}","{litres:0.2f}","{full}","{full_price:0.2f}","{average:0.2f}",,,,"","0","1","0","{unit_price:0.2f}","0","0","{id}","0.0"\n'.format(
                date=entry.date, odometer=entry.odometer, litres=entry.volume, full='0' if entry.partial else '1', full_price=entry.price_full, average=average,
                unit_price=entry.price_unit, id=id))
        lines = lines + entries[::-1]
        output_file.writelines(lines)

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



