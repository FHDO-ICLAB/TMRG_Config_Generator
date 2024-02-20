import re


def load_file(filepath):
    with open(filepath) as f:
        lines = f.read().splitlines()
    # Remove empty strings
    lines = [line.strip() for line in lines if line.strip()]
    return lines


def sort_signals(topmodule, signals):
    sorted_signals = {
        "A": [],
        "B": [],
        "C": []
    }
    for signal in signals:
        signal = signal.split("/")
        addendum = re.search(r".*([A-C])", signal[-1])
        if addendum:
            sorted_signals[addendum.group(1)].append(topmodule + "." + ".".join(signal))
        else:
            print(f"Error in: {topmodule}.{".".join(signal)}")
    return sorted_signals


def create_assertion(sorted_signals):
    for key in sorted_signals.keys():
        # Loop over copy of sorted_signals
        for i, signal in enumerate(sorted_signals[key][:]):
            sorted_signals[key][i] = (
                f"assert({signal})\n"
                f"\t\telse\n"
                f"\t\t\t$fdisplay(this.rdc_fail, \"{signal}\");"
            )
    return sorted_signals
def create_tb_class(assertions):
    template = f"""
class rdc;
    int rdc_success ,rdc_fail;

    function new;
        this.rdc_success = $fopen("./rdc_success.txt", "w");
        this.rdc_fail = $fopen("./rdc_fail.txt", "w");
    endfunction

    function logging(string func,string add, string msg);
        if (func == add) begin
            $fdisplay(this.rdc_success, "%s", msg);
        end else begin
            $fdisplay(this.rdc_success, "%s", msg);
        end
    endfunction
    
    function reset(string appendix);
        case (appendix)
            "A" : this.resetA;
            "B" : this.resetB;
            "C" : this.resetC;
            default : $stop;
        endcase
    endfunction
    
    function resetA;
        {"\n\n\t\t".join(assertions["A"])}
    endfunction

    function resetB;
        {"\n\n\t\t".join(assertions["B"])}
    endfunction

    function resetC;
        {"\n\n\t\t".join(assertions["A"])}
    endfunction
endclass    
"""
    return template

def write_file(filepath, content):
    with open(filepath, "w") as f:
        f.write(content)


def main():
    test = load_file("./reset_signals.txt")
    test2 = sort_signals("top_test.can2TMR_u", test)
    test3 = create_assertion(test2)
    test4 = create_tb_class(test3)
    write_file("./rdc.sv", test4)


main()
