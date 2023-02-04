#!/usr/bin/env python3

##Designed by XueJingyuan/Platinum
##说明：在写入题库的功能中，未设计自动去除重复题的功能，相当于自动对高频错题自动进行了加权，使其容易被抽到(doge)
import pandas as pd
import xlwt 
import random
import time
##import string

print("本程序由NJMU2020级XueJingyuan设计，转载请注明出处。\n若出现bug可联系QQ:2465610238")

##以下是预处理
df=pd.read_excel("/Users/mac/Desktop/题库程序/题库.xls")
Platinum=1
print("\n现在是{}\n\n欢迎使用NJMU毛概自测程序V2.0".format(time.strftime("%Y年%m月%d日   %H时%M分%S秒", time.localtime())))
print("\nV2.0更新内容：选项随机排列功能,优化了显示界面\n")
print("\nTips:\n1.错题回顾不设次数限制\n2.如果直接关闭程序会导致错题无法记录\n3.请按设定输入字符!!!\n")
print("\n请选择功能：\n0.顺序做题\n1.随机抽题(不重复)\n2.错题回顾(顺序)\n3.清空错题库\n4.退出")
num=0
##主干程序
while Platinum==1:
    wb1=xlwt.Workbook()
    ws1=wb1.add_sheet("Sheet1")
    ws1.write(0,0,"目录")
    ws1.write(0,1,"题号")
    ws1.write(0,2,"章节")
    ws1.write(0,3,"题干")
    ws1.write(0,4,"选择A")
    ws1.write(0,5,"选择B")
    ws1.write(0,6,"选择C")
    ws1.write(0,7,"选择D")
    ws1.write(0,8,"答案")
    ws1.write(0,9,"题型")
    xl=pd.read_excel("/Users/mac/Desktop/题库程序/错题记录2.xls")
    for a in range(len(xl)):
        listwrong1=xl.values[a]
        for b in range(len(listwrong1)):
            if str(listwrong1[b])!="nan":
                ws1.write(a+1,b,listwrong1[b])
    num+=1
    if num!=1:
        print("\n请再次选择功能：\n0.顺序做题\n1.随机抽题(不重复)\n2.错题回顾(顺序)\n3.清空错题库\n4.退出")
    choose=input("\n请输入：")
    if choose=="0":
        serialnumber=0 #本题序号
        totalnumber=0   #总的题目数量
        rightnumber=0
        wrongnumber=len(xl)
        flag=True
        numlist=[]
        count=0
        totalstarttime=time.time()
        while flag==True:
            for randomnumber in range(len(df)):
                listcontent1=df.values[randomnumber]
                count+=1
                listcontent=[]
                newanswer=""
                for r in range(len(listcontent1)):
                    listcontent.append(listcontent1[r])
                newlist=[]
                chapter=listcontent[2]
                correctanswer=listcontent[8]
                correctcontent=[]
                print("\n当前进度{}/{}".format(count,len(df)))
                answerindex=0
                for t in correctanswer:
                    if t=="A":
                        answerindex=4
                    elif t=="B":
                        answerindex=5
                    elif t=="C":
                        answerindex=6
                    elif t=="D":
                        answerindex=7
                    elif t=="E":
                        answerindex=8
                    correctcontent.append(listcontent[answerindex])
                for a in range(len(listcontent)):
                        b=random.randint(4,7)
                        c=random.randint(4,7)
                        listcontent[b],listcontent[c]=listcontent[c],listcontent[b]
                newanswer=""
                newanswer1=""
                for u in listcontent:
                    if u in correctcontent:
                        w=listcontent.index(u)
                        if w==4:
                            newanswer1="A"
                        elif w==5:
                            newanswer1="B"
                        elif w==6:
                            newanswer1="C"
                        elif w==7:
                            newanswer1="D"
                        elif w==8:
                            newanswer1="E"
                        newanswer+=newanswer1
                print("目录:{} 题号:{} \n\n{}——{}\nA:{}\nB:{}\nC:{}\nD:{}".format(listcontent[0],listcontent[1],listcontent[9],listcontent[3],listcontent[4],listcontent[5],listcontent[6],listcontent[7]))
                newlist=listcontent[:8]+[newanswer]+[listcontent[9]]
                starttime=time.time()
                answer=input("请输入答案:")
                if len(answer)==1 and len(newanswer)!=1 and answer!="?" and answer!=" " and answer!="+1":
                    answer=input("本题是多选题！请再次输入答案：")
                if len(answer)!=1 and len(newanswer)==1 and answer!="?" and answer!=" " and answer!="+1":
                    answer=input("本题是单选题！请再次输入答案：")
                if answer=="+1":
                    rightnumber+=1
                    answer=input("请输入答案:")
                if answer=="?":
                    print("提示:本题是",len(newanswer),"选题")
                    answer=input("请再次输入答案：")
                endtime=time.time()
                usedtime=endtime-starttime #计算答题使用的时间

                if answer==newanswer or answer.upper()==newanswer: 
                    print("答案正确")
                    totalnumber+=len(newanswer)
                    rightnumber+=len(newanswer)
                    print("当前正确率{:.2f}%".format(rightnumber/totalnumber*100))
                elif answer=="": #退出
                    check=input("你真的要退出吗，输入1退出：")
                    if check=="1":
                        serialnumber=newlist[1]
                        flag=False
                        break
                elif str(answer)!=str(newanswer):
                    #将错题保存到用于存放错题的excel文件当中
                    
                    print("答案错误，本题答案是",newanswer)
                    
                    totalnumber+=len(newanswer)
                    wrongnumber+=1
                    print("当前正确率{:.2f}%".format(rightnumber/totalnumber*100))
                    for t in range(len(newlist)):
                        if str(newlist[t])!="nan":
                            ws1.write(wrongnumber,t,newlist[t])
                        else:
                            ws1.write(wrongnumber,t," ")
                print("本题用时{:.3f}s".format(usedtime))
            else:
                continue
        if totalnumber!=0:
            rate=rightnumber/totalnumber
            totalendtime=time.time()
            totaltime=totalendtime-totalstarttime
            wb1.save("/Users/mac/Desktop/题库程序/错题记录1.xls")
            print("\n本次做了{}题，正确率为{:.2f}%，共用时{:.1f}s，题均用时{:.1f}s".format(count,rate*100,totaltime,totaltime/count))
        wb2=xlwt.Workbook()
        ws2=wb2.add_sheet("Sheet1")
        ws2.write(0,0,"目录")
        ws2.write(0,1,"题号")
        ws2.write(0,2,"章节")
        ws2.write(0,3,"题干")
        ws2.write(0,4,"选择A")
        ws2.write(0,5,"选择B")
        ws2.write(0,6,"选择C")
        ws2.write(0,7,"选择D")
        ws2.write(0,8,"答案")
        ws2.write(0,9,"题型")
        md=pd.read_excel("/Users/mac/Desktop/题库程序/错题记录1.xls")
        for t in range(len(md)):
            listwrong=md.values[t]
            for i in range(len(listwrong)):
                if str(listwrong[7])!="nan":
                    ws2.write(t+1,i,str(listwrong[i]))
        wb2.save("/Users/mac/Desktop/题库程序/错题记录2.xls")  
        
        
    
    
    elif choose=="1":
        serialnumber=0
        totalnumber=0
        rightnumber=0
        wrongnumber=len(xl)
        flag=True
        numlist=[]
        count=0
        totalstarttime=time.time()
        while flag==True:
            randomnumber=random.randint(1,len(df)-1)
            listcontent1=df.values[randomnumber]
            if randomnumber not in numlist:
                numlist.append(randomnumber)
                count+=1
                listcontent1=df.values[randomnumber]
                ##listcontent的第3号是题干第4-8号为A-E选项，答案的索引是9，题型的索引是10，题号是2
                listcontent=[]
                newanswer=""
                for r in range(len(listcontent1)):
                    listcontent.append(listcontent1[r])
                newlist=[]
                chapter=listcontent[2]
                correctanswer=listcontent[8]
                correctcontent=[]
                print("\n当前进度{}/{}".format(count,len(df)))
                answerindex=0
                for t in correctanswer:
                    if t=="A":
                        answerindex=4
                    elif t=="B":
                        answerindex=5
                    elif t=="C":
                        answerindex=6
                    elif t=="D":
                        answerindex=7
                    elif t=="E":
                        answerindex=8
                    correctcontent.append(listcontent[answerindex])
                for a in range(len(listcontent)):
                        b=random.randint(4,7)
                        c=random.randint(4,7)
                        listcontent[b],listcontent[c]=listcontent[c],listcontent[b]
                newanswer=""
                newanswer1=""
                for u in listcontent:
                    if u in correctcontent:
                        w=listcontent.index(u)
                        if w==4:
                            newanswer1="A"
                        elif w==5:
                            newanswer1="B"
                        elif w==6:
                            newanswer1="C"
                        elif w==7:
                            newanswer1="D"
                        elif w==8:
                            newanswer1="E"
                        newanswer+=newanswer1
                print("目录:{} 题号:{} \n\n{}——{}\nA:{}\nB:{}\nC:{}\nD:{}".format(listcontent[0],listcontent[1],listcontent[9],listcontent[3],listcontent[4],listcontent[5],listcontent[6],listcontent[7]))
                newlist=listcontent[:8]+[newanswer]+[listcontent[9]]
                starttime=time.time()
                answer=input("请输入答案:")
                if len(answer)==1 and len(newanswer)!=1 and answer!="?" and answer!=" " and answer!="+1":
                    answer=input("本题是多选题！请再次输入答案：")
                if len(answer)!=1 and len(newanswer)==1 and answer!="?" and answer!=" " and answer!="+1":
                    answer=input("本题是单选题！请再次输入答案：")
                if answer=="+1":
                    rightnumber+=1
                    answer=input("请输入答案:")
                if answer=="?":
                    print("提示:本题是",len(newanswer),"选题")
                    answer=input("请再次输入答案：")
                endtime=time.time()
                usedtime=endtime-starttime
                if answer==newanswer or answer.upper()==newanswer:
                    print("答案正确")
                    totalnumber+=len(newanswer)
                    rightnumber+=len(newanswer)
                    print("当前正确率{:.2f}%".format(rightnumber/totalnumber*100))
                elif answer=="":
                    check=input("你真的要退出吗，输入1退出：")
                    if check=="1":
                        serialnumber=newlist[1]
                        flag=False
                        break
                elif answer==" ":
                    continue
                elif str(answer)!=str(newanswer):
                    print("答案错误，本题答案是",newanswer)
                    totalnumber+=len(newanswer)
                    wrongnumber+=1
                    print("当前正确率{:.2f}%".format(rightnumber/totalnumber*100))
                    for t in range(len(newlist)):
                        if str(newlist[t])!="nan":
                            ws1.write(wrongnumber,t,newlist[t])
                        else:
                            ws1.write(wrongnumber,t," ")
                print("本题用时{:.3f}s".format(usedtime))
            else:
                continue
        if totalnumber!=0:
            rate=rightnumber/totalnumber
            totalendtime=time.time()
            totaltime=totalendtime-totalstarttime
            wb1.save("/Users/mac/Desktop/题库程序/错题记录1.xls")
            print("\n本次做了{}题，正确率为{:.2f}%，共用时{:.1f}s，题均用时{:.1f}s".format(count,rate*100,totaltime,totaltime/count))
        wb2=xlwt.Workbook()
        ws2=wb2.add_sheet("Sheet1")
        ws2.write(0,0,"目录")
        ws2.write(0,1,"题号")
        ws2.write(0,2,"章节")
        ws2.write(0,3,"题干")
        ws2.write(0,4,"选择A")
        ws2.write(0,5,"选择B")
        ws2.write(0,6,"选择C")
        ws2.write(0,7,"选择D")
        ws2.write(0,8,"答案")
        ws2.write(0,9,"题型")
        md=pd.read_excel("/Users/mac/Desktop/题库程序/错题记录1.xls")
        for t in range(len(md)):
            listwrong=md.values[t]
            for i in range(len(listwrong)):
                if str(listwrong[7])!="nan":
                    ws2.write(t+1,i,str(listwrong[i]))
        wb2.save("/Users/mac/Desktop/题库程序/错题记录2.xls")  
        
        
        
        
    ##错题回顾——顺序
    elif choose=="2":
        wt=pd.read_excel("/Users/mac/Desktop/题库程序/错题记录1.xls")
        totalnumber=0
        rightnumber=0
        if len(wt)==0:
            print("\n错题库为空，请先做题")
        else:
            chapter=1
            if chapter not in range(1,18):
                print("\n不存在该章节，请重新输入")
            else:
                for t in range(len(wt)):
                    lictcontent1=wt.values[t]
                    listcontent=[]
                    newanswer=""
                    for r in range(len(lictcontent1)):
                        listcontent.append(lictcontent1[r])
                    correctanswer=listcontent[8]
                    if str(listcontent[0])==str(chapter):
                        correctcontent=[]
                        answerindex=0
                        for t in correctanswer:
                            if t=="A":
                                answerindex=4
                            elif t=="B":
                                answerindex=5
                            elif t=="C":
                                answerindex=6
                            elif t=="D":
                                answerindex=7
                            elif t=="E":
                                answerindex=8
                            correctcontent.append(listcontent[answerindex])
                        for a in range(len(listcontent)):
                            b=random.randint(4,7)
                            c=random.randint(4,7)
                            listcontent[b],listcontent[c]=listcontent[c],listcontent[b]
                        newanswer=""
                        newanswer1=""
                        for u in listcontent:
                            if u in correctcontent:
                                w=listcontent.index(u)
                                if w==4:
                                    newanswer1="A"
                                elif w==5:
                                    newanswer1="B"
                                elif w==6:
                                    newanswer1="C"
                                elif w==7:
                                    newanswer1="D"
                                elif w==8:
                                    newanswer1="E"
                                newanswer+=newanswer1
                        print("目录:{} 题号:{} \n\n题型：{} \n\n{}\nA:{}\nB:{}\nC:{}\nD:{}".format(listcontent[0],listcontent[1],listcontent[9],listcontent[3],listcontent[4],listcontent[5],listcontent[6],listcontent[7]))
                        starttime=time.time()
                        answer=input("请输入答案:")
                        if len(answer)==1 and len(newanswer)!=1:
                            answer=input("本题是多选题！请再次输入答案：")
                        endtime=time.time()
                        usedtime=endtime-starttime
                        if answer==" ":
                            continue
                        elif answer==newanswer or answer.upper()==newanswer:
                            print("答案正确")
                            totalnumber+=1
                            rightnumber+=1
                            print("当前正确率{:.2f}%".format(rightnumber/totalnumber*100))
                        elif answer=="":
                            wb1.save("/Users/mac/Desktop/题库程序/错题记录1.xls")
                            flag=False
                            break
                        elif answer=="?":
                            continue
                        elif str(answer)!=str(newanswer):
                            print("答案错误，本题答案是",newanswer)
                            totalnumber+=1
                            print("当前正确率{:.2f}%".format(rightnumber/totalnumber*100))
                else:
                    print("错题记录中对应章节错题已做完，请先做题")
                if totalnumber!=0:
                    rate=rightnumber/totalnumber
                    print("\n本次做了{}题，正确率为{:.2f}%".format(totalnumber,rate*100))


                    
    

    elif choose=="3":
        print("\n你真的要清空全部错题吗？")
        m=input("\n输入yes表示确定,输入其他任意字符退出：")
        if m=="yes":
            pt1=xlwt.Workbook()
            xs1=pt1.add_sheet("Sheet1")
            pt1.save("/Users/mac/Desktop/题库程序/错题记录1.xls")
            pt2=xlwt.Workbook()
            xs2=pt2.add_sheet("Sheet1")
            pt2.save("/Users/mac/Desktop/题库程序/错题记录2.xls")
            print("\n清除错题成功")
        else:
            print("\n取消清除错题成功")

    elif choose=="":
        Platinum=0
        print("\n感谢使用")
        print("\n退出成功")
    elif choose=="4":
        Platinum=0
        print("\n感谢使用")
        print("\n退出成功")
