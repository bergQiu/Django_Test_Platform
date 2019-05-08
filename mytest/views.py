# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse,Http404
import pymssql,json,pymongo,re,datetime
# 前臺默認不會渲染後臺傳入的html標籤
from django.utils.safestring import mark_safe
from pyecharts import Line,Pie,WordCloud
from bs4 import BeautifulSoup
import time,requests,json,execjs,urllib,chardet
from .models import translate as Translate
import sqlite3,jieba
from dwebsocket.decorators import accept_websocket,require_websocket
# Create your views here.

def mytest_jquery(request):
    return render(request,'mytest/jquery.html')

def mytest_table(request):
    return render(request,'mytest/table.html')

def mytest_table_select(request):
    # print(request.method)
    print("here")
    #數據庫連接
    conn = pymssql.connect(host = "minerva",user = "sa",password = "00",database = "berg_db")
    #打開游標
    cur = conn.cursor()
    if not cur:
        result = "Database connection failed!!"
    else:
        # result = "Database connection is successful!"
        sqlStr = "select * from berg_test"
        cur.execute(sqlStr)
        result = cur.fetchall()
        # print(type(result))
        # print(result[0])
        # print(type(json.dumps({"result":result})))
    return HttpResponse(json.dumps({"result":result}))

def Mongo_conn(dbname,collame):
    conn = pymongo.MongoClient("10.10.0.96",27017)
    db = conn[dbname]  
    coll = db[collame]
    return coll

def mytest_ht_select(request):
    if request.method == "POST":
        # data = {}
        WA = request.POST["WA"]
        Building = request.POST["Building"]
        # print WA
        # print Building
        # coll =Mongo_conn("test_Berg","tpmis_temp_humi_realtime")
        coll =Mongo_conn("test","tpmis_temp_humi_realtime")
        # html_head_str = "<table border='1px' class='table' id='table1'><tr><th>Location</th><th>Temp</th><th>Humi</th><tr>"
        # html_body_str = ""
        data_array = []
        for each in coll.find({"WA":WA,"Building":Building}):
            each['_id'] = ''
            each['Start'] = str(each['Start'])
            each['End'] = str(each['End'])
            data_array.append(each)
            # html_body_str += "<tr><td>" + each["Location"] + "</td><td>" + str(each["Temp"]) + "</td><td>" + str(each["Humi"]) + "</td><tr>"
        # html_str = html_head_str + html_body_str + "</table>"
        # data["table"] = mark_safe(html_str)
        # print (data_array)
        # return HttpResponse(html_str)
        return HttpResponse(json.dumps({"result":data_array}))
 
    if request.method == "GET":
        if request.GET:
            coll =Mongo_conn("test","tpmis_temp_humi_config")
            pipeline = [
                    {"$match":{"WA":request.GET["WA"]}},
                    {"$group":{"_id":"$Building"}},
                    {"$sort":{"_id":-1}}
            ]
            Bui_arr = []
            for d in coll.aggregate(pipeline):
                if request.GET["WA"] == "永成":
                    Bui_arr.append(int(d["_id"]))
                else:
                    Bui_arr.append(d["_id"])
            # print(Bui_arr)
            return HttpResponse(json.dumps({"Bui_arr":sorted(Bui_arr)}))
        else:
            coll =Mongo_conn("test","tpmis_temp_humi_config")
            pipeline = [
                    {"$match":{"WA":"永成"}},
                    {"$group":{"_id":"$Building"}},
                    {"$sort":{"_id":1}}
            ]
            Bui_arr = []
            for d in coll.aggregate(pipeline):
                Bui_arr.append(int(d["_id"]))
            pipeline = [
                    {"$group":{"_id":"$WA"}},
            ]
            WA_arr = []
            for d in coll.aggregate(pipeline):
                WA_arr.append(d["_id"])
        return render(request,"mytest/htselect.html",{"WA_arr":WA_arr,"Bui_arr":sorted(Bui_arr)})

