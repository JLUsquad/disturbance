import os
import linecache
from matplotlib import pyplot as plt

path_xyz='/home/chenzhaoxv/Desktop/analysis_C/1-ICSD-2513.vasp/file_xyz'

dirlist=os.listdir(path_xyz)
os.chdir(path_xyz)
for i in range(20):
    work_dir = os.getcwd() + '/' + str(dirlist[i])
    os.chdir(work_dir)
    file_list = os.listdir(os.getcwd())
    file_list_length = len(file_list)
    filelist = []
    for j in range(file_list_length):
        if  str(file_list[j]).endswith('.sim'):
            filelist.append(file_list[j])
    filelist_length = len(filelist)
    ave = 0.0
    for j in range(filelist_length):
        filelist[j] = os.getcwd() + '/' + str(filelist[j])
        distance = linecache.getline(filelist[j],2).strip('\n').split()[1]
        distance=float(distance)
        plt.scatter(i,distance,marker='+',c='r',s=1)
        ave += distance
    plt.scatter(i,ave)
    os.chdir(path_xyz)
plt.show()