import base64
import time
import requests
import json
from PIL import Image


def request(USERNAME:str):
    response = requests.get("https://api.mojang.com/users/profiles/minecraft/"+USERNAME)
    response.encoding = "UTF-8"
    print(response.text)
    a = json.loads(str(response.text))
    id = a["id"]
    time.sleep(1)
    response = requests.get("https://sessionserver.mojang.com/session/minecraft/profile/"+id)
    print(response.text)
    response.encoding = "UTF-8"
    b = json.loads(str(response.text))
    skill = b["properties"][0]["value"]
    textures = json.loads(base64.b64decode(skill))
    print(textures)
    time.sleep(1)
    response = requests.get(textures["textures"]['SKIN']['url']).content
    # response.encoding = "UTF-8"
    open("./static/img/head/"+USERNAME+".png","wb").write(response)
def cut(USERNAME):
    # 打开图片
    img = Image.open("./static/img/head/"+USERNAME+".png")

    # 图片的裁剪区域（区域左上角的坐标为(100, 100)，右下角的坐标为(300, 300)）
    crop_area = (8, 8, 16, 16)

    # 裁剪并保存图片
    crop_img = img.crop(crop_area)
    crop_img.save("./static/img/head/"+USERNAME+".png")

def Generate():
    input("确定要生成吗？")

    a = json.loads(open('./static/json/main.json','r').read())

    s = []

    for i in a['个人']:
        for m in a['个人'][i]:
            for n in a['个人'][i][m]:
                if n not in s:
                    s.append(n)

    for h in s:
        request(h)
        cut(h)

#如果要安装main.js生成头像请再三确认
#Generate()