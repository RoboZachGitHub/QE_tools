import numpy as np
import re
from collections import namedtuple


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

def return_k_point_definition(outfile_path):
    in_lines = return_qe_outfile_lines(outfile_path)
    
    index_i = 0
    for i, line in enumerate(in_lines):
    	pass
        #if line.find('number of atoms/cell') != -1:
        #    index_i = i
        #    break
    return 0

def return_number_of_atoms(outfile_path):
    in_lines = return_qe_outfile_lines(outfile_path)
    
    index_i = 0
    for i, line in enumerate(in_lines):
        if line.find('number of atoms/cell') != -1:
            index_i = i
            break
    
    number_of_atoms = int(in_lines[index_i].split()[4])
    return number_of_atoms

def return_ecuts(outfile_path):
	in_lines = return_qe_outfile_lines(outfile_path)
	index_i = 0
	for i, line in enumerate(in_lines):
	    if line.find('kinetic-energy cutoff') != -1:
	        index_i = i
	        break
	    
	ecut_wfc = float(in_lines[index_i].split()[3])
	ecut_rho = float(in_lines[index_i+1].split()[4])
	return ecut_wfc, ecut_rho


def return_number_of_bands(outfile_path):
    in_lines = return_qe_outfile_lines(outfile_path)
    
    index_i = 0
    for i, line in enumerate(in_lines):
        if line.find('number of Kohn-Sham states') != -1:
            index_i = i
            break
    
    number_of_bands = int(in_lines[index_i].split()[4])
    return number_of_bands


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
	# extract only the final coordinates from QE optimization output
	# return a list, each entry is in the form ['atom_string', [float(x), float(y), float(z)]]
	coordinates_list = []
	crystal_vectors_list = return_crystal_vectors(optimization_outfile_path)

	in_lines = return_qe_outfile_lines(optimization_outfile_path)

	a1, a2, a3 = crystal_vectors_list[0], crystal_vectors_list[1], crystal_vectors_list[2]

	index_i = 0
	index_f = 0
	for i, line in reversed(list(enumerate(in_lines))):
		if line.find('ATOMIC_POSITIONS (') != -1:
			index_i = i + 1
			break


	for i, line in reversed(list(enumerate(in_lines))):
		if line.find('End final coordinates') != -1:
			index_f = i
			break
	

	parsed_lines = in_lines[index_i:index_f]
	#print parsed_lines
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
	

	return coordinates_list, crystal_vectors_list
	
def return_full_optimization(optimization_outfile_path):
	# extract all coordinate sets from QE optimization output
	# return a list of namedtuples, each entry is in the form namedtuple('Configuration', 'energy coordinates')
    outfile_path = optimization_outfile_path
    Configuration = namedtuple('Configuration', 'energy coordinates')
    
    list_of_coordinates_lists = []
    list_of_energies =[]
    
    in_lines = return_qe_outfile_lines(outfile_path)
    number_of_atoms = return_number_of_atoms(outfile_path)
 

    # initial geometry has a different structure than other geometries, the following cleans the initial geometry
    #index_i = None
    #index_f = None
    #for i, line in enumerate(in_lines):
    #    if line.find('site n.') != -1:
    #        index_i = i + 1
    #        break
            
    #index_f = index_i + number_of_atoms
    
    #parsed_lines = in_lines[index_i:index_f]
    
    #clean_lines = [[line.split()[1], [float(line.split()[6]), float(line.split()[7]), float(line.split()[8])]] for line in parsed_lines]
    #list_of_coordinates_lists.append(clean_lines)

    atomic_positions_indeces = []
    for i,line in enumerate(in_lines):
        if line.find('ATOMIC_POSITIONS') != -1:
            atomic_positions_indeces.append(i+1)
    # delete last element, it is a repeat reporting the final information of the optimization
    atomic_positions_indeces = atomic_positions_indeces[:-1]

    for index_i in atomic_positions_indeces:
        index_f = index_i + number_of_atoms
        parsed_lines = in_lines[index_i:index_f]
        clean_lines = [[line.split()[0], [float(line.split()[1]), float(line.split()[2]), float(line.split()[3])]] for line in parsed_lines]
        list_of_coordinates_lists.append(clean_lines)
        
      
    # get energies
    for i,line in enumerate(in_lines):
        if line.find('energy   new') != -1 or line.find('Final energy') != -1:
            list_of_energies.append(line.split()[3])

    # remove first energy, it belongs to the initial geometry and we did not save that geometry since it is in differing units
    list_of_energies = list_of_energies[1:]

    list_of_configurations = []
    for i, e in enumerate(list_of_energies):     
        new_config = Configuration(energy=e, coordinates=list_of_coordinates_lists[i])
        list_of_configurations.append(new_config)
    
    return list_of_configurations


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

	try:
		scf_energy = float(in_lines[i].split()[3])
	except:
		tagger = "!    total energy"
		for i, line in reversed(list(enumerate(in_lines))):
			if line.find(tagger) != -1:
				#print line.split()
				index = i + 1
				break
		try:
			scf_energy = float(in_lines[i].split()[4])
		except:
			print qe_scf_or_opt_outfile_path
			scf_energy = "no final energy. optimization probably unfinished"
			print "error. no energy found. perhaps calcuation is not complete.\n"

	return scf_energy


