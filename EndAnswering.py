import time
def EndAnswering(totalnumber,rightnumber, totalstarttime,count):#结束答题程序
    if totalnumber != 0:
        rate = rightnumber / totalnumber
        totalendtime = time.time()
        totaltime = totalendtime - totalstarttime
        # wb1.save("/Users/mac/Desktop/题库程序/错题记录1.xls")
        print("\n本次做了{}题，正确率为{:.2f}%，共用时{:.1f}s，题均用时{:.1f}s".format(count, rate * 100, totaltime,
                                                                                    totaltime / count))