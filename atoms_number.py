from read import Read
import os

def get_atom_number(structure_dir):
	file_list=os.listdir(structure_dir)
	print 'structure_dir:\n'
	print structure_dir
	print '\n'
	print 'file_list\n'
	print file_list
	structure_list=[]
	length=len(file_list)
	for i in range(length):
			if not os.path.isdir(file_list[i]):
				structure_list.append(file_list[i])
	print '\nstructure_list\n'
	print structure_list
	a=open('structures_atom_number.txt','w')
	length=len(structure_list)
	for i in range(length):
		print structure_list[i]
		number=Read('%s').getStructure()['numbers'] % structure_list[i]
		print number
		a.write('%s---------%d\n') % (structure_list[i],number)
	a.close()

