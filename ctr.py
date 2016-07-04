# ---------------------------------------------------|
# Project Name : mieSys.                             |
# Description : A minimal display advertising system.|
# Author : 曾宪超(面包包包包包包)                    |
# time : 2016-07-04                                  |
# ---------------------------------------------------|


#coding:utf-8
import db
import recSys
import pandas as pd
import numpy as np
import pickle

def load_ctr_log():
    path = "ctr/log.csv"
    name = ['click', 'ad_id', 'position', 'advertiser_id', 'price', 'ad_tag', 'user_tag', 'user_sex', 'user_id', 'line']
    f = pd.read_csv(path, sep="\t", names=name, header=0)
    f = f.drop(['line', 'user_id'], axis=1)
    # print f.info()
    return f

    
def load_ad_info(dict_ad_info, user_behavior):
    list_ad_info = []
    for ad in dict_ad_info:
        ad_id = dict_ad_info[ad][0]
        position = 1
        advertiser_id = int(dict_ad_info[ad][1])
        price = int(dict_ad_info[ad][5])
        ad_tag = dict_ad_info[ad][4]
        user_tag = user_behavior[0][0]
        user_sex = user_behavior[0][1]
        list_ad_info.append([-1, ad_id, position, advertiser_id, price, ad_tag, user_tag, user_sex])
        # print list_ad_info
    list_ad_info.append([-1, ad_id, 2, advertiser_id, price, ad_tag, user_tag, user_sex])
    name = ['click', 'ad_id', 'position', 'advertiser_id', 'price', 'ad_tag', 'user_tag', 'user_sex']
    # np_ad_info = np.mat(list_ad_info)
    df_ad_info = pd.DataFrame(list_ad_info, columns=name)
    file = open("f_origin_8features.pkl", 'wb')
    pickle.dump(df_ad_info, file)
    file.close()
    
    #print 'DONE'
    return df_ad_info
        
    
def feature_engineering(f): 
    # name = ['click', 'ad_id', 'position', 'advertiser_id', 'price', 'ad_tag', 'user_tag', 'user_sex']
    # ad_id
    ad_id = pd.get_dummies(f['ad_id'])
    ad_id = ad_id.rename(columns=lambda x: str(x))
    f = pd.concat([f, ad_id], axis = 1)
    
    # position
    position = pd.get_dummies(f['position'])
    position = position.rename(columns=lambda x: "position_" + str(x))
    f = pd.concat([f, position], axis = 1)
    
    # advertiser_id
    advertiser_id = pd.get_dummies(f['advertiser_id'])
    advertiser_id = advertiser_id.rename(columns=lambda x: "advertiser_id_" + str(x))
    f = pd.concat([f, advertiser_id], axis = 1)
    
    # price
    price = pd.get_dummies(f['price'])
    price = price.rename(columns=lambda x: "price_" + str(x))
    f = pd.concat([f, price], axis = 1)
    
    # ad_tag
    ad_tag = pd.get_dummies(f['ad_tag'])
    ad_tag = ad_tag.rename(columns=lambda x: "ad_tag_" + str(x))
    f = pd.concat([f, ad_tag], axis = 1)
    
    # ad_tag
    user_tag = pd.get_dummies(f['user_tag'])
    user_tag = user_tag.rename(columns=lambda x: "user_tag_" + str(x))
    f = pd.concat([f, user_tag], axis = 1)
    
    # user_sex
    user_sex = pd.get_dummies(f['user_sex'])
    user_sex = user_sex.rename(columns=lambda x: "user_sex_" + str(x))
    f = pd.concat([f, user_sex], axis = 1)

    return f

    
def fit_model(f):
    from sklearn.linear_model import LogisticRegression
    # fit a model
    f = f.drop(['ad_id', 'ad_tag', 'user_tag', 'user_sex'], axis=1)
    
    f = f[37:]
    Y = f['click']
    X = f.drop(['click'], axis=1)
    LR = LogisticRegression(max_iter=2000, penalty="l1")
    LR.fit(X, Y)
    
    return LR


