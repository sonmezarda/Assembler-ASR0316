import json

# B komutundan sonra gelen label'a gidemiyor

INSTRUCTION_FILE = "settings/instructions.json"
HEADER = "v2.0 raw"
CONSTANT_PREFIX = '$'
COMMENT_CHAR = ';'

with open(INSTRUCTION_FILE, 'r') as inf:
    ins = json.loads(inf.read())

def getInstDic(ins_name)->dict: 
    ins_name = ins_name.upper()
    return ins[ins_name]    

defaults = getInstDic("defaults")

def decimal_to_binary(num:str) -> str:
    num = int(num)
    return bin(num)[2:]

def hex_to_binary(num:str) -> str:
    return decimal_to_binary(int(num, 16))

def set_binary_len(binary_str:str, target_len:int) -> str:
    while len(binary_str) < target_len:
        binary_str = "0" + binary_str

    return binary_str


def prepare_code(filename:str, outfile:str='.temp.asm'):
    # label en son kontrol edilmeli çünkü constant yazmak makro yazmak gibi işlemler satır sayısını değiştirecek
    set_constants(filename, outfile)
    code_str = ""
    labels = {}

    with open(outfile, "r", encoding="UTF-8") as file:
        x = 0
        for line in file:
            if line.strip() == "":
                continue
            elif line.strip()[-1] == ':':
                labels[line[:-2].upper()] = x
                code_str += "lbl "+line
                #x += 1
            elif line.upper().startswith('EQU'):
                pass
            elif line != "":
                code_str+=line.upper()
                x += 1
    print(labels)
    
                    
    code_str = set_labels(labels, code_str)

    outputfile = open(outfile, "w", encoding="UTF-8")
    outputfile.write(code_str)
    outputfile.close()

def set_labels(labels:dict, code:str):
    
    for label in labels:
        code = code.replace(label, f"#{labels[label]}")
    
    return code

def set_constants(filename:str, outfile:str='.temp.asm'):
    constants = {}
    code = ""
    with open(filename, 'r', encoding='utf-8') as file:
        for x, line in enumerate(file):
            if CONSTANT_PREFIX in line:
                constant = [cs for cs in line.split(' ') if cs.startswith(CONSTANT_PREFIX)][0].strip()
                line = line.replace(constant, constants[constant])

            if line.upper().startswith('EQU'):
                splitted = line.split(' ')
                constants[CONSTANT_PREFIX+splitted[1]] = splitted[2].strip()
                print(constants)
            else:
                code += line
            
            
    with open(outfile, 'w', encoding='utf-8') as file:
        file.write(code)


def get_parameters(line:str):
    line = line.strip()
    ins_code = line.split(' ')[0].upper()
    line = line.replace(' ', '')
    line = line.replace(ins_code, '')
    line = line.replace('[', '')
    line = line.replace(']', '')
    registers = line.split(',')
    return (ins_code, registers)


def getInstVal(ins_dic:dict, val_name):
    val = ins_dic.get(val_name)
    if(val == None):
        val = defaults[val_name]
    return val

def reg_ok(regstr):
    return "rd" in regstr or "ra" in regstr or "rb" in regstr

def imm_ok(regstr):
    return "#imm16" in regstr 

def reg_add_ok(regstr):
    return "[r" in regstr

def generate_bits(instruction, registers):
    instDict = getInstDic(instruction)
    Ra = getInstVal(instDict,"Ra")
    Rd = getInstVal(instDict,"Rd")
    Rb = getInstVal(instDict,"Rb")
    IM = getInstVal(instDict,"IM")
    RW = getInstVal(instDict,"RW")
    SF = getInstVal(instDict,"SF")
    MR = getInstVal(instDict,"MR")
    OPCODE = getInstVal(instDict,"OPCODE")

    format = getInstDic(instruction)["format"]
    if len(format) != 0:
        for x, reg in enumerate(registers):
            if reg.startswith('#'):
                IM = "1"
                if '0x' in reg.lower():
                    Rb = hex_to_binary(reg[3:])
                elif '0b' in reg.lower():
                    Rb = reg[3:]
                else:
                    Rb = decimal_to_binary(reg[1:])
                Rb = set_binary_len(Rb, 16)
            
            elif "rd" in format[x]:
                Rd = decimal_to_binary(reg[1:])
                Rd = set_binary_len(Rd, 4)
            elif "ra" in format[x]:
                Ra = decimal_to_binary(reg[1:])
                Ra = set_binary_len(Ra, 4)
            elif "rb" in format[x]:
                Rb = decimal_to_binary(reg[1:])
                Rb = set_binary_len(Rb, 16)
    
    return IM+RW+SF+MR+OPCODE+Rd+Ra+Rb

def convert_code(filename:str=".temp.asm", output_name:str="last.hex"):
    file = open(filename, "r", encoding="UTF-8")
    with open(output_name, "w") as output_file:
        output_file.write(HEADER+"\n")
        for line in file.readlines():
            if not line.startswith("lbl"):
                instruction, registers =  get_parameters(line)
                lineCode = generate_bits(instruction, registers)
                decimal = int(lineCode, 2)
                hexadecimal = hex(decimal)[2:]
                output_file.write(hexadecimal.zfill(8)+"\n")
    
    file.close()

def main():
    filename = "examples/io_test.asm"
    prepare_code(filename)
    convert_code()
    pass




if __name__ == "__main__":
    main()