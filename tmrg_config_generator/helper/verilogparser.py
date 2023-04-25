import re


class VerilogParser:

    def __init__(self, lines):
        self.re_module = re.compile(r"module\s+(\w+)")
        self.re_always = re.compile(r"\s*always")
        self.dict = {}
        self.module_name = ""
        self.__block_comment = False
        self.__parse(lines)

    def __handle_comments(self, line):
        if self.__block_comment:
            if '*/' in line:
                line = line.rsplit('*/', 1)[1]
                self.__block_comment = False
            else:
                line = ""
        else:
            if '//' in line:
                line = line.split('//', 1)[0]
            if '/*' and '*/' in line:
                line = line.rsplit('*/', 1)[1]
            if '/*' in line:
                line = line.split('/*', 1)[0]
                self.__block_comment = True
        return line

    def __parse(self, lines):
        for i, line in enumerate(lines):
            line = self.__handle_comments(line)
            if self.re_module.match(line):
                self.module_name = self.re_module.match(line).group(1)
                self.dict[self.module_name] = []
            if self.re_always.match(line):
                self.dict[self.module_name].append(i + 1)

    def get_module_name(self):
        return list(self.dict.keys())

    def get_first_always_block(self, module_name):
        if module_name in self.dict:
            if self.dict[module_name]:
                return self.dict[module_name][0]
            else:
                return 1