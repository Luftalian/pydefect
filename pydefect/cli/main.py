# -*- coding: utf-8 -*-
#  Copyright (c) 2020 Kumagai group.

import argparse
import sys
import warnings
from pathlib import Path

from pydefect import __version__
from pydefect.defaults import defaults

def lazy_load_unitcell(path):
    from pydefect.analyzer.unitcell import Unitcell
    return Unitcell.from_yaml(path)

def lazy_load_json(path):
    from monty.serialization import loadfn
    return loadfn(path)

def lazy_load_structure(path):
    from pymatgen.core import IStructure, Structure
    return IStructure.from_file(path)

def lazy_load_structure_mutable(path):
    from pymatgen.core import Structure
    return Structure.from_file(path)

def lazy_load_standard_energies(path):
    from pydefect.chem_pot_diag.chem_pot_diag import StandardEnergies
    return StandardEnergies.from_yaml(path)

def lazy_str_int_to_int(value):
    from pydefect.cli.main_tools import str_int_to_int
    return str_int_to_int(value)

def setup_warnings():
    try:
        from pymatgen.io.vasp.inputs import UnknownPotcarWarning
        warnings.simplefilter('ignore', UnknownPotcarWarning)
    except ImportError:
        pass

description = """pydefect is a package that helps researchers to 
do first-principles point defect calculations with the VASP code."""

epilog = f"Author: Yu Kumagai Version: {__version__}"


def add_sub_parser(_argparse, name: str):
    result = _argparse.ArgumentParser(description="", add_help=False)
    if name == "dir":
        result.add_argument(
            "-d", "--dir", type=Path, required=True,
            help="Directory path to be parsed.")
    elif name == "dirs":
        result.add_argument(
            "-d", "--dirs", nargs="+", type=Path, required=True,
            help="Directory paths to be parsed.")
    elif name == "unitcell":
        result.add_argument(
            "-u", "--unitcell", type=lazy_load_unitcell, required=True,
            help="Path to the unitcell.yaml file.")
    elif name == "supercell_info":
        result.add_argument(
            "-s", "--supercell_info", type=lazy_load_json,
            default="supercell_info.json",
            help="Path to the supercell_info.json file.")
    elif name == "perfect_calc_results":
        result.add_argument(
            "-pcr", "--perfect_calc_results", required=True, type=lazy_load_json,
            help="Path to the calc_results.json for the perfect supercell.")
    elif name == "perfect_band_edge_state":
        result.add_argument(
            "-pbes", "--p_state", required=True, type=lazy_load_json,
            help="Path to the perfect_band_edge_state.json.")
    elif name == "no_calc_results_check":
        result.add_argument(
            "-nccr", "--no_calc_results_check",
            action="store_false", dest="check_calc_results",
            help="Select this option when not checking calc_results.json.")
    elif name == "verbose":
        result.add_argument(
            "-v", "--verbose",
            action="store_true", dest="verbose",
            help="Select if one wants to show traceback.")
    elif name == "defect_energy_summary":
        result.add_argument(
            "-d", "--defect_energy_summary", required=True, type=lazy_load_json,
            help="defect_energy_summary.json file path.")
        result.add_argument(
            "--allow_shallow", action="store_true",
            help="Set when the energies of shallow defects are allowed.")
        result.add_argument(
            "--no_corrections", dest="with_corrections", action="store_false",
            help="Set when corrections are switched off.")
        result.add_argument(
            "-l", "--label", type=str, required=True,
            help="Label in the chemical potential diagram")
    else:
        raise ValueError
    return result

def wrapped_make_standard_and_relative_energies(args):
    setup_warnings()
    from pydefect.cli.main_functions import make_standard_and_relative_energies
    return make_standard_and_relative_energies(args)

def wrapped_make_cpd_and_vertices(args):
    setup_warnings()
    from pydefect.cli.main_functions import make_cpd_and_vertices
    return make_cpd_and_vertices(args)

def wrapped_plot_chem_pot_diag(args):
    setup_warnings()
    from pydefect.cli.main_functions import plot_chem_pot_diag
    return plot_chem_pot_diag(args)

def wrapped_make_supercell(args):
    setup_warnings()
    from pydefect.cli.main_functions import make_supercell
    return make_supercell(args)

