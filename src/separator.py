import jieba.analyse
from termcolor import colored

from src import formator


def calculate_scores():
    tf_idf_res = jieba.analyse.extract_tags(poem, topK=3, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
    # Normalize the tf-idf score to be in range [0, 1] by being divided by the maximum score
    tf_idf_res.append(("0", 0))
    base = tf_idf_res[0][1]
    tf_idf_normal = []
    for tf_idf in tf_idf_res:
        if base != 0:
            score = tf_idf[1] / base
            tf_idf_normal.append((tf_idf[0], score))
        else:
            tf_idf_normal.append(("0", 0))
    tf_idf_unzip_lst = list(zip(*tf_idf_normal))
    tf_idf_word = tf_idf_unzip_lst[0]
    tf_idf_score = tf_idf_unzip_lst[1]

    text_rank = jieba.analyse.textrank(poem, topK=3, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
    text_rank.append(("0", 0))
    text_rank_unzip_list = list(zip(*text_rank))
    text_rank_word = text_rank_unzip_list[0]
    text_rank_score = text_rank_unzip_list[1]
    return tf_idf_word, tf_idf_score, text_rank_word, text_rank_score


def output_to_file(results):
    with open("poem_with_keyword.txt", "a") as file_object:
        for item in results:
            file_object.write(item)
        file_object.write("\n")


if __name__ == '__main__':
    jieba.enable_parallel(4)
    poem_file = formator.input_from_file("poem_new.txt")
    for poem in poem_file:
        tf_idf_word, tf_idf_score, text_rank_word, text_rank_score = calculate_scores()
        repeat_words = list(set.intersection(set(tf_idf_word), set(text_rank_word)))
        words = tf_idf_word + text_rank_word
        scores = tf_idf_score + text_rank_score

        final_words = list(set(words) - set(repeat_words))
        final_lst = []

        # not repeat words
        for final_word in final_words:
            index = words.index(final_word)
            score = scores[index]
            final_lst.append((final_word, score))

        # repeat words score sum
        for repeat_word in repeat_words:
            repeat_word_indexs = []
            update_score = 0
            for index, word in enumerate(words):
                if repeat_word == word:
                    update_score += scores[index]
            final_lst.append((repeat_word, update_score))

        unzip_final_lst = list(zip(*final_lst))
        result_lst = list(sorted(zip(unzip_final_lst[1], unzip_final_lst[0]), reverse=True))
        result_words = list(list(zip(*result_lst))[1])
        result_words.remove("0")
        if result_words:
            print(colored(result_words, "yellow"))
            words_string = "/".join([str(word) for word in result_words])
            output_to_file([poem.strip(), "@", words_string])
