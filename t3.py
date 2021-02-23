import csv

if __name__ == '__main__':
    with open('files/ALL_IMPORT_MAIN_dropdublicates_actualprice_img.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        with open('files/ALL_IMPORT_MAIN_non_asos.csv', 'a', encoding='utf-8', newline='\n') as fw:
            writer = csv.DictWriter(fw, fieldnames=reader.fieldnames)
            writer.writeheader()

            for row in reader:
                if 'Asos' in row['sku']:
                    continue
                writer.writerow(row)
