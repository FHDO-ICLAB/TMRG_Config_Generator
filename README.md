# TMRG_Config_Generator

The TMRG_CONFIG_GENERATOR is a Python tool designed to assist in the triplication process of Verilog code with the [TMRG](https://gitlab.cern.ch/tmrg/tmrg) toolset by CERN. In its current version, it is able to place the necessary directives into the Verilog source code, as well as creating a configuration file, all based on a list of flipflops.

The list is structured as follows:
```
<module_identifier>, hierarchical_element_name>
```
It can be generated using the [reg2](../main/reg2) tcl script. This script is designed for use with Vivado and exports all flipflop primitives from the netlist. It can also be used later as a first validation method of the triplicated code. The script checks whether the output of a flipflop is connected to a voting cell. If this is the case, then it will be placed in the triplicated.txt file. Otherwise it is placed in not_triplicated.txt.


Currently the tool supports a partial triplication approach as shown below and is used extensively for the triplication of the MOPS-HUB FPGA firmware project. Full triplication should also work, but has not been tested.

<a href="url"><img src="https://user-images.githubusercontent.com/78490283/234264206-46c0ed3b-4e7c-4308-b0a2-2cdeb3a1a694.svg" height="auto" width="auto" ></a>

...
<br/>
<br/>
