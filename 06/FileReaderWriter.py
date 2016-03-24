"""

p = Parser(sys.argv[1])
c = Code()

filename = sys.argv[1].split(".")[0]
hack_file = open(filename + ".hack", "w+")

# first pass
while (p.hasMoreCommands()):
    nType = p.getCommandType()
    symT.update(nType)




# second pass
while (p.hasMoreCommands()):
    dest = c.dest(str(p.dest()))
    comp = c.comp(str(p.comp()))
    jmp = c.jmp(str(p.jmp()))
    binary_line = dest | comp | jmp
    hack_file.write(str(bin(binary_line))[2:] + '\n') 
    hack_file.flush()
    p.advance()


hack_file.close()

"""