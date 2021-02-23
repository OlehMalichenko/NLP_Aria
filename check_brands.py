import csv
import re

if __name__ == '__main__':
	reg = re.compile('[^\w]')
	brands = set()

	with open('files/brand_list.csv', 'r', encoding='utf-8') as f:
		reder = csv.DictReader(f)

		for row in reder:
			if 'да' not in row['we']:
				continue

			brand = reg.sub('', row['brand']).lower()
			brands.add(brand)

	with open('files/keng/keng_ADM.csv', 'r', encoding='utf-8') as ff:
		reader = csv.DictReader(ff)

		with open('files/keng/keng_ADM_brand.csv', 'a', encoding='utf-8', newline='\n') as fw:
			writer = csv.DictWriter(fw, fieldnames=reader.fieldnames)
			writer.writeheader()

			with open('files/keng/keng_ADM_notbrands.csv', 'a', encoding='utf-8', newline='\n') as fe:
				writer_e = csv.DictWriter(fe, fieldnames=reader.fieldnames)
				writer_e.writeheader()

				for row in reader:
					b = reg.sub('', row['brand']).lower()
					if b in brands:
						writer.writerow(row)
					else:
						writer_e.writerow(row)
