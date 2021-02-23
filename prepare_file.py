from pprint import pprint

import demjson

if __name__ == '__main__':
	with open('C:\\Users\\advok\\PycharmProjects\\NLP_Aria\\files\\cat_2.txt', 'r', encoding='utf-8') as fc:
		# pprint(fc.read())
		js = demjson.decode(fc.read())

		pprint(js['мужчина']['красота']['стрижка бритьё']['груминг'])
		# # pprint(fc.read())
