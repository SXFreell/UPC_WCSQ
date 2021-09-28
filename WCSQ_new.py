import json
import requests
from upc_login import login
import datetime
import urllib.parse

user = ""
password = ""

now = datetime.datetime.now()+datetime.timedelta(days=-1)
today = now.strftime("%Y-%m-%d")+"T16:00:00.000Z"

session = login(user, password)
session.get("https://service.upc.edu.cn/site/user/get-name")

t_info_ = session.get("https://service.upc.edu.cn/site/process/start-info?app_id=458&node_id=")
t_info = t_info_.json()["d"]["nodes"][3]
node_key = t_info["act_node_id"]
uids = [str(i["id"]) for i in t_info["assignee"]]

r = session.get("https://service.upc.edu.cn/site/form/start-data?app_id=458&node_id=&draft=1")
data = r.json()["d"]["data"]["1259"]
data["Calendar_20"]=today

Info = {
    "app_id":"458",
	"node_id":"",
	"form_data":{
        "1259":data
    }
}

Info["special_approver"] = [
		{
			"node_key":node_key,
			"uids":uids
		}
	]

header = {
	"Content-Type": "application/x-www-form-urlencoded"
}

Info_en="data="+urllib.parse.quote(str(Info).replace("'",'"').replace(" ",""))

r = session.post('https://service.upc.edu.cn/site/apps/launch',data=Info_en,headers=header)
