import random
import EndAnswering
import time
import xlwt
import pandas as pd

def solveTheProblemInRandom(df,xl,ws1):
    # print("功能仍然在开发当中，敬请期待")
    # return
    print("目前随机做题功能暂时不支持记录错题的功能\n")

    serialnumber = 0
    totalnumber = 0
    rightnumber = 0
    wrongnumber = len(xl)
    flag = True
    # numlist = []
    count = 0
    totalstarttime = time.time()
    while flag == True:
        isHaveBeingDone =[False] * len(df)
        randomnumber = random.randint(1, len(df) - 1)
        if not isHaveBeingDone[randomnumber] :
            isHaveBeingDone[randomnumber]=True
            count += 1
            listcontent1 = df.values[randomnumber]
            ##listcontent的第3号是题干第4-8号为A-E选项，答案的索引是9，题型的索引是10，题号是2
            listcontent = []
            newanswer = ""
            for r in range(len(listcontent1)):
                listcontent.append(listcontent1[r])
            newlist = []
            chapter = listcontent[2]
            correctanswer = listcontent[8]
            correctcontent = []
            print("\n当前进度{}/{}".format(count, len(df)))
            answerindex = 0
            for t in correctanswer:
                if t == "A":
                    answerindex = 4
                elif t == "B":
                    answerindex = 5
                elif t == "C":
                    answerindex = 6
                elif t == "D":
                    answerindex = 7
                elif t == "E":
                    answerindex = 8
                correctcontent.append(listcontent[answerindex])
            for a in range(len(listcontent)):
                b = random.randint(4, 7)
                c = random.randint(4, 7)
                listcontent[b], listcontent[c] = listcontent[c], listcontent[b]
            newanswer = ""
            newanswer1 = ""
            for u in listcontent:
                if u in correctcontent:
                    w = listcontent.index(u)
                    if w == 4:
                        newanswer1 = "A"
                    elif w == 5:
                        newanswer1 = "B"
                    elif w == 6:
                        newanswer1 = "C"
                    elif w == 7:
                        newanswer1 = "D"
                    elif w == 8:
                        newanswer1 = "E"
                    newanswer += newanswer1
            print("目录:{} 题号:{} \n\n{}——{}\nA:{}\nB:{}\nC:{}\nD:{}".format(listcontent[0], listcontent[1],
                                                                              listcontent[9], listcontent[3],
                                                                              listcontent[4], listcontent[5],
                                                                              listcontent[6], listcontent[7]))
            newlist = listcontent[:8] + [newanswer] + [listcontent[9]]
            starttime = time.time()
            answer = input("请输入答案:")
            if len(answer) == 1 and len(newanswer) != 1 and answer != "?" and answer != " " and answer != "+1":
                answer = input("本题是多选题！请再次输入答案：")
            if len(answer) != 1 and len(newanswer) == 1 and answer != "?" and answer != " " and answer != "+1":
                answer = input("本题是单选题！请再次输入答案：")
            if answer == "+1":
                rightnumber += 1
                answer = input("请输入答案:")
            if answer == "?":
                print("提示:本题是", len(newanswer), "选题")
                answer = input("请再次输入答案：")
            endtime = time.time()
            usedtime = endtime - starttime
            if answer == newanswer or answer.upper() == newanswer:
                print("答案正确")
                totalnumber += len(newanswer)
                rightnumber += len(newanswer)
                print("当前正确率{:.2f}%".format(rightnumber / totalnumber * 100))
            elif answer == "":
                check = input("你真的要退出吗，输入1退出：")
                if check == "1":
                    serialnumber = newlist[1]
                    flag = False
                    break
            elif answer == " ":
                continue
            elif str(answer) != str(newanswer):
                print("答案错误，本题答案是", newanswer)
                totalnumber += len(newanswer)
                wrongnumber += 1
                print("当前正确率{:.2f}%".format(rightnumber / totalnumber * 100))
                for t in range(len(newlist)):
                    if str(newlist[t]) != "nan":
                        ws1.write(wrongnumber, t, newlist[t])
                    else:
                        ws1.write(wrongnumber, t, " ")
            print("本题用时{:.3f}s".format(usedtime))
        else:
            continue
    EndAnswering.EndAnswering(totalnumber, rightnumber, totalstarttime, count)

    wb2 = xlwt.Workbook()
    ws2 = wb2.add_sheet("Sheet1")
    ws2.write(0, 0, "目录")
    ws2.write(0, 1, "题号")
    ws2.write(0, 2, "章节")
    ws2.write(0, 3, "题干")
    ws2.write(0, 4, "选择A")
    ws2.write(0, 5, "选择B")
    ws2.write(0, 6, "选择C")
    ws2.write(0, 7, "选择D")
    ws2.write(0, 8, "答案")
    ws2.write(0, 9, "题型")
    md = pd.read_excel("/Users/mac/Desktop/题库程序/错题记录1.xls")
    for t in range(len(md)):
        listwrong = md.values[t]
        for i in range(len(listwrong)):
            if str(listwrong[7]) != "nan":
                ws2.write(t + 1, i, str(listwrong[i]))
    wb2.save("/Users/mac/Desktop/题库程序/错题记录2.xls")
