from __future__ import absolute_import
from __future__ import print_function
import veriloggen
import stream_reduceadd_valid

expected_verilog = """
module test;

  reg CLK;
  reg RST;
  reg ivalid;
  wire ovalid;
  reg signed [32-1:0] xdata;
  reg signed [32-1:0] ydata;
  wire signed [32-1:0] zdata;
  wire [1-1:0] vdata;

  main
  uut
  (
    .CLK(CLK),
    .RST(RST),
    .ivalid(ivalid),
    .ovalid(ovalid),
    .xdata(xdata),
    .ydata(ydata),
    .zdata(zdata),
    .vdata(vdata)
  );

  reg reset_done;

  initial begin
    $dumpfile("uut.vcd");
    $dumpvars(0, uut);
  end


  initial begin
    CLK = 0;
    forever begin
      #5 CLK = !CLK;
    end
  end


  initial begin
    RST = 0;
    reset_done = 0;
    xdata = 0;
    ydata = 0;
    ivalid = 0;
    #100;
    RST = 1;
    #100;
    RST = 0;
    #1000;
    reset_done = 1;
    @(posedge CLK);
    #1;
    #10000;
    $finish;
  end

  reg [32-1:0] send_fsm;
  localparam send_fsm_init = 0;
  reg [32-1:0] send_count;
  reg [32-1:0] _d1_send_fsm;
  reg _send_fsm_cond_2_0_1;
  reg _send_fsm_cond_3_1_1;
  reg [32-1:0] recv_fsm;
  localparam recv_fsm_init = 0;
  reg [32-1:0] recv_count;
  localparam send_fsm_1 = 1;
  localparam send_fsm_2 = 2;
  localparam send_fsm_3 = 3;
  localparam send_fsm_4 = 4;

  always @(posedge CLK) begin
    if(RST) begin
      send_fsm <= send_fsm_init;
      _d1_send_fsm <= send_fsm_init;
      send_count <= 0;
      _send_fsm_cond_2_0_1 <= 0;
      _send_fsm_cond_3_1_1 <= 0;
    end else begin
      _d1_send_fsm <= send_fsm;
      case(_d1_send_fsm)
        send_fsm_2: begin
          if(_send_fsm_cond_2_0_1) begin
            $display("xdata=%d", xdata);
            $display("ydata=%d", ydata);
          end 
        end
        send_fsm_3: begin
          if(_send_fsm_cond_3_1_1) begin
            $display("xdata=%d", xdata);
            $display("ydata=%d", ydata);
          end 
        end
      endcase
      case(send_fsm)
        send_fsm_init: begin
          if(reset_done) begin
            send_fsm <= send_fsm_1;
          end 
        end
        send_fsm_1: begin
          ivalid <= 0;
          send_count <= send_count + 1;
          if(send_count == 10) begin
            send_count <= 0;
          end 
          if(send_count == 10) begin
            send_fsm <= send_fsm_2;
          end 
        end
        send_fsm_2: begin
          xdata <= 0;
          ydata <= 0;
          ivalid <= 1;
          send_count <= send_count + 1;
          _send_fsm_cond_2_0_1 <= 1;
          send_fsm <= send_fsm_3;
        end
        send_fsm_3: begin
          xdata <= xdata + 1;
          ydata <= ydata + 2;
          ivalid <= 1;
          send_count <= send_count + 1;
          _send_fsm_cond_3_1_1 <= 1;
          if(send_count == 65) begin
            ivalid <= 0;
          end 
          if(send_count == 65) begin
            send_fsm <= send_fsm_4;
          end 
        end
      endcase
    end
  end

  localparam recv_fsm_1 = 1;

  always @(posedge CLK) begin
    if(RST) begin
      recv_fsm <= recv_fsm_init;
      recv_count <= 0;
    end else begin
      case(recv_fsm)
        recv_fsm_init: begin
          if(reset_done) begin
            recv_fsm <= recv_fsm_1;
          end 
        end
        recv_fsm_1: begin
          if(ovalid && vdata) begin
            $display("zdata=%d", zdata);
            recv_count <= recv_count + 1;
          end 
        end
      endcase
    end
  end


endmodule



module main
(
  input CLK,
  input RST,
  input ivalid,
  output ovalid,
  input signed [32-1:0] xdata,
  input signed [32-1:0] ydata,
  output signed [32-1:0] zdata,
  output [1-1:0] vdata
);

  reg _ivalid_0;
  reg _ivalid_1;
  assign ovalid = _ivalid_1;
  reg signed [32-1:0] _plus_data_2;
  reg signed [32-1:0] _reduceadd_data_5;
  reg [6-1:0] _reduceadd_count_5;
  reg [1-1:0] _pulse_data_8;
  reg [6-1:0] _pulse_count_8;
  assign zdata = _reduceadd_data_5;
  assign vdata = _pulse_data_8;

  always @(posedge CLK) begin
    if(RST) begin
      _ivalid_0 <= 0;
      _ivalid_1 <= 0;
      _plus_data_2 <= 0;
      _reduceadd_data_5 <= 1'sd0;
      _reduceadd_count_5 <= 0;
      _pulse_data_8 <= 1'sd0;
      _pulse_count_8 <= 0;
    end else begin
      _ivalid_0 <= ivalid;
      _ivalid_1 <= _ivalid_0;
      _plus_data_2 <= xdata + ydata;
      if(_ivalid_0) begin
        _reduceadd_data_5 <= _reduceadd_data_5 + _plus_data_2;
      end 
      if(_ivalid_0) begin
        _reduceadd_count_5 <= (_reduceadd_count_5 >= 5'sd8 - 1)? 0 : _reduceadd_count_5 + 1;
      end 
      if(_ivalid_0 && (_reduceadd_count_5 == 0)) begin
        _reduceadd_data_5 <= 1'sd0 + _plus_data_2;
      end 
      if(_ivalid_0) begin
        _pulse_data_8 <= _pulse_count_8 >= 5'sd8 - 1;
      end 
      if(_ivalid_0) begin
        _pulse_count_8 <= (_pulse_count_8 >= 5'sd8 - 1)? 0 : _pulse_count_8 + 1;
      end 
      if(_ivalid_0 && (_pulse_count_8 == 0)) begin
        _pulse_data_8 <= _pulse_count_8 >= 5'sd8 - 1;
      end 
    end
  end


endmodule
"""


def test():
    veriloggen.reset()
    test_module = stream_reduceadd_valid.mkTest()
    code = test_module.to_verilog()

    from pyverilog.vparser.parser import VerilogParser
    from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
    parser = VerilogParser()
    expected_ast = parser.parse(expected_verilog)
    codegen = ASTCodeGenerator()
    expected_code = codegen.visit(expected_ast)

    assert(expected_code == code)
