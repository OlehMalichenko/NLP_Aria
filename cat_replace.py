import csv

import pandas as pd

CATEGORY = {}

with open('files/keng/keng_new_category.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, fieldnames=['old', 'new'])
    next(reader)

    for row in reader:
        CATEGORY[row['old']] = row['new']


def func(x):
    try:
        xs = x.split('/')
        if 'Жен' in xs[0]:
            xs[0] = 'Женщинам'
        if 'Муж' in xs[0]:
            xs[0] = 'Мужчинам'
        return CATEGORY['/'.join(xs)]
    except:
        return x


def fun1(x):
    try:
        xs = x.split('/')
        if 'Жен' in xs[0]:
            xs[0] = 'Женщинам'
        if 'Муж' in xs[0]:
            xs[0] = 'Мужчинам'
        return '/'.join(xs)
    except:
        return x


def func2(x):
    if 'http' in x:
        return x
    else:
        return f'https:{x}'


if __name__ == '__main__':
    df = pd.read_csv('files/keng/keng_ADM_brand.csv')
    df['category'] = df['category'].apply(lambda x: func(x))
    # df['img'] = df['img'].apply(lambda x: func2(x))
    df.to_csv('files/keng_MAIN.csv')
