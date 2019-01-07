import os

path_xyz='/home/chenzhaoxv/Desktop/analysis_C/1-ICSD-2513.vasp/file_xyz'

filelist = []
for root,dirs,files in os.walk(path_xyz):
    for file in files:
        temp=os.path.join(root,file)
        if str(temp).endswith('.xyz'):
          filelist.append(temp)
filelist_length = len(filelist)
fp = open(path_xyz+'.txt','w')
for i in range(filelist_length):
    fp.write(filelist[i])
    fp.write('\n')
fp.close()
fp = open(path_xyz+'.txt','r')
for line in fp.readlines():
    line=str(line)
    line=line.strip('\n')
    strcmd = str('python glosim.py '+line+' --distance')
    
    strcmd=strcmd.replace('(','\(')
    strcmd=strcmd.replace(')','\)')
    os.system('cd /home/chenzhaoxv/glosim ; %s' % strcmd)