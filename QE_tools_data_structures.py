import numpy as np

class Atom(object):

    def __init__(self, elem_symbol = None, crystal_coordinates = None, cartesian_coordinates = None):
        self.elem_symbol = elem_symbol
        if cartesian_coordinates:
        	self.cartesian_coordinates = np.array(cartesian_coordinates)
        else:
        	self.cartesian_coordinates = None
        if crystal_coordinates:
        	self.crystal_coordinates = np.array(crystal_coordinates)
        else:
        	self.crystal_coordinates = None


    def __str__(self):
    	crds = self.crystal_coordinates
    	x, y, z = crds[0], crds[1], crds[2]
        return "{}     Cartesian coordinates (x, y, z): ({:.5f}, {:.5f}, {:.5f})".format(self.elem_symbol, x, y, z)


class Periodic_structure(object):
	# technically a periodic structure is classified in order of most to least specific:
	# 230 space groups
	# 32 crystal classes
	# 14 bravais lattices
	# 7 crystal systems

	# for now, the code implements only the bravais lattices and crystal systems
	# default is the most simple (simple cubic, scc), not the most general

	def __init__(self, 
		crystal_system = 'cubic', 
		bravais_lattice = 'simple', 
		crystallographic_constants = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		list_of_atom_objects = None
	):
		self.crystal_system = crystal_system
		self.bravais_lattice = bravais_lattice
		self.crystallographic_constans = crystallographic_constans
		self.list_of_atom_objects = list_of_atom_objects
		if self.list_of_atom_objects is not None:
			self.num_atoms = len(self.list_of_atom_objects)
		else:
			self.num_atoms = 0


	def __str__(self):
		atoms_string = ''
		for a in self.list_of_atom_objects:
			atoms_string += "    {}\n".format(str(a))

		lattice_vecs_string = ''
		for i,v in enumerate(self.crystallographic_constans):
			lattice_vecs_string += "    celldm{:d}: {:.5f}\n".format(i,v)

		return """
{:_<70} \n
Periodic_structure description: 

  crystal_system:
    {}

  bravais_lattice: 
    {}

  crystallographic_constans:
{}  

  Atoms (Crystal Coordinates):
{}
{:_<70}
""".format('',self.crystal_system, self.bravais_lattice, lattice_vecs_string, atoms_string,'')


