
module test(
    input clk,
    input d,
    output q
    );

reg reg0;
reg reg1;
reg reg2;


always @ (posedge clk) begin
    reg0 <= d;
    reg1 <= reg0;
    reg2 <= reg1;
end

assign q = reg2;

endmodule
