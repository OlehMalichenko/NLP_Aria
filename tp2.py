import csv
import re


def make_seo_from(word):
    try:
        word = str(word)
        space = re.compile('[^a-zA-Zа-яА-ЯёЁĆćÁáÉé0-9\s]').sub(' ', word).lower()
        space = re.compile('é').sub('e', space)
        space = re.compile('á').sub('a', space)
        return re.compile('\s{2,}').sub(' ', space)
    except:
        return ''


if __name__ == '__main__':
    with open('files/ALL_IMPORT_MAIN.csv', 'r', encoding='utf-8') as f_import:
        reader = csv.DictReader(f_import)

        with open('files/ALL_IMPORT_MAIN_brandseo_lastpath.csv', 'a', encoding='utf-8', newline='\n') as f_new:
            fieldnames = list(reader.fieldnames) + ['brand_seo', 'last_path']
            writer = csv.DictWriter(f_new, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                try:
                    last_category = row['category'].split('/')[-1]
                except:
                    last_category = ''

                row['brand_seo'] = make_seo_from(row['brand'])
                row['last_path'] = last_category
                writer.writerow(row)
