"""
Module dictparser
================
This module parses the arguments from the config files
"""
import argparse
import sys


def clean_dict(data):
    keys = list(data.keys())
    for key in keys:
        if data.get(key) is None:
            data.pop(key, None)
    return data


class DictParser(argparse.ArgumentParser):
    def parse_args_dict(self):
        args = self.parse_args()
        return clean_dict(vars(args))

    def error(self, message):
        self.print_help(sys.stderr)
        print("\nExample Usage:")
        print(
            "\n    "
            "a3dcli --config_file config.json create --dicom_location ./path_to_dicom_folder/ --order-type 3DPrint "
            "--notes notes --surgery 'Surgery' --patient-gender M --patient-birth-year 2001 "
            "--catalogue-item 101 --required-date '10-08-2021'"
            "\n"
        )
        self.exit(2, "%s: error: %s\n" % (self.prog, message))
