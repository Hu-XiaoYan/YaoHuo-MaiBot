from nonebot import on_command
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import MessageSegment
import os,urllib.request,json,sqlite3
from PIL import Image,ImageDraw,ImageFont

FilePath=f"file:///{os.getcwd()}/yaohuo_bot/src"
FilePath_nohead=f"{os.getcwd()}/yaohuo_bot/src"
#全局路径函数
SDict={}
#用于支持GetSongJson方法使用的全局函数

def GetSongJson(Turn:int=0):
    '''
    用于获取歌曲信息,Turn控制是否反转ID和歌曲名和歌曲图片
    '''
    response=urllib.request.urlopen(url="https://www.diving-fish.com/api/maimaidxprober/music_data")
    All_Songs=json.loads(response.read())
    #从水鱼查分器拉取歌曲信息
    for x in range(len(All_Songs)):
        if Turn==0:
            NowSongInfo=All_Songs[x]

#>>>
            if "sølips" in NowSongInfo["title"]:
                title="solips"
            elif "GIGANTØMAKHIA" in NowSongInfo["title"]:
                title="GIGANTOMAKHIA"
            else:
                title=NowSongInfo["title"]
            #将ø转化成o，简单粗暴
#>>>
#此段代码待优化

            NowSongInfo=All_Songs[x]
            stype=NowSongInfo["type"]
            sid=NowSongInfo["id"]
            sid_int=int(NowSongInfo["id"])
            #这里转成int方便格式化字符串
            basic_info=NowSongInfo["basic_info"]
            artist=basic_info["artist"]
            ds_list=NowSongInfo["ds"]
            ds_str=""
            for element in ds_list:
                ds_str=f"{element}/{ds_str}"
                #小循环拆一下定数信息
            info=[title,sid,"https://www.diving-fish.com/covers/{:05}.png".format(sid_int),stype,artist,ds_str]
            #歌曲标题，歌曲ID，谱面类型，作曲家，定数信息
            SDict[title]=info
            x+=1
        else:
            NowSongInfo=All_Songs[x]
            title=NowSongInfo["title"]
            sid=NowSongInfo["id"]
            SDict[sid]=title
            #反查只有ID不需要转换
            x+=1   
    #循环创建字典SDict
#获取曲目Json信息

DanTable=on_command("段位认定",aliases={"dan"},priority=10)
@DanTable.handle()
async def DanTable_fanc(event:Event):
    usr_mes=event.get_plaintext().split(" ")
    usr_id=event.get_user_id()
    try:
        if usr_mes[1]=="1":
            await DanTable.finish(MessageSegment.image(f"{FilePath}/DanTable/1.jpg"))
        elif usr_mes[1]=="2":
            await DanTable.finish(MessageSegment.image(f"{FilePath}/DanTable/2.jpg"))
        else:
            await DanTable.finish(MessageSegment.at(usr_id)+"\n自己检查一下有什么没填对罢~\n"+MessageSegment.image(f"{FilePath}/FaceImage/白露骂人.jpg"))
    #段位图By:Team miComet
    except IndexError:
        await DanTable.finish("命令格式:\n段位认定/dan 1/2\n当前段位版本:UniversePlus")
    #这边其实挺玄学的,不加IndexError也会输出有错误但是控制台很正常?
    #好在如果什么都不输会IndexError

