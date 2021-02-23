import csv
import re
from string import punctuation

import demjson
import pymorphy2
from fuzzywuzzy import process
from nltk.corpus import stopwords


def export_categories_from(file_in, to_file):
	with open(file_in, 'r', encoding='utf-8') as f:
		reader = csv.DictReader(f)

		categories = set()

		with open(to_file, 'a', encoding='utf-8', newline='\n') as fc:
			writer = csv.DictWriter(fc, fieldnames=['old', 'new'])
			writer.writeheader()

			for row in reader:
				cat = row['category']
				if cat in categories:
					continue
				categories.add(cat)
				if 'Женск' in cat:
					new = f'Женщинам/{"/".join(cat.split("/")[1:])}'
				else:
					new = f'Детям/{cat}'
				writer.writerow({
						'old': cat,
						'new': new
				})


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
			score_cutoff=90
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
					score_cutoff=80
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


def get_1_values_list_for_(word, js):
	results = []

	b1 = get_best(process.extractBests(
			query=word,
			choices=js.keys(),
			score_cutoff=70
	))
	if b1[0]:
		results.append(
				{
						'word': word,
						'best': b1,
						'path': js[b1[0]].get('path'),
						'js'  : js[b1[0]]
				}
		)
		return results

	else:
		for k, v in js.items():
			if isinstance(v, dict):
				r = get_1_values_list_for_(word, v)
				if r:
					results += r

	return results


def category_to_normal_from_(file_in, file_out):
	morph = pymorphy2.MorphAnalyzer()
	stop_words = stopwords.words('russian')
	reg = re.compile('[%s]' % re.escape(punctuation))

	with open(file_in, 'r', encoding='utf-8', newline='\n') as f:
		reader = csv.DictReader(f)
		# next(reader)

		reg = re.compile('[a-zA-Z]')

		result = []
		checker_cat = []
		count = 0

		for row in reader:
			if row['new'] in checker_cat:
				continue
			checker_cat.append(row['new'])

			count += 1
			s_list = [r.strip()
			          for r in row['new'].split('/')
			          if r and not reg.findall(r)]

			tmp_dict = dict.fromkeys(['clear', 'new', 'old'])
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
				tmp_dict['new'] = row['new']
				tmp_dict['old'] = row['old']
				result.append(tmp_dict)

			# if count == 50:
			#     break

		with open(file_out, 'a', encoding='utf-8', newline='\n') as ff:
			writer = csv.DictWriter(ff, fieldnames=['clear', 'new', 'old'])
			writer.writeheader()

			for rrow in result:
				writer.writerow(rrow)


def new_category_from(file_in, file_out):
	with open('files/cat_2.txt', 'r', encoding='utf-8') as fc:
		js: dict = demjson.decode(fc.read())

	with open(file_in, 'r', encoding='utf-8') as f:

		with open('files/keng/keng_NOT_found_category.csv', 'a', encoding='utf-8', newline='\n') as fe:
			writer_er = csv.DictWriter(fe, fieldnames=['clear', 'new', 'old'])
			writer_er.writeheader()

			reader = csv.DictReader(f, fieldnames=['clear', 'new', 'old'])
			next(reader)

			results = []

			js_keys = js.keys()

			count = 0

			for row in reader:
				count += 1

				clear_split = row['clear'].split('/')
				if len(clear_split) == 1:
					clear_split += ['разный'] * 2

				row_s = [t.strip() for t in clear_split if t]

				row_split = []
				for r in row_s:
					if r not in row_split:
						row_split.append(r)

				try:
					js_deep = js[row_split.pop(0)]
				except:
					print(f'GENDER {row}')
					continue

				bests = {}

				# ввести указание на последний элемент, что б останавливаться !!!!!!!!!!!!!!!!
				for word in row_split:
					value_list = get_1_values_list_for_(word, js_deep)
					best = best_values(value_list)
					if best:
						bests = best
						js_deep = best['js']

				if bests:
					row_new = {
							'old': row['old'],
							'new': '/'.join(bests['path']),
					}
					results.append(row_new)
				else:
					writer_er.writerow(row)
					print(f'NOT FOUND {row}')

				# if count > 40:
				#     break

			with open(file_out, 'a', encoding='utf-8', newline='\n') as fn:
				writer = csv.DictWriter(fn, fieldnames=['old', 'new'])
				writer.writeheader()

				for i in results:
					writer.writerow(i)


if __name__ == '__main__':
	# export_categories_from(file_in='files/keng_ADM_brand.csv',
	#                        to_file='files/keng_cat.csv')

	# category_to_normal_from_(file_in='files/keng_cat.csv',
	#                          file_out='files/keng_cat_normal.csv')

	new_category_from(file_in='files/keng/keng_cat_normal.csv',
	                  file_out='files/keng/keng_new_category.csv')
