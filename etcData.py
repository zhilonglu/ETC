# #找出一个月中广东省内的数据，目的是看虎门大桥的情况
import os

def findGDdata():
    inpath = "D:\\ETC\\"
    outpath = "D:\\ETC_GD\\"
    files = os.listdir(inpath)
    for file in files:
        if not os.path.exists(outpath+file):
            os.mkdir(outpath+file)
        files2 = os.listdir(inpath+file)
        for file2 in files2:
            # print(file)
            with open(outpath + file+"\\"+file2, "w") as f2:
                try:
                    with open(inpath+file+"\\"+file2,"r",encoding='UTF-8') as f:
                        lines = f.readlines()
                        for line in lines:
                            try:
                                attrs = line.split(",")
                                if attrs[8][8:10] == '44':
                                    f2.write(line)
                            except:
                                continue
                except:
                    with open(inpath+file+"\\"+file2,"r",encoding='gbk') as f:
                        lines = f.readlines()
                        for line in lines:
                            try:
                                attrs = line.split(",")
                                if attrs[8][8:10] == '44':
                                    f2.write(line)
                            except:
                                continue
            f2.close()
#按月分车型统计车辆运行情况
def typeCnt():
    inpath = "D:\\ETC_GD\\"
    outputpath = "D:\\ETC\\"
    monthvType = {}
    files = os.listdir(inpath)
    for file in files:
        files2 = os.listdir(inpath + file)
        vtype = {}
        for file2 in files2:
            try:
                with open(inpath + file + "\\" + file2, "r", encoding='UTF-8') as f:
                    lines = f.readlines()
                    for line in lines:
                        try:
                            attrs = line.split(",")
                            key = attrs[20]
                            if key in vtype.keys():
                                vtype[key] +=1
                            else:
                                vtype[key] = 1
                            if key+","+file in monthvType.keys():
                                monthvType[key+","+file] += 1
                            else:
                                monthvType[key+","+file] = 1
                        except:
                            continue
            except:
                with open(inpath + file + "\\" + file2, "r", encoding='gbk') as f:
                    lines = f.readlines()
                    for line in lines:
                        try:
                            attrs = line.split(",")
                            key = attrs[20]
                            if key in vtype.keys():
                                vtype[key] += 1
                            else:
                                vtype[key] = 1
                            if key + "," + file in monthvType.keys():
                                monthvType[key + "," + file] += 1
                            else:
                                monthvType[key + "," + file] = 1
                        except:
                            continue
        with open(outputpath + file + "_typecnt.csv", "w") as f2:
            for key in vtype.keys():
                f2.write(key+","+str(vtype[key])+"\n")
            f2.close()
    with open(outputpath + "allmonth_typecnt.csv", "w") as f2:
        for key in monthvType.keys():
            f2.write(key + "," + str(monthvType[key]) + "\n")
        f2.close()

def findStation():
    inpath = "D:\\ETC_GD\\"
    outpath = "D:\\ETC\\findStationBoth.csv"
    files = os.listdir(inpath)
    with open(outpath,"w") as f:
        for file in files:
            files2 = os.listdir(inpath+file+"\\")
            for file1 in files2:
                with open(inpath+file+"\\"+file1) as f1:
                    alllines = f1.readlines()
                    for line in alllines:
                        try:
                            if ('亭角' in line.split(",")[18] and '南沙' in line.split(",")[19]) or ('南沙' in line.split(",")[18] and '亭角' in line.split(",")[19]):
                                f.write(line)
                        except:
                            continue
    f.close()

if __name__ == '__main__':
    # typeCnt()
    findStation()