SearchSong=on_command("查歌",aliases={"search"},priority=10)
@SearchSong.handle()
async def SearchSong_fanc(event:Event):
    usr_id=event.get_user_id()
    usr_mes=event.get_plaintext().split(" ")
    try:
        stitle=usr_mes[1]
        GetSongJson()
        Searched_Songs={}
        _No=0
        song_titles=list(SDict.keys())
        for element in song_titles:
            #将字典中的所有键(歌曲名)创建成列表
            re_element=element.replace(" ","")
            #忽略空格
            if stitle.lower() in re_element.lower():
                Searched_Songs[_No]=(SDict[element])
                _No+=1
        if len(Searched_Songs)==0:
            await SearchSong.finish(MessageSegment.at(usr_id)+"\n未找到相应歌曲,请重试!\n"+MessageSegment.image(f"{FilePath}/FaceImage/气死辣.gif"))
        bg=Image.open(f"{FilePath_nohead}/Pic/bg.png")
        bg_ssd=Image.open(f"{FilePath_nohead}/Pic/song_sd_bg.png")
        bg_sdx=Image.open(f"{FilePath_nohead}/Pic/song_dx_bg.png")
        #导入背景，歌曲框
        search_info=ImageDraw.Draw(bg)
        font=ImageFont.truetype(FilePath_nohead+"/Pic/Font_Main.ttf",70)
        search_info.text((520,915),f"搜索结果:{stitle}",(0,0,0),font)
        #输出用户搜索的信息
        x=175
        y=1250
        #图片起点位置

        def sd_song_proc():
            bg.paste(bg_ssd,[x,y],bg_ssd)
            pic_resize=img_.resize((175,175))
            bg.paste(pic_resize,[x+25,y+52],pic_resize)
            info_text=ImageDraw.Draw(bg)
            info_text.text((x+5,y+6),f"ID:{SongInfo[1]}",(0,0,0),font)
            #处理图片信息
            if len(SongInfo[0])>14:
                info_text.text((x,y+250),SongInfo[0][0:14]+"...",(0,0,0),font)
            else:
                info_text.text((x,y+250),SongInfo[0],(0,0,0),font)
            #标题过长处理
            info_text.text((x,y+310),SongInfo[5],(0,0,0),font)
            #定数信息处理
            if len(SongInfo[4])>14:
                info_text.text((x,y+280),SongInfo[4][0:14]+"...",(0,0,0),font)
            else:
                info_text.text((x,y+280),SongInfo[4],(0,0,0),font)
            #作曲家信息处理
        def dx_song_proc():
            bg.paste(bg_sdx,[x,y],bg_sdx)
            pic_resize=img_.resize((175,175))
            bg.paste(pic_resize,[x+23,y+55],pic_resize)
            info_text=ImageDraw.Draw(bg)
            info_text.text((x+115,y+8),f"ID:{SongInfo[1]}",(0,0,0),font)
            if len(SongInfo[0])>14:
                info_text.text((x,y+250),SongInfo[0][0:14]+"...",(0,0,0),font)
            else:
                info_text.text((x,y+250),SongInfo[0],(0,0,0),font)
            info_text.text((x,y+310),SongInfo[5],(0,0,0),font)
            if len(SongInfo[4])>14:
                info_text.text((x,y+280),SongInfo[4][0:14]+"...",(0,0,0),font)
            else:
                info_text.text((x,y+280),SongInfo[4],(0,0,0),font)
            #同上
        def pic_proc():
            if SongInfo[3]=="SD":
                sd_song_proc()
            else:
                dx_song_proc()
            #二次封装(呃啊我是菜狗)

        if len(Searched_Songs)>25:
            await SearchSong.finish(MessageSegment.at(usr_id)+"\n搜索内容过多,请缩小搜索范围!\n"+MessageSegment.image(f"{FilePath}/FaceImage/气死辣.gif"))
        else:
            for _count in range(len(Searched_Songs)):
                if _count>len(Searched_Songs):
                    break
                #处理完图片跳出循环
                SongInfo=Searched_Songs[_count]
                path=FilePath_nohead+"/Song_Pic"
                font=ImageFont.truetype(FilePath_nohead+"/Pic/Font_Main.ttf",30)
                #导入字体,以及被搜索到的歌曲信息
                if os.path.exists(path)==False:
                    os.makedirs(path)
                if os.path.exists(f"{path}/{SongInfo[1]}.png")==False:
                    urllib.request.urlretrieve(SongInfo[2],f"{FilePath_nohead}/Song_Pic/{SongInfo[1]}.png")
                #创建文件夹以储存歌曲图片信息
                #理论上只有第一次查询速度较慢(因为要缓存图片)后续查询就快了
                img_=Image.open(f"{path}/{SongInfo[1]}.png")
                #导入歌曲图片
                if _count<5:
                    pic_proc()
                    x+=350
                elif _count>=5 and _count<10:
                    if x==1925:
                        x=175
                        y+=350
                    pic_proc()
                    x+=350
                elif _count>=10 and _count<15:
                    if x==1925:
                        x=175
                        y+=350
                    pic_proc()
                    x+=350
                elif _count>=15 and _count<20:
                    if x==1925:
                        x=175
                        y+=350
                    pic_proc()
                    x+=350
                elif _count>=20 and _count<25:
                    if x==1925:
                        x=175
                        y+=350
                    pic_proc()
                    x+=350
                #处理图片(5行)
        bg.save(f"{FilePath_nohead}/Search_{usr_id}.png")
        await SearchSong.send(MessageSegment.at(usr_id)+"\n"+MessageSegment.image(f"{FilePath}/Search_{usr_id}.png"))
        os.remove(f"{FilePath_nohead}/Search_{usr_id}.png")
        #保存,发送,删除一条龙服务
    except IndexError:
        await SearchSong.finish("命令格式 查歌/search 歌曲名或全称的一部分")

