import re

import requests
from bs4 import BeautifulSoup
from googletrans import Translator

from src import formator


def poem_keyword_split(poem_keyword):
    poem = poem_keyword.split("@")[0]
    keyword = poem_keyword.split("@")[1]
    return poem, keyword


def generate_url(keywords, search_engine):
    # unsplash or pixabay
    # "https://unsplash.com/s/photos/naseng"
    # "https://pixabay.com/zh/images/search/naseng/"
    search_urls = []
    if search_engine == "unsplash":
        combine_search_text = "-".join(keywords)
        search_urls.append("https://unsplash.com/s/photos/" + combine_search_text)
        for keyword in keywords:
            search_urls.append("https://unsplash.com/s/photos/" + keyword)

    elif search_engine == "pixabay":
        search_text = "%20".join(keywords)
        search_urls.append("https://pixabay.com/zh/images/search/" + search_text + "/")
    else:
        return "Engine not defined"
    # print(search_urls)
    return search_urls


def translate(translator, texts, source, destination):
    # translate chinese to english
    result = []
    for item in texts:
        result.append(translator.translate(item, src=source, dest=destination).text)
    return result


def keyword_format(keywords):
    return keywords.split("/")


def unsplash_get(unsplash_search_url):
    html_res = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }
    session = requests.Session()
    for url in unsplash_search_url:
        html_res.append(session.get(url=url, headers=headers).text)
    return html_res


def parser(img_html):
    img_url_res = []
    for html in img_html:
        soup = BeautifulSoup(html, 'lxml')
        img_urls = str(soup.find_all("img"))[1:-1]
        # print(img_urls)
        img_urls_lst = re.split("[, ]", img_urls)
        for img_url in img_urls_lst:
            if img_url.__contains__(
                    "src") and "profile" not in img_url and "secure" not in img_url and "scorecardresearch" not in img_url and "placeholder" not in img_url:
                pattern = re.compile('\"h.+\w+\"')
                img_src_url = str(pattern.findall(img_url))[3:-3]
                img_url_res.append(img_src_url)

    img_url_res_checked = list(set(img_url_res))
    img_url_res_checked.sort(key=img_url_res.index)
    # print(img_url_res, len(img_url_res))
    if "" in img_url_res_checked:
        img_url_res_checked.remove("")
    # print(img_url_res_checked, len(img_url_res_checked))
    return img_url_res_checked


def output_to_file(results):
    with open("../poem_img_url_2.txt", "a") as file_object:
        for item in results:
            file_object.write(item)
        file_object.write("\n")


if __name__ == '__main__':
    translator = Translator()

    count = 0
    for line in reversed(list(open("../poem_with_keyword.txt"))):
        poem, keyword = poem_keyword_split(line)
        cn_text = keyword_format(keyword)
        en_text = translate(translator, cn_text, "zh-cn", "en")

        uns_url_cn = generate_url(cn_text, "unsplash")
        uns_url_en = generate_url(en_text, "unsplash")

        uns_cn_html = unsplash_get(uns_url_cn)
        uns_en_html = unsplash_get(uns_url_en)

        img_url_to_display_cn = parser(uns_cn_html)
        img_url_to_display_en = parser(uns_en_html)
        img_url = img_url_to_display_cn+img_url_to_display_en
        count += 1
        print(count, "of 129216 ", 100 * (float(count) / float(129216)))
        output_to_file([line, "@", str(img_url)])
    poem_file.close()