def ht_view(request):
    # print("here")
    # print(request.POST)
    # WA = request.POST["WA"]
    # Building = request.POST["Building"]
    # print (request.POST["query"])
    Repo = request.POST["query"].split("_")[2]
    Location = request.POST["query"].split("_")[3]
    coll = Mongo_conn("test","tpmis_temp_humi_shorthistory")
    pipeline = [
         {'$match':{
             'Repo':Repo,
             'Location':re.compile(r'.+' + Location),
            }
         },
         {'$unwind':'$Data'},
         {'$match':{
             'Data.Update':{'$gt':datetime.datetime.now() - datetime.timedelta(hours  = 8 , days  = 5)}
         }}
    ]
    h_data = []
    t_data = []
    R_h_data = []
    R_t_data = []
    time = []
    for each in coll.aggregate(pipeline):
        h_data.append(float(each['Data']['Humi']))
        t_data.append(float(each['Data']['Temp']))
        R_h_data.append(float('%.1f'%each['Data']['HumiRef']))
        R_t_data.append(float('%.1f'%each['Data']['TempRef']))
        # 轉換成Localtime
        locatime = each['Data']['Update'] + datetime.timedelta(hours = 8)
        time.append(locatime.strftime("%Y-%m-%d %H:%M:%S"))
    # is_stack = True,堆疊顯示
    line = Line(request.POST["query"])
    line.add("Temp",time,t_data,is_label_show = True,mark_point = ["average"],)
    line.add("Humi",time,h_data,is_label_show = True,mark_point = ["average"])
    line.add("RefTemp",time,R_t_data,is_label_show = True,mark_line = ["min","max"])
    line.add("RefHumi",time,R_h_data,is_label_show = True,mark_line = ["min","max"],is_datazoom_show = True,datazoom_type = "both",datazoom_range = [90,100])

    context = line.render_embed()
    js = line.get_js_dependencies()
    return HttpResponse(json.dumps({'context':context}))

def a(request):
    return render(request,"mytest/a.html")

# def show_data(request):
#     return render()

def test(request):
    return render(request,"mytest/test.html")

def kepserver_time(request):
    return render(request,"mytest/keps_time.html")

def new_kepserver_time(request):
    coll = Mongo_conn("test_Berg","tpmis_control_KEP")
    rows = []
    for data in coll.find():
        start = data['Start'] + datetime.timedelta(hours =8)
        data['Start'] = start.strftime("%Y-%m-%d %H:%M:%S")
        end = data['End'] + datetime.timedelta(hours =8)
        data['End'] = end.strftime("%Y-%m-%d %H:%M:%S")
        rows.append(data)
    return render(request,"mytest/new_keps_time.html",{'rows':rows})

