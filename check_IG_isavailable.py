from instagrapi import Client
import pandas as pd

data_file = '美賣網紅IG_userID - 已啟用且有IG網紅.csv'
KOL_list = pd.read_csv(f'/Users/suenweixiang/Downloads/{data_file}')
KOL_IG_list = []
with open(f'/Users/suenweixiang/Downloads/{data_file}','r') as f:
    for i in f.readlines()[1:]:
        try:
            id = i.split(',')[0]
            ig = i.split(',')[1]
            name = i.split(',')[2]
            # print(f'ID : {id}, IG : {ig}, Name : {name}')
            KOL_IG_list.append(
                {
                    'id' : id,
                    'ig' : ig,
                    'name' : name
                }
            )
        except:
            continue
cl = Client()
# cl.login('suenweixiang@gmail.com', 'Actegey192ct')
cl.login('sean.sun@meimaii.com','actegey192ct')

KOL_IG_ID = []
KOL_IG_Unavailable = []
for i in KOL_IG_list[0:10]:
    try:
        id = i['ig'].strip('\n')
        KOL_IG_ID.append(
            {
                'KOL_id': i['id'],
                'KOL': i['name'].strip("\n"),
                'user_name': i['ig'].strip("\n"),
                'ig_id': cl.user_id_from_username(id)
            }
        )
    except:
        KOL_IG_Unavailable.append(
            {
                'KOL_id': i['id'],
                'KOL': i['name'].strip("\n"),
                'user_name': i['ig'],
                'ig_id': 'Not Found'
            }

        )

pd.DataFrame(KOL_IG_ID).to_csv('/Users/suenweixiang/Desktop/valid_ig.csv',index=False)
pd.DataFrame(KOL_IG_Unavailable).to_csv('/Users/suenweixiang/Desktop/invalid_ig.csv',index=False)

