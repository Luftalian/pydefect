# -*- coding: utf-8 -*-
#  Copyright (c) 2020. Distributed under the terms of the MIT License.


import argparse
import sys
import warnings

from pydefect.analyzer.grids import Grids
from pydefect.cli.main import epilog, description, add_sub_parser, setup_warnings, lazy_load_json, lazy_load_structure_mutable
from pydefect.cli.vasp.main_vasp import lazy_vasprun, lazy_outcar, lazy_chgcar
from vise.defaults import defaults

def wrapped_make_parchg_dir(args):
    setup_warnings()
    from pydefect.cli.vasp.main_vasp_util_functions import make_parchg_dir
    return make_parchg_dir(args)

def wrapped_make_refine_defect_poscar(args):
    setup_warnings()
    from pydefect.cli.vasp.main_vasp_util_functions import make_refine_defect_poscar
    return make_refine_defect_poscar(args)

def wrapped_calc_charge_state(args):
    setup_warnings()
    from pydefect.cli.vasp.main_vasp_util_functions import calc_charge_state
    return calc_charge_state(args)

def wrapped_make_defect_entry_main(args):
    setup_warnings()
    from pydefect.cli.vasp.main_vasp_util_functions import make_defect_entry_main
    return make_defect_entry_main(args)

def wrapped_calc_grids(args):
    setup_warnings()
    from pydefect.cli.vasp.main_vasp_util_functions import calc_grids
    return calc_grids(args)

def wrapped_make_defect_charge_info_main(args):
    setup_warnings()
    from pydefect.cli.vasp.main_vasp_util_functions import make_defect_charge_info_main
    return make_defect_charge_info_main(args)

def wrapped_make_total_dos(args):
    setup_warnings()
    from pydefect.cli.vasp.main_vasp_util_functions import make_total_dos
    return make_total_dos(args)


def parse_args_main_vasp_util(args):
    parser = argparse.ArgumentParser(epilog=epilog,
                                     description=description + """      
    This command provides some utilities related to the VASP calculations""")

    subparsers = parser.add_subparsers()
    dir_parser = add_sub_parser(argparse, name="dir")
    vasprun_parser = add_sub_parser(argparse, name="dir")

    # -- calc charge state -----------------------------------------------------
    parser_calc_charge_state = subparsers.add_parser(
        name="calc_charge_state",
        description="Calc defect charge states from INCAR, POSCAR and POTCAR"
                    "files.",
        parents=[dir_parser],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['ccs'])

    parser_calc_charge_state.set_defaults(func=wrapped_calc_charge_state)

    # -- make defect entry -----------------------------------------------------
    parser_make_defect_entry = subparsers.add_parser(
        name="make_defect_entry",
        description="Make defect entry from INCAR, POSCAR and POTCAR"
                    "files.",
        parents=[dir_parser],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['de'])
    parser_make_defect_entry.add_argument(
        "-n", "--name", type=str, required=True,
        help="Name used for plotting energy diagram.")
    parser_make_defect_entry.add_argument(
        "-p", "--perfect", type=lazy_load_structure_mutable, required=True,
        help="Perfect supercell POSCAR file name.")

    parser_make_defect_entry.set_defaults(func=wrapped_make_defect_entry_main)

    # -- make parchg dir -----------------------------------------------
    parser_make_parchg_dir = subparsers.add_parser(
        name="parchg_dir",
        description="Make parchg directory containing a set of VASP files "
                    "required for generating PARCHG files.",
        parents=[dir_parser],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['pd'])

    parser_make_parchg_dir.add_argument(
        "-i", "--ibands", type=int, nargs="+",
        help="Band indices to be drawn, which start from 1.")
    parser_make_parchg_dir.set_defaults(func=wrapped_make_parchg_dir)

    # -- make refine defect poscar ---------------------------------------------
    parser_make_refine_defect_poscar = subparsers.add_parser(
        name="refine_defect_poscar",
        description="Refine defect structure POSCAR.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['rdp'])

    parser_make_refine_defect_poscar.add_argument(
        "-p", "--poscar", dest="structure", type=lazy_load_structure_mutable)
    parser_make_refine_defect_poscar.add_argument(
        "-d", "--defect_entry", type=lazy_load_json)
    parser_make_refine_defect_poscar.add_argument(
        "-n", "--poscar_name", type=str)
    parser_make_refine_defect_poscar.set_defaults(
        func=wrapped_make_refine_defect_poscar)

    # -- calc grids ------------------------------------------------------------
    parser_calc_grids = subparsers.add_parser(
        name="calc_grids",
        description="Calc Grids.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['cg'])

    parser_calc_grids.add_argument(
        "-c", "--chgcar", type=lazy_chgcar, required=True)
    parser_calc_grids.set_defaults(func=wrapped_calc_grids)

    # -- calc defect charge info -----------------------------------------------
    parser_calc_def_charge_info = subparsers.add_parser(
        name="calc_defect_charge_info",
        description="Calc defect charge info.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['cdc'])

    parser_calc_def_charge_info.add_argument(
        "-p", "--parchgs", type=str, nargs="+", required=True,
        help="PARCHG files.")
    parser_calc_def_charge_info.add_argument(
        "-b", "--bin_interval", type=float, default=0.2)
    parser_calc_def_charge_info.add_argument(
        "-g", "--grids", type=Grids.from_file, required=True)

    parser_calc_def_charge_info.set_defaults(func=wrapped_make_defect_charge_info_main)

    # -- make total dos for defect and carrier density -------------------------
    parser_make_total_dos = subparsers.add_parser(
        name="make_total_dos",
        description="make total dos for defect and carrier density.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        aliases=['mtd'])
    parser_make_total_dos.add_argument(
        "-v", "--vasprun", type=lazy_vasprun, default=defaults.vasprun,
        help="vasprun.xml file name.")
    parser_make_total_dos.add_argument(
        "-o", "--outcar", type=lazy_outcar, default=defaults.outcar,
        help="OUTCAR file name.")
    parser_make_total_dos.set_defaults(func=wrapped_make_total_dos)
    # ----------------------------------------------------------------
    return parser.parse_args(args)


def main():
    args = parse_args_main_vasp_util(sys.argv[1:])
    args.func(args)


if __name__ == "__main__":
    main()


