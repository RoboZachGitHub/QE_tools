from collections import namedtuple

Ibrav_data = namedtuple('Ibrav', ['name', 'compulsory_values'])
# Dictionary mapping integer and string values for QE's ibrav keyword

ibrav_dictionary = {
   0 : Ibrav_data('free',
         []
       ),
   1 : Ibrav_data('cubic P (sc)',
         ['a']
       ),
   2 : Ibrav_data('cubic F (fcc)',
         ['a'] 
       ),
   3 : Ibrav_data('cubic I (bcc)',
        ['a']
       ),
   4 : Ibrav_data('Hexagonal qnd Triagonal P',
        ['a', 'c']
       ),
   5 : Ibrav_data('Trigonal R, 3fold axis c',
        ['a', 'c']
       ),
  -5 : Ibrav_data('Trigonal R, 3fold axis <111>', 
        ['a', 'c']
       ),
   6 : Ibrav_data('Tetragonal P (st)', 
        ['a', 'c']
       ),
   7 : Ibrav_data('Tetragonal I (bct)', 
        ['a', 'c']
       ),
   8 : Ibrav_data('Orthorhombic P', 
        ['a', 'b', 'c']
       ),
   9 : Ibrav_data('Orthorhombic base-centered(bco)', 
        ['a', 'b', 'c']
       ),
  -9 : Ibrav_data('Orthorhombic base-centered(bco) alternate', 
        ['a', 'b', 'c']
       ),
  10 : Ibrav_data('Orthorhombic face-centered', 
        ['a', 'b', 'c']
       ),
  11 : Ibrav_data('Orthorhombic body-centered', 
        ['a', 'b', 'c']
       ),
  12 : Ibrav_data('Monoclinic P, unique axis c', 
        ['a', 'b', 'c', 'cosab', 'cosac', 'cosbc']
       ),
 -12 : Ibrav_data('Monoclinic P, unique axis b', 
        ['a', 'b', 'c', 'cosab', 'cosac', 'cosbc']
       ),
  13 : Ibrav_data('Monoclinic base-centered', 
        ['a', 'b', 'c', 'cosab', 'cosac', 'cosbc']
       ),
  14 : Ibrav_data('Triclinic', 
        ['a', 'b', 'c', 'cosab', 'cosac', 'cosbc']
       ),
}






