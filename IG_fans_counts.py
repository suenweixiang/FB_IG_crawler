import requests,json
import pandas as pd
df_ig_id = pd.read_csv('~/Downloads/IG 網紅_id.csv')
ig_id_list_= []
# for i in df_ig_id.values:
for i in df_ig_id.values:
    keyword = i[1]
    form = {
    'st': '2021-01-01',
    'et': '2022-04-29',
    'q': json.dumps([f"user:{keyword}"]),
    'vw':'multiplechannel',
    "nation": 'TW',
    'channels': '["IG"]',
    'panels':'["LC","TC","HP","WC","HC","TL"]',
    'key': "1d7016605dcbd5fe717b61cd39c737bba4cc3095345557313eff8c92de45bd53"
}
    r = requests.get('https://api.qsearch.cc/api/trend/v1/posts', params=form)
    try:
        KOL_id = i[0]
        ig_id = i[1]
        name = r.json()['data'][0]['ig_raw'][0]['from_name']
        followers = r.json()['data'][0]['ig_raw'][0]['followers_count']
        print('KOL_id:',KOL_id,"IG_id:",ig_id,"KOL:",name,"followes:",followers)
        ig_id_list_.append({
            "KOL_id":KOL_id,'ig_name':name,"followers":followers
        })
    except:
        print("KOL_id,",i,"IG_id:","","name:","","followes:","")
        ig_id_list_.append({ "KOL_id":KOL_id,'ig_name':"","followers":""})
        continue