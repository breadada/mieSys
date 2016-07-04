# ---------------------------------------------------|
# Project Name : mieSys.                             |
# Description : A minimal display advertising system.|
# Author : 曾宪超(面包包包包包包)                    |
# time : 2016-07-04                                  |
# ---------------------------------------------------|


#coding:utf-8
import MySQLdb
import pickle

def mysqlConnect():
    return MySQLdb.connect(host='YOUR_MYSQL_ADD',
                           user='YOUR_MYSQL_USER',
                           passwd='YOUR_MYSQL_PASSWD',
                           db = 'mieSys',
                           port = 3306,
                           charset='utf8')

                           
# insert ip, uid, date and ads in database
def insert_instance_table(instance, table_name):
    conn = mysqlConnect()
    cur = conn.cursor()
    if table_name == "arr_log":
        try:
            cur.execute("insert into arr_log values(%s, %s, %s, %s, %s)", instance)
            conn.commit()
            conn.close()
        except Exception as e:
            f = open("db_errors.txt", "a")
            print 'db error!'
            print >> f, "erros %s" %e
            f.close()
            
    elif table_name == "user_click":
        try:
            cur.execute("insert into user_click values(%s, %s)", instance)
            conn.commit()
            conn.close()
        except Exception as e:
            f = open("db_errors.txt", "a")
            print 'db error!'
            print >> f, "erros %s" %e
            f.close()    
            
    elif table_name == "user_tag":
        try:
            cur.execute("insert into user_tag values(%s, %s, %s)", instance)
            conn.commit()
            conn.close()
        except Exception as e:
            f = open("db_errors.txt", "a")
            print 'db error!'
            print >> f, "erros %s" %e
            f.close()
            
    elif table_name == "ad_info":
        try:
            cur.execute("insert into ad_info values(%s, %s, %s, %s, %s, %s, %s)", instance)
            conn.commit()
            conn.close()
        except Exception as e:
            f = open("db_errors.txt", "a")
            print 'db error!'
            print >> f, "erros %s" %e
            f.close()
 
 
def insert_ctr_log(ad_set, user_behavior, uid):
    conn = mysqlConnect()
    cur = conn.cursor()
    query = "select count(*) from ctr_log where user_id = '" + uid + "'"
    cur.execute(query)
    conn.commit()
    num = int(cur.fetchall()[0][0])
    file = open("ad_info.pkl", 'rb')
    dict_ad_info = pickle.load(file)
    if num == 0:
        #feature:click, ad_id, position, advertiser_id, price, ad_tag, user_tag, user_sex, user_id
        cnt_pos = 0
        for ad_id in ad_set:
            pos = 1 if cnt_pos < 5 else 2
            #1.copy ad_id, advertiser_id, price, ad_tag from ad_info
            position = str(pos)
            advertiser_id = str(dict_ad_info[ad_id][1])
        price = str(dict_ad_info[ad_id][5])
        ad_tag = str(dict_ad_info[ad_id][4])
            user_tag = user_behavior[0][0]
            user_sex = user_behavior[0][1]
            user_id = uid
            instance = ['0', ad_id, position, advertiser_id, price, ad_tag, user_tag, user_sex, user_id]
        
            try:
                cur.execute("INSERT INTO ctr_log values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", instance)
            except Exception as e:
                f = open("db_errors.txt", "a")
                print 'db error! insert_ctr_log'
                print >> f, "erros %s" %e
                f.close()
            cnt_pos += 1
        conn.commit()
        conn.close()
    else:
        query = "select ad_id from ctr_log where user_id = '" + uid + "'"
        cur.execute(query)
        conn.commit()
        ad_already_in = cur.fetchall()
    ad_already_in = [i[0] for i in ad_already_in]
        cnt_pos = 0
        for ad_id in ad_set:
            if ad_id in ad_already_in:
                pass
            else:
                pos = 1 if cnt_pos < 5 else 2
                #1.copy ad_id, advertiser_id, price, ad_tag from ad_info
                position = str(pos)
                advertiser_id = str(dict_ad_info[ad_id][1])
                price = str(dict_ad_info[ad_id][5])
                ad_tag = str(dict_ad_info[ad_id][4])
                user_tag = str(user_behavior[0][0])
                user_sex = str(user_behavior[0][1])
                user_id = str(uid)
                instance = ['0', str(ad_id), position, advertiser_id, price, ad_tag, user_tag, user_sex, user_id]
        
                try:
                    cur.execute("INSERT INTO ctr_log values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", instance)
                except Exception as e:
                    f = open("db_errors.txt", "a")
                    print 'db error! insert_ctr_log'
                    print >> f, "erros %s" %e
                    f.close()
                cnt_pos += 1
        conn.commit()
        conn.close()
    print 'DONE'
    

