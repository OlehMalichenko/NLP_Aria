import csv

if __name__ == '__main__':
	with open('files/decode_files/oz_goods_stat.csv', 'r', encoding='cp1251') as f:
		reader = csv.DictReader(f, delimiter=';')
		# pprint(reader.fieldnames)
		with open('files/decode_files/oz_goods_stat_utf8.csv', 'a', encoding='utf-8', newline='\n') as file:
			writer = csv.DictWriter(file, fieldnames=list(reader.fieldnames))
			writer.writeheader()

			counter = 0
			for row in reader:
				counter += 1
				writer.writerow(row)
				# if counter > 100:
				#     break
