# destuffing2 state gets removed (unused)
# elink_proc_in_dec8b10b_struct busy_r gets removed (unused)


import glob
import os
import re
import argparse

import sys

sys.path.append("./helper")
from constraintsgen import ConstraintsGen
from verilogparser import VerilogParser
from cfggen import CFGGen

def read_file(filename):
    with open(filename, "rt") as file:
        data = file.readlines()
    return data


def write_file(filename, data):
    with open(filename, "wt") as file:
        file.writelines(data)


# def input_handling():
# parser = argparse.ArgumentParser(description="A simple example of argparse")
# parser.add_argument('-f', help="Input filepath", required=True)
# parser.parse_args()
# print("Name:", args.filepath)
# path = input("Filepath of Verilog File(s), press Enter if in current working directory: ")
# while not os.path.exists(path):
#     path = input("Invalid Filepath, try again: ")

# print(path)

def file_handling(directory):
    return glob.glob(directory + '/*.v', recursive=False)


def fsm_fix(lines):
    # very quick and dirty fsm fix for now
    # groups current_state, next_state in two group.
    # not case sensitive
    re_fsm = re.compile(r"(?i)^\s*(reg\s*\[[0-9]+:[0-9]+])\s*(current_state),\s*(next_state)\s*;")
    for i, line in enumerate(lines[:]):
        match = re_fsm.match(line)
        if match:
            lines[i] = match.group(1) + ' ' + match.group(2) + '; ' + match.group(1) + ' ' + match.group(3) + ';' + '\n'
    return lines


write_cfg_only = False


def main():
    data = read_file("not_triplicated_rtl.txt")
    ctg = ConstraintsGen(data, suffix="V")
    cfg = CFGGen()
    if not write_cfg_only:
        for file in file_handling("./hdl"):
            # Maybe check for ***Voter*** in VerilogParser
            data = read_file(file)
            vp = VerilogParser(data)
            cfg.add_modules(vp.get_module_name())
            if os.path.basename(file).endswith("VTR.v"):
                write_file("./hdl/output/" + os.path.basename(file), data)
            else:
                for module in vp.get_module_name():
                    data = fsm_fix(data)
                    data.insert(vp.get_first_always_block(module) - 1, "\n".join(ctg.get_module_constraints(module)))
                    write_file("./hdl/output/" + os.path.basename(file).split('.v')[0] + "_VTR" + ".v", data)

    write_file("config/tmrg.cfg", cfg.config_gen())


if __name__ == "__main__":
    main()
