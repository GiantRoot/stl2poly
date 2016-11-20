#!/user/bin/python
# -* - coding:UTF-8 -*-
import os
#打开文件
stlm = open("matrix.stl")
stlr = open("reinforcement.stl")
poly = open("poly.poly","w")

mAllLineList = stlm.readlines()
rAllLineList = stlr.readlines()
xyzNumber=0
#创建一个空的字典，用来保存点坐标编号
xyzDict={}
xyzDictNodeToNum={}
#创建一个空的set，用来储存点坐标，判断该点是否已经存在于集合中
xyzSet=set()
#vertex 个数，用于判断一个面是否结束
vertexNum=0
#面个数计算
faceNum=0
#建立一个面与面编号的字典
faceNumToNode={}


facetNormal=[0,0,0]
volumeNodeOne=[0,0,0]
volumeNodeTwo=[0,0,0]
volumeNodeThree=[0,0,0]
mVolumeNode=[0,0,0]
rVolumeNode=[0,0,0]
#先统计基体点和面
for mLine in mAllLineList:
	mLineList=mLine.split()#mlinelist是基体储存每一行字符串的list.
	if mLineList[0]=="vertex":
		vertexNum+=1
		#将坐标保存成字符串:x y z相邻中间有一个空格
		xyz=mLineList[1]+" "+mLineList[2]+" "+mLineList[3]
		if xyz not in xyzSet:
			#点编号
			xyzNumber+=1
			#向集合中添加一个点坐标
			xyzSet.add(xyz)
			#每一个编号对应一个点的坐标
			xyzDictNodeToNum[xyz]=xyzNumber
			xyzDict[xyzNumber]=xyz
		if vertexNum%3 == 1:#面的第一个点
			vertexOne=xyz
		if vertexNum%3 == 2:#面的第二个点
			vertexTwo=xyz
		if vertexNum%3 == 0:#面的第三个点，此处不用考虑vertexNum==0的情况。
			faceNum+=1
			vertexThree=xyz
			#把面的三个点编号保存为“1 2 3”形式
			faceNodeNum = (str(xyzDictNodeToNum[vertexOne])+" "
				+str(xyzDictNodeToNum[vertexTwo])+" "
				+str(xyzDictNodeToNum[vertexThree]))
			faceNumToNode[faceNum]=faceNodeNum
#体积信息
volumeMark=0#标记体积信息是否收集全
for mLine in mAllLineList:
	mLineList=mLine.split()#mlinelist是基体储存每一行字符串的list.
	if mLineList[0]=="facet":
		facetNormal[0]=mLineList[2]
		facetNormal[1]=mLineList[3]
		facetNormal[2]=mLineList[4]
	if mLineList[0]=="vertex":
		volumeMark+=1
		if volumeMark%3 == 1:#面的第一个点
			volumeNodeOne[0]=mLineList[1]
			volumeNodeOne[1]=mLineList[2]
			volumeNodeOne[2]=mLineList[3]
		if volumeMark%3 == 2:#面的第二个点
			volumeNodeTwo[0]=mLineList[1]
			volumeNodeTwo[1]=mLineList[2]
			volumeNodeTwo[2]=mLineList[3]
		if volumeMark%3 == 0:#面的第三个点，此处不用考虑vertexNum==0的情况。
			volumeNodeThree[0]=mLineList[1]
			volumeNodeThree[1]=mLineList[2]
			volumeNodeThree[2]=mLineList[3]
			mVolumeNode[0]=((float(volumeNodeOne[0])+float(volumeNodeTwo[0])+
				float(volumeNodeThree[0]))/3 - 0.001*float(facetNormal[0]))
			mVolumeNode[1]=((float(volumeNodeOne[1])+float(volumeNodeTwo[1])+
				float(volumeNodeThree[1]))/3 - 0.001*float(facetNormal[1]))
			mVolumeNode[2]=((float(volumeNodeOne[2])+float(volumeNodeTwo[2])+
				float(volumeNodeThree[2]))/3 - 0.001*float(facetNormal[2]))
			break



#体积信息
volumeMark=0#标记体积信息是否收集全
for rLine in rAllLineList:
	rLineList=rLine.split()#mlinelist是基体储存每一行字符串的list.
	if rLineList[0]=="facet":
		facetNormal[0]=rLineList[2]
		facetNormal[1]=rLineList[3]
		facetNormal[2]=rLineList[4]
	if rLineList[0]=="vertex":
		volumeMark+=1
		if volumeMark%3 == 1:#面的第一个点
			volumeNodeOne[0]=rLineList[1]
			volumeNodeOne[1]=rLineList[2]
			volumeNodeOne[2]=rLineList[3]
		if volumeMark%3 == 2:#面的第二个点
			volumeNodeTwo[0]=rLineList[1]
			volumeNodeTwo[1]=rLineList[2]
			volumeNodeTwo[2]=rLineList[3]
		if volumeMark%3 == 0:#面的第三个点，此处不用考虑vertexNum==0的情况。
			volumeNodeThree[0]=rLineList[1]
			volumeNodeThree[1]=rLineList[2]
			volumeNodeThree[2]=rLineList[3]
			rVolumeNode[0]=((float(volumeNodeOne[0])+float(volumeNodeTwo[0])+
				float(volumeNodeThree[0]))/3 - 0.001*float(facetNormal[0]))
			rVolumeNode[1]=((float(volumeNodeOne[1])+float(volumeNodeTwo[1])+
				float(volumeNodeThree[1]))/3 - 0.001*float(facetNormal[1]))
			rVolumeNode[2]=((float(volumeNodeOne[2])+float(volumeNodeTwo[2])+
				float(volumeNodeThree[2]))/3 - 0.001*float(facetNormal[2]))
			break

#写入poly
#写入点标号对照表
poly.write("# Part 1 - the node list.""\n")
poly.write(str(xyzNumber))
poly.write(" 3 0 0""\n")
for i in range(1,xyzNumber+1):
	poly.write(str(i))
	poly.write(" ")
	poly.write(xyzDict[i])
	poly.write("\n")
#写入面标号对照表
poly.write("# Part 2 - the facet list""\n")
poly.write(str(faceNum))
poly.write(" 0""\n")
for i in range(1,faceNum+1):
	poly.write("1""\n")
	poly.write("3")
	poly.write(" ")
	poly.write(faceNumToNode[i])
	poly.write("\n")
poly.write("# Part 3 - hole list""\n")
poly.write("0")
poly.write("# Part 4 - region list""\n")
poly.write("2""\n")
poly.write("1 ")
poly.write(str(mVolumeNode[0])+" "+str(mVolumeNode[1])+" "+str(mVolumeNode[2])+" ")
poly.write(" -1 0.01""\n")
poly.write("2 ")
poly.write(str(rVolumeNode[0])+" "+str(rVolumeNode[1])+" "+str(rVolumeNode[2])+" ")
poly.write(" -2 0.01")				
#关闭文件
stlm.close()
stlr.close()
poly.close()
