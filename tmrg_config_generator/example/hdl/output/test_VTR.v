
module test(
    input clk,
    input d,
    output q
    );

reg reg0;
reg reg1;
reg reg2;



//***Voter***
//tmrg triplicate reg2
wire [0:0] reg2V = reg2;
//tmrg triplicate reg1
wire [0:0] reg1V = reg1;
//tmrg triplicate reg0
wire [0:0] reg0V = reg0;
//***Voter***

always @ (posedge clk) begin
    reg0 <= d;
    reg1 <= reg0V;
    reg2 <= reg1V;
end

assign q = reg2V;

endmodule
