import csv

if __name__ == '__main__':
	with open('files/vipavenue_adm_PR_CAT.csv', 'r', encoding='utf-8') as f:
		reader = csv.DictReader(f)
		next(reader)

		fieldnames = reader.fieldnames

		with open('files/vipavenue_adm_PR_CAT_price.csv', 'a', encoding='utf-8', newline='\n') as file:
			writer = csv.DictWriter(file, fieldnames=fieldnames)
			writer.writeheader()

			for row in reader:
				price = row['price'].strip()
				old_price = row['old_price'].strip()

				try:
					sim = float(old_price) > float(price)
				except:
					sim = False

				if sim:
					row['sale_price'] = price
					row['price'] = old_price

				# row['img'] = f'https:{row["img"]}'

				writer.writerow(row)
