
# 爬取抖音视频

# 1.在手机上找到一个抖音视频，右边有分享的箭头 -- 复制链接

    # 5.8 IV:/ %一条小团团ovo %绝地求生搞笑时刻 这几个跟我爸听的歌差不多。。
    # https://v.douyin.com/eBaXTLe/ 复制Ci鏈接，打開Dou音搜索，直接观看视频！

# 2.把链接复制到浏览器打开--跳转到视频的播放页
# url经过重定向生成比较长的一串地址，删除一些参数

# 变成：https://www.iesdouyin.com/share/video/6950029039302151438/?region=CN

# 3. 复制url中的6950029039302151438 ， 找到相关的数据包
# 4. 抓包 -- 视频url ： https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0300fg10000c1pnd5ivqu4jc78jikmg&ratio=720p&line=0
# 5. 发送请求，获取响应


import requests
import json
import jsonpath
# from jsonpath import jsonpath

# 视频播放页url
url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=6950029039302151438'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'
}


res = requests.get(url, headers=headers)
# print(res.text)  # json数据  -- str


# 获取抖音视频url链接
# 1.json数据转换为python数据
# result = json.loads(res.text)

result = res.json()
# print(type(result))   # --dict

# 2.通过jsonpath 提取数据
vd_url = jsonpath.jsonpath(result, '$..video.play_addr.url_list')[0][0]
# print(vd_url)

# vd_result = requests.get(vd_url, headers=headers)

# 有水印的视频
# with open('小团团.mp4', 'wb') as f:
#     f.write(vd_result.content)

# 去水印：  目前可以用这种方法，但是以后不一定
# 有水印的url：https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0300fg10000c1pnd5ivqu4jc78jikmg&ratio=720p&line=0
# 无水印的url：https://aweme.snssdk.com/aweme/v1/play/?video_id=v0300fg10000c1pnd5ivqu4jc78jikmg&ratio=720p&line=0


# 去掉水印  -- replace替换  (旧内容，新内容)
vd2_result = vd_url.replace('/playwm/', '/play/')
# print(vd2_result)
vd_result = requests.get(vd2_result, headers=headers)

with open('小团团无水印.mp4', 'wb') as f:
    f.write(vd_result.content)











