
class Code:

    mnemonics = {"comp": {"null": 0b1110000000 << 6,
                          "0":  0b1110101010 << 6,
                          "1":  0b1110111111 << 6,
                          "-1": 0b1110111010 << 6,
                          "D":  0b1110001100 << 6,
                          "A":  0b1110110000 << 6,
                          "M":  0b1111110000 << 6,
                          "!D": 0b1110001101 << 6,
                          "!A": 0b1110110001 << 6,
                          "!M": 0b1111110001 << 6,
                          "-D": 0b1110001111 << 6,
                          "-A": 0b1110110011 << 6,
                          "-M": 0b1111110011 << 6,
                          "D+1":0b1110011111 << 6,
                          "A+1":0b1110110111 << 6,
                          "M+1":0b1111110111 << 6,
                          "D-1":0b1110001110 << 6,
                          "A-1":0b1110110111 << 6,
                          "M-1":0b1111110111 << 6,
                          "D+A":0b1110000010 << 6,
                          "D+M":0b1111000010 << 6,
                          "D-A":0b1110010011 << 6,
                          "D-M":0b1111010011 << 6,
                          "A-D":0b1110000111 << 6,
                          "M-D":0b1111000111 << 6,
                          "D&A":0b1110000000 << 6,
                          "D&M":0b1111000000 << 6,
                          "D|A":0b1110010101 << 6,
                          "D|M":0b1111010101 << 6
                          },
                "dest": {"null": 0b000 << 3,
                         "M": 0b001 << 3,
                         "D": 0b010 << 3,
                         "MD": 0b011 << 3,
                         "A": 0b100 << 3,
                         "AM": 0b101 << 3,
                         "AD": 0b110 << 3,
                         "AMD": 0b111 << 3
                         },
                "jump": {"null": 0b000,
                         "JGT": 0b001,
                         "JEQ": 0b010,
                         "JGE": 0b011,
                         "JLT": 0b100,
                         "JNE": 0b101,
                         "JLE": 0b110,
                         "JMP": 0b111
                        }
                }
            
    # dest(str) -> binary equivalent of str        
    def dest(self, dstr):
        if (self.mnemonics["dest"].has_key(dstr)):
            return self.mnemonics["dest"].get(dstr)
        else:
            return self.mnemonics["dest"]["null"]

    # comp(cstr) -> binary value of cstr
    def comp(self, cstr):
        if (self.mnemonics["comp"].has_key(cstr)):
            return self.mnemonics["comp"].get(cstr)
        else:
            return self.mnemonics["comp"]["null"]  

    # jmp(jstr) -> binary value of jstr
    def jmp(self, jstr):
        if (self.mnemonics["jump"].has_key(jstr)):
            return self.mnemonics["jump"].get(jstr)
        else:
            return self.mnemonics["jump"]["null"]

    # for @value instructions. Returns binary of value truncated
    # to 15 bits
    def value(self, val):
        binval = bin(val)
        if (len(binval) - 2 > 15):
            binval = '0b' + binval[-15:]
        return binval
