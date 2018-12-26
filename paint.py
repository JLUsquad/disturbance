#coding: utf-8

import sys
sys.path.append('/home/chenzhaoxv/BCM/BCM/BCM')
from pbcm import Bcm
from matplotlib import pyplot as plt
import os
from read import Read
import numpy as np
import shutil

def BCM_distance(folderpath,path_o):
	#folder-file——vasp文件夹
	#path_o——结构原型的文件夹
	a=open('disturbance.txt','w')
	listdir_o=os.listdir(folderpath)
	listdir=[]
	length=len(listdir_o)
	for i in range(length):
		listdir_o[i]=folderpath + '/' +str(listdir_o[i])
		if  os.path.isdir(listdir_o[i]):
			listdir.append(listdir_o[i])
	dir_num=len(listdir)
	bcmostore = Bcm().calc_folder(path_o)
	bcmostore=np.mat(bcmostore[0][0])
	for i in range(1,dir_num+1):
		times=i
		filepath='%s/file_%d' % (folderpath,i)
		bcmstore = []
		distostore = []
		resultmat = Bcm().calc_folder(filepath)
		for result in resultmat:
			bcmstore.append(np.mat(result[0]))	
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
		for k in range(100):
			plt.scatter(times,distostore[k],marker='+',c='r',s=1)
			x+=distostore[k]
		plt.scatter(times,x/100.0,marker='o',c='b')
	a.close()
	plt.show()

#def glosim_distance(structure_path):
	
	'''
	k=0
	for root,dirs,files in os.walk(structure_path):
		for file in files:
			try:
				test = Read(file)
			except Exception:
				continue
			k += 1
			filepath=
	#列出所有文件和目录名的列表
	x_list=os.listdir(structure_path)
	structure_path='/home/chenzhaoxv/Desktop/1/POSCAR'
	x_num=len(x_list)
	#列出所有目录名的列表
	dir_list=[]
	for i in range(x_num):
		x_list[i]=structure_path+'/'+str(x_list[i]) 
		print x_list[i]
		if os.path.isdir(x_list[i]):
			dir_list.append(x_list[i])
	#进入某一结构的目录，包含原结构及子文件夹中的扰动结构
	print dir_list
	dir_num=len(dir_list)
	

	for i in range(dir_num):
		os.chdir(dir_list[i])
		cwd=os.getcwd()
		print "dir:%s" % cwd
		y_list=os.listdir(dir_list[i])
		print y_list
		y_num=len(y_list)
		disturbance_dir=[]
		for j in range (y_num):
			y_list[j]=cwd + '/' + str(y_list[j])
			print y_list[j]
			#扰动结构文件夹
			if os.path.isdir(y_list[j]):
				disturbance_dir.append(y_list[j])
			#结构原型文件
			elif y_list[j].endswith('.vasp'):
				poscar=Read(y_list[j]).getStructure()
				xyz_coor=np.mat(poscar['positions'])*np.mat(poscar['lattice'])
				xyz_numbers=len(poscar['positions'])
				xyz_explain=str(poscar['elements'])+str(poscar['numbers'])

				if xyz_numbers != np.shape(xyz_coor)[0]:
					print "file has mistake"
		print disturbance_dir

		disturbance_dir_num=len(disturbance_dir)
		#生成xyz文件夹
		xyz_dir_list=[]
		for k in range(1,1+disturbance_dir_num):
			xyz_dir=dir_list[i] + '/' + 'xyz_file_%d' % k
			folder=os.path.exists(xyz_dir)
			if not folder:
				os.mkdir(xyz_dir)
				xyz_dir_list.append(xyz_dir)
			else:
				pass
		#在扰动结构文件夹中生成xyz文件
		for o in range(1,1+disturbance_dir_num):
			os.chdir(disturbance_dir[o])
			file_list=os.listdir(os.getcwd())
			file_num=len(file_list)
			cwd_file=os.getcwd()
			print cwd_file
			
			for p in range(1,21):
				if str(cwd_file).endswith(str(p)):
					break
				else:
					p += 1
			temp=p
			for l in range(1,1+file_num):
				#写出结构原型的xyz形式
				filename_xyz='%s/Coordinate(%d_%d).xyz' % (cwd_file,temp,l)
				fp_xyz=open(filename_xyz,'w')
				fp_xyz.write(str(xyz_numbers))
				fp_xyz.write('\n')
				fp_xyz.write(str(xyz_explain))
				fp_xyz.write('\n')
				for atom_num in range(np.shape(xyz_coor)[0]):
					for atom_position in range(np.shape(xyz_coor)[1]):
						fp_xyz.write(str(xyz_coor[atom_num,atom_position]))
						fp_xyz.write(' ')
					fp_xyz.write('\n')
				#写出扰动结构的xyz形式
				filename_vasp='%s/Coordinate(%d_%d).vasp' % (cwd_file,temp,l)
				fp_vasp=open(filename_vasp,'r')
				line=0
				lattice_m=np.shape(np.mat(poscar['lattice']))[0]
				disturbance_xyz_lattice=[]
				distirbance_xyz_positions=[]
				for line in fp_vasp.readlines():
					line +=1
					if line>2 and line<3+lattice_m:
						line=line.split()
						disturbance_xyz_lattice.append(line)
					elif line>5+lattice_m and line<=5+lattice_m+xyz_numbers:
						line=line.split()
						distirbance_xyz_positions.append(line)
				fp_vasp.close()
				disturbance_xyz_lattice=np.mat(disturbance_xyz_lattice)
				distirbance_xyz_positions=np.mat(distirbance_xyz_positions)
				distirbance_xyz_positions=distirbance_xyz_positions*disturbance_xyz_lattice
				fp_xyz.write(str(xyz_numbers))
				fp_xyz.write('\n')
				fp_xyz.write(str(filename_vasp))
				fp_xyz.write('\n')
				for atom_number in range(np.shape(distirbance_xyz_positions)[0]):
					for atom_position in range(np.shape(distirbance_xyz_positions)[1]):
						fp_xyz.write(str(distirbance_xyz_positions[atom_number,atom_position]))
						fp_xyz.write(' ')
					fp_xyz.write('\n')
				fp_xyz.close()
				shutil.move('%s','%s') % filename_xyz,xyz_dir[j]
	'''



					
				
				
				
				
				


		