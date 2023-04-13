# -----------------------------------------------------------
# Example code to check ip addresses assigned to a specific
# country.  Uses the maxmind geolocation databases files.
#
# Author: Dave Horton
# -----------------------------------------------------------
import geoip2.database
import ipaddress
import argparse

DATABASE = "maxmind/GeoLite2-City.mmdb"

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ip", help="IPv4 address")
parser.add_argument("-f", "--file", help="File of IPv4 addresses")
parser.add_argument("-c", "--iso", help="ISO 3166-1 alpha-2 code e.g, UK or ALL")
args = parser.parse_args()


def report_match(record, ip):
    output = (
        str(record.country.iso_code)
        + ","
        + str(record.country.name)
        + ","
        + str(record.city.name)
        + ","
        + str(record.location.latitude)
        + ","
        + str(record.location.longitude)
        + ","
        + str(ip)
    )
    print(output.strip())


def validate_ip(ipv4):
    try:
        ip = ipaddress.ip_address(ipv4)
        return True
    except ValueError:
        print("address " + ipv4 + " is invalid.")
    return False


with geoip2.database.Reader(DATABASE) as reader:
    # process file of ip addresses
    if args.file:
        with open(args.file) as iplist:
            for ip in iplist.readlines():
                try:
                    response = reader.city(ip.rstrip())
                    match args.iso:
                        case response.country.iso_code:
                            report_match(response, ip)
                        case "ALL":
                            report_match(response, ip)

                # skip error when processing a file of ip addresses
                except geoip2.errors.AddressNotFoundError:
                    continue
                except ValueError:
                    continue
        exit(0)
    # lookup a single ip address
    if args.ip:
        if validate_ip(args.ip):
            response = reader.city(args.ip)
            report_match(response, args.ip)
            exit(0)