def insert_offline_rec(user_behavior, prior, post):
    conn = mysqlConnect()
    cur = conn.cursor()
    user_tag = user_behavior[0]
    user_sex = user_behavior[1]
    prior = [i for i in prior]
    prior = ",".join(prior)
    post = [i for i in post]
    post = ",".join(post)
    #print prior, "~~~"
    #检查表中是否存在该user_behavior的候选广告，若无则插入；有则更新
    query_check = "select * from offline_rec where user_tag = '" + user_tag + "' and user_sex = '" + user_sex + "'"
    try:
        cur.execute(query_check)
        conn.commit()
    except Exception as e:
        f = open("db_errors.txt", "a")
        print 'db error!'
        print >> f, "erros %s" %e
        f.close()
    exist = cur.fetchall()
    instance = [user_tag, user_sex, prior, post]   
    if len(exist) == 0:
        try:
            cur.execute("insert into offline_rec values(%s, %s, %s, %s)", instance)
            conn.commit()
            conn.close()
        except Exception as e:
            f = open("db_errors.txt", "a")
            print 'db error!'
            print >> f, "erros %s" %e
            f.close()
    else:
        query_update = "UPDATE offline_rec SET prior = '" + prior + "', post = '" + post + "' WHERE user_tag = '" + instance[0] + "' and user_sex = '" + instance[1] + "'"
        #print query_update
        try:
            cur.execute(query_update)
            conn.commit()
            conn.close()
        except Exception as e:
            f = open("db_errors.txt", "a")
            print 'db error!'
            print >> f, "erros %s" %e
            f.close()
    
    
def get_ranking_ads(user_behavior):
    conn = mysqlConnect()
    cur = conn.cursor()
    user_tag = user_behavior[0][0]
    user_sex = user_behavior[0][1]
    query = "select prior, post from offline_rec where user_tag = '" + user_tag + "' and user_sex = '" + user_sex + "'"
    try:
        cur.execute(query)
        conn.commit()
    except Exception as e:
        f = open("db_errors.txt", "a")
        print 'db error!'
        print >> f, "erros %s" %e
        f.close()
    rst = cur.fetchall()
    prior = rst[0][0]
    post = rst[0][1]
    conn.close()
    return prior, post
    
        
def fetch(table_name):
    conn = mysqlConnect()
    cur = conn.cursor()
    query = "SELECT * FROM " + table_name
    try:
        cur.execute(query)
        conn.commit()
    except Exception as e:
        f = open("db_errors.txt", "a")
        print 'db error!'
        print >> f, "erros %s" %e
        f.close()
    result = cur.fetchall()
    conn.close()
    return result


def update_userbehavior(instance, table_name):
    conn = mysqlConnect()
    cur = conn.cursor()
    if table_name == 'user_tag':
        query = "UPDATE " + table_name + " SET tag = '" + instance[1] + "', sex = '" + instance[2] + "' WHERE uid = '" + instance[0] + "'"
        #print query
        try:
            cur.execute(query)
            conn.commit()
            conn.close()
        except Exception as e:
            f = open("db_errors.txt", "a")
            print 'db error! update_userbehavior user_tag'
            print >> f, "erros %s" %e
            f.close()
    elif table_name == 'ctr_log':
        query = 'UPDATE ' + table_name + " SET user_tag ='" + instance[1] + "', user_sex = '" + instance[2] + "' where user_id = '" + instance[0] + "'"
    try:
            cur.execute(query)
            conn.commit()
            conn.close()
        except Exception as e:
            f = open("db_errors.txt", "a")
            print 'db error! update_userbehavior ctr_log'
            print >> f, "erros %s" %e
            f.close()

        
