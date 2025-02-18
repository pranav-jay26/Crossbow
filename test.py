#!/usr/bin/env python3

import crossbow as cxb
import pyarrow as pa

filepath = "/Users/pranavjay/Downloads/Client 1 - FedEx Ground Economy Data - 1-1-2024 to 1-31-2024 - $30M Spend (2).xlsx"
sheetname = "Sheet1"

batch = cxb.read_excel_py(filepath, sheetname)

table = pa.Table.from_batches([batch])
df = table.to_pandas()
print(df)
