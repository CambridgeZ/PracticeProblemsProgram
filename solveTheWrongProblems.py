import random
import time
def solveTheWrongProblems(df):

    count=0
    rightnumber=0
    totalnumber=0
    wrongProblemsRecordFilenam='./错题记录.txt'

    with open(wrongProblemsRecordFilenam,'r') as f:
        lastRecord = f.readlines()  # 本题序号

    numberNowBeDown=0
    wrongProblemNumber=0
    while(1):
        if(df.values[numberNowBeDown][1]==int(lastRecord[wrongProblemNumber])):
            listcontent1 = df.values[numberNowBeDown] #读取题目的内容
            count += 1
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
            usedtime = endtime - starttime  # 计算答题使用的时间

            if answer == newanswer or answer.upper() == newanswer:
                print("答案正确")
                totalnumber += len(newanswer)
                rightnumber += len(newanswer)
                print("当前正确率{:.2f}%".format(rightnumber / totalnumber * 100))
            elif answer == "":  # 退出
                check = input("你真的要退出吗，输入1退出：")
                if check == "1":
                    serialnumber = newlist[1]
                    recordOfFinishFilaname= './lastFinish.txt'
                    with open(recordOfFinishFilaname, 'w') as file_object:
                        file_object.write(str(serialnumber) + '\n')
                    flag = False
                    break
            elif str(answer) != str(newanswer):
                print("答案错误，本题答案是", newanswer)
                print("当前正确率{:.2f}%".format(rightnumber / totalnumber * 100))
            wrongProblemNumber = wrongProblemNumber + 1 # 错题序号加一
            if(wrongProblemNumber>=len(lastRecord)):
                break
        else:
            numberNowBeDown=numberNowBeDown+1
            continue




