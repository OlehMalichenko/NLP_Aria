import csv

if __name__ == '__main__':
	with open('files/aizel/ALL_IMPORT_MAIN.csv', 'r', encoding='utf-8') as fc:
		reader = csv.DictReader(fc)

		check_urls = set()

		with open('files/rows_without_price.csv', 'a', encoding='utf-8', newline='\n') as fa:
			writer = csv.DictWriter(fa, fieldnames=reader.fieldnames)
			writer.writeheader()

			for row in reader:
				if row['ref'] in check_urls:
					continue
				check_urls.add(row['ref'])
				if row['price'] == '0.0' or not row['price']:
					writer.writerow(row)
