import jieba

jieba.enable_paddle()
strs = ["一犁足春雨", "一丝摇晴风", "乐此至乐地", "其惟蓑笠翁"]
for str in strs:
    seg_list = jieba.cut(str, use_paddle=True)
    print("Paddle Mode: " + '/'.join(list(seg_list)))

seg_list = jieba.cut("一犁足春雨，一丝摇晴风。乐此至乐地，其惟蓑笠翁。", cut_all=True)
print("Full Mode: " + " ".join(seg_list))

seg_list = jieba.cut("一犁足春雨，一丝摇晴风。乐此至乐地，其惟蓑笠翁。", cut_all=False)
print("Default Mode: " + " ".join(seg_list))

seg_list_2 = jieba.cut_for_search("一犁足春雨，一丝摇晴风。乐此至乐地，其惟蓑笠翁。")
# print("Search Mode: " + " ".join(seg_list_2))
res_lst = list(seg_list_2)
print(res_lst)
print([res for res in list(res_lst) if len(res) > 1])
