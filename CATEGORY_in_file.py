import csv
import json
import re
from string import punctuation

import demjson
import pymorphy2
from fuzzywuzzy import process
from nltk.corpus import stopwords


def ru_create_category_in_normal(file_in, file_ex):
	morph = pymorphy2.MorphAnalyzer()
	stop_words = stopwords.words('russian')
	reg = re.compile('[%s]' % re.escape(punctuation))

	with open(file_in, 'r', encoding='utf-8', newline='\n') as f:
		reader = csv.reader(f)
		# next(reader)

		result = []

		count = 0

		for row in reader:
			count += 1
			s_list = [r.strip() for r in row[0].split('/') if r]

			tmp_dict = dict.fromkeys(['clear', 'all'])
			tmp_list = []
			for text in s_list:
				t = reg.sub(' ', text)
				t_list = [word
				          for word in t.split()
				          if word not in stop_words]
				t_lem = [morph.parse(w)[0].normal_form for w in t_list]
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


def category_to_normal_from_(file_in, file_out):
	morph = pymorphy2.MorphAnalyzer()
	stop_words = stopwords.words('russian')
	reg = re.compile('[%s]' % re.escape(punctuation))

	with open(file_in, 'r', encoding='utf-8', newline='\n') as f:
		reader = csv.reader(f)
		# next(reader)

		reg = re.compile('[a-zA-Z]')

		result = []
		checker_cat = []
		count = 0

		for row in reader:
			if row[3] in checker_cat:
				continue
			checker_cat.append(row[3])

			count += 1
			s_list = [r.strip()
			          for r in row[3].split('/')
			          if r and not reg.findall(r)]

			tmp_dict = dict.fromkeys(['clear', 'all', 'old'])
			tmp_list = []
			for text in s_list:
				t = reg.sub(' ', text)
				t_list = [word
				          for word in t.split()
				          if word not in stop_words]
				t_lem = [morph.parse(w)[0].normal_form for w in t_list]
				if t_lem:
					tmp_list.append(' '.join(t_lem))

			if tmp_list:
				tmp_dict['clear'] = '/'.join(tmp_list)
				tmp_dict['all'] = '/'.join(s_list)
				tmp_dict['old'] = row[3]
				result.append(tmp_dict)

			# if count == 50:
			#     break

		with open(file_out, 'a', encoding='utf-8', newline='\n') as ff:
			writer = csv.DictWriter(ff, fieldnames=['clear', 'all', 'old'])
			writer.writeheader()

			for rrow in result:
				writer.writerow(rrow)


def ru_create_standard_category_json():
	with open('files/CATEGORIES/STANDART_clear.csv', 'r', encoding='utf-8', newline='\n') as f:
		reader = csv.DictReader(f, fieldnames=['clear', 'all'])
		next(reader)

		tmp = dict()

		count = 0

		for row in reader:
			count += 1
			clear_split = row['clear'].split('/')
			all_split = row['all'].split('/')

			try:
				gender = clear_split[0]
				category = clear_split[1]
			except:
				continue

			if 'женщин' not in gender and 'мужч' not in gender and 'ребён' not in gender:
				continue

			if not gender in tmp:
				tmp[gender] = {
						category: {
								'path': all_split[:2],
								'deep': True
						}
				}

			if category not in tmp[gender]:
				tmp[gender][category] = {
						'path': all_split[:2],
						'deep': True
				}

			try:
				category_1 = clear_split[2]
			except:
				tmp[gender][category]['deep'] = False
				continue
			else:
				if category_1 in tmp[gender][category]:
					tmp[gender][category][category_1]['path'] = all_split[:3]
					tmp[gender][category][category_1]['deep'] = True
				else:
					tmp[gender][category][category_1] = {
							'path': all_split[:3],
							'deep': True
					}

				try:
					category_2: str = clear_split[3]
				except:
					tmp[gender][category][category_1]['deep'] = False
					continue
				else:
					if category_2 in tmp[gender][category][category_1]:
						tmp[gender][category][category_1][category_2]['path'] = all_split[:4]
						tmp[gender][category][category_1][category_2]['deep'] = True
					else:
						tmp[gender][category][category_1][category_2] = {
								'path': all_split[:4],
								'deep': True
						}

					try:
						category_3: str = clear_split[4]
					except:
						tmp[gender][category][category_1][category_2]['deep'] = False
						continue
					else:
						if category_3 in tmp[gender][category][category_1][category_2]:
							tmp[gender][category][category_1][category_2][category_3]['path'] = all_split[:5]
							tmp[gender][category][category_1][category_2][category_3]['deep'] = False
						else:
							tmp[gender][category][category_1][category_2][category_3] = {
									'path': all_split[:5],
									'deep': False
							}

			# if count > 100:
			#     break

		js = json.dumps(tmp)

		with open('files/CATEGORIES/caretory_json.txt', 'w', encoding='utf-8') as file:
			file.write(js)


