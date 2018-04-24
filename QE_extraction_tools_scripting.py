import numpy as np


def return_qe_outfile_lines(qe_outfile_path):
	in_file = open(qe_outfile_path, 'r')
	in_lines = in_file.readlines()
	in_file.close()
	return in_lines


def return_celldms(qe_outfile_lines):
	# returns all 6 celldm() values as a list of floats, those not used are simply equal to 0.0
	# no unit converstions are made

	in_lines = qe_outfile_lines

	index_i = None
	index_f = None
	for i, line in enumerate(in_lines):
		if line.find('celldm(1)') != -1:
			index_i = i
			break

	split_line = (in_lines[index_i] + in_lines[index_i + 1]).split()
	celldms_strings_list = split_line[1::2]
	celldms = [float(i) for i in celldms_strings_list]
	
	return celldms


def return_number_of_atoms(qe_outfile_lines):
    
    in_lines = qe_outfile_lines

    index_i = 0
    for i, line in enumerate(list(in_lines)):
        if line.find('number of atoms/cell') != -1:
			index_i = i
			break

    number_of_atoms = int(in_lines[index_i].split()[4])
    return number_of_atoms


#def return_crystal_vectors(qe_outfile_lines):
#	# extract the primitive vectors from QE optimization output
#	# return a list of three np.array() vectors in cartesian space with units of Angstrom
#	in_lines = qe_outfile_lines
#
#	for i, line in enumerate(in_lines):
#		if line.find('celldm(1)') != -1:
#			split_line = line.split()
#			alat_bohr = float(split_line[1])
#			alat = alat_bohr/float(1.8897259885789)
#		
#		if line.find('crystal axes: (cart. coord. in units of alat)') != -1:
#			index_i = i + 1
#
#		if line.find('reciprocal axes: (cart. coord. in units 2 pi/alat)') != -1:
#			index_f = i - 1
#			break
#
#	parsed_lines = in_lines[index_i:index_f]
#	crystal_vectors_list = []
#	for i, line in enumerate(parsed_lines):
#		split_line = line.split()
#		parsed_line = split_line[3:-1]
#		x = alat*float(parsed_line[0])
#		y = alat*float(parsed_line[1])
#		z = alat*float(parsed_line[2])
#		crystal_vectors_list.append(np.array([x, y, z]))
#
#	return crystal_vectors_list

def coordinate_processing(celldms, number_of_atoms, coordinates_list):
	# returns two lists, coordinates in crystal units and in Cartesians 
	# [['H', [0.0, 0.0, 0.0]], ['C', [0.0, 1.0, 1.35]], ...]
	# perhaps i should use named tuples 

	# search first line for coordinate type
	if coordinates_list[0].find('crystal') != -1:
		coordinates_list_no_header = coordinates_list[1:number_of_atoms+1]
		crystal_coordinates = coordinates_list_no_header
		print crystal_coordinates

		#blah blah conversian to cartesians
		cartesian_coordinates = None

	elif coordinates_list[0].find('positions (a_0 units)') != -1:
		coordinates_list_no_header = coordinates_list[1:number_of_atoms+1]
		a_0_bohr = celldms[0]
		a_0_angstrom = a_0_bohr*0.529177
		print coordinates_list_no_header
		#cartesian_coordinates = coordinates_list_no_header

		#blah blah conversian to crystals
		#crystal_coordinates = None


	#return cartesian_coordinates, crystal_coordinates



def return_coordinates2(qe_outfile_lines):
	# extract the final coordinates from QE output
	# return a list, each entry is in the form ['atom_string', [float(x), float(y), float(z)]]
	# right now, assume cartesian space

	in_lines = qe_outfile_lines

	number_of_atoms = return_number_of_atoms(in_lines)

	#a1, a2, a3 = crystal_vectors_list[0], crystal_vectors_list[1], crystal_vectors_list[2]

	index_i = None
	index_f = None

	#different routines needed for scf and opt
	opt_id_string = 'ATOMIC_POSITIONS '
	opt_check = False
	for i, line in reversed(list(enumerate(in_lines))):
		if line.find(opt_id_string) != -1:
			opt_check = True

	print "opt_check is {}".format(opt_check)

	if opt_check:		
		index_finder_string = 'ATOMIC_POSITIONS '
		for i, line in reversed(list(enumerate(in_lines))):
			if line.find(index_finder_string) != -1:
				index_i = i 
				break

	else:
		index_finder_string = 'site n.     atom '
		for i, line in enumerate(in_lines):
			if line.find(index_finder_string) != -1:
				index_i = i 
				break

	index_f = index_i + number_of_atoms

	parsed_lines = in_lines[index_i:index_f]

	coordinate_processing(return_celldms(in_lines), return_number_of_atoms(in_lines), parsed_lines)
	#cartesian_coordinates, crystal_coordinates = coordinate_processing(return_celldms(in_lines), return_number_of_atoms(in_lines), parsed_lines)

