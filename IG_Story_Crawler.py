import pandas as pd
from datetime import *
from instagrapi import Client
import os
from time import sleep
import time
import re

# 從第幾筆資料開始
start_from = 0
# 開始時間
start = time.time()
# 載入KOL資料
data_file = '美賣網紅IG_userID - 已啟用且有IG網紅.csv'
# KOL_list = pd.read_csv('/Users/suenweixiang/Downloads/美賣網紅IG_userID.csv')
KOL_list = pd.read_csv(f'/Users/suenweixiang/Downloads/{data_file}')
all_KOL_count = len(KOL_list[start_from:])

# 登入帳號
cl = Client()
# cl.login('suenweixiang@gmail.com', 'Actegey192ct')
cl.login('sean.sun@meimaii.com','actegey192ct')
error_KOL = []
# 爬取Data
today = datetime.today().date() # 今天日期
yesterday = (today + timedelta(-1)) # 昨天日期
file_path_today = f'/Users/suenweixiang/Desktop/MeiMaii_KOL_IGStory/{today}' # 儲存資料夾路徑
if not os.path.isdir(file_path_today):
    os.makedirs(file_path_today) # 如果不存在資料夾，建立資料夾
file_path_yesterday = f'/Users/suenweixiang/Desktop/MeiMaii_KOL_IGStory/{yesterday}'
if not os.path.isdir(file_path_yesterday):
    os.makedirs(file_path_yesterday)
n = 0
for i in KOL_list.values[start_from:]:
    n += 1
    KOL_name = i[2]
    KOL_ig_username = i[1]
    try:
        KOL_id = cl.user_info_by_username(KOL_ig_username).dict()['pk'] # 取得 KOL_id(pk)
        story_data = cl.user_stories(KOL_id) # KOL 限動清單
        id2day = 0
        idyester = 0
        for j in story_data:
            date = j.dict()['taken_at'] # 限動建立時間
            if date.date() == datetime.today().date():
                id2day += 1 # 動態序號
                story_id = j.dict()['pk'] # 動態id(pk)
                if not os.path.isdir(f'/Users/suenweixiang/Desktop/MeiMaii_KOL_IGStory/{today}/【{i[0]}】{KOL_name}'):
                    os.makedirs(
                        f'/Users/suenweixiang/Desktop/MeiMaii_KOL_IGStory/{today}/【{i[0]}】{KOL_name}')
                file_name = re.findall("(.*)\+", str(date))[0]
                cl.story_download(
                    story_id, f"{file_name}", f'/Users/suenweixiang/Desktop/MeiMaii_KOL_IGStory/{today}/【{i[0]}】{KOL_name}')
                print(f'{KOL_name} {today} 第{id2day}篇完成')
                sleep(5)
            else:
                idyester += 1
                story_id = j.dict()['pk']
                if not os.path.isdir(f'/Users/suenweixiang/Desktop/MeiMaii_KOL_IGStory/{yesterday}/【{i[0]}】{KOL_name}'):
                    os.makedirs(
                        f'/Users/suenweixiang/Desktop/MeiMaii_KOL_IGStory/{yesterday}/【{i[0]}】{KOL_name}')
                file_name = re.findall("(.*)\+", str(date))[0]
                cl.story_download(story_id, f"{file_name}",
                                  f'/Users/suenweixiang/Desktop/MeiMaii_KOL_IGStory/{yesterday}/【{i[0]}】{KOL_name}')
                print(f'{KOL_name} {yesterday} 第{idyester}篇完成')
                sleep(5)
        print(
            f'＊＊＊＊＊＊＊＊＊＊ {KOL_name}的限動抓取完畢，{today}有{id2day}篇，{yesterday}有{idyester}篇，總共{idyester+id2day}篇，已完成{n}位，共{all_KOL_count}位KOL，進度{ (round(n/all_KOL_count , 4)) * 100}％ ＊＊＊＊＊＊＊＊＊＊')
        print("已過", round((time.time()-start) / 60, 2), "mins")

    except:
        error_KOL.append(
            {
                'KOL_id': i[0],
                'KOL_ig': i[1],
                'KOL_name': i[2]
            }
        )
        print(f'＊＊＊＊＊＊＊＊＊＊【{i[0]}】{i[2]}', "找不到資料", "\n", 'IG_UserName：', KOL_ig_username,
              f' 已完成{n}位，共{all_KOL_count}位KOL，進度{ (round( n/all_KOL_count, 4)) * 100}％ ＊＊＊＊＊＊＊＊＊＊')
        print("已過", round((time.time()-start) / 60, 2), "mins")
