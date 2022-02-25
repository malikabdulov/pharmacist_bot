from pymystem3 import Mystem
from collections import Counter
import dict

ms = Mystem()


def clear_lemmas(lemmas):
    return [x for x in lemmas if len(x.replace(' ', '')) > 3]


def lemmatization(text):
    lemmas = ms.lemmatize(text)
    result = clear_lemmas(lemmas)
    return result


def match_percentage(arr1, arr2):
    unique_arr1 = set(arr1)
    unique_arr2 = set(arr2)
    intersection = list(unique_arr1 & unique_arr2)
    try:
        percentage = int(len(intersection) / len(unique_arr2) * 100)
    except ZeroDivisionError:
        return 0
    return percentage


def add_lemmas():
    counter = 0
    for dis in dict.disease:
        counter += 1
        if len(dis['lemmas']) == 0:
            text = dis['symptoms_desc']
            lemmas = lemmatization(text)
            dis['lemmas'] = lemmas
            print(lemmas)
        print('Лематизация', int(counter/len(dict.disease)*100), '%')
    print('Лематизация завершена')
