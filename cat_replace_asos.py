import csv
import re

if __name__ == '__main__':
	category_dict = {}

	reg = re.compile('[^\w]')

	with open('files/elits/elits_new_categories.csv', 'r', encoding='utf-8') as fc:
		reader_c = csv.DictReader(fc, fieldnames=['old', 'new'])

		for row in reader_c:
			key = reg.sub('', row['old']).lower()
			category_dict[key] = row['new']

	# pprint(category_dict)
	file_path = 'files/elits/urls_elits.csv'
	fieldnames = []

	with open(file_path, 'r', encoding='utf-8') as f:
		reader = csv.reader(f)

		with open('files/elits/urls_elits_cat.csv',
		          'a',
		          encoding='utf-8',
		          newline='\n') as fnew:
			writer = csv.writer(fnew)

			for row in reader:
				key_new = reg.sub('', row[3]).lower()
				row[3] = category_dict.get(key_new)
				writer.writerow(row)