def get_user_behavior(uid):
    conn = mysqlConnect()
    cur = conn.cursor()
    if uid != "all":
        query = "SELECT tag, sex FROM user_tag where uid = " + uid[4:]
    else:
        query = "SELECT tag, sex FROM user_tag"
    #print query
    try:
        cur.execute(query)
        conn.commit()
    except Exception as e:
        f = open("db_errors.txt", "a")
        print 'db error!'
        print >> f, "erros %s" %e
        f.close()
    result = cur.fetchall()
    conn.close()
    
    return result
    
    
def get_cookies():
    conn = mysqlConnect()
    cur = conn.cursor()
    query = "SELECT DISTINCT uid FROM arr_log"
    try:
        cur.execute(query)
        conn.commit()
        #print 'UPDATE DONE'
    except Exception as e:
        f = open("db_errors.txt", "a")
        print 'db error!'
        print >> f, "erros %s" %e
        f.close()
    uid = cur.fetchall()
    
    conn.close()
    
    return uid


def get_last_arr_time(uid):
    conn = mysqlConnect()
    cur = conn.cursor()
    query = "SELECT MAX(TIME) FROM arr_log WHERE uid = " + uid
    try:
        cur.execute(query)
        conn.commit()
        #print 'UPDATE DONE'
    except Exception as e:
        f = open("db_errors.txt", "a")
        print 'db error!'
        print >> f, "erros %s" %e
        f.close()
    last_arr_time = cur.fetchall()
    conn.close()
    
    return str(last_arr_time[0][0])
    

def get_relative_ads(user_tag, user_sex):
    conn = mysqlConnect()
    cur = conn.cursor()
    if len(user_tag) == 1:
        query = "select ad_id from ad_info where tag = '" + user_tag[0] + "' and sex = '" + user_sex + "'"
    else:
        set_ad_tag = set(['skin', 'shoes', 'digital', 'Unknown'])
        set_user_tag = set(user_tag)
        temp = list(set_ad_tag - set_user_tag)
        query = "select ad_id from ad_info where tag != '" + temp[0] + "' and sex = '" + user_sex + "'"
    #print query
    try:
        cur.execute(query)
        conn.commit()
        #print 'get_ralative_ads DONE'
    except Exception as e:
        f = open("db_errors.txt", "a")
        print 'db error!'
        print >> f, "erros %s" %e
        f.close()
    relative_ads = cur.fetchall()
    conn.close()
    return relative_ads
   
        
def update_ctr_log(uid, ad_id):
    conn = mysqlConnect()
    cur = conn.cursor()
    query = "select count(*) from ctr_log where user_id = '" + uid + "'"
    cur.execute(query)
    conn.commit()
    num = int(cur.fetchall()[0][0])
    query = "UPDATE ctr_log SET click='1' where \
         ad_id='" + ad_id + "' and \
         user_id = '" + uid + "'"
    try:
        cur.execute(query)
        conn.commit()
        conn.close()
        print 'UPDATE DONE'
    except Exception as e:
        f = open("db_errors.txt", "a")
        print 'db error!'
        print >> f, "erros %s" %e
        f.close()
    print "update_ctr_log DONE!"


""""
#insert ad_info
for i in range(1,13):
    if i <= 9:
        instance = ['shoes0'+str(i), "change", "change", "/static/mieSys/ads/shoes/shoes0"+str(i), "change", "shoes", "change"]
    else:
        instance = ['shoes'+str(i), "change", "change", "/static/mieSys/ads/shoes/shoes"+str(i), "change", "shoes", "change"]
    insert(instance, "ad_info")
"""