TrackPreview=on_command("曲目预览",aliases={"preview"},priority=10)
@TrackPreview.handle()
async def TrackPreview_fanc(event:Event):
    usr_id=event.get_user_id()
    usr_msg=event.get_plaintext().split(" ")
    sid=usr_msg[1]
    GetSongJson(1)
    #获取反转后的字典
    try:
        trackname=SDict[sid]
        await TrackPreview.send(f"正在加载...\n{trackname}")
        #输出将要播放的歌曲
        if os.path.exists(f"{FilePath[8:]}/T_Preview/{sid}.mp3")==False:
            await TrackPreview.finish(MessageSegment.at(usr_id)+"\n未找到你想要的曲目,可能是还没有添加?\n"+MessageSegment.image(f"{FilePath}/FaceImage/呜哇呜哇.jpg"))
        else:
            await TrackPreview.finish(MessageSegment.record(f"{FilePath}/T_Preview/{sid}.mp3"))
    except KeyError:
        await TrackPreview.finish(MessageSegment.at(usr_id)+"\n你是不是输了什么奇奇怪怪的东西?\n或者ID没对，请检查~\n"+MessageSegment.image(f"{FilePath}/FaceImage/呜哇呜哇.jpg"))
    #过滤一下不是曲目ID的东西(
    except IndexError:
        await TrackPreview.finish("命令格式 曲目预览/preview 乐曲ID")
#乐曲预览

Area_Introduce=on_command("区域介绍",aliases={"areai"},priority=10)
@Area_Introduce.handle()
async def Area_Introduce_fanc(event:Event):
    usr_msg=event.get_plaintext().split(" ")
    usr_id=event.get_user_id()
    geted_list=[]
    try:
        a_name=usr_msg[1]
        conn=sqlite3.connect(f"{FilePath_nohead}/A_Introduce/A_DataBase.db")
        cur=conn.cursor()
        cur.execute("SELECT NAME FROM A_Info")
        name_list_cur=cur.fetchall()
        for _count in range(len(name_list_cur)): 
            name_getting=name_list_cur[_count]
            name=name_getting[0]
            geted_list.append(name)
            _count+=1
        for element in geted_list:
            if a_name==element:
                cur.execute(f"SELECT PATH FROM A_Info WHERE NAME='{a_name}'")
                path_cur=cur.fetchall()
                path_getting=path_cur[0]
                path=path_getting[0]
                await Character_Introduce.finish(MessageSegment.image(f"{FilePath}{path}"))
            else:
                await Character_Introduce.finish(MessageSegment.at(usr_id)+f"\n你要找的区域好像还没有被添加哦~\n当前可查的区域列表:{geted_list}\n"+MessageSegment.image(f"{FilePath}/FaceImage/owo.jpg"))
    except IndexError:
        await Character_Introduce.finish(f"命令格式 区域介绍/areai 区域名")

Character_Introduce=on_command("角色介绍",aliases={"chari"},priority=10)
@Character_Introduce.handle()
async def Character_Introduce_fanc(event:Event):
    usr_msg=event.get_plaintext().split(" ")
    usr_id=event.get_user_id()
    geted_list=[]
    try:
        c_name=usr_msg[1]
        conn=sqlite3.connect(f"{FilePath_nohead}/C_Introduce/C_DataBase.db")
        cur=conn.cursor()
        cur.execute("SELECT NAME FROM C_Info")
        name_list_cur=cur.fetchall()
        for _count in range(len(name_list_cur)): 
            name_getting=name_list_cur[_count]
            name=name_getting[0]
            geted_list.append(name)
            _count+=1
        for element in geted_list:
            if c_name==element:
                cur.execute(f"SELECT PATH FROM C_Info WHERE NAME='{c_name}'")
                path_cur=cur.fetchall()
                path_getting=path_cur[0]
                path=path_getting[0]
                await Character_Introduce.finish(MessageSegment.image(f"{FilePath}{path}"))
            else:
                await Character_Introduce.finish(MessageSegment.at(usr_id)+f"\n你要找的角色好像还没有被添加哦~\n当前可查的角色列表:{geted_list}\n"+MessageSegment.image(f"{FilePath}/FaceImage/owo.jpg"))
    except IndexError:
        await Character_Introduce.finish(f"命令格式 角色介绍/chari 角色名")

Help=on_command("帮助",aliases={"help"},priority=10)
@Help.handle()
async def Help_fanc():
    await Help.finish(
"""尧火Bot菜单 V0.5 Alpha
1.段位认定/dan 1/2
  查看段位认定表 1表 2里
  当前段位版本:UniversePlus
2.查歌/search 歌曲标题(或一部分) 查询符合条件的歌曲
  可以不含空格,o=ø
3.曲目预览/preview 歌曲ID 播放歌曲预览
4.区域介绍/areai 区域名 查看区域介绍
  个人汉化,渣翻勿介
5.角色介绍/chari 角色名
  同上""")
#输出帮助信息(文字版)