def wrapped_append_interstitial_to_supercell_info(args):
    setup_warnings()
    from pydefect.cli.main_functions import append_interstitial_to_supercell_info
    return append_interstitial_to_supercell_info(args)

def wrapped_pop_interstitial_from_supercell_info(args):
    setup_warnings()
    from pydefect.cli.main_functions import pop_interstitial_from_supercell_info
    return pop_interstitial_from_supercell_info(args)

def wrapped_make_defect_set(args):
    setup_warnings()
    from pydefect.cli.main_functions import make_defect_set
    return make_defect_set(args)

def wrapped_calc_defect_structure_info(args):
    setup_warnings()
    from pydefect.cli.main_functions import calc_defect_structure_info
    return calc_defect_structure_info(args)

def wrapped_make_efnv_correction_main_func(args):
    setup_warnings()
    from pydefect.cli.main_functions import make_efnv_correction_main_func
    return make_efnv_correction_main_func(args)

def wrapped_make_band_edge_states_main_func(args):
    setup_warnings()
    from pydefect.cli.main_functions import make_band_edge_states_main_func
    return make_band_edge_states_main_func(args)

def wrapped_make_defect_energy_infos_main_func(args):
    setup_warnings()
    from pydefect.cli.main_functions import make_defect_energy_infos_main_func
    return make_defect_energy_infos_main_func(args)

def wrapped_make_defect_energy_summary_main_func(args):
    setup_warnings()
    from pydefect.cli.main_functions import make_defect_energy_summary_main_func
    return make_defect_energy_summary_main_func(args)

def wrapped_make_calc_summary_main_func(args):
    setup_warnings()
    from pydefect.cli.main_functions import make_calc_summary_main_func
    return make_calc_summary_main_func(args)

def wrapped_plot_defect_energy(args):
    setup_warnings()
    from pydefect.cli.main_functions import plot_defect_energy
    return plot_defect_energy(args)

dirs_parsers = [add_sub_parser(argparse, name="dirs"),
                add_sub_parser(argparse, name="verbose")]