def predict(model, test_data):
    test_data = test_data.drop(['ad_id', 'ad_tag', 'user_tag', 'user_sex', 'click'], axis=1)
    test_data = test_data[37:]
    prob = model.predict_proba(test_data)
    
    return prob

    
# feature:ad_id, position, advertiser_id, price, ad_tag, user_tag, user_sex, user_id
def get_ad_prob(ad_set, dict_ad_info, user_behavior, position, origin, model):
    # 构造候选广告DataFrame，以待与origin结合后，扩展特征。
    list_ad_info = []
    for ad in ad_set:
        ad = ad[0]
        ad_id = dict_ad_info[ad][0]
        position = 1 if position == 1 else 2
        advertiser_id = int(dict_ad_info[ad][1])
        price = int(dict_ad_info[ad][5])
        ad_tag = dict_ad_info[ad][4]
        user_tag = user_behavior[0][0]
        user_sex = user_behavior[0][1]
        list_ad_info.append([0, ad_id, position, advertiser_id, price, ad_tag, user_tag, user_sex])
    name = ['click', 'ad_id', 'position', 'advertiser_id', 'price', 'ad_tag', 'user_tag', 'user_sex']
    
    df_ad_info = pd.DataFrame(list_ad_info, columns=name)
    
    # origin+ad_set的特征组合，pandas操作
    origin_add_test = pd.concat([origin, df_ad_info])
    origin_add_test.reset_index(inplace=True)
    origin_add_test.drop(['index'], axis=1, inplace=True)
    
    # 特征组合
    f = feature_engineering(origin_add_test)
    
    # 预测概率
    prob = predict(model, f)
    
    return prob
        
 
def main():
    # 获得所有用户的定向信息
    user_behavior = db.get_user_behavior("all")
    
    # 获得ad_info数据库信息
    ad_info = open("ad_info.pkl", 'rb')
    dict_ad_info = pickle.load(ad_info)
    load_ad_info(dict_ad_info, [['Unknown', 'Unknown']])
    
    # 读取origin数据， 37*8
    origin_features = open("f_origin_8features.pkl", "wb")
    origin = pickle.load(origin_features)
    
    
    # *****************here***************
    # 读取ctr_log，作为CTR模型训练数据
    ctr_log = load_ctr_log()
    origin_add_train = pd.concat([origin, ctr_log])
    origin_add_train.reset_index(inplace=True)
    origin_add_train.drop(['index'], axis=1, inplace=True)
    
    # 对origin_add_train做特征工程
    origin_add_train = feature_engineering(origin_add_train)
    
    # 训练模型
    LR = fit_model(origin_add_train)
    
    # 对每类用户属性(tag, sex)都获得其候选广告集prior, post
    for cur in user_behavior:
        prior, post = recSys.get_prior_and_post_ads([cur])
        
        # 对prior，若有推荐结果，则算CTR并排序，否则返回默认广告
        if len(prior):

            # 获得候选广告的概率
            prob_prior = get_ad_prob(prior, dict_ad_info, user_behavior, 1, origin, LR)
            
            # 排序，得到rank
            list_prior = []
            for cur_prob in prob_prior:
                list_prior.append(cur_prob[1])
            temp = zip(list_prior, prior)
            temp.sort(key=lambda x: x[0], reverse=True)
            list_prior = [i[1][0] for i in temp][:5]
        else:
            list_prior = ["skin01", "skin05", "skin09", "digital01", "digital05"]
        if len(post):
            # 获得候选广告的概率
            prob_post = get_ad_prob(post, dict_ad_info, user_behavior, 2, origin, LR)
            
            # 排序，得到rank
            list_post = []
            for cur_prob in prob_post:
                list_post.append(cur_prob[1])
            temp = zip(list_post, post)
            temp.sort(key=lambda x: x[0], reverse=True)
            list_post = [i[1][0] for i in temp][:5]
        else:
            list_post = ["shoes01", "shoes07", "shoes04", "shoes10", "digital09"]
        
        #print "########"
        #print cur
        db.insert_offline_rec(cur, list_prior, list_post)
        #print 'OFFLINE_REC DONE!'
        #print ""
    print "3. ctr.py DONE..."
    print "The ads have been updates..."
    
    
if __name__ == "__main__":
    main() 
