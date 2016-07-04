# ---------------------------------------------------|
# Project Name : mieSys.                             |
# Description : A minimal display advertising system.|
# Author : 曾宪超(面包包包包包包)                    |
# time : 2016-07-04                                  |
# ---------------------------------------------------|


#coding:utf-8
import db
import pickle

class UserBehavior(object):
    def __init__(self, uid, sex, tag):
        self.uid = uid
        self.sex = sex
        self.tag = tag
        
        
def get_db_user_click():
    # <dict> user1:set(ad1, ad2..)
    db_user_click = db.fetch("user_click")
    dict_user_click = {}
    for i in db_user_click:
        if dict_user_click.get(i[0], "no") == "no":
            dict_user_click[i[0]] = [i[1]]
        else:
            list_ad = dict_user_click[i[0]]
            if i[1] not in list_ad:
                list_ad.append(i[1])
                dict_user_click[i[0]] = list_ad
            else:
                pass
                
    return dict_user_click

    
def get_db_ad_info():
    # <dict> ad_id:tuple(ad_id, advertiser_id, position, path, sex, price)
    ad_info = db.fetch("ad_info")
    dict_ad_info = {}
    for ad in ad_info:
        if dict_ad_info.get(ad[0], "no") == "no":   
            dict_ad_info[ad[0]] = ad
        else:                                       
            pass
            
    return dict_ad_info

    
def get_user_behavior(dict_user_click, dict_ad_info):
    list_user_behavior = []     
    for cur_user in dict_user_click:
        # for every user, create an UserBehavior object
        class_userbehavior = UserBehavior(cur_user, '0', "New User")
        sex = 0
        tag = [0, 0, 0]
        
        # for each ad the user clicked, check the sex and tag attr.
        # We can determine by voting
        click_ads = dict_user_click[cur_user]
        for ad in click_ads:
            ad_sex = dict_ad_info[ad][3]
            ad_tag = dict_ad_info[ad][4]
            #print ad_sex, ad_tag
            if ad_sex == '1':        sex += 1
            elif ad_sex == '0':      sex -= 1
            if ad_tag == "skin":     tag[0] += 1
            elif ad_tag == "digital":tag[1] += 1
            elif ad_tag == "shoes":  tag[2] += 1   
        
        # More is better
        if sex > 0:     class_userbehavior.sex = '1'
        elif sex < 0:   class_userbehavior.sex = '0'
        else:           class_userbehavior.sex = "Unknown"
        
        if tag.index(max(tag)) == 0:         class_userbehavior.tag = "skin"
        elif tag.index(max(tag)) == 1:       class_userbehavior.tag = "digital"
        elif tag.index(max(tag)) == 2:       class_userbehavior.tag = "shoes"
        elif tag[0] == tag[1] == tag[2]:     class_userbehavior.tag = "Unknown"
        class_userbehavior.uid = cur_user
        list_user_behavior.append(class_userbehavior)
    
    return list_user_behavior
    
    
def main():
    dict_user_click = get_db_user_click()
    dict_ad_info = get_db_ad_info()
    # create pickle object to local hardware
    # output = open("ad_info.pkl", 'wb')
    # pickle.dump(dict_ad_info, output)
    # output.close()
    # print 'Pickle output done!'
    list_user_behavior = get_user_behavior(dict_user_click, dict_ad_info)
    for i in list_user_behavior:
        instance = [i.uid, i.tag, i.sex]
        # print instance
        db.update_userbehavior(instance, "user_tag")
	db.update_userbehavior(instance, "ctr_log")
    print "1. behavior_targeting.py DONE..."
    
    
if __name__ == "__main__":
    main()
    
