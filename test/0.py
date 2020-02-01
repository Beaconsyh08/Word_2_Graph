from googletrans import Translator

if __name__ == '__main__':
    translator = Translator()
    en_text = translator.translate("云何大块噫，乃尔不可遏。黎明衆窍虚，白日丽空阔。", src="zh-cn", dest="en").text
    print(en_text)