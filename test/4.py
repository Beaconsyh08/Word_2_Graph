import re

import requests
from bs4 import BeautifulSoup
from googletrans import Translator


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
    print(img_url_res_checked, len(img_url_res_checked))
    return img_url_res_checked


if __name__ == '__main__':
    translator = Translator()
    p1, k1 = poem_keyword_split("一队衲僧来，一队衲僧去。打破睦州关，大地无寸土。@衲僧/寸土/大地")
    p2, k2 = poem_keyword_split("一日复一日，一杯复一杯。青山无限好，俗客不曾来。@青山/无限")
    cn_text_1 = keyword_format(k1)
    en_text_1 = translate(translator, cn_text_1, "zh-cn", "en")
    print(en_text_1)

    cn_text_2 = keyword_format(k2)
    en_text_2 = translate(translator, cn_text_2, "zh-cn", "en")
    print(en_text_2)

    uns_url_1_cn = generate_url(cn_text_1, "unsplash")
    uns_url_1_en = generate_url(en_text_1, "unsplash")

    uns_url_2_cn = generate_url(cn_text_2, "unsplash")
    uns_url_2_en = generate_url(en_text_2, "unsplash")
    # pix_url_2_cn = generate_url(cn_text_2, "pixabay")
    # pix_url_2_en = generate_url(en_text_2, "pixabay")

    un_c_html_1 = unsplash_get(uns_url_1_cn)
    un_e_html_1 = unsplash_get(uns_url_1_en)

    un_c_html_2 = unsplash_get(uns_url_2_cn)
    un_e_html_2 = unsplash_get(uns_url_2_en)

    # parser(un_e_html_1)
    img_url_to_display = parser(un_c_html_1)
