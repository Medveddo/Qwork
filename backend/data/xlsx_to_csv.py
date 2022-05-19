# Script to extract whole Excel column to CSV file

import csv
import io
import openpyxl
from openpyxl.utils import column_index_from_string
import shutil

filename = "big_i48"
value_column = "A"
column_index = column_index_from_string(value_column) - 1

wb = openpyxl.load_workbook(f"{filename}.xlsx", read_only=True)

ws = wb.active

i = 0

fileobj = io.StringIO()

writer = csv.writer(fileobj)

for row in ws.rows:
    if row[column_index].value:
        i += 1
        writer.writerow(
            [row[column_index].value.replace("_x000D_", "").replace("\n", " ")]
        )

with open(f"{filename}.csv", "w") as out_file:
    fileobj.seek(0)
    shutil.copyfileobj(fileobj, out_file)

print(i)
