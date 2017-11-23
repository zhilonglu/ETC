import numpy as np

# 判断GPS点是否在桥上  这个貌似有点问题
# def pnpoly(nvert, vertx, verty, testx, testy):
#     c = 0
#     for i in range(nvert - 1):
#         if ((verty[i] > testy) and (verty[i + 1] < testy)) or ((verty[i] < testy) and (verty[i + 1] > testy)) and (
#                     testx < (vertx[i] - vertx[i + 1]) * (testy - verty[i + 1]) / (verty[i] - verty[i + 1]) + vertx[
#                         i + 1]):
#             c = 1
#     return c

# 直接判断范围，左下角和右上角
# def judgePoint(minX, minY, maxX, maxY, testx, testy):
#     c = 0
#     if (testx > minX) and (testx < maxX) and (testy > minY) and (testy < maxY):
#         c = 1
#     return c

# bool pointInPolygon() {
#
#   int   i,j=polySides-1 ;
#   bool  oddNodes=NO     ;
#
#   for (i=0;i<polySides; i++) {
#     if(polyY[i]<y && polyY[j]>=y
#     ||  polyY[j]<y&& polyY[i]>=y) {
#       if(polyX[i]+(y-polyY[i])/(polyY[j]-polyY[i])*(polyX[j]-polyX[i])<x) {
#         oddNodes=!oddNodes;}}
#     j=i;}
#
#   returnoddNodes; }

# def pointInPolygon(nvert, vertx, verty, testx, testy):
#     j = nvert - 1
#     oddNodes = 0
#     for i in range(nvert):
#         if ((verty[i] < testy) and (verty[j] >= testy)) or ((verty[j] < testy) and (verty[i] >= testy)):
#             if (vertx[i] + (testy - verty[i]) / (verty[j] - verty[i]) * (vertx[j] - vertx[i])) < testx:
#                 oddNodes = 1
#         j = i
#     return oddNodes


#这个是判断一个GPS点是否在一个区域内，经过验证是正确的
# def isPtInPoly(ALon, ALat, ps):
#     if len(ps) < 3:
#         return 0
#     iSum = 0
#     iCount = len(ps)
#     for iIndex in range(iCount):
#         if iIndex == iCount - 1:
#             dLon1 = ps[iIndex][0]
#             dLat1 = ps[iIndex][1]
#             dLon2 = ps[0][0]
#             dLat2 = ps[0][1]
#         else:
#             dLon1 = ps[iIndex][0]
#             dLat1 = ps[iIndex][1]
#             dLon2 = ps[iIndex+1][0]
#             dLat2 = ps[iIndex+1][1]
#         # 以下语句判断A点是否在边的两端点的水平平行线之间，在则可能有交点，开始判断交点是否在左射线上
#         if ((ALat >= dLat1) and (ALat < dLat2)) or ((ALat >= dLat2) and (ALat < dLat1)):
#             if abs(dLat1 - dLat2) > 0:
#                 # 得到 A点向左射线与边的交点的x坐标
#                 dLon = dLon1 - ((dLon1 - dLon2) * (dLat1 - ALat)) / (dLat1 - dLat2)
#                 # // 如果交点在A点左侧（说明是做射线与 边的交点），则射线与边的全部交点数加一
#                 if dLon < ALon:
#                     iSum += 1
#     if iSum % 2 != 0:
#         return 1
#     return 0


# 113.619014,22.795023  1
# 113.622176, 22.769566 0
# 113.613157,22.791491
# 113.597491,22.798088
# testx = 113.619984
# testy = 22.767033
# vertex = [(113.592388,22.768433),(113.611289,22.776697),(113.618044,22.776097),(113.611648,22.7663)]
# vertx = [113.591993, 113.592191, 113.645658, 113.646305]
# verty = [22.773415, 22.771765, 22.811631, 22.809715]
# print(pnpoly(4, vertx, verty, testx, testy))
# print(pointInPolygon(vertx, verty, testx, testy))
# print(isPtInPoly(testx,testy,vertex))

outputValue = np.zeros(35*24).reshape(35,24)
outputValue[0][1] = 4
print(outputValue)