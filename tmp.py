from anakin.step_count import words2step
from anakin.step_count import METHODS

from anakin.util.word import Word

s = '部屋/ヘヤ は/ハ 普通/フツウ です/デス が/ガ 清潔/セイケツ 感/カン が/ガ あり/アリ まずまず/マズマズ です/デス'
words = Word.from_sentence(s)

for method in METHODS:
    print(method + '\t' + str(words2step(words, method)))
