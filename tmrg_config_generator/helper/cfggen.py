class CFGGen:
    def __init__(self, tmr_dir="../hdl/output/tmr", rtl_dir="../hdl/output", default="do_not_triplicate", tmr_error="false", top_module="",
                 sdc_generate="False"):
        self.tmr_dir = tmr_dir
        self.rtl_dir = rtl_dir
        self.default = default
        self.tmr_error = tmr_error
        self.top_module = top_module
        self.sdc_generate = sdc_generate
        self.config_template = {"[tmrg]": {"tmr_dir": self.tmr_dir,
                                           "rtl_dir": self.rtl_dir,
                                           "sdc_generate": self.sdc_generate,
                                           "files": ""
                                           },
                                "[global]": {"default": default,
                                             "tmr_error": tmr_error,
                                             "top_module": top_module
                                             }
                                }
        self.module_template = {"default": self.default}

    def add_files(self, file_list):
        self.config_template["[tmrg]"]["files"] += " " + ' '.join(file_list)

    def add_modules(self, module_list):
        for module in module_list:
            self.config_template['[' + module + ']'] = self.module_template

    def config_gen(self):
        config = []
        for key in self.config_template:
            config.append(key + '\n')
            for value in self.config_template[key]:
                config.append(value + " = " + self.config_template[key][value] + '\n')
            config.append("\n" * 2)
        return config
