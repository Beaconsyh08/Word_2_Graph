import jieba.analyse

poem = "一犁足春雨，一丝摇晴风。乐此至乐地，其惟蓑笠翁。"
tf_idf_res = jieba.analyse.extract_tags(poem, topK=3, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))

# Normalize the tf-idf score to be in range [0, 1] by being divided by the maximum score
base = tf_idf_res[0][1]
print(base)
tf_idf_normal = []
for tf_idf in tf_idf_res:
    score = tf_idf[1] / base
    tf_idf_normal.append((tf_idf[0], score))
print("tf-idf", poem, tf_idf_normal)
tf_idf_unzip_lst = list(zip(*tf_idf_normal))
print(tf_idf_unzip_lst)
tf_idf_word = tf_idf_unzip_lst[0]
tf_idf_score = tf_idf_unzip_lst[1]

text_rank = jieba.analyse.textrank(poem, topK=3, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
print("text_rank", poem, text_rank)
text_rank_unzip_list = list(zip(*text_rank))
print(text_rank_unzip_list)
text_rank_word = text_rank_unzip_list[0]
text_rank_score = text_rank_unzip_list[1]

repeat_words = list(set.intersection(set(tf_idf_word), set(text_rank_word)))
print(repeat_words)
words = tf_idf_word + text_rank_word
scores = tf_idf_score + text_rank_score

final_words = list(set(words)-set(repeat_words))
final_lst = []

for final_word in final_words:
    index = words.index(final_word)
    score = scores[index]
    final_lst.append((final_word,score))
print(final_lst)

print("final_words", final_words)
for repeat_word in repeat_words:
    repeat_word_indexs = []
    update_score = 0
    for index, word in enumerate(words):
        if repeat_word == word:
            update_score += scores[index]
    final_lst.append((repeat_word, update_score))

unzip_final_lst = list(zip(*final_lst))
fw = unzip_final_lst[0]
fs = unzip_final_lst[1]
result_lst = list(sorted(zip(fw,fs)))
print(result_lst)
result_words = list(zip(*result_lst))[0]
print(result_words)