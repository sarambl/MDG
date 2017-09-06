import os
import glob
import csv
import xlwt # from http://www.python-excel.org/
import sys
print(sys.argv)
files=sys.argv[1::]
print(files)

def csv_to_excel(files):
	for csvfile in files: #glob.glob(os.path.join('.', '*.csv')):
		wb = xlwt.Workbook()
		ws = wb.add_sheet('data')
		with open(csvfile, 'r') as f:
			print(f)
			reader = csv.reader(f,delimiter=',',
			quotechar='|', quoting=csv.QUOTE_MINIMAL)
			for r, row in enumerate(reader):
				for c, val in enumerate(row):
					ws.write(r, c, val)
		wb.save(csvfile + '.xls')
