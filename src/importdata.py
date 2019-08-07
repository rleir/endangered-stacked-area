#!/usr/bin/env python3
"""
Handy utility to reformat some data for use in a d3js chart.
  read input xls data file
  find transposed sheet
  read data, save in new format
  write the json output
"""
import json
import time
import datetime
from xlrd import open_workbook  # type: ignore
from typing import Dict, List

input_path = "data/species_summary.xlsx"
output_file = "data/species_summary.json"


def readFiles() -> None:
    all_data = []
    timestamps = []

    # read xls, find avg sheet
    wb = open_workbook(input_path)
    transp_s_found = 0
    for sheet in wb.sheets():
        shname = sheet.name
        if shname.startswith("transp"):
            transp_s_found += 1

            for row in range(sheet.nrows):
                if row == 0:
                    for col in range(sheet.ncols):
                        if col == 0:
                            timestamps.append(None)
                        else:
                            year = int(sheet.cell(row, col).value)
                            # print("yerr")
                            # print(year)
                            dt = datetime.datetime(year=year, month=1, day=1)
                            timestamps.append(time.mktime(dt.timetuple()))

                else:
                    points = []
                    rec = {}
                    for col in range(sheet.ncols):
                        if col == 0:
                            category = sheet.cell(row, col).value
                            rec["key"] = category
                        else:
                            count = sheet.cell(row, col).value
                            point = [timestamps[col], count]
                            points.append(point)
                    rec["values"] = points
                    all_data.append(rec)
    if transp_s_found == 0:
        print("ERR: transp sheet not found in " + input_path)
    elif transp_s_found > 1:
        print("ERR: multiple transp sheets found in " + input_path)

    return all_data


def writeFile(all_data):
    with open(output_file, "w") as fp:
        json.dump(all_data, fp)


if __name__ == "__main__":
    # execute only if run as a script

    all_data = readFiles()
    writeFile(all_data)
