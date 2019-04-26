import math
import numpy as np

# thermodynamic functions for harmonic oscillators/vibrations
def e_vib_T(phonons_list_Hz, T_kelvin):
    T = T_kelvin
    h = 4.135667662e-15 #h in eV*seconds
    k = 8.6173303e-5  #kb in eV/kelvin
    
    if phonons_list_Hz:
        terms_list = [x*k*T*(0.5 + (1/(math.exp(x)-1))) for x in [(h*nu)/(k*T) for nu in phonons_list_Hz]]
        h_vib_t = sum(terms_list)
    else: h_vib_t = 0.0
    return h_vib_t

def s_vib_T(phonons_list_Hz, T_kelvin):
    T = T_kelvin
    h = 4.135667662e-15 #h in eV*seconds
    k = 8.6173303e-5  #kb in eV/kelvin
    
    if phonons_list_Hz:
        terms_list = [x*(math.exp(-x)/(1-math.exp(-x)))-(np.log(1-math.exp(-x))) for x in [(h*nu)/(k*T) for nu in phonons_list_Hz]]
        s_vib_t = k*sum(terms_list)
    else: s_vib_t = 0.0
    return s_vib_t



# entropy equations
def s_diatomic_gas_rot(t_in_kelvin, atomic_mass_amu, bond_length_angstrom):
    amu_in_kg = 1.66053904e-27
    m = atomic_mass_amu*amu_in_kg  
    t = t_in_kelvin
    k = 1.38064852e-23 #kb in J per K
    k_eV_per_K = 8.617343e-5
    sigma = 2 #2 for diatomic single element gas due to rotational symmetry
    d_gas = bond_length_angstrom*1e-10  #bond length in meters  
    h = 6.62607004e-34 #h in J*seconds
    
    I = 0.5*m*(d_gas**2) # moment of inertia
    theta_rot = (h**2)/(8.0*(np.pi**2)*I*k)
    q_rot = t/(theta_rot*sigma) 
    s_rot_t = k_eV_per_K*(1.0 + math.log(q_rot))
    return s_rot_t

def s_diatomic_gas_rot2(t_in_kelvin, b_rot=60.853):  ## b_rot rotational constant for H2  in cm^-1 according to NIST
    t = t_in_kelvin
    k = 8.6173303e-5  #kb in eV/kelvin
    h = 4.135667662e-15 #h in eV*seconds
    e = np.exp(1)
    c = 299792458*100.0 # speed of light in cm/s
    b = b_rot # 60.853 rotational constant for H2  in cm^-1 according to NIST
    sigma = 2.0 #2 for h2 due to rotational symmetry    
    N = 1.0  # number of H2 molecules
    ln_argument = (1/b)*(1/(sigma*c*h))*(k*t)*(e/N)
    s = N*(k + k*math.log(ln_argument))
    return s


def s_diatomic_gas_trans(t_in_kelvin, p_in_atm, single_atom_mass_amu):
    amu_in_kg = 1.66053904e-27
    joules_to_eV = 1.0/1.6021766208e-19
    pascals_per_atm = 101325
    t = t_in_kelvin
    k = 1.38064852e-23 #kb in J per K
    h = 6.62606896e-34 #h in J*seconds
    p = p_in_atm*pascals_per_atm
    m = 2*single_atom_mass_amu*amu_in_kg  
    e = np.exp(1)  # the number e
    V = k*t/p

    ln_argument = math.pow(2*np.pi*m*k*t/math.pow(h,2),1.5)*(e*V)
    s_Joules = k*(1.5 + math.log(ln_argument))
    s_eV = s_Joules*joules_to_eV
    #print s_eV
    return s_eV





def s_diatomic_gas_T_P(t_in_k, p_in_atm, phonons_list_Hz, single_atom_mass_amu, bond_length_angstrom):
    # returns the entropy of one H2/O2/etc molecule
    # ideal gas assumption
    # unit of ouput it eV/T_in_kelvin
    t = t_in_k
    p = p_in_atm
    s_vib = s_vib_T(phonons_list_Hz, t)
   # s_rot = s_diatomic_gas_rot(t, single_atom_mass_amu, bond_length_angstrom)
    s_rot = s_diatomic_gas_rot2(t)
    s_trans = s_diatomic_gas_trans(t, p, single_atom_mass_amu)
    return s_vib + s_rot + s_trans





def e_diatomic_gas_trans_rot(t_in_kelvin):
    k = 8.617343e-5  #kb in eV/kelvin
    t = t_in_kelvin
    # 3k/2 trans + k/2 rot 
    return 2.5*k*t

def h_diatomic_gas_T(e_diatomic_elec_eV, phonon_list_diatomic_Hz, t_in_kelvin):
    e_elec = e_diatomic_elec_eV
    t = t_in_kelvin
    k = 8.617343e-5  #kb in eV/kelvin
    h_h2 = e_elec + e_vib_T(phonon_list_diatomic_Hz, t) + e_diatomic_gas_trans_rot(t) 
    return h_h2

def u_diatomic_gas(t_in_k, p_in_atm, e_elec_molecule_Ry, phonon_list_Hz, single_atom_mass_amu, bond_length_angstrom):
    # the chemical potential of one diatomic homo-nuclear gas molecule as a function of T and P
    # based on ideal equations
    rydberg_to_eV = 13.605693009
    e_diatomic_gas_eV = e_elec_molecule_Ry*rydberg_to_eV
    ph_Hz = phonon_list_Hz
    t = t_in_k
    p = p_in_atm
    h = h_diatomic_gas_T(e_diatomic_gas_eV, ph_Hz, t)
    s = s_diatomic_gas_T_P(t, p, ph_Hz, single_atom_mass_amu, bond_length_angstrom)
    return h - t*s


