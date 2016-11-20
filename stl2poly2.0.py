#!/user/bin/python
# -* - coding:UTF-8 -*-
import os,sys

#查找目录下所有的stl文件
def findstl():
	#建立一个空的list用来保存stl文件名。
	stllist=[]
	#os.listdir()返回制定目录下的所有文件名为一个list
	#os.getcwd()返回当前目录路径，为一个文本
	allfile = os.listdir(os.getcwd())
	for filename in allfile:
		if filename.find(".stl") != -1:
			stllist.append(filename)
	return stllist

#遍历所有的stl，找到node，face，part，hole信息
def nodeFaceHolePart():
	facetNormal=[0,0,0]
	volumeNodeOne=[0,0,0]
	volumeNodeTwo=[0,0,0]
	volumeNodeThree=[0,0,0]
	volumeNode=[0,0,0]
	#记录点的个数
	nodeNumber=0
	#创建一个空的字典，用来保存点坐标编号
	nodeDict={}
	nodeDictNodeToNum={}
	#创建一个空的set，用来储存点坐标/面，判断该点/面是否已经存在于集合中
	nodeSet=set()
	faceSet=set()
	#！！！由于stl文件的问题，可能导致这里出错。
	#vertex 个数，用于判断一个面是否结束
	vertexNum=0
	#面个数计算
	faceNum=0
	#建立一个面与面编号的字典
	faceNumToFace={}
	#建立一个空list，储存part信息
	part=[]	
	#建立一个空list，储存hole信息
	hole=[]
	for file in findstl():
		stl=open(file)
		allLineList = stl.readlines()
		
		#node和face信息获取
		for line in allLineList:
			lineList=line.split()#lineList是基体储存每一行字符串的list.
			if lineList[0]=="vertex":
				vertexNum+=1
				#将坐标保存成字符串:x y z相邻中间有一个空格
				node=lineList[1]+" "+lineList[2]+" "+lineList[3]
				if node not in nodeSet:
					#点编号
					nodeNumber+=1
					#向集合中添加一个点坐标
					nodeSet.add(node)
					#每一个编号对应一个点的坐标
					nodeDictNodeToNum[node]=nodeNumber
					nodeDict[nodeNumber]=node
				if vertexNum%3 == 1:#面的第一个点
					vertexOne=node
				if vertexNum%3 == 2:#面的第二个点
					vertexTwo=node
				if vertexNum%3 == 0:#面的第三个点，此处不用考虑vertexNum==0的情况。
					vertexThree=node
					#把面的三个点编号保存为“1 2 3”形式，序号从小到大排列，防止面重复
					if nodeDictNodeToNum[vertexOne] < nodeDictNodeToNum[vertexTwo]:#1<2
						if nodeDictNodeToNum[vertexOne] < nodeDictNodeToNum[vertexThree]: #1<3
							faceNodeNum = str(nodeDictNodeToNum[vertexOne])+" "
							if nodeDictNodeToNum[vertexTwo] < nodeDictNodeToNum[vertexThree]: #1<2<3
								faceNodeNum += str(nodeDictNodeToNum[vertexTwo])+" "\
									+str(nodeDictNodeToNum[vertexThree])
							else:#1<3<2
								faceNodeNum += str(nodeDictNodeToNum[vertexThree])+" "\
									+str(nodeDictNodeToNum[vertexTwo])
						else:#3<1<2
							faceNodeNum = str(nodeDictNodeToNum[vertexThree])+" "\
								+str(nodeDictNodeToNum[vertexOne])+" "+str(nodeDictNodeToNum[vertexTwo])
					else:#2<1
						if nodeDictNodeToNum[vertexOne] < nodeDictNodeToNum[vertexThree]:#2<1<3
							faceNodeNum = str(nodeDictNodeToNum[vertexTwo])+" "\
								+str(nodeDictNodeToNum[vertexOne])+" "+str(nodeDictNodeToNum[vertexThree])
						else:#3<1
							if nodeDictNodeToNum[vertexTwo] < nodeDictNodeToNum[vertexThree]:#2<3<1
								faceNodeNum = str(nodeDictNodeToNum[vertexTwo])+" "\
									+str(nodeDictNodeToNum[vertexThree])+" "+str(nodeDictNodeToNum[vertexOne])
							else:#3<2<1
								faceNodeNum = str(nodeDictNodeToNum[vertexThree])+" "\
									+str(nodeDictNodeToNum[vertexTwo])+" "+str(nodeDictNodeToNum[vertexOne])
					
					
					if faceNodeNum not in faceSet:
						faceNum+=1
						faceSet.add(faceNodeNum)
						faceNumToFace[faceNum]=faceNodeNum
			
		#part和hole信息
		#判断是part还是hole
		if file.find("hole") == -1:#是part，不是hole
			volumeMark=0#标记体积信息是否收集全
			for line in allLineList:
				lineList=line.split()#linelist是基体储存每一行字符串的list.
				if lineList[0]=="facet":
					facetNormal[0]=lineList[2]
					facetNormal[1]=lineList[3]
					facetNormal[2]=lineList[4]
				if lineList[0]=="vertex":
					volumeMark+=1
					if volumeMark%3 == 1:#面的第一个点
						volumeNodeOne[0]=lineList[1]
						volumeNodeOne[1]=lineList[2]
						volumeNodeOne[2]=lineList[3]
					if volumeMark%3 == 2:#面的第二个点
						volumeNodeTwo[0]=lineList[1]
						volumeNodeTwo[1]=lineList[2]
						volumeNodeTwo[2]=lineList[3]
					if volumeMark%3 == 0:#面的第三个点，此处不用考虑vertexNum==0的情况。
						volumeNodeThree[0]=lineList[1]
						volumeNodeThree[1]=lineList[2]
						volumeNodeThree[2]=lineList[3]
						#计算体内的点坐标
						volumeNode[0]=((float(volumeNodeOne[0])+float(volumeNodeTwo[0])+
							float(volumeNodeThree[0]))/3 - 0.01*float(facetNormal[0]))
						volumeNode[1]=((float(volumeNodeOne[1])+float(volumeNodeTwo[1])+
							float(volumeNodeThree[1]))/3 - 0.01*float(facetNormal[1]))
						volumeNode[2]=((float(volumeNodeOne[2])+float(volumeNodeTwo[2])+
							float(volumeNodeThree[2]))/3 - 0.01*float(facetNormal[2]))
						part.append((volumeNode[0],volumeNode[1],volumeNode[2]))
						break
						
		else:#不是part, 是hole
			volumeMark=0#标记体积信息是否收集全
			for line in allLineList:
				lineList=line.split()#linelist是基体储存每一行字符串的list.
				if lineList[0]=="facet":
					facetNormal[0]=lineList[2]
					facetNormal[1]=lineList[3]
					facetNormal[2]=lineList[4]
				if lineList[0]=="vertex":
					volumeMark+=1
					if volumeMark%3 == 1:#面的第一个点
						volumeNodeOne[0]=lineList[1]
						volumeNodeOne[1]=lineList[2]
						volumeNodeOne[2]=lineList[3]
					if volumeMark%3 == 2:#面的第二个点
						volumeNodeTwo[0]=lineList[1]
						volumeNodeTwo[1]=lineList[2]
						volumeNodeTwo[2]=lineList[3]
					if volumeMark%3 == 0:#面的第三个点，此处不用考虑vertexNum==0的情况。
						volumeNodeThree[0]=lineList[1]
						volumeNodeThree[1]=lineList[2]
						volumeNodeThree[2]=lineList[3]
						#计算hole的点坐标
						volumeNode[0]=((float(volumeNodeOne[0])+float(volumeNodeTwo[0])+
							float(volumeNodeThree[0]))/3 - 0.1*float(facetNormal[0]))
						volumeNode[1]=((float(volumeNodeOne[1])+float(volumeNodeTwo[1])+
							float(volumeNodeThree[1]))/3 - 0.1*float(facetNormal[1]))
						volumeNode[2]=((float(volumeNodeOne[2])+float(volumeNodeTwo[2])+
							float(volumeNodeThree[2]))/3 - 0.1*float(facetNormal[2]))
						hole.append((volumeNode[0],volumeNode[1],volumeNode[2]))
						break
		stl.close()
	#返回一个tuple，为（nodeNumber, nodeDict, faceNum,  faceNumToFace,  hole,      part）
	#                  data[0],     data[1] , data[2],  data[3],        data[4],   data[5]
	return nodeNumber,nodeDict,faceNum,faceNumToFace,hole,part
	
						
