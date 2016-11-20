#!/user/bin/python
# -* - coding:UTF-8 -*-
import os
#���ļ�
stlm = open("matrix.stl")
stlr = open("reinforcement.stl")
poly = open("poly.poly","w")

mAllLineList = stlm.readlines()
rAllLineList = stlr.readlines()
xyzNumber=0
#����һ���յ��ֵ䣬���������������
xyzDict={}
xyzDictNodeToNum={}
#����һ���յ�set��������������꣬�жϸõ��Ƿ��Ѿ������ڼ�����
xyzSet=set()
#vertex �����������ж�һ�����Ƿ����
vertexNum=0
#���������
faceNum=0
#����һ���������ŵ��ֵ�
faceNumToNode={}


facetNormal=[0,0,0]
volumeNodeOne=[0,0,0]
volumeNodeTwo=[0,0,0]
volumeNodeThree=[0,0,0]
mVolumeNode=[0,0,0]
rVolumeNode=[0,0,0]
#��ͳ�ƻ�������
for mLine in mAllLineList:
	mLineList=mLine.split()#mlinelist�ǻ��崢��ÿһ���ַ�����list.
	if mLineList[0]=="vertex":
		vertexNum+=1
		#�����걣����ַ���:x y z�����м���һ���ո�
		xyz=mLineList[1]+" "+mLineList[2]+" "+mLineList[3]
		if xyz not in xyzSet:
			#����
			xyzNumber+=1
			#�򼯺������һ��������
			xyzSet.add(xyz)
			#ÿһ����Ŷ�Ӧһ���������
			xyzDictNodeToNum[xyz]=xyzNumber
			xyzDict[xyzNumber]=xyz
		if vertexNum%3 == 1:#��ĵ�һ����
			vertexOne=xyz
		if vertexNum%3 == 2:#��ĵڶ�����
			vertexTwo=xyz
		if vertexNum%3 == 0:#��ĵ������㣬�˴����ÿ���vertexNum==0�������
			faceNum+=1
			vertexThree=xyz
			#������������ű���Ϊ��1 2 3����ʽ
			faceNodeNum = (str(xyzDictNodeToNum[vertexOne])+" "
				+str(xyzDictNodeToNum[vertexTwo])+" "
				+str(xyzDictNodeToNum[vertexThree]))
			faceNumToNode[faceNum]=faceNodeNum
#�����Ϣ
volumeMark=0#��������Ϣ�Ƿ��ռ�ȫ
for mLine in mAllLineList:
	mLineList=mLine.split()#mlinelist�ǻ��崢��ÿһ���ַ�����list.
	if mLineList[0]=="facet":
		facetNormal[0]=mLineList[2]
		facetNormal[1]=mLineList[3]
		facetNormal[2]=mLineList[4]
	if mLineList[0]=="vertex":
		volumeMark+=1
		if volumeMark%3 == 1:#��ĵ�һ����
			volumeNodeOne[0]=mLineList[1]
			volumeNodeOne[1]=mLineList[2]
			volumeNodeOne[2]=mLineList[3]
		if volumeMark%3 == 2:#��ĵڶ�����
			volumeNodeTwo[0]=mLineList[1]
			volumeNodeTwo[1]=mLineList[2]
			volumeNodeTwo[2]=mLineList[3]
		if volumeMark%3 == 0:#��ĵ������㣬�˴����ÿ���vertexNum==0�������
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



#�����Ϣ
volumeMark=0#��������Ϣ�Ƿ��ռ�ȫ
for rLine in rAllLineList:
	rLineList=rLine.split()#mlinelist�ǻ��崢��ÿһ���ַ�����list.
	if rLineList[0]=="facet":
		facetNormal[0]=rLineList[2]
		facetNormal[1]=rLineList[3]
		facetNormal[2]=rLineList[4]
	if rLineList[0]=="vertex":
		volumeMark+=1
		if volumeMark%3 == 1:#��ĵ�һ����
			volumeNodeOne[0]=rLineList[1]
			volumeNodeOne[1]=rLineList[2]
			volumeNodeOne[2]=rLineList[3]
		if volumeMark%3 == 2:#��ĵڶ�����
			volumeNodeTwo[0]=rLineList[1]
			volumeNodeTwo[1]=rLineList[2]
			volumeNodeTwo[2]=rLineList[3]
		if volumeMark%3 == 0:#��ĵ������㣬�˴����ÿ���vertexNum==0�������
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

#д��poly
#д����Ŷ��ձ�
poly.write("# Part 1 - the node list.""\n")
poly.write(str(xyzNumber))
poly.write(" 3 0 0""\n")
for i in range(1,xyzNumber+1):
	poly.write(str(i))
	poly.write(" ")
	poly.write(xyzDict[i])
	poly.write("\n")
#д�����Ŷ��ձ�
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
#�ر��ļ�
stlm.close()
stlr.close()
poly.close()
