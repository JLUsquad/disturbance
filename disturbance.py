# coding: utf-8

'''
实现对结构的扰动
给出扰动之后的分数坐标
写出文件
'''

import numpy as np
import sys
import os
from read import Read
import math
PI=3.1415926

def disturbance(path,strength=20,index=40.0):
	poscar=Read(path).getStructure()
	
	'''
	poscar={'comment':comment,
				'lattice':lattice,
				'elements':elements,
				'numbers':numbers,
				'type':type,
				'positions':positions,
				'constraints':constraints}
	coor_0为分数坐标矩阵，每行对应每个原子的分数坐标
	lat_mat为基矢量矩阵
	n_atoms为原子数
	elements为元素列表
	numbers为对应的元素原子数目列表
	strength控制扰动强度
	index控制扰动精度
	'''

	filetype=poscar['type']



	coor_0=np.mat(poscar['positions'])
	lat_mat=np.mat(poscar['lattice'])
	if (filetype=='Direct'):
		coor_1=coor_0*lat_mat
	else:
		print 'you need a Direct type poscar file'
		return 
	elements=list(poscar['elements'])
	numbers=list(poscar['numbers'])
	n_atoms=np.shape(coor_0)[0]
	#coor_1,coor_2为原子的直角坐标

	
	for i in range(1,strength+1):
	#20轮扰动测试,一轮更比一轮强
		disturbance_path='./file_vasp/file_%d'%i
		xyz_path='./file_xyz/file_xyz_%d' % i
		folder_xyz=os.path.exists(xyz_path)
		if not folder_xyz:
			os.makedirs(xyz_path)
		else:
			pass
		folder=os.path.exists(disturbance_path)
		if not folder:
			os.makedirs(disturbance_path)
		else:
			pass
		j=1
		while j <= 100:
		#每次扰动测试进行100次
			
			coor_2=coor_1.copy()
			#random_mat=(np.mat(np.random.rand(n_atoms,3))-0.5)*i/40.0
			
			random_mat_0=np.mat(np.random.rand(n_atoms,2))
			random_mat_0[:,0]=2*PI*random_mat_0[:,0]
			random_mat_0[:,1]=PI*random_mat_0[:,1]
			random_mat=np.mat(np.ones((n_atoms,3)))
			for k in range(n_atoms):
				random_mat[k,0]=i/index*math.sin(random_mat_0[k,1])*math.cos(random_mat_0[k,0])
				random_mat[k,1]=i/index*math.sin(random_mat_0[k,1])*math.sin(random_mat_0[k,0])
				random_mat[k,2]=i/index*math.cos(random_mat_0[k,1])
			
			#生成与直角坐标对应的扰动矩阵
			coor_2=coor_2+random_mat
			#扰动后的直角坐标矩阵
			coor_3=coor_2*lat_mat.I
			#扰动后的分数坐标矩阵;
			coor_3=np.array(coor_3)
			ida=coor_3<0.0
			coor_3[ida]=coor_3[ida]+1.0
			ida=coor_3>1.0
			coor_3[ida]=coor_3[ida]-1.0
			coor_3=np.mat(coor_3)
			#调整扰动后的原子位置到一个晶胞中
			
			filename='./%s/Coordinate(%d_%d).vasp' % (disturbance_path,i,j)
			filename_xyz='./%s/Coorinate(%d_%d).xyz' %(xyz_path,i,j)
			filename=unicode(filename,"utf8")
			fp=open(filename,'w')
			for k in range(len(elements)):
				fp.write(elements[k])
				fp.write(str(numbers[k]))
			fp.write('\n')
			fp.write('1.00000\n    ')
			#fp.write(str(lat_mat))
			for m in range(np.shape(lat_mat)[0]):
				for n in range(np.shape(lat_mat)[1]):
					fp.write(str(lat_mat[m,n]))
					fp.write('      ')
				fp.write('\n    ')
			for k in range(len(elements)):
				fp.write(elements[k])
				fp.write('  ')
			fp.write('\n    ')
			for k in range(len(numbers)):
				fp.write(str(numbers[k]))
				fp.write('  ')
			fp.write('\n')
			#fp.write(str(coor_3))
			fp.write('Direct\n    ')
			for m in range(np.shape(coor_3)[0]):
				for n in range(np.shape(coor_3)[1]):
					fp.write(str(coor_3[m,n]))
					fp.write('  ')
				fp.write('\n     ')
			fp.close()
			fp=open(filename_xyz,'w')
			fp.write(str(n_atoms))
			fp.write('\n')
			fp.write(str(poscar['elements'])+str(poscar['numbers']))
			fp.write('\n')
			
			for atom_number in range(n_atoms):
				fp.write(poscar['elements'][0])
				fp.write(' ')
				for position in range(3):
					fp.write(str((coor_1)[atom_number,position]))
					fp.write(' ')
				fp.write('\n')
			fp.write(str(n_atoms))
			fp.write('\n')
			fp.write(str(i))
			fp.write('_')
			fp.write(str(j))
			fp.write('\n')
			for atom_number in range(n_atoms):
				fp.write(poscar['elements'][0])
				fp.write(' ')
				for position in range(3):
					fp.write(str((coor_2)[atom_number,position]))
					fp.write(' ')
				fp.write('\n')
			fp.close()

				
			
			j += 1