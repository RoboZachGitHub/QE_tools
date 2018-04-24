import numpy as np


def return_qe_outfile_lines(qe_outfile_path):
	in_file = open(qe_outfile_path, 'r')
	in_lines = in_file.readlines()
	in_file.close()
	return in_lines


def job_done_checker(qe_outfile_path):
    in_file = open(qe_outfile_path)
    text = in_file.read()
    if text.rfind('JOB DONE.') != -1:
        return True
    else:
        print "\"JOB DONE.\" not found in {}".format(qe_outfile_path)
        return False



def return_number_of_atoms(outfile_path):
    in_lines = return_qe_outfile_lines(outfile_path)
    
    index_i = 0
    for i, line in enumerate(in_lines):
        if line.find('number of atoms/cell') != -1:
            index_i = i
            break
    
    number_of_atoms = int(in_lines[index_i].split()[4])
    return number_of_atoms


def return_bravais_lattice(qe_outfile_path):
	lines = return_qe_outfile_lines(qe_outfile_path)
	for i, line in enumerate(lines):
		if line.find('bravais-lattice index') != -1:
			split_line = line.split()
			bravais_lattice = int(split_line[3])
			# need to create dictionary for bravais lattice information
	return bravais_lattice

def return_a_0(qe_outfile_path):
	# returns first primitive vector in angstroms
	lines = return_qe_outfile_lines(qe_outfile_path)
	for i, line in enumerate(lines):
		if line.find('lattice parameter (a_0)') != -1:
			split_line = line.split()
			a_0_bohr = float(split_line[4])
			# convert to angstroms
			a_0 = a_0_bohr*0.529177
			break
	return a_0

def return_celldms(qe_outfile_path):
	# returns all 6 celldm() values as a list of floats, those not used are simply equal to 0.0
	# no unit converstions are made
	in_file = open(qe_outfile_path, 'r')
	in_lines = in_file.readlines()
	in_file.close()

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


def return_crystal_vectors(optimization_outfile_path):
	# extract the primitive vectors from QE optimization output
	# return a list of three np.array() vectors in cartesian space with units of Angstrom
	in_file = open(optimization_outfile_path, 'r')
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


def return_optimization_coordinates(optimization_outfile_path):
	# extract the final coordinates from QE optimization output
	# return a list, each entry is in the form ['atom_string', [float(x), float(y), float(z)]]
	# right now, assume cartesian space
	crystal_vectors_list = return_crystal_vectors(optimization_outfile_path)

	in_lines = return_qe_outfile_lines(optimization_outfile_path)

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


def return_phonons_list(phonon_outfile_path):
    # extract the phonons from QE output
    # returns a list of phonons in wavenumbers as floats

    in_lines = return_qe_outfile_lines(phonon_outfile_path)
    
    # search for the number of atoms for which phonons were computed
    tagger = 'Compute atoms:'
    for i, line in enumerate(in_lines):
    	if line.find(tagger) != -1:
    		index = i
    		break
    num_atoms = len(in_lines[i].split()) - 2

    # search in reverse for the list of phonon values
    tagger = '**************************************************************************'
    for i, line in reversed(list(enumerate(in_lines))):
        if line.find(tagger) != -1:
            index = i
            break
    
    phonon_lines = in_lines[index - 3*num_atoms:index]
    #for line in phonon_lines:
    #    print line
    #number_to_grab = int(raw_input("number of phonons to grab (starting from bottom): "))
    number_to_grab = num_atoms*3

    parsed_phonons = phonon_lines[-number_to_grab:]

    phonons_floats_list = [float(phonon.split()[4]) for phonon in parsed_phonons]   
    return phonons_floats_list

	

def return_final_energy(qe_scf_or_opt_outfile_path):

	in_lines = return_qe_outfile_lines(qe_scf_or_opt_outfile_path)

	tagger = 'Final energy'
	for i, line in reversed(list(enumerate(in_lines))):
			if line.find(tagger) != -1:
				index = i + 1
				break

	scf_energy = float(in_lines[i].split()[3])

	return scf_energy

