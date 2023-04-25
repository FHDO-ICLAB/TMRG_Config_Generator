import re
import glob

# filter line, ignore starting whitespace, one group
pattern = re.compile('^\s*(reg \[[0-9]+:[0-9]+]) current_state, next_state;')

for x in glob.glob("**/hdl/*fsm.v", recursive=True) + glob.glob("**/hdl/*struct.v", recursive=True):
    print(x)
    with open(x, "rt") as file:
        # read every line
        data = file.readlines()
        # replace string with group1 if match found

    data_replace = [pattern.match(l).group(1) + " current_state; " + pattern.match(l).group(1) + " next_state;" if pattern.match(l) else l for l in data]

    with open(x, "wt") as file:
        file.writelines(data_replace)