def return_latest_energy(qe_scf_or_opt_outfile_path):
	in_lines = return_qe_outfile_lines(qe_scf_or_opt_outfile_path)
	# a function, to be written
	# should return the latest converged energy; whether or not an optimization finished
	# perhaps it should even return a non-converged energy ???
	return None


def return_crystal_or_angstrom(qe_scf_or_opt_outfile_path):
	in_lines = return_qe_outfile_lines(qe_scf_or_opt_outfile_path)	
	tagger = 'ATOMIC_POSITIONS'
	for i, line in enumerate(in_lines):
		if line.find(tagger) != -1:
			index = i
			break
	try:
		coord_type = in_lines[index]
	except:
		print "fail"

	return coord_type


def return_cpu_information(qe_scf_or_opt_outfile_path):
	in_lines = return_qe_outfile_lines(qe_scf_or_opt_outfile_path)

   	for line in in_lines:
   		if line.find('Number of MPI processes') != -1:
        	#print line
			num_procs = int(line.split()[4])
		elif line.find('Parallel version (MPI)') != -1:
			#print line
			num_procs = int(line.split()[5])
		elif line.find('Parallel version (MPI & OpenMP)') != -1:
			#print line
			num_procs = int(line.split()[7])
		else:
			continue

	k_points_div = "none"            
	for line in in_lines:
		if line.find('K-points division:') != -1:
			#print line.split()
			k_points_div = int(line.split()[4])
		else:
			continue

	rg_space_div = "none"
	for line in in_lines:     
		if line.find('R & G space division:') != -1:
		    #print line
		    rg_space_div = int(line.split()[7])
		else:
			continue
        #print num_procs
        #print k_points_div
        #print rg_space_div
        return num_procs, k_points_div, rg_space_div

def return_walltime_hours(qe_scf_or_opt_outfile_path):
    in_lines = return_qe_outfile_lines(qe_scf_or_opt_outfile_path)

    string_to_parse = "fail"
    for i, line in enumerate(reversed(in_lines)):
        if line.find('This run was terminated on:') != -1:        
            time_string_split = in_lines[-i-4].split()
            #print len(time_string_split)
            if len(time_string_split) == 6:
                string_to_parse = ''.join(time_string_split[-3:-1])
                if string_to_parse.startswith("CPU"):
                    string_to_parse = string_to_parse[3:]
                break
            if len(time_string_split) == 7:
                string_to_parse = ''.join(time_string_split[-3:-1]) 
                if string_to_parse.startswith("CPU"):
                    string_to_parse = string_to_parse[3:]
                break
            if len(time_string_split) == 8:
                string_to_parse = ''.join(time_string_split[-4:-1])
                if string_to_parse.startswith("CPU"):
                    string_to_parse = string_to_parse[3:]
                break
            if len(time_string_split) == 9:
                string_to_parse = ''.join(time_string_split[-4:-1]) 
                if string_to_parse.startswith("CPU"):
                    string_to_parse = string_to_parse[3:]
                break
        else:
            continue
    #print string_to_parse
    # convert everything to minutes
    num_alpha_pairs = []
    index = 0
    for i, x in enumerate(string_to_parse):
        if x.isalpha():
            num_alpha_pairs.append([string_to_parse[index:i],x])
            #print [string_to_parse[index:i],x]
            index = i+1
            
    walltime_in_hours = 0
    for pair in num_alpha_pairs:
        if pair[1] == 'd':
            walltime_in_hours += float(pair[0])*24.0
        if pair[1] == 'h':
            walltime_in_hours += float(pair[0])*1.0   
        if pair[1] == 'm':
            walltime_in_hours += float(pair[0])/60.0
        if pair[1] == 's':
            walltime_in_hours += float(pair[0])/3600.0
    #print walltime_in_hours

    return walltime_in_hours

def return_input_coordinates(qe_input_path):
	# extract input coordinates from QE input file
	# return a list, each entry is in the form ['atom_string', [float(x), float(y), float(z)]]

	inFile = open(qe_input_path, 'r')
	in_lines = inFile.readlines()
	inFile.close()

	coordinates_list = []

	index_i = 0
	index_f = 0
	for i, line in reversed(list(enumerate(in_lines))):
		if line.find('ATOMIC_POSITIONS (') != -1:
			index_i = i + 1
			break

	for i, line in (enumerate(in_lines)):
		if line.find('nat =') != -1:
			num_atoms = int(re.sub("[^0-9]", "", line))
			index_f = index_i + num_atoms
	

	parsed_lines = in_lines[index_i:index_f]
	#print parsed_lines
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


