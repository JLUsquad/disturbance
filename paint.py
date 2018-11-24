import sys
sys.path.append('/home/chenzhaoxv/BCM/BCM/BCM')
from pbcm import Bcm
from matplotlib import pyplot as plt
import os


def disturbance(folderpath,path_o):
	a=open('disturbance.txt','w')
	listdir_o=os.listdir(folderpath)
	listdir=[]
	length=len(listdir_o)
	for i in range(length):
		if  os.path.isdir(listdir_o[i]):
			listdir.append(listdir_o[i])
	dir_num=len(listdir)
	bcmostore = Bcm().calc_folder(path_o)
	bcmostore=bcmostore[0][0]
	for i in range(1,dir_num+1):
		times=i
		filepath='%s/file_%d' % (folderpath,i)
		bcmstore = []
		distostore = []
		resultmat = Bcm().calc_folder(filepath)
		for result in resultmat:
			bcmstore.append(result[0])	
		k = len(bcmstore)
		for k in range(k):
			dist = Bcm().distxy(bcmstore[k],bcmostore)
			distostore.append(dist)
		for num in distostore:
			num = str(num)
			a.write(num)
			a.write('\n')
		a.write('\n\n\n')
		x=0
		for ll in range(100):
			plt.scatter(times,distostore[ll],marker='+',c='r',s=1)
			x+=distostore[ll]
		plt.scatter(times,x/100.0,marker='o',c='b')
	a.close()
	plt.show()