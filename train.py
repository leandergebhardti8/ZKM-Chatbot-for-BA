import os
import subprocess
import requests

print("start")
rasa_token = os.environ.get("RASA_AUTH_TOKEN", None)

os.system("cp -r models/* oldmodels/")
os.system("rm -rf models/*")
os.system("rasa train --debug")

model = subprocess.check_output("ls -t models", shell=True)
model = str(model, "utf-8")
last_model_name = model.split("\n")[0]

url = "http://rasa-production:5005/model?token=%s" % rasa_token
payload = {
        "model_file": last_model_name,
        "model_server": 
          {
              "url": "https://",
              "params": "",
              "headers": "",
              "basic_auth": "",
              "token": "",
              "token_name": "",
              "wait_time_between_pulls": 0
          },
        "remote_storage": "aws"
        }
update_model = requests.put(url , json=payload)
print("Training is done")