def get_best(pe):
	result = ('', 0)
	for tp in pe:
		if tp[1] == 100:
			return tp
		if tp[1] > result[1]:
			result = tp
	return result


def best_values(best):
	tmp = {}
	mx = 0
	for d in best:
		if d['best'][1] > mx:
			mx = d['best'][1]
			tmp = d
	return tmp


def get_values_list_for_(word, js, parents=None):
	if parents is None:
		parents = []

	results = []

	b1 = get_best(process.extractBests(
			query=word,
			choices=js.keys(),
			score_cutoff=75
	))
	if b1[0]:
		results.append(
				{
						'word'   : word,
						'best'   : b1,
						'path'   : js[b1[0]].get('path'),
						'parents': parents
				}
		)
		return results

	for k in js.keys():
		try:
			best = get_best(process.extractBests(
					query=word,
					choices=js[k].keys(),
					score_cutoff=75
			))

			if best[0]:
				path = js[k][best[0]].get('path')
			else:
				continue

			p = parents.copy()
			p.append(k)

			results.append(
					{
							'word'   : word,
							'best'   : best,
							'path'   : path,
							'parents': p
					}
			)
		except:
			continue

	if not results:
		for k, v in js.items():
			if isinstance(v, dict):
				p = parents.copy()
				p.append(k)
				results += get_values_list_for_(word, v, p)

	return results


def create_NORMAL_category_from_reader(reader):
	morph = pymorphy2.MorphAnalyzer()
	stop_words = stopwords.words('russian')
	reg_punctuation = re.compile('[%s]' % re.escape(punctuation))

	reg = re.compile('[a-zA-Z]')

	dct = dict()
	checker_cat = []
	count = 0

	for row in reader:
		row_cat = row['category']
		if row_cat in checker_cat:
			continue
		checker_cat.append(row_cat)

		count += 1
		s_list = [r.strip()
		          for r in row_cat.split('/')
		          if r and not reg.findall(r)]

		tmp_list = []

		for text in s_list:
			t = reg_punctuation.sub(' ', text)
			t_list = [word
			          for word in t.split()
			          if word not in stop_words]
			t_lem = [morph.parse(w)[0].normal_form for w in t_list]
			if t_lem:
				tmp_list.append(' '.join(t_lem))

		if tmp_list:
			dct[row_cat] = '/'.join(tmp_list)

	return dct


def change_CATEGORY_in_file(file_name):
	file_new_category = file_name.replace('.csv', '_CATEGORY.csv')
	file_not_found_category = file_name.replace('.csv', '_not_found_category.csv')

	with open('files/cat_2.txt', 'r', encoding='utf-8') as fc:
		js: dict = demjson.decode(fc.read())

	dct_normal = dict()
	with open(file_name, 'r', encoding='utf-8') as f:
		read_file = csv.DictReader(f)
		dct_normal = create_NORMAL_category_from_reader(read_file)

	with open(file_new_category, 'a', encoding='utf-8', newline='\n') as fn:
		writer_new = csv.DictWriter(fn, fieldnames=read_file.fieldnames)
		writer_new.writeheader()

		with open(file_not_found_category, 'a', encoding='utf-8', newline='\n') as fe:
			writer_er = csv.DictWriter(fe, fieldnames=read_file.fieldnames)
			writer_er.writeheader()

			results = []
			js_keys = js.keys()
			count = 0

			with open(file_name, 'r', encoding='utf-8') as f:
				read_file = csv.DictReader(f)
				# read_file = csv.DictReader(f)
				for row in read_file:
					count += 1

					clear_split = dct_normal[row['category']].split('/')
					if len(clear_split) == 1:
						clear_split += ['разный'] * 2

					row_s = [t.strip() for t in clear_split if t]

					row_split = []
					for r in row_s:
						if r not in row_split:
							row_split.append(r)

					try:
						js_gender = js[row_split.pop(0)]
					except:
						print(f'GENDER {row}')
						continue

					bests = {}
					for word in row_split:
						best = best_values(get_values_list_for_(word, js_gender))
						bests = best if best else {}

					if bests:
						row['category'] = '/'.join(bests['path'])
					else:
						writer_er.writerow(row)
						print(f'NOT FOUND {row["category"]}')

					row['description'] = row['description'].replace('\n', ' ').replace('\t', ' ')

					writer_new.writerow(row)


if __name__ == '__main__':
	file_name = 'files/intermodan/intermodan_PARSE.csv'
	change_CATEGORY_in_file(file_name)
