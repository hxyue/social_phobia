# coding=utf-8

import xlrd
import pickle
import pandas as pd
import os
import json
import jieba
import jieba.posseg as pseg #词性标注
import jieba.analyse as anls #关键词提取


def get_follower():
    """
    获取粉丝信息
    :return:
    """
    follower_pd = pd.read_excel('../Data/follower.xlsx')
    return follower_pd


def get_following():
    """
    获取关注者信息
    :return:
    """
    following_pd = pd.read_excel('../Data/following.xlsx')
    return following_pd


def get_blog_content():
    """
    获取微博内容详情
    :return:
    """
    file_name = '../Data/Processed/blog_content'
    if os.path.exists(file_name):
        return read_pickle_data(file_name)
    blog_detail_1_pd = pd.read_excel('../Data/blog_content-1.xlsx')
    blog_detail_2_pd = pd.read_excel('../Data/blog_content-2.xlsx')
    blog_content_pd = pd.concat([blog_detail_1_pd, blog_detail_2_pd])
    with open(file_name, 'wb') as f:
        pickle.dump(blog_content_pd, f)
    return blog_content_pd


def get_comments():
    """
    获取微博用户评论
    :return:
    """
    file_name = '../Data/Processed/comments'
    if os.path.exists(file_name):
        return read_pickle_data(file_name)
    filePath = '../Data/blog_comment/'
    names = ['博主头像', '博主id', '博主', '博主主页', '评论内容', '发布时间', '点赞数', '回复数',
             '<fullpath>', '<createdate>']
    comments = pd.DataFrame([], columns=names)
    for filename in os.listdir(filePath):
        f = filePath + filename
        comments = pd.concat([comments, pd.read_excel(f)])
    comments['origin_blog_id'] = comments['<fullpath>'].map(lambda x: x.split('&type')[0])
    comments['origin_user_id'] = comments['<fullpath>'].map(lambda x: x.split('/')[3])
    with open(file_name, 'wb') as f:
        pickle.dump(comments, f)
    return comments

def pre_filter():
    """
    对获取的样本进行特征预处理：
    1.过滤特征数值全部一致（包括全空的特征）
    2.
    :return:
    """



def get_user_profile():
    """
    获取微博用户基础信息
    :return:
    """
    user_profile_df = []
    with open("../Data/user_detail.json", 'r') as load_f:
        load_dict = json.load(load_f)
    for id in load_dict.keys():
        user_profile = load_dict[id]['weiboData']
        if user_profile.__contains__('status'):
            user_profile.pop('status')
        user_profile['survey_data'] = load_dict[id]['surveyData']
        user_profile['survey_sum_score'] = sum(map(eval, load_dict[id]['surveyData']))
        user_profile_df.append(user_profile)
    print(user_profile_df)
    user_profile_df = pd.DataFrame(user_profile_df)
    #with open('../Data/Processed/user_profile', 'wb') as f:
        #pickle.dump(user_profile_df, f)
    return user_profile_df

def read_pickle_data(file_name):
    with open(file_name,'rb')as f:
        a = pickle.load(f)
        return a


if __name__ == '__main__':

    user_profile_df = get_user_profile()
    blog_content_df = get_blog_content()
    print(blog_content_df)
    print(blog_content_df.columns)
    choiceres = blog_content_df.pivot_table(values='博文', index='博主', aggfunc=lambda x: x.str.cat(sep='\n'))
    print(choiceres['博文'])
    seg_list = jieba.cut_for_search("他毕业于上海交通大学机电系，后来在一机部上海电器科学研究所工作")
    print("【搜索引擎模式】：" + "/ ".join(seg_list))