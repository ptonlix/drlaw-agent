import os

DOMAIN = "comm.chatglm.cn"
TEAM_TOKEN = os.environ.get("TEAM_TOKEN")

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {TEAM_TOKEN}"}
