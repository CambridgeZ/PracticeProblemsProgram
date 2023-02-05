import pandas as pd
import xlwt
import time
import solveTheProblemInRandom
import solveTheWrongProblems
import solveTheProblemInSequence

wb1 = xlwt.Workbook()
ws1 = wb1.add_sheet("Sheet1")
ws1.write(0, 0, "目录")
ws1.write(0, 1, "题号")
ws1.write(0, 2, "章节")
ws1.write(0, 3, "题干")
ws1.write(0, 4, "选择A")
ws1.write(0, 5, "选择B")
ws1.write(0, 6, "选择C")
ws1.write(0, 7, "选择D")
ws1.write(0, 8, "答案")
ws1.write(0, 9, "题型")


num = 0
df = pd.read_excel("/Users/mac/Desktop/题库程序/题库.xls")

def beginTheProgram():
    print("本程序由NJMU2020级XueJingyuan设计，转载请注明出处。\n若出现bug可联系QQ:2465610238\n 也可以向代码重构者的邮箱发送邮件 jianqiaozh01@gmail.com")

    ##以下是预处理
    df = pd.read_excel("/Users/mac/Desktop/题库程序/题库.xls")
    # Platinum = 1
    print("\n现在是{}\n\n欢迎使用NJMU毛概自测程序V2.0".format(
        time.strftime("%Y年%m月%d日   %H时%M分%S秒", time.localtime())))
    print("\nV2.0更新内容：选项随机排列功能,优化了显示界面\n")
    print("\nTips:\n1.错题回顾不设次数限制\n2.如果直接关闭程序会导致错题无法记录\n3.请按设定输入字符!!!\n")
    print("\n请选择功能：\n0.顺序做题\n1.随机抽题(不重复)\n2.错题回顾(顺序)\n3.清空错题库\n4.退出")
    num=0


if __name__ == '__main__':

    beginTheProgram()

    FLAG=1
    while(FLAG):
        xl = pd.read_excel("/Users/mac/Desktop/题库程序/错题记录2.xls") # 通过读xls文件得到的二维数组
        # for a in range(len(xl)):
        #     listwrong1 = xl.values[a]
        #     for b in range(len(listwrong1)):
        #         if str(listwrong1[b]) != "nan":
        #             ws1.write(a + 1, b, listwrong1[b])
        num += 1
        if num != 1:
            print("\n请再次选择功能：\n0.顺序做题\n1.随机抽题(不重复)\n2.错题回顾(顺序)\n3.清空错题库\n4.退出")
        choose = input("\n请输入：")
        if choose=='0':
            solveTheProblemInSequence.solveTheProblemInSequence(xl,df,ws1)
        elif choose=='1':
            solveTheProblemInRandom.solveTheProblemInRandom()
        elif choose=='2':
            solveTheWrongProblems.solveTheWrongProblems(df)
        elif choose=='3':
            print("\n你真的要清空全部错题吗？")
            m = input("\n输入yes表示确定,输入其他任意字符退出：")
            if m == "yes":
                pt1 = xlwt.Workbook()
                xs1 = pt1.add_sheet("Sheet1")
                pt1.save("/Users/mac/Desktop/题库程序/错题记录1.xls")
                pt2 = xlwt.Workbook()
                xs2 = pt2.add_sheet("Sheet1")
                pt2.save("/Users/mac/Desktop/题库程序/错题记录2.xls")
                print("\n清除错题成功")
            else:
                print("\n取消清除错题成功")
        elif choose=='4':
            print("\n感谢使用")
            print("\n退出成功")
            break