def parse_args_main(args):

    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    subparsers = parser.add_subparsers()

    unitcell_parser = add_sub_parser(argparse, name="unitcell")
    si_parser = add_sub_parser(argparse, name="supercell_info")
    pcr_parser = add_sub_parser(argparse, name="perfect_calc_results")
    pbes_parser = add_sub_parser(argparse, name="perfect_band_edge_state")
    no_calc_results = add_sub_parser(argparse, name="no_calc_results_check")
    defect_e_sum_parser = add_sub_parser(argparse, name="defect_energy_summary")

    # -- make_standard_and_relative_energies -----------------------------------
    parser_make_standard_and_relative_energies = subparsers.add_parser(
        name="standard_and_relative_energies",
        description="",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['sre'])

    parser_make_standard_and_relative_energies.add_argument(
        "-y", "--composition_energies_yaml", type=str,
        default="composition_energies.yaml",
        help="composition_energies.yaml file name.")
    parser_make_standard_and_relative_energies.set_defaults(
        func=wrapped_make_standard_and_relative_energies)

    # -- make_cpd_and_vertices -------------------------------------------------
    parser_cv = subparsers.add_parser(
        name="cpd_and_vertices",
        description="Make chemical potential diagram.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['cv'])

    parser_cv.add_argument(
        "-y", "--rel_energy_yaml", type=str, default="relative_energies.yaml",
        help=" yaml file name.")
    parser_cv.add_argument(
        # this must be string as keys of RelativeEnergies are strings.
        "-t", "--target", type=str,
        help="Target composition, e.g., MgO.")
    parser_cv.add_argument(
        "-e", "--elements", type=str, nargs="+",
        help="Element names considered in chemical potential diagram. Used for "
             "creating the diagram.")
    parser_cv.set_defaults(func=wrapped_make_cpd_and_vertices)

    # -- plot_cpd ------------------------------------------------
    parser_pcpd = subparsers.add_parser(
        name="plot_cpd",
        description="Plot chemical potential diagram and make pdf file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['pc'])
    parser_pcpd.add_argument(
        "-cpd", "--chem_pot_diag", default="chem_pot_diag.json", type=lazy_load_json,
        help="Path to the chem_pot_diag.json file.")
    parser_pcpd.set_defaults(func=wrapped_plot_chem_pot_diag)

    # -- supercell ------------------------------------------------
    parser_supercell = subparsers.add_parser(
        name="supercell",
        description="Make SPOSCAR file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['s'])

    parser_supercell.add_argument(
        "-p", "--unitcell", type=lazy_load_structure, required=True,
        help="Base structure file, which must be the standardized primitive "
             "cell.")
    parser_supercell.add_argument(
        "--matrix", nargs="+", type=int,
        help="Supercell matrix applied to the conventional cell. "
             "1, 3 or 9 components are accepted.")
    parser_supercell.add_argument(
        "--min_atoms", dest="min_num_atoms", default=50, type=int,
        help="Minimum number of atoms")
    parser_supercell.add_argument(
        "--max_atoms", dest="max_num_atoms", default=300, type=int,
        help="Maximum number of atoms")
    parser_supercell.add_argument(
        "--no_symmetry_analysis", dest="analyze_symmetry", action="store_false",
        help="Set if symmetry is not analyzed. If set, sites.yaml file is "
             "required.")
    parser_supercell.add_argument(
        "-s", "--sites_yaml_filename", type=str,
        help="""sites.yaml. An example is 
Mg1:
  site_index: 0  
  site_symmetry: Pm-3m
  wyckoff_letter: b
O1:
  site_index: 1 
  site_symmetry: Pm-3m
Here site_index is based on the given structure.
""")

    parser_supercell.set_defaults(func=wrapped_make_supercell)

    # -- append_interstitial ------------------------------------------------
    parser_append_interstitial = subparsers.add_parser(
        name="append_interstitial",
        description="Append interstitial information to supercell_info.yaml",
        parents=[si_parser],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['ai'])

    parser_append_interstitial.add_argument(
        "-p", "--base_structure", required=True, type=lazy_load_structure_mutable,
        help="Structure file defining the fractional coordinates such as the "
             "standardized primitive cell.")
    parser_append_interstitial.add_argument(
        "-c", "--frac_coords", required=True, nargs=3, type=float,
        help="Fractional coordinates in the standardized primitive cell added "
             "as an interstitial ")
    parser_append_interstitial.add_argument(
        "-i", "--info", type=str, default="None",
        help="Information related to the appended interstitial site if exists.")

    parser_append_interstitial.set_defaults(
        func=wrapped_append_interstitial_to_supercell_info)

    # -- pop_interstitial ------------------------------------------------
    parser_pop_interstitial = subparsers.add_parser(
        name="pop",
        description="Pop interstitial site from supercell_info.json. ",
        parents=[si_parser],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['pi'])

    parser_pop_interstitial.add_argument(
        "-i", "--index", type=int,
        help="Popped interstitial index. Note that the indices begin from 1.")
    parser_pop_interstitial.add_argument(
        "--pop_all", action="store_true",
        help="Pop all interstitials. If this is set, index option is ignored.")

    parser_pop_interstitial.set_defaults(
        func=wrapped_pop_interstitial_from_supercell_info)

    # -- defect_set ------------------------------------------------
    parser_defect_set = subparsers.add_parser(
        name="defect_set",
        description="Make defect_in.yaml file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['ds'])

    parser_defect_set.add_argument(
        "-o", "--oxi_states", nargs="+", type=lazy_str_int_to_int,
        help="Oxidation states in integers, e.g., Mg 2 O -2.")
    parser_defect_set.add_argument(
        "-d", "--dopants", nargs="+", type=str,
        help="Names of dopant element, e.g., Al Ga.")
    parser_defect_set.add_argument(
        "-k", "--keywords", nargs="+", type=str,
        help="Keywords used to screen the target defects. Since, the re.search "
             "is used inside, Regular expression can be used. ")

    parser_defect_set.set_defaults(func=wrapped_make_defect_set)

    # -- defect structure info ------------------------------------------------
    parser_defect_structure_info = subparsers.add_parser(
        name="defect_structure_info",
        description="Defect structure info.",
        parents=dirs_parsers + [si_parser, no_calc_results],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['dsi'])

    parser_defect_structure_info.add_argument(
        "-dt", "--dist_tolerance", type=float, default=defaults.dist_tol,
        help="Tolerance in Angstrom for distance to judge if the "
             "atoms in initial and final structures are same ones.")
    parser_defect_structure_info.add_argument(
        "--symprec", type=float, default=defaults.symmetry_length_tolerance,
        help="Tolerance for determining point groups in the final "
             "structures. Note that point groups in the initial structures are "
             "set via defect_entry.json files.")
    parser_defect_structure_info.set_defaults(func=wrapped_calc_defect_structure_info)

    # -- efnv correction ------------------------------------------------
    parser_efnv = subparsers.add_parser(
        name="efnv",
        description="Generate extended FNV-correction related efnv_correction "
                    "files. ",
        parents=dirs_parsers + [pcr_parser, unitcell_parser, no_calc_results],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['efnv'])

    parser_efnv.add_argument(
        "-r", "--radius", type=float,
        help="Set spherical radius of defect region. The average of potential "
             "alignment term is calculated at sites outside the sphere.")
    parser_efnv.add_argument(
        "--calc_all_sites", action="store_true",
        help="Set if one wants to calculate the potential at all the sites.")
    parser_efnv.set_defaults(func=wrapped_make_efnv_correction_main_func)

    # -- band edge states ------------------------------------------------
    parser_band_edge_states = subparsers.add_parser(
        name="band_edge_states",
        description="Show edge state for each spin channel.",
        parents=dirs_parsers + [pbes_parser, no_calc_results],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['bes'])

    parser_band_edge_states.set_defaults(func=wrapped_make_band_edge_states_main_func)

    # -- defect energy infos ---------------------------------------------------
    parser_defect_energy_infos = subparsers.add_parser(
        name="defect_energy_infos",
        description="",
        parents=dirs_parsers + [unitcell_parser, pcr_parser, no_calc_results],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['dei'])
    parser_defect_energy_infos.add_argument(
        "-s", "--std_energies", required=True, type=lazy_load_standard_energies,
        help="Path to the StandardEnergies.yaml file.")

    parser_defect_energy_infos.set_defaults(
        func=wrapped_make_defect_energy_infos_main_func)

    # -- defect energy summary -------------------------------------------------
    parser_defect_energy_summary = subparsers.add_parser(
        name="defect_energy_summary",
        description="",
        parents=dirs_parsers + [unitcell_parser, pbes_parser],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['des'])
    parser_defect_energy_summary.add_argument(
        "-t", "--target_vertices_yaml", required=True, type=str,
        help="Path to the target_vertices.yaml file.")

    parser_defect_energy_summary.set_defaults(
        func=wrapped_make_defect_energy_summary_main_func)

    # -- calc summary -------------------------------------------------
    parser_calc_summary = subparsers.add_parser(
        name="calc_summary",
        description="",
        parents=dirs_parsers + [pcr_parser, no_calc_results],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['cs'])

    parser_calc_summary.set_defaults(
        func=wrapped_make_calc_summary_main_func)

    # -- plot defect formation energy ------------------------------------------
    parser_plot_energy = subparsers.add_parser(
        name="plot_defect_formation_energy",
        description="Show and plot defect formation energies.",
        parents=[defect_e_sum_parser],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['pe'])

    parser_plot_energy.add_argument(
        "-y", "--y_range", nargs=2, type=float,
        help="Energy range in y-axis")
    parser_plot_energy.add_argument(
        "--no_label_line", dest="label_line", action="store_false",
        help="Set the labels not to locate on the lines.")
    parser_plot_energy.add_argument(
        "--no_add_charges", dest="add_charges", action="store_false",
        help="Set the charges not to appear.")
    parser_plot_energy.add_argument(
        "--plot_all_energies", dest="plot_all_energies", action="store_true",
        help="Plot energies of all charge states including unstable ones.")
    parser_plot_energy.set_defaults(func=wrapped_plot_defect_energy)
    # ------------------------------------------------------------------------
    return parser.parse_args(args)


def main():
    args = parse_args_main(sys.argv[1:])
    args.func(args)


if __name__ == "__main__":
    main()