#写入poly文件
def writepoly():
	data=nodeFaceHolePart()#获得nodeFaceHolePart的数据
	poly = open("poly.poly","w")
	poly.write("# Part 1 - the node list.""\n")
	poly.write(str(data[0]))
	poly.write(" 3 0 0""\n")
	for i in range(1,data[0]+1):
		poly.write(str(i))
		poly.write(" ")
		poly.write(data[1][i])
		poly.write("\n")
	#写入面标号对照表
	poly.write("# Part 2 - the facet list""\n")
	poly.write(str(data[2]))
	poly.write(" 0""\n")
	for i in range(1,data[2]+1):
		poly.write("1""\n")
		poly.write("3")
		poly.write(" ")
		poly.write(data[3][i])
		poly.write("\n")
	
	#写入hole
	poly.write("# Part 3 - hole list""\n")
	poly.write(str(len(data[4]))+"\n")
	for i in range(1,len(data[4])+1):
		poly.write(str(i)+" ")
		poly.write(str(data[4][i-1][0])+" "+str(data[4][i-1][1])+" "+str(data[4][i-1][2])+"\n")
	
	#写入part
	poly.write("# Part 4 - region list""\n")
	poly.write(str(len(data[5]))+"\n")
	for i in range(1,len(data[5])+1):
		poly.write(str(i)+" ")
		poly.write(str(data[5][i-1][0])+" "+str(data[5][i-1][1])+" "+str(data[5][i-1][2])+" ")
		poly.write(str(i)+" 10000""\n")
	poly.close()
writepoly()	
