import numpy as np

def return_qe_outfile_lines(qe_outfile_path):
	in_file = open(qe_outfile_path, 'r')
	in_lines = in_file.readlines()
	in_file.close()
	return in_lines

def return_bravais_lattice(qe_outfile_path):
	lines = return_qe_outfile_lines(qe_outfile_path)
	for i, line in enumerate(lines):
		if line.find('bravais-lattice index') != -1:
			split_line = line.split()
			bravais_lattice = int(split_line[3])
			# need to create dictionary for bravais lattice information
	return bravais_lattice


def reassign_negative_coordinates(xyz_vector, crystal_vectors_list):
   # takes a cartesian vector and crystal vectors, then converts any negative values to positive values
   # at present, I am only certain it works for cases where the crystal vectors are single component example:
   # ([a1, 0.0, 0.0], [0.0, a2, 0.0], [0.0, 0.0, a3])
   	for i, coordinate in enumerate(xyz_vector):
   		if coordinate < 0.0:
   			tmp_xyz_vector = np.array(xyz_vector) + np.array(crystal_vectors_list[i])
   			xyz_vector = tmp_xyz_vector

   	return xyz_vector





def get_crystal_vectors(optimization_file):
	# extract the primitive vectors from QE optimization output
	# return a list of three np.array() vectors in cartesian space with units of Angstrom
	in_file = open(optimization_file, 'r')
	in_lines = in_file.readlines()
	in_file.close()

	for i, line in enumerate(in_lines):
		if line.find('celldm(1)') != -1:
			split_line = line.split()
			alat_bohr = float(split_line[1])
			alat = alat_bohr/float(1.8897259885789)
		
		if line.find('crystal axes: (cart. coord. in units of alat)') != -1:
			index_i = i + 1

		if line.find('reciprocal axes: (cart. coord. in units 2 pi/alat)') != -1:
			index_f = i - 1
			break

	parsed_lines = in_lines[index_i:index_f]
	crystal_vectors_list = []
	for i, line in enumerate(parsed_lines):
		split_line = line.split()
		parsed_line = split_line[3:-1]
		x = alat*float(parsed_line[0])
		y = alat*float(parsed_line[1])
		z = alat*float(parsed_line[2])
		crystal_vectors_list.append(np.array([x, y, z]))

	return crystal_vectors_list



def get_optimized_coordinates(optimization_file):
	# extract the final coordinates from QE optimization output
	# return a list, each entry is in the form ['atom_string', [float(x), float(y), float(z)]]
	# right now, assume cartesian space
	crystal_vectors_list = get_crystal_vectors(optimization_file)

	in_file = open(optimization_file, 'r')

	in_lines = in_file.readlines()
	in_file.close()

	a1, a2, a3 = crystal_vectors_list[0], crystal_vectors_list[1], crystal_vectors_list[2]

	index_i = 0
	index_f = 0
	for i, line in reversed(list(enumerate(in_lines))):
		if line.find('ATOMIC_POSITIONS (angstrom)') != -1:
			index_i = i + 1
			break

	for i, line in reversed(list(enumerate(in_lines))):
		if line.find('End final coordinates') != -1:
			index_f = i
			break

	parsed_lines = in_lines[index_i:index_f]
	for line in parsed_lines:
		split_line = line.split()
		atom_string = split_line[0]
		x = split_line[1]		
		y = split_line[2]
		z = split_line[3]
		xyz_vector = np.array([float(x), float(y), float(z)])
		# convert any negative numbers
		#if any(value < 0.0 for value in xyz_vector):
		#	xyz_vector = reassign_negative_coordinates(xyz_vector, crystal_vectors_list)

		coordinates_list.append( [atom_string, xyz_vector] )
	

	return coordinates_list







def main():

	filename = "w2_100_SB_H4.out"

	crystal_vectors = get_crystal_vectors(filename)


	coordinates = get_optimized_coordinates(filename)
	
	for coordinate in coordinates:
		print coordinate
		print type(coordinate)

#main()
