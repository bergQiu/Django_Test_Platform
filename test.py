import sqlite3,jieba,jieba.analyse


def view():
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    str_sql = "select date(updated) as d ,count(*) as c from Mytest_translate group by d"
    cursor = c.execute(str_sql)
    result = {}
    for row in cursor:
        # print("%s  ----   %d"%(row[0],row[1]))
        result[row[0]] = row[1]
    return result

def t():
    conn = sqlite3.connect("db_t.sqlite3")
    c = conn.cursor()
    str_sql = "select word,translate from Mytest_translate"
    cursor = c.execute(str_sql)
    en = ""
    zh_CN = ""
    en_result={}
    zh_result = {}
    for row in cursor:
        word = row[0].encode("utf-8")
        word_tr = row[1].encode("utf-8")
        for ch in r'!"@#$%^&\*()_\?:;,<>\\\/\|{}':
            word.replace(ch,"")
            word_tr.replace(ch,"")
        if u'\u4e00' <= row[0][0] <= u'\u9fff':
            zh_CN += word 
            en += word_tr + " "
        else:  
            zh_CN += word_tr
            en += word + " "
    # word_arr = en.split()
    # for e in word_arr:
    #     en_result[e] = en_result.get(e,0) + 1
    # en_res = list(en_result.items())
    # en_res.sort(key=lambda x:x[1],reverse=True)
    # print(zh_CN)
    zh_CN_arr = {}
    zh_arr = jieba.cut(zh_CN,cut_all=False)
    # print("/".join(zh_arr))
    for d in zh_arr:
        zh_CN_arr[d] = zh_CN_arr.get(d,0) + 1
    print(zh_CN_arr)


if __name__ == "__main__":
    # res = view()
    # print(res)
    t()