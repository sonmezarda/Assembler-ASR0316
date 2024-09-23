import sys, getopt
from modules.assembler import Assembler

def main(argv):
    inputfile:str = ''
    outputfile:str = None
    out_type:str = 'hex'
    try:
        opts, args = getopt.getopt(argv,"hi:o:t",["ifile=","ofile=","type="])
        print(opts, args)
    except getopt.GetoptError:
        print ('main.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-t", "--type"):
            out_type = arg
            print('Type is ', out_type)
    
    assembler = Assembler()
    assembler.assemble_file(inputfile, outputfile, out_type)

    print ('Input file is "', inputfile)

if __name__ == "__main__":
   main(sys.argv[1:])