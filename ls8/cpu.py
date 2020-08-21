"""CPU functionality."""

import sys

# machine codes to track bits
# LDI = 0b10000010
# MUL = 0b10100010
# PRN = 0b01000111
# HLT = 0b00000001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.ir = None
        self.pc = 0
        self.fl_less = False
        self.fl_greater = False
        self.fl_equal = False
        self.loop = True
        self.branchtable = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b00000001: self.HLT,
            0b10100010: self.MUL,
            0b10100111: self.CMP,
            0b01010101: self.JEQ,
            0b01010110: self.JNE
        }

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        # grab file name passed in through terminal argument
        a_file = sys.argv[1]
        # using with open file using dynamic a_file
        with open(a_file, 'r') as program:
            data = program.read()
            data_num = data.split("\n")

            # use index default 0 to insert in ram using enumerate and sanitize data
            for num in data_num:
                if len(num) > 0 and num[0] in "10":
                    value = int(num[:8], 2)
                    self.ram[address] = value
                    address += 1

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        # check if operation code equals "CMP"
        elif op == "CMP":
            # check if reg_a is equal to reg_b
            if self.reg[reg_a] == self.reg[reg_b]:
                # then set self.fl_equal = True
                self.fl_equal = True
            # check if reg_a is less than reg_b
            elif self.reg[reg_a] < self.reg[reg_b]:
                # then set self.fl_less = True
                self.fl_less = True
            # check if reg_a is greater than reg_b
            elif self.reg[reg_a] > self.reg[reg_b]:
                # then set self.fl_greater = True
                self.fl_greater = True
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def JMP(self):
        # grab value using key following after machine code
        operand_a = self.ram_read(self.pc + 1)
        # set pc to the key
        self.pc = self.reg[operand_a]

    def JEQ(self):
        # check if the equal flag is true
        if self.fl_equal == True:
            # then call JMP method
            self.JMP()
            # reset equal flag to false
            self.equal = False
            # add one to self.pc
            # self.pc += 1

    def JNE(self):
        # check if the equal flag is False
        if self.fl_equal == False:
            # then call JMP method
            self.JMP()
            # reset equal flag to false
            self.equal = False
            # add one to self.pc
            # self.pc += 1

    def LDI(self):
        # then grab first and second bits that follow after machine code
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        # set operand_a as key and operand_b as value in register
        self.reg[operand_a] = operand_b
        # add 2 to program counter
        self.pc += 2

    def MUL(self):
        # then grab first and second bits that follow after machine code
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        # print the value that returns from alu
        self.alu("MUL", operand_a, operand_b)
        # add 2 to program counter
        self.pc += 2

    def PRN(self):
        key = self.ram_read(self.pc + 1)
        # print the value that corresponds to key in register
        print(self.reg[key])
        # add 1 to program counter
        self.pc += 1

    def CMP(self):
        # then grab first and second bits that follow after machine code
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        # use alu on the to determine flag for
        self.alu("CMP", operand_a, operand_b)
        # add 1 to program counter
        self.pc += 2

    def HLT(self):
        # break from while loop
        self.loop = False

    def run(self):
        """Run the CPU."""
        # while through while true
        while self.loop:
            # set ir to self.ram[self.pc]
            self.ir = self.ram[self.pc]
            print("while ir and branch", self.ir, self.branchtable[self.ir])

            # use ir with call for 0(1) lookup
            self.branchtable[self.ir]()

            # add one to program counter
            self.pc += 1

    # check if ir equals LDI
    def ram_read(self, address):
        # return value for passed in address/key
        return self.ram[address]

    def ram_write(self, value, address):
        # access or create address/key with value
        self.ram[address] = value
