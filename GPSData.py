# -*-coding:utf-8-*-
import os
from math import radians, cos, sin, asin, sqrt
import numpy as np
from ETC import coordTransform


# 经度1，纬度1，经度2，纬度2 （十进制度数） 计算两点间的距离
def haversine(lon1, lat1, lon2, lat2):
    """ 
    Calculate the great circle distance between two points  
    on the earth (specified in decimal degrees) 
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r * 1000


# 读取载重货车的车型情况
def vehicleType():
    vType = {}
    with open("D:\\UGC\\vehicleType.txt") as f:
        lines = f.readlines()
        for line in lines:
            attrs = line.split(",")
            vType[attrs[0]] = int(attrs[1])
    return vType


# 找出每辆车GPS点个数
def cntVolumebyType():
    vType = vehicleType()
    # print(vType)
    inpath = "D:\\UGC\\20171021_gps_area\\"
    # inpath2 = "D:\\UGC\\GPS2\\humen\\20171021\\"
    # inpath = [inpath1, inpath2]
    outputPath = "D:\\UGC\\20171021_gps_area.csv"
    vDict = {}
    files = os.listdir(inpath)
    for file in files:
        if ".csv" in file:
            with open(inpath + file) as f:
                lines = f.readlines()
                for line in lines:
                    attr = line.split(",")
                    try:
                        carID = attr[2]
                        if carID not in vDict.keys():
                            vDict[carID] = 1
                        else:
                            vDict[carID] += 1
                    except:
                        continue
    # print(vDict)
    with open(outputPath, "w") as f2:
        for key in vDict.keys():
            type = "none"
            if key in vType.keys():
                type = str(vType[key])
            f2.write(key + "," + type + "," + str(vDict[key]) + "\n")
        f2.close()


# 找出一辆车的所有行驶轨迹
def findCarcompleteTrajectory():
    vType = vehicleType()
    inpath1 = "D:\\UGC\\GPS\\humen\\20171021\\"
    inpath2 = "D:\\UGC\\GPS2\\humen\\20171021\\"
    inpath = [inpath1, inpath2]
    outputPath = "D:\\UGC\\20171021_gps\\"
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)
    vDict = {}
    for path in inpath:
        files = os.listdir(path)
        for file in files:
            with open(path + file) as f:
                lines = f.readlines()
                for line in lines:
                    attr = line.split(",")
                    try:
                        carID = attr[2]
                        k = attr[0] + attr[1]  # GPS产生的时间点，按这个排序
                        if carID not in vDict.keys():
                            vDict[carID] = []
                            vDict[carID].append((k, line.replace(";\n", "")))
                        else:
                            vDict[carID].append((k, line.replace(";\n", "")))
                            # print(vDict)
                    except:
                        continue
    for key in vDict.keys():
        type = "none"
        if key in vType.keys():
            type = str(vType[key])
        filename = key + "#" + type + ".csv"
        with open(outputPath + filename, "w") as f2:
            values = vDict[key]
            values.sort(key=lambda k: k[0])
            for value in values:
                f2.write(value[1] + "\n")
        f2.close()


# 找出一辆车在某段区域内的GPS轨迹，如在虎门大桥上的轨迹
def findCarAreaTrajectory():
    # 这是百度BD-09坐标系
    # vertx = [113.591993, 113.592191, 113.645658, 113.646305]
    # verty = [22.773415, 22.771765, 22.811631, 22.809715]
    # 这是WGS84坐标系
    # vertx = [113.58038635076973, 113.58058455826885, 113.63414741407747, 113.6347957471411]
    # verty = [22.77075191873537, 22.769101480751267, 22.80825245356406, 22.806336223409822]
    # vertx = [113.589135, 113.580386, 113.634147, 113.653706]
    # verty = [22.765365, 22.770752, 22.808252, 22.803831]
    vert = [(113.589135, 22.765365), (113.580386, 22.770752), (113.634147, 22.808252), (113.653706, 22.803831)]
    vType = vehicleType()
    inpath1 = "D:\\UGC\\GPS\\humen\\20171021\\"
    inpath2 = "D:\\UGC\\GPS2\\humen\\20171021\\"
    inpath = [inpath1, inpath2]
    outputPath = "D:\\UGC\\20171021_gps_area\\"
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)
    vDict = {}
    for path in inpath:
        files = os.listdir(path)
        for file in files:
            with open(path + file) as f:
                lines = f.readlines()
                for line in lines:
                    attr = line.split(",")
                    try:
                        carID = attr[2]
                        k = attr[0] + attr[1]  # GPS产生的时间点，按这个排序
                        testx = float(attr[3])
                        testy = float(attr[4])
                        if isPtInPoly(testx, testy, vert) == 1:
                            if carID not in vDict.keys():
                                vDict[carID] = []
                                vDict[carID].append((k, line.replace(";\n", "")))
                            else:
                                vDict[carID].append((k, line.replace(";\n", "")))
                    except:
                        continue
    for key in vDict.keys():
        type = "none"
        if key in vType.keys():
            type = str(vType[key])
        filename = key + "#" + type + ".csv"
        with open(outputPath + filename, "w") as f2:
            values = vDict[key]
            values.sort(key=lambda k: k[0])
            for value in values:
                f2.write(value[1] + "\n")
        f2.close()


# 按GPS产生时间对一辆车的轨迹排序后，记录两个点之间的距离。
def cntDistance():
    inpath = "D:\\UGC\\20171021_gps\\"
    outputpath = "D:\\UGC\\20171021_gps_dis.csv"
    files = os.listdir(inpath)
    with open(outputpath, "w") as f:
        for file in files:
            if ".csv" in file:
                with open(inpath + file) as f1:
                    alllines = f1.readlines()
                    disList = file.split(".")[0] + ","
                    for i in range(len(alllines) - 1):
                        a_pos_lon = float(alllines[i].split(",")[3])
                        a_pos_lat = float(alllines[i].split(",")[4])
                        b_pos_lon = float(alllines[i + 1].split(",")[3])
                        b_pos_lat = float(alllines[i + 1].split(",")[4])
                        dis = haversine(a_pos_lon, a_pos_lat, b_pos_lon, b_pos_lat)
                        disList += str(dis) + ","
                f.write(disList + "\n")
    f.close()


# 根据一辆车，计算两点间的距离
def countOneCarDis():
    inpath = "D:\\UGC\\20171021_gps\\7ab15f0306eec5a20601d9da7cc18c2a#3.csv"
    outputpath = "D:\\UGC\\20171021_7ab15f0306eec5a20601d9da7cc18c2a#3_dis.csv"
    with open(outputpath, "w") as f:
        with open(inpath) as f1:
            alllines = f1.readlines()
            for i in range(len(alllines) - 1):
                a_pos_lon = float(alllines[i].split(",")[3])
                a_pos_lat = float(alllines[i].split(",")[4])
                b_pos_lon = float(alllines[i + 1].split(",")[3])
                b_pos_lat = float(alllines[i + 1].split(",")[4])
                dis = haversine(a_pos_lon, a_pos_lat, b_pos_lon, b_pos_lat)
                f.write(alllines[i].replace("\n", ",") + "," + str(dis) + "\n")
            f.write(alllines[len(alllines) - 1])
    f.close()


def isPtInPoly(ALon, ALat, ps):
    if len(ps) < 3:
        return 0
    iSum = 0
    iCount = len(ps)
    for iIndex in range(iCount):
        if iIndex == iCount - 1:
            dLon1 = ps[iIndex][0]
            dLat1 = ps[iIndex][1]
            dLon2 = ps[0][0]
            dLat2 = ps[0][1]
        else:
            dLon1 = ps[iIndex][0]
            dLat1 = ps[iIndex][1]
            dLon2 = ps[iIndex + 1][0]
            dLat2 = ps[iIndex + 1][1]
        # 以下语句判断A点是否在边的两端点的水平平行线之间，在则可能有交点，开始判断交点是否在左射线上
        if ((ALat >= dLat1) and (ALat < dLat2)) or ((ALat >= dLat2) and (ALat < dLat1)):
            if abs(dLat1 - dLat2) > 0:
                # 得到 A点向左射线与边的交点的x坐标
                dLon = dLon1 - ((dLon1 - dLon2) * (dLat1 - ALat)) / (dLat1 - dLat2)
                # // 如果交点在A点左侧（说明是做射线与 边的交点），则射线与边的全部交点数加一
                if dLon < ALon:
                    iSum += 1
    if iSum % 2 != 0:
        return 1
    return 0

#画出所有车GPS点聚焦的热力图
def generateDemo():
    inpath = "D:\\UGC\\20171021_gps\\"
    # outpath = "D:\\UGC\\20171021_gps_demo\\"
    outpath = "D:\\UGC\\20171021_gps_allcar.json"
    # if not os.path.exists(outpath):
    #     os.mkdir(outpath)
    files = os.listdir(inpath)
    with open(outpath, "w") as f:
        f.write("data=[\n")
        for i in range(600):
            if ".csv" in files[i]:
                # with open(outpath+file.split(".")[0]+".json","w") as f:
                f.write("[")
                with open(inpath + files[i]) as f1:
                    alls = f1.readlines()
                    for line in alls:
                        lon = line.split(",")[3]
                        lat = line.split(",")[4]
                        speed = line.split(",")[5]
                        f.write("{\"coord\":[" + lon + "," + lat + "],\"elevation\":" + speed + "},\n")
                f.write("],\n")
        f.write("]")
        f.close()


# 判断GPS属于哪一段
def inWhichSeg(lon, lat):
    # 共计35段，编号从0到34
    splitPt = [(113.586227, 22.76697), (113.588024, 22.76825), (113.589642, 22.769852), (113.591587, 22.771818),
               (113.593269, 22.773435), (113.59483, 22.774935), (113.596165, 22.776225), (113.597862, 22.777842),
               (113.599491, 22.779401), (113.601212, 22.781003), (113.602486, 22.782127), (113.604088, 22.783445),
               (113.605682, 22.784678), (113.607658, 22.78611), (113.609669, 22.78746), (113.611275, 22.788467),
               (113.613258, 22.789627), (113.615124, 22.790749), (113.616219, 22.79139), (113.618191, 22.792544),
               (113.621788, 22.794624), (113.624237, 22.796041), (113.626137, 22.797122), (113.62764, 22.797997),
               (113.630062, 22.799395), (113.631939, 22.800479), (113.633743, 22.801524), (113.635376, 22.802409),
               (113.637371, 22.803256), (113.63858, 22.80364), (113.64109, 22.804471), (113.642979, 22.804886),
               (113.644272, 22.804937), (113.646355, 22.804647), (113.648918, 22.804359), (113.652252, 22.803983)]
    for i in range(len(splitPt) - 1):
        minLon = min(splitPt[i][0], splitPt[i + 1][0])
        maxLon = max(splitPt[i][0], splitPt[i + 1][0])
        minLat = min(splitPt[i][1], splitPt[i + 1][1])
        maxLat = max(splitPt[i][1], splitPt[i + 1][1])
        if lon >= minLon and lon <= maxLon and lat >= minLat and lat <= maxLat:
            return i
    return -1  # 表示不在这段区间内


# 计算每200米路段大桥的小时负载情况，主要是按小时统计200米内车辆的情况，然后根据重量来计算路段的整体载重
def cntweight():
    vType = vehicleType()
    type_weight = {2: 17, 3: 25, 4: 35, 5: 43, 6: 49}
    outputValue = np.zeros(35*24).reshape(35,24)
    inpath1 = "D:\\UGC\\GPS\\humen\\20171021\\"
    inpath2 = "D:\\UGC\\GPS2\\humen\\20171021\\"
    inpath = [inpath1, inpath2]
    outputPath = "D:\\UGC\\20171021_gps_segCountHourly.csv"
    for path in inpath:
        files = os.listdir(path)
        for file in files:
            with open(path + file) as f:
                lines = f.readlines()
                for line in lines:
                    attr = line.split(",")
                    try:
                        hour = int(attr[1][0:2])  # GPS产生的时间点，按这个排序
                        lon = float(attr[3])#原始文件是WGS84坐标系，地图数据是GCJ02坐标系
                        lat = float(attr[4])
                        # result = coordTransform.wgs84_to_gcj02(lon,lat)
                        seg = inWhichSeg(lon,lat)
                        carweight = type_weight[vType[attr[2]]]
                        if seg != -1:
                            outputValue[seg][hour] += carweight
                    except:
                        continue
    np.savetxt(outputPath,outputValue,fmt="%s",delimiter=",")
#算出大桥GPS点之间的距离
def cntDis():
    inpath = "D:\\UGC\\bridgeGPS.txt"
    outpath = "D:\\UGC\\bridgeGPS_dis.csv"
    with open(outpath, "w") as f:
        with open(inpath) as f1:
            alllines = f1.readlines()
            for i in range(len(alllines) - 1):
                a_pos_lon = float(alllines[i].split(",")[1])
                a_pos_lat = float(alllines[i].split(",")[2])
                b_pos_lon = float(alllines[i + 1].split(",")[1])
                b_pos_lat = float(alllines[i + 1].split(",")[2])
                dis = haversine(a_pos_lon, a_pos_lat, b_pos_lon, b_pos_lat)
                f.write(alllines[i].replace("\n", ",") + "," + str(dis) + "\n")
            f.write(alllines[len(alllines) - 1])
        f.close()


# 将大桥分成一段段的，根据想要的段长度，来确定分界点
def splitPoint(length):
    inpath = "D:\\UGC\\bridgeGPS_dis.csv"
    outpath = "D:\\UGC\\bridgeGPS_splitPoint.txt"
    with open(outpath, "w") as f:
        with open(inpath) as f1:
            alllines = f1.readlines()
            for i in range(len(alllines) - 1):
                a_pos_lon = float(alllines[i].split(",")[1])
                a_pos_lat = float(alllines[i].split(",")[2])
                b_pos_lon = float(alllines[i + 1].split(",")[1])
                b_pos_lat = float(alllines[i + 1].split(",")[2])
                dis = haversine(a_pos_lon, a_pos_lat, b_pos_lon, b_pos_lat)
                f.write(alllines[i].replace("\n", ",") + "," + str(dis) + "\n")
            f.write(alllines[len(alllines) - 1])
        f.close()
#画出路段演变情况，生成json文件
def generateJson():
    inpath = "D:\\UGC\\20171021_gps_segCountHourly.csv"
    outpath = "D:\\UGC\\assets\\data\\data.json"
    data = np.loadtxt(inpath,delimiter=',')
    with open(outpath,"w") as f:
        f.write("var odmax0=[\n")
        for i in range(data.shape[1]):
            f.write("[")
            for j in range(data.shape[0]):
                f.write("{o:"+str(j+1)+",d:"+str(j+2)+",flow:"+str(data[j][i])+"},\n")
            f.write("],\n")
        f.write("]")
        f.close()



if __name__ == '__main__':
    # cntVolumebyType()
    # findCarcompleteTrajectory()
    # findCarAreaTrajectory()
    # cntDistance()
    # countOneCarDis()
    # generateDemo()
    # cntDis()
    cntweight()
    # generateJson()