# ---------------------------------------------------|
# Project Name : mieSys.                             |
# Description : A minimal display advertising system.|
# Author : 曾宪超(面包包包包包包)                    |
# time : 2016-07-04                                  |
# ---------------------------------------------------|


#coding:utf-8
import db

def get_prior_and_post_ads(user_behavior):
    user_profile = user_behavior[0][0]
    user_sex = user_behavior[0][1]
     
    post = ['skin', 'shoes', 'digital', 'Unknown']
    prior = [user_profile]
    post.remove(user_profile)
    
    prior_set = db.get_relative_ads(prior, user_sex)
    post_set = db.get_relative_ads(post, user_sex)
    
    return prior_set, post_set

# get_prior_and_post_ads([['skin', '0']])
