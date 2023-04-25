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

import argparse
import os


class InputParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="tmrg_cfg_gen")
        self.parser.add_argument("file", nargs='*', type=self.is_valid_file,
                                 help="Input file.")
        self.parser.add_argument("-d", "--directory", dest="directory", type=self.is_valid_directory,
                                 help="Specify directory of Verilog files.")
        self.parser.add_argument("-l", "--txt_file", dest="txt_file", type=self.is_valid_file,
                                 help="Load reg2 list")

        self.args = self.parser.parse_args()

    def is_valid_directory(self, arg):
        if not os.path.isdir(arg):
            self.parser.error(f"The directory {arg} does not exist!")
        else:
            verilog_files = [os.path.join(arg, f) for f in os.listdir(arg) if f.endswith('.v')]
            if not verilog_files:
                self.parser.error(f"No Verilog files found in {arg}!")
            else:
                return verilog_files

    def is_valid_file(self, arg):
        extension = None
        if arg.endswith('.txt'):
            extension = '.txt'
        elif arg.endswith('.v'):
            extension = '.v'
        if not os.path.exists(arg) or (extension and not arg.endswith(extension)):
            self.parser.error(f"The file {arg} does not exist or is not a {extension} file!")
        else:
            return arg

    def check(self):
        valid_args = {'files': []}

        if self.args.files:
            for file_path in self.args.files:
                print(f"The file {file_path} is valid.")
                valid_args['files'].append(file_path)

        if self.args.directory:
            print(f"The folder {self.args.directory} contains valid Verilog files.")
            verilog_files = self.is_valid_directory(self.args.directory)
            valid_args['files'].extend(verilog_files)

        if self.args.txt_file:
            print(f"The .txt file {self.args.txt_file} is valid.")
            valid_args['txt_file'] = self.args.txt_file

        return valid_args

    @property
    def file(self):
        return self.args.file

    @property
    def directory(self):
        return self.args.directory

    @property
    def txt_file(self):
        return self.args.txt_file

    # if __name__ == "__main__":


def read_file(filename):
    with open(filename, "rt") as file:
        data = file.readlines()
    return data


def write_file(filename, data):
    with open(filename, "wt") as file:
        file.writelines(data)


def fsm_fix(lines):
    # very quick and dirty fsm fix for now
    re_fsm = re.compile(r"(?i)^\s*(reg\s*\[[0-9]+:[0-9]+])\s*(current_state),\s*(next_state)\s*;")
    for i, line in enumerate(lines[:]):
        match = re_fsm.match(line)
        if match:
            lines[i] = match.group(1) + ' ' + match.group(2) + '; ' + match.group(1) + ' ' + match.group(3) + ';' + '\n'
    return lines


def create_file_structure(filepath):
    structure = [['output'],
                 ['output', 'hdl'],
                 ['output', 'config'],
                 ['output', 'hdl', 'TMR']
                 ]
    lst = []
    for path in structure:
        lst.append(os.path.join(filepath, *path))
        os.makedirs(lst[-1], exist_ok=True)
    return lst


write_cfg_only = False


def main():
    parser = InputParser()
    test = parser.check()
    print(test)

    # # data = read_file("runme.log")
    # # test = VivadoLogParser(data)
    # parser = InputParser()
    # paths = create_file_structure(parser.get_output_dir())
    # # print(parser.get_reg2_lst())
    # # print(parser.get_file_lst())
    # data = read_file(parser.get_reg2_lst())
    # ctg = ConstraintsGen(data=data, suffix="Voted")
    # cfg = CFGGen(rtl_dir=paths[2], tmr_dir=paths[3])
    #
    # for file in parser.get_file_lst():
    #     file = ''.join(file)
    #     data = read_file(file)
    #     data = fsm_fix(data)
    #     vp = VerilogParser(data)
    #     cfg.add_modules(vp.get_module_name())
    #     if os.path.basename(file).endswith("VTR.v"):
    #         write_file(paths[1] + os.path.basename(file), data)
    #     else:
    #         for module in vp.get_module_name():
    #             data.insert(vp.get_first_always_block(module) - 1, "\n".join(ctg.get_module_constraints(module)))
    #             write_file(os.path.join(paths[1], os.path.basename(file).split('.v')[0] + "_VTR.v"), data)
    #     write_file(os.path.join(paths[2], 'tmrg.cfg'), cfg.config_gen())

    # if not write_cfg_only:
    #     for file in parser.get_file_lst():
    #         # Maybe check for ***Voter*** in VerilogParser
    #         data = read_file(file)
    #         vp = VerilogParser(data)
    #         cfg.add_modules(vp.get_module_names())
    #         if os.path.basename(file).endswith("VTR.v"):
    #             write_file("./hdl/output/" + os.path.basename(file), data)
    #         else:
    #             for module in vp.get_module_names():
    #                 data = fsm_fix(data)
    #                 data.insert(vp.get_first_always_block(module) - 1, "\n".join(ctg.get_module_constraints(module)))
    #                 write_file("./hdl/output/" + os.path.basename(file).split('.v')[0] + "_VTR" + ".v", data)


if __name__ == "__main__":
    main()