def modify_tpmis_kep_control(request):
    req = request.POST
    coll = Mongo_conn("test_Berg","tpmis_control_KEP")
    try:
        if req['user'] == '--':
            coll.insert({
                            "User":req['new_user'],
                            "Start":datetime.datetime.strptime(req['new_start'].encode('utf-8'),'%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours =8),
                            "End":datetime.datetime.strptime(req['new_end'].encode('utf-8'),'%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours =8),
                            "Desc":req['new_desc']
                    })
        else:
            coll.update(
                {
                    "User":req['user'],
                    "Start":{"$gt":datetime.datetime.strptime(req['old_start'].encode('utf-8'),'%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours =8,seconds =1),
                                    "$lt":datetime.datetime.strptime(req['old_start'].encode('utf-8'),'%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours =8) + datetime.timedelta(seconds =1)},
                    "End":{"$gt":datetime.datetime.strptime(req['old_end'].encode('utf-8'),'%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours =8,seconds =1),
                                    "$lt":datetime.datetime.strptime(req['old_end'].encode('utf-8'),'%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours =8,) + datetime.timedelta(seconds =1)}
                    },
                {"$set":{
                            "User":req['new_user'],
                            "Start":datetime.datetime.strptime(req['new_start'].encode('utf-8'),'%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours =8),
                            "End":datetime.datetime.strptime(req['new_end'].encode('utf-8'),'%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours =8),
                            "Desc":req['new_desc']
                    }
                }
            )
        return HttpResponse("1")
    except:
        return HttpResponse("0")

def del_tpmis_kep_control(request):
    req = request.POST
    coll = Mongo_conn("test_Berg","tpmis_control_KEP")
    try:
        coll.delete_one({
                "User":req['User'],
               "Start":{"$gt":datetime.datetime.strptime(req['Start'].encode('utf-8'),'%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours =8,seconds =1),
                                "$lt":datetime.datetime.strptime(req['Start'].encode('utf-8'),'%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours =8) + datetime.timedelta(seconds =1)},
                "End":{"$gt":datetime.datetime.strptime(req['End'].encode('utf-8'),'%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours =8,seconds =1),
                                "$lt":datetime.datetime.strptime(req['End'].encode('utf-8'),'%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours =8,) + datetime.timedelta(seconds =1)}
        })
        return HttpResponse("1")
    except:        
        return HttpResponse("0")

def kepserver_time_find_modify(request):
    print(request.method)
    print(request.POST)
    if request.method == "GET":
        coll = Mongo_conn("test_Berg","time_control_KEP")
        data = []
        t = lambda f:f if  f else ""
        for each in coll.find():
            each['_id'] = ''
            each['Num'] = str(each['Num'])
            each['Week']["Mon"] = t(each['Week']["Mon"])
            each['Week']["Tues"] = t(each['Week']["Tues"])
            each['Week']["Wed"] = t(each['Week']["Wed"])
            each['Week']["Thur"] = t(each['Week']["Thur"])
            each['Week']["Fri"] = t(each['Week']["Fri"])
            each['Week']["Sat"] = t(each['Week']["Sat"])
            each['Week']["Sun"] = t(each['Week']["Sun"])
            each["Enable"] = t(each["Enable"])
            data.append(each)
        # print(data)
        return HttpResponse(json.dumps({"result":data}))
    elif request.method == "POST":
        # print("here")
        array = request.POST.getlist("data[]")
        # print(len(array))
        # print(array[4])
        coll = Mongo_conn("test_Berg","time_control_KEP")
        try:
            coll.update(
                {"Num":float(array[0])},
                {'$set':{
                    # 'Start':re.sub(":","",array[1]),
                    # 'End':re.sub(":","",array[2]),
                    'Start':array[1],
                    'End':array[2],
                    'Week.Mon':bool(array[3]),
                    'Week.Tues':bool(array[4]),
                    'Week.Wed':bool(array[5]),
                    'Week.Thur':bool(array[6]),
                    'Week.Fri':bool(array[7]),
                    'Week.Sat':bool(array[8]),
                    'Week.Sun':bool(array[9]),
                    'Enable':bool(array[10])
                }},
                True
                )
            # print ("success")
            return HttpResponse("1")
        except:
            return HttpResponse("0")

def pressure(request):
    if request.method == "GET":
        # config_c = Mongo_conn("test_Berg","pressure")
        # config = config_c.find_one({"Key":"a-pressure"})
        config_coll = Mongo_conn("test","tpmis_pressure_config")
        data = config_coll.aggregate([
            {'$unwind':"$Location"},
            {'$project':{
                    "MID":1,
                    "WA":1,
                    "Desc":"$Location.Desc",
                    "Floor":"$Location.Floor",
                    "Point":"$Location.Point"
                }}
        ])
        result = {}
        for i in data:
            # print(i)
            if i['WA'] not in result:
                result[i['WA']]= {}
            # else:
            result[i['WA']][i['MID']] = {i['Point']:i['Floor']}
        # print(result)
        return render(request,"mytest/pressure.html",{'result':result})
        #  return render(request,"mytest/pressure.html")


    if request.method == "POST":
        # print(request.POST.getlist('query[]'))
        pressure_coll = Mongo_conn("test","tpmis_pressure_shorthistory")
        req =request.POST
        time_ = {}
        val_ ={}
        max_ = 0
        min_ = 1000
        for d in request.POST.getlist('query[]'):
            q = d.split(' --- ')
            key = ""
            data = pressure_coll.aggregate([
                        {'$match':{
                                'Start':{'$gt':datetime.datetime.strptime(req['start'].encode('utf-8'),'%Y-%m-%d %H:%M:%S')},
                                'End':{'$lt':datetime.datetime.strptime(req['end'].encode('utf-8'),'%Y-%m-%d %H:%M:%S')}
                        }},
                        {'$match':{"MID":q[1],"Point":int(q[2])}},
                        # {'$match':{"MID":"C","Point":1}},
                        {'$unwind':"$Data"},
                        {'$sort':{"Data.Update":1}},
                        {'$project':{
                                "WA":"$WA",
                                "MID":1,
                                "Point":1,
                                "Building":1,
                                "Floor":1,
                                "Val":"$Data.Pressure",
                                "Time":"$Data.Update"
                            }},
                        # {'$limit':5}
                    ])
            # key = d['name']
            
            for q in  data:    
                if key == "":
                    key = q['WA'] + "-" + q['Building'] +"-"+ str(q['Floor'])
                    val_[key] = []
                    time_[key] = []
                    
                val_[key].append(q["Val"])
                time_[key].append(datetime.datetime.strftime(q['Time'],'%Y-%m-%d %H:%M:%S'))
                if max(val_[key]) > max_:
                    max_ = max(val_[key])
                if min(val_[key]) < min_:
                    min_ = min(val_[key])
        min_ = int(min_/100)*100 
        max_ = int(max_/100)*100 + 100
        line = Line('氣壓值統計圖','範例一')
        # time_ = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        for k in val_:
            line.add(k,time_[k],val_[k],is_label_show = True,is_datazoom_show=True,yaxis_force_interval=50,xaxis_rotate=-15,yaxis_max=max_,yaxis_min= min_,datazoom_extra_type = "both",xaxis_margin=20,xaxis_interval=10,is_more_utils=True)
        context = line.render_embed()
        return HttpResponse(json.dumps({"context":context}))
    else:
        return render(request,"mytest/pressure.html")

def pressure_get_info(request):
    config_c = Mongo_conn("test_Berg","pressure")
    config = config_c.find_one({"Key":"a-pressure"})
    config['_id'] = "test"
    if request.POST['type'] == "GET_BUI":
        # config_c = Mongo_conn("test_Berg","pressure")
        # config = config_c.find_one({"Key":"a-pressure"})
        # config['_id'] = "test"
        result = config[request.POST['data']]
        # print(result)
        return HttpResponse(json.dumps({'result':result}))
    if request.POST['type'] == "GET_LINE":
        result = config[request.POST['wa']][request.POST['bui']]
        print(result)
        return HttpResponse(json.dumps({'result':result}))


def vote(request):
    if request.method == "GET":
        return render(request,"mytest/vote.html")
        # pass
    if request.method == "POST":
        vote_c = Mongo_conn("test_Berg","vote")
        data = request.POST   
        # print(data)
        if data['type']  == "query":
            try:
                result = vote_c.find({"Name":data['name'],"Password":data['password']})
                print(result)
                if result.count() == 0:
                    return HttpResponse("0")
                else:
                    return HttpResponse(result[0]['Choice'])
            except:
                pass
        if data['type'] == "insert": 
            try:
                vote_c.insert_one({"Name":data['name'],"Password":data['password'],"Choice":data['choice']})
                return HttpResponse("0")
            except:
                return HttpResponse("1")
        if data['type'] == "update": 
            try:
                vote_c.update_one({"Name":data['name'],"Password":data['password']},{"$set":{"Choice":data['choice']}})
                return HttpResponse("0")
            except:
                return HttpResponse("1")

def vote_chart(request):
    # print("here")
    vote_c = Mongo_conn("test_Berg","vote")
    result = vote_c.aggregate([
        {"$group":{'_id':"$Choice",'sum':{"$sum":1}}}
    ])
    attr = []
    val = []
    for d in result:
        attr.append(d['_id'])
        val.append(d['sum'])
    pie = Pie("Result for vote")
    pie.add("",attr,val,is_label_show=True,rosetype="radius")
    chart = pie.render_embed()
    # print(chart)
    return HttpResponse(json.dumps({"chart":chart}))

    # context = line.render_embed()
    # js = line.get_js_dependencies()
    # return HttpResponse(json.dumps({'context':context}))

def translate(request):
    if request.method == "GET":
        Real_ip = request.META['REMOTE_ADDR']
        if Real_ip in IP_whitelist:
            return render(request,"mytest/translate.html",{"context_show":True if Real_ip == "10.9.224.66" else False,"motto":motto[int(time.strftime("%M"))%10],"love":love,"cathy":cathy})
        else:
            raise Http404("The page you visited does not exist!") 
    if request.method == "POST":
        # print("here")
        # for k,v in request.META.items(): 系统信息
        #     print(k)
        #     print("****" + str(v))
        type_ = request.POST['type']
        if type_ == 'translate':
            # tran_coll = Mongo_conn("test_Berg","translate")
            text = request.POST['text']
            tk = Get_TK()
            url = buildUrl(text,tk.getTk(text))      
            r=requests.get(url,proxies = proxy)
            result=json.loads(r.text)
            # print(type(result))
            try:
                Real_ip = request.META['REMOTE_ADDR']
                # tran_coll.insert_one({
                #         "word":text,
                #         "translate":result[0][0][0],
                #         "from":Real_ip
                #     })
                Translate.objects.create(word=text,translate=result[0][0][0],ip=Real_ip)
                # print(Real_ip)
            except:
                pass
            return HttpResponse(json.dumps({"result":result}))
        if type_ == 'story':
            print(request.POST['to'])
            text = request.POST['text']
            index = motto.index(text)
            if request.POST['to'] == 'next':
                return HttpResponse(json.dumps({"result":motto[(index + 1 )% 10]}))
            if request.POST['to'] == 'last':
                return HttpResponse(json.dumps({"result":motto[9 if index == 0 else index - 1]}))
            # return HttpResponse("1")

 
def model_test(requests):
    # print("i am here")
    # data = Translate.objects.create(word="good",translate="优秀",ip="10.9.232.57")
    # data.translate = "棒棒哒"
    # data.save()
    # text = "你是个好女孩"
    # tk = Get_TK()
    # tk_1,tk_2 = tk.getTk(text)
    # print(tk_1)
    # print(tk_2)
    # url1 = buildUrl(text,tk_1)
    # url2 = buildUrl(text,tk_2)
    # print(url1)
    # print(url2)
    return HttpResponse("1")

# var b = 406644; 
# var b1 = 3293161072; 

def translate_char(requests):
    # print(requests.POST["type"])
    context = ""
    conn = sqlite3.connect("db_t.sqlite3")
    c = conn.cursor()
    if requests.POST["type"] == "Line":
        str_sql = "select date(updated) as d ,count(*) as c from Mytest_translate group by d"
        cursor = c.execute(str_sql)
        data_arr = []
        data_num_arr = []
        for row in cursor:
            # result[row[0]] = row[1]
            data_arr.append(row[0])
            data_num_arr.append(row[1])
        line = Line("歷史查詢統計","單位： 次")
        line.add("times",data_arr,data_num_arr,mark_point=["max","min"],is_label_show=True,is_datazoom_show=True,xaxis_rotate=30,xaxis_interval=2,datazoom_extra_type = "both",xaxis_margin=20,is_more_utils=True)
        # line.add("times",data_arr,data_num_arr)
        context = line.render_embed()
    elif requests.POST["type"] == "Cloud":
        str_sql = "select word,translate from Mytest_translate"
        cursor = c.execute(str_sql)
        en = ""
        zh_CN = ""
        en_result={}
        zh_result = {}
        for row in cursor:
            word = row[0].encode("utf-8")
            word_tr = row[1].encode("utf-8")
            for ch in r'!"@#$%^&\*()_\?:;,<>\\/\|{}':
                word.replace(ch,"")
                word_tr.replace(ch,"")
            if u'\u4e00' <= row[0][0] <= u'\u9fff':
                zh_CN += word 
                en += word_tr + " "
            else:  
                zh_CN += word_tr
                en += word + " "
        # 英文統計        
        word_arr = en.split()
        for e in word_arr:
            en_result[e] = en_result.get(e,0) + 1
        en_res = list(en_result.items())
        en_res.sort(key=lambda x:x[1],reverse=True)

        # 中文統計
        zh_CN_arr = jieba.cut(zh_CN,cut_all=False)
        zh_CN_res = {}
        for d in zh_CN_arr:
            zh_CN_res[d] = zh_CN_res.get(d,0) + 1
        zh_CN_res = list(zh_CN_res.items())
        zh_CN_res.sort(key=lambda x:x[1],reverse=True)
        en_name_arr = []
        en_num_arr = []
        zh_CN_name_arr = []
        zh_CN_num_arr = []
        for i in en_res[:100]:
            en_name_arr.append(i[0])
            en_num_arr.append(i[1])
        for d in zh_CN_res[10:110]:
            zh_CN_name_arr.append(d[0])
            zh_CN_num_arr.append(d[1])

        en_char = WordCloud()
        # ,word_size_range=[20,100]
        try:
            if requests.POST["k"] == u"漢字":
                en_char.add("zh_CN",zh_CN_name_arr,zh_CN_num_arr,shape=requests.POST["t"])
            else:
                en_char.add("En",en_name_arr,en_num_arr,shape=requests.POST["t"])
        except:
            en_char.add("En",en_name_arr,en_num_arr,shape="diamond")
        context = en_char.render_embed()
        # return HttpResponse(json.dumps({"context":{"en_name":en_name_arr,"en_num":en_num_arr,"zh_CN_name":zh_CN_name_arr,"zh_CN_num":zh_CN_num_arr}}))    
        # return HttpResponse(json.dumps({"context":en_res[:10]}))    
        
    else:
        pass
    return HttpResponse(json.dumps({"context":context}))

def chat(request):
    if request.method == "GET":
        return render(request,"mytest/chat.html")
    else:
        return HttpResponse(1)

######################################Class defined##############
class Get_TK:
    def __init__(self):  
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072;       
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f";    
        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
    };      
    function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
    } 
    """)

    def getTk(self,text):  
        tk_1 = self.ctx.call("TL",text)
        return tk_1

######################################Function defined##############

def buildUrl(text,tk):
    # print(chardet.detect(text))
    # print(type(text.encode('utf-8')))
    # text = "你好"
    # print(type(text))
    # print(chardet.detect(text))
    for ch in text:
        if u'\u4e00' <= ch <= u'\u9fff':
            from_ = 'zh-CN'
            to_ = 'en'
        else:
            from_ = 'en'
            to_ = 'zh-CN'

    print(from_)
    print(to_)
    baseUrl='https://translate.google.cn/translate_a/single'
    baseUrl+='?client=t&'
    baseUrl+='sl='+from_+ '&'
    baseUrl+='tl='+ to_ +'&'
    baseUrl+='h1=zh-CN&'
    baseUrl+='dt=at&'
    baseUrl+='dt=bd&'
    baseUrl+='dt=ex&'
    baseUrl+='dt=ld&'
    baseUrl+='dt=md&'
    baseUrl+='dt=qca&'
    baseUrl+='dt=rw&'
    baseUrl+='dt=rm&'
    baseUrl+='dt=ss&'
    baseUrl+='dt=t&'
    baseUrl+='ie=UTF-8&'
    baseUrl+='oe=UTF-8&'
    baseUrl+='pc=1&'
    baseUrl+='source=btn&'
    baseUrl+='ssel=3&'
    baseUrl+='tsel=3&'
    baseUrl+='kc=2&'
    baseUrl+='tk='+str(tk)+'&'
    baseUrl+='q='+ urllib.quote_plus(text.encode('utf-8'))  
    return baseUrl

######################################Variable defined##############
cathy = "親愛的周純，"
proxy = {"http":"http://berg.qiu:9608769171@10.10.1.7:18263","https":"https://berg.qiu:9608769171@10.10.1.7:18263"}
IP_whitelist = ["10.9.232.75","10.9.224.66"]
header={    
        'authority':'translate.google.cn',
        'method':'GET',    
        'path':'',    
        'scheme':'https',    
        'accept':'*/*',    
        'accept-encoding':'gzip, deflate, br',    
        'accept-language':'zh-CN,zh;q=0.9',    
        'cookie':'',    
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64)  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'x-client-data':'CIa2yQEIpbbJAQjBtskBCPqcygEIqZ3KAQioo8oBGJGjygE='
    }
motto = [
    "To the world you may be one person, but to one person you may be the world",
    "Life is compared to a voyage",
    "love at first sight",
    "Life is a leaf of paper white, there on each of us may write his word or two",
    "you're uinique, nothing can replace you",
    "All that truly matters in the end is that you loved",
    "You know i love you, but you don`t know how much i love you",
    "It is better bo have love and lost than never to have loved at all",
    "Love's mysteries in souls do grow, but yet the body in his book",
    "Wherever you go, whatever you do, i will be right here waiting for you",
    "But soft! What lightthrough yonder windows breaks? It`s the east and cathy is thu sun",
    "Grow old along with me! The best is yet to be",
    "I love you not because of who youare, but because of who i am when  i am with you",
    "You complete me",
    "No matter the ending is perfect or not, you cannot disappear from my world",
    "If i know what love is,it is because of you",
    "If you don`t  let me go, i will love you forever",
    "What you meet is fate, and all you have is luck(遇見都是天意，擁有都是幸運)",
    "Do you want to drink and reach old age together, The vast snow, even if rain, whole life only for you(想陪你白頭到老，共飲風霜。就算夏雨洪荒，冬雪蒼茫，窮及一生也只為你)",
    
]
love = [
        u"　　請原諒我的不善言辭，但請相信我會用行動證明。",
        u"　　佛家說：“無論你遇到誰，她都是對的人，無論發生什麼事，那都是唯一會發生的事，不管事情開始與哪個時刻，都是對的時刻”。就像我喜歡你，曾經的你和現在的你還有未來的你，不管是在未知的天之涯，海之角，我希望将来老到掉牙的那一天，陪我牵手看夕阳的看云舒云卷的还是你。",    
        u"　　對了，我想起來那句話了，下次告訴你！"
]

            


