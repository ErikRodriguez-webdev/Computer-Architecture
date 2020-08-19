"""CPU functionality."""

import sys

# machine codes to track bits
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        # address = 0

        # For now, we've just hardcoded a program:
        # grab file name passed in through terminal argument
        a_file = sys.argv[1]
        # using with open file using dynamic a_file
        with open(a_file, 'r') as program:
            data = program.read()
            data_num = data.split("\n")

            for idx, num in enumerate(data_num):
                if num != "":
                    self.ram[idx] = num[:8]

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

    def run(self):
        """Run the CPU."""
        # while through while true
        while True:
            # set ir to self.ram[self.pc]
            ir = self.ram[self.pc]

            # check if ir equals LDI
            if ir == LDI:
                # then grab two bits that follow after machine code LDI
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                # set operand_a as key and operand_b as value in register
                self.reg[operand_a] = operand_b
                # add 2 to program counter
                self.pc += 2

            # check if ir equals PRN
            if ir == PRN:
                # then grab the bit that follows after machine code PRN
                key = self.ram_read(self.pc + 1)
                # print the value that corresponds to key in register
                print(self.reg[key])
            # check if ir equals HLT
            elif ir == HLT:
                # break from while loop
                break

            # add one to program counter
            self.pc += 1

    def ram_read(self, address):
        # return value for passed in address/key
        return self.ram[address]

    def ram_write(self, value, address):
        # access or create address/key with value
        self.ram[address] = value