#		coordinates_list = []
#		for line in parsed_lines:
#			split_line = line.split()
#			print "NEED TO DEAL WITH CRYSTAL VS CART COORDS, probably always convert to crystals"
#			atom_string = split_line[0]
#			x = split_line[1]		
#			y = split_line[2]
#			z = split_line[3]
#			xyz_vector = np.array([float(x), float(y), float(z)])
#
#			coordinates_list.append( [atom_string, xyz_vector] )
	




#		coordinates_list = []
#		for line in parsed_lines:
#			print "NEED TO DEAL WITH CRYSTAL VS CART COORDS, probably always convert to crystals"
#			split_line = line.split()
#			atom_string = split_line[1]
#			x = split_line[6]		
#			y = split_line[7]
#			z = split_line[8]
#			xyz_vector = np.array([float(x), float(y), float(z)])
#			# convert any negative numbers
#			#if any(value < 0.0 for value in xyz_vector):
#			#	xyz_vector = reassign_negative_coordinates(xyz_vector, crystal_vectors_list)
#	
#			coordinates_list.append( [atom_string, xyz_vector] )
#	
#	return coordinates_list



def return_coordinates(qe_outfile_lines):
	# extract the final coordinates from QE output
	# return a list, each entry is in the form ['atom_string', [float(x), float(y), float(z)]]
	# right now, assume cartesian space

	in_lines = qe_outfile_lines

	number_of_atoms = return_number_of_atoms(in_lines)

	#a1, a2, a3 = crystal_vectors_list[0], crystal_vectors_list[1], crystal_vectors_list[2]

	index_i = None
	index_f = None

	#different routines needed for scf and opt
	opt_id_string = 'End final coordinates'
	opt_check = False
	for i, line in reversed(list(enumerate(in_lines))):
		if line.find(opt_id_string) != -1:
			opt_check = True

	print "opt_check is {}".format(opt_check)

	if opt_check:		
		index_finder_string = 'ATOMIC_POSITIONS '
		for i, line in reversed(list(enumerate(in_lines))):
			if line.find(index_finder_string) != -1:
				index_i = i + 1
				break

		index_f = index_i + number_of_atoms

		parsed_lines = in_lines[index_i:index_f]

		coordinates_list = []
		for line in parsed_lines:
			split_line = line.split()
			print "NEED TO DEAL WITH CRYSTAL VS CART COORDS, probably always convert to crystals"
			atom_string = split_line[0]
			x = split_line[1]		
			y = split_line[2]
			z = split_line[3]
			xyz_vector = np.array([float(x), float(y), float(z)])

			coordinates_list.append( [atom_string, xyz_vector] )
	
	else:
		index_finder_string = 'site n.     atom '
		for i, line in enumerate(in_lines):
			if line.find(index_finder_string) != -1:
				index_i = i + 1
				break

		index_f = index_i + number_of_atoms

		parsed_lines = in_lines[index_i:index_f]

		coordinates_list = []
		for line in parsed_lines:
			print "NEED TO DEAL WITH CRYSTAL VS CART COORDS, probably always convert to crystals"
			split_line = line.split()
			atom_string = split_line[1]
			x = split_line[6]		
			y = split_line[7]
			z = split_line[8]
			xyz_vector = np.array([float(x), float(y), float(z)])
			# convert any negative numbers
			#if any(value < 0.0 for value in xyz_vector):
			#	xyz_vector = reassign_negative_coordinates(xyz_vector, crystal_vectors_list)
	
			coordinates_list.append( [atom_string, xyz_vector] )
	
	return coordinates_list




