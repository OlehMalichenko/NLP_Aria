import csv
import json
import re
# from nltk.stem import PorterStemmer
from string import punctuation

import demjson
import pymorphy2
# from nltk import word_tokenize
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


def ru_create_category_in_normal(file_in, file_ex):
    morph = pymorphy2.MorphAnalyzer()
    stop_words = stopwords.words('russian')
    reg = re.compile('[%s]' % re.escape(punctuation))

    with open(file_in, 'r', encoding='utf-8', newline='\n') as f:
        reader = csv.reader(f)
        next(reader)

        result = []
        count = 0

        # for all rows
        for row in reader:
            count += 1

            # separate each row <<symbol for separate>>
            s_list = [r.strip() for r in row[0].split('/') if r]

            # place for store results
            tmp_dict = dict.fromkeys(['clear', 'all'])
            tmp_list = []

            # in one row
            for text in s_list:
                # punctuation
                t = reg.sub(' ', text)

                # stopwords
                t_list = [word
                          for word in t.split()
                          if word not in stop_words]

                # lem
                t_lem = [morph.parse(w)[0].normal_form for w in t_list]

                #
                if t_lem:
                    tmp_list.append(' '.join(t_lem))

            if tmp_list:
                tmp_dict['clear'] = '/'.join(tmp_list)
                tmp_dict['all'] = '/'.join(s_list)
                result.append(tmp_dict)

            # if count == 50:
            #     break

        with open(file_ex, 'a', encoding='utf-8', newline='\n') as ff:
            writer = csv.DictWriter(ff, fieldnames=['clear', 'all'])
            writer.writeheader()

            for rrow in result:
                writer.writerow(rrow)


def ru_change_gender_in_(file_in, file_ex, separator):
    with open(file_in, 'r', encoding='utf-8', newline='\n') as f:
        reader = csv.reader(f)
        next(reader)

        with open(file_ex, 'a', encoding='utf-8', newline='\n') as fe:
            writer = csv.writer(fe)

            for row in reader:
                row_split = [t for t in row[0].split(separator) if t]
                if 'женское' in row_split[0].lower():
                    row_split[0] = 'Женщинам'
                if 'мужское' in row_split[0].lower():
                    row_split[0] = 'Мужчинам'
                if 'notgender' in row_split[0].lower():
                    row_split[0] = 'Унисекс'

                new_row = '/'.join(row_split)
                writer.writerow([new_row])


def parse_json(jsd):
    for k, v in jsd.items():
        try:
            yield (k, v['path'])

            if isinstance(v, dict):
                yield from parse_json(v)

        except:
            continue


if __name__ == '__main__':
    with open('files/CATEGORIES/caretory_json.txt', 'r', encoding='utf-8') as f:
        js = demjson.decode(f.read())
        d_main = {}
        for k, v in js.items():
            d_main[k] = {}
            for k1, v1 in v.items():
                d_main[k][k1] = ''

        with open('files/cat_j.txt', 'w', encoding='utf-8') as ff:
            ff.write(json.dumps(d_main))
