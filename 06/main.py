
from Assembler import Assembler
from Parser import Parser
from Code import Code
import sys

filename = sys.argv[1].split(".")[0]
hack_file = open(filename + ".hack", "w+")