import requests
import re


# No connection 就是被反爬了
'''
# 这是分析进入该网页的代码

# 确定m4s是视频还是音乐   观察响应里面的乱码 多还是少来确定音频还是视频
# 视频url
url='https://upos-sz-mirrorks3o1.bilivideo.com/upgcxcode/63/28/180942863/180942863_nb2-1-30032.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1615452069&gen=playurlv2&os=ks3o1bv&oi=1900716476&trid=1994cc2af0c447699430a368dd6503edu&platform=pc&upsig=010b36cb89994ab30776f71f96df0374&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=0&orderid=0,3&agrr=1&logo=80000000'
# 音频url
yy_url='https://upos-sz-mirrorcoso1.bilivideo.com/upgcxcode/63/28/180942863/180942863_nb2-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1615452069&gen=playurlv2&os=coso1bv&oi=1900716476&trid=1994cc2af0c447699430a368dd6503edu&platform=pc&upsig=ff7326bfb0aeef3231e57cb214292c72&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=0&orderid=0,3&agrr=1&logo=80000000'
# 请求头
headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45',
    'referer': 'https://www.bilibili.com/video/BV1oV411o7w7?from=search&seid=17188291390458568192'
}
# 请求视频
res=requests.get(url,headers=headers)
# 请求音频
data_res=requests.get(yy_url,headers=headers)
# 这个是视频
with open('b站视频.mp4','wb')as f:
    f.write(res.content)
# # 这个是音频
with open('b站音频.mp3','wb')as f:
    f.write(data_res.content)
'''


# 方法二
# # 访问单个视频页进行下载
# url=input('请输入你想要爬取的网站：')
url='https://www.bilibili.com/video/BV1da4y1n7Lc?from=search&seid=4167549961888405530'
headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45',
    'referer': 'https://search.bilibili.com/',
    'cookie': '_uuid=93C0930E-28F4-ECE7-C119-2E50AD4AA8D333579infoc; buvid3=D93CD4F3-D9CF-46B8-AD57-8CBA60B0291C18559infoc; CURRENT_FNVAL=80; blackside_state=1; LIVE_BUVID=AUTO5216149589958970; rpdid=|(um~u)llu~)0JuYuluk|RRu; CURRENT_QUALITY=32; bsource=search_baidu; finger=158939783; sid=6lymq8ko; PVID=1'
}

res=requests.get(url,headers=headers)
# print(res.content.decode())

# 利用正则提取网页的源代码的视频，音频数据url
# 去按下ctrl+shift+f去搜索一部分的 在网页中分析的url  不用全部复制下来，复制一部分就去搜索  然后点击{} 进行解刨数据
# 因为有一部分url搜索到的源代码可能会不同 就是清晰度的问题了  没登入一般提取第一个url就行了
# video就是视频的意思    audio 是音频的意思-

# 利用正则来进行提取  提取video下的代码   视频
video_url=re.findall(r'"baseUrl":"(.*?)",',res.content.decode())[0]  # 提取第一个就行了   因为收集的为列表索引为0  这里要注意最后的，逗号
# 找到 audio下面的第一个url进行正则提取  音频
audio_url=re.findall(r'"id":30280,"baseUrl":"(.*?)",',res.content.decode())[0]
# 获取电影名 必须的是唯一的   标题
title=re.findall(r'<title data-vue-meta="true">(.*?)</title>',res.content.decode())[0]
# # 视频的地址 获取到了 请求视频的地址 获取视频
video_res=requests.get(video_url,headers=headers)           # 请求访问视频的地址 获取视频 video_res.content
audio_res=requests.get(audio_url,headers=headers)          # 请求访问音频的地址 获取音频 audio_res.content


# 保存视频 保存音频
with open('%s.mp4'%title,'wb') as f:
    f.write(video_res.content)

with open('%s.mp3'%title,'wb') as f:
    f.write(audio_res.content)




# 导入模块来进行合并音频
from moviepy.editor import *
import time
# 读取视频文件 和读取音频文件
videoclip = VideoFileClip("%s.mp4"%title)

Audioclip = AudioFileClip("%s.mp3"%title)

# 给videoclip视频 添加音频Audioclip
video_data = videoclip.set_audio(Audioclip)

# 添加好了后 在输出为一个视频  这里的文件名不能冲突
video_data.write_videofile("bb.mp4")

