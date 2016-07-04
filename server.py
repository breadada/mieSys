# ---------------------------------------------------|
# Project Name : mieSys.                             |
# Description : A minimal display advertising system.|
# Author : 曾宪超(面包包包包包包)                    |
# time : 2016-07-04                                  |
# ---------------------------------------------------|


#coding:utf-8
from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
from flask.ext.script import Manager
import datetime
import db
import random
import recSys
import ctr

_EXPIRE_TIME = datetime.datetime.strptime("2020-12-31", "%Y-%m-%d")
app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def index():
    ip = request.remote_addr
    uid = request.headers.get('Cookie')   
    time = datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')
    print 'start'    
    cookie_set = db.get_cookies()
    print 'end'
    if uid == None:
    """
    # new user, do the following steps.
    # 1. set cookies to label this user.
    # 2. return default ads which contains all types and price.
    # 3. show pages.
    # 4. record arr_log and user_tag
    """
        
    
    #set cookies
        cookie = random.randint(0, 10000000)
        while cookie in cookie_set:
            cookie = random.randint(0, 10000000)
        user_profile = "Unknown"
        user_sex = "Unknown"
       
        #return default template
        ad_set_prior = ["skin01", "skin05", "skin09", "digital01", "digital05"]
        ad_set_post = ["shoes01", "shoes07", "shoes04", "shoes10", "digital09"]
        ad_set = ad_set_prior + ad_set_post
        
        user_behavior = [[user_profile, user_sex]]
    
        db.insert_ctr_log(ad_set, user_behavior, str(cookie))
        
        #show pages
        response = make_response(render_template('index_default.html', ad_set_prior = ad_set_prior, ad_set_post = ad_set_post)+ "<h1>Welcome to MieSys!</h1>")
        response.set_cookie('uid', str(cookie), expires=_EXPIRE_TIME)
       
        #default user profiling and insert arr_log & user_tag
        instance = [cookie, ip, time, user_profile, user_sex]
        db.insert_instance_table(instance, "arr_log")
        instance = [cookie, user_profile, user_sex]
        db.insert_instance_table(instance, "user_tag")
        return response

    else:
    """
    # old user, recommand ads
    # 1. check tag and sex which labeled by Behavioural Targeting.
    # 2. get recommand ads by recSys and CTR model.
    # 3. set impression time=10m to update click_log
    """


        #get user_behavior
        user_behavior = db.get_user_behavior(uid)
        user_tag = user_behavior[0][0]
        user_sex = user_behavior[0][1]
        user_sex = "male" if user_sex == '1' else 'female'
        addition = "Your tag is:<strong>"+user_tag+"</strong>, and your sex is: <strong>"+user_sex +"</strong>"
        
    #get recommand ad_set
        ad_prior, ad_post = recSys.get_prior_and_post_ads(user_behavior)
        ad_set_prior, ad_set_post = db.get_ranking_ads(user_behavior)
        ad_set_prior = ad_set_prior.split(",")
        ad_set_post = ad_set_post.split(",")        
        # print '2~~~~here'
    # HERE,时间格式不对，是Thu Dec  3 22:15:59 2015，而不是12/03/15,明天试试linux上的datetime，然后更改成我要的格式
        last_arr_time = datetime.datetime.strptime(db.get_last_arr_time(uid[4:]), "%m/%d/%y %H:%M:%S") 
    this_arr_time = datetime.datetime.strptime(time, "%m/%d/%y %H:%M:%S")
        delta = this_arr_time - last_arr_time
        if delta.seconds > 10: 
            ad_set = ad_set_prior + ad_set_post
            db.insert_ctr_log(ad_set, user_behavior, uid[4:])
        else:
            pass
        
        #update arr_log
        instance = [uid[4:], ip, time, user_behavior[0][0], user_behavior[0][1]]
        db.insert_instance_table(instance, "arr_log")
        
        #show pages
        response = make_response(render_template('index_recommand.html', ad_set_prior = ad_set_prior, ad_set_post = ad_set_post)+ "<h1>Welcome Back! " + addition +"</h1>")

        return response
    

@app.route('/click/<img_id>')
def click(img_id):
    """
    # 1. store the ad which the user clicked.
    # 2. redirect(302) to the main page to make sure function index() works.
    """
    from flask import redirect
    from flask import url_for
    uid = request.headers.get('Cookie')[4:]
    ad_id = img_id
    instance = [uid, ad_id]
    db.insert_instance_table(instance, "user_click")
    db.update_ctr_log(uid, ad_id)
    return redirect(url_for('index'))
 

    
if __name__ == '__main__':
    manager.run()   
    #app.run(debug="True")
