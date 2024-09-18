import json

LABEL_PREFIX = '@'
CONSTANT_PREFIX = '$'
HEADER="v2.0 raw"
COMMENT_CHAR='//'
INSTRUCTIN_FILE='settings/instructions.json'

class AssembleHelper:
    def load_file(filename:str) -> list[str]:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            return lines
        
    @staticmethod
    def save_file(filename:str, lines:list[str]):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(HEADER+'\n')
            file.writelines(lines)

    @staticmethod
    def load_instructions(filename:str):
        return json.loads(open(filename, 'r').read())
     
    @staticmethod
    def bin_to_hex(binary:str) -> str:
        return hex(int(binary, 2))[2:].zfill(8)
    
    @staticmethod
    def remove_whitespace(line:str) -> str:
        line = line.strip()
        if COMMENT_CHAR in line:
            line = line.split(COMMENT_CHAR)[0]
        return line

class Assembler:
    def __init__(self):
        self.set_defaults()
    
    def set_defaults(self):
        self.instructions = AssembleHelper.load_instructions(INSTRUCTIN_FILE)
        self.labels = {}
        self.variables = {}
        self.default_values = self.instructions['DEFAULTS']
        self.constants = self.set_default_constants()

    def get_default_param(self, inst_name:str, param_name) -> str:
        # Gets the default value of the given parameter from the instructions file
        # Gets from instructions[instruction_name] if exists, otherwise gets from default_values (instrtuctions['DEFAULTS'])
        instruction = self.instructions[inst_name]
        return instruction[param_name] if instruction.get(param_name) else self.default_values[param_name]
    
    def get_merged_instruction(self, inst_name:str, registers:dict[str, str]) -> str:
        # Gets the instruction name and the registers and returns the merged binary instruction
        # Gets default values from the instructions file and if the register is not given, it uses the default value

        IM = self.get_default_param(inst_name, 'IM') # Is Immediate
        
        RW = self.get_default_param(inst_name, 'RW') 
        SF = self.get_default_param(inst_name, 'SF') # Sign Flag
        MR = self.get_default_param(inst_name, 'MR') # Memory Read
        OPCODE = self.get_default_param(inst_name, 'OPCODE') # Operation Code
        RA = registers.get('ra') if registers.get('ra') else self.get_default_param(inst_name, 'Ra')
        RD = registers.get('rd') if registers.get('rd') else self.get_default_param(inst_name, 'Rd')
        RB = registers.get('rb') if registers.get('rb') else self.get_default_param(inst_name, 'Rb')
        if len(RB) == 4:
            IM = '0'
            RB = RB.zfill(16)
        else:
            IM = '1'
        return IM+RW+SF+MR+OPCODE+RD+RA+RB
    

    def set_default_constants(self) -> dict[str, str]:
        return {}

    def clear_whitespace(self, lines:list[str]) -> list[str]:
        # Removes the whitespace from the lines and returns the list of lines
        return [AssembleHelper.remove_whitespace(line) for line in lines if line.strip() != '']
    
    def get_constants(self, lines:list[str]) -> dict[str, str]:
        # Gets constants from the lines and adds them to the constants dictionary
        constants = self.constants
        for line in lines:
            if line.upper().startswith('EQU'):
                splitted = line.split(' ')
                constants[splitted[1].strip()] = splitted[2].strip()
    
    def get_labels(self, lines:list[str]) -> dict[str, int]:
        # Gets labels from the lines and adds them to the labels dictionary
        labels = self.labels
        # Since label lines are not included in the instructions, the value of the next label must be 1 less each time a label is found.
        labelCount = 0 
        for x, line in enumerate(lines):
            if line.strip()[-1] == ':': # If the line ends with ':', it is a label
                labels[line[:-1]] = x - labelCount
                labelCount += 1

    def set_line_constants(self, line:str) -> str:
        # Replaces the constants in the line with their values
        constants = self.constants
        if CONSTANT_PREFIX in line:
            for constant in constants.keys():
                line = line.replace(CONSTANT_PREFIX+constant, constants[constant])
        return line

    def set_line_labels(self, line:str) -> str:
        # if it is a branch instruction, it replaces the label with it's value  
        # if line contains LABEL_PREFIX, it replaces the label with it's value
        labels = self.labels
        if LABEL_PREFIX in line or line.upper().startswith('B'):
            for label in labels.keys():
                line = line.replace(LABEL_PREFIX+label, '#'+str(labels[label]))
                line = line.replace(label, '#'+str(labels[label]))
        return line

    def set_constants(self, lines:list[str]) -> list[str]:
        # Removes the constant lines from the list and changes $constant with values and returns the list of lines
        lines = [line for line in lines if not line.upper().startswith('EQU')]            
        return [self.set_line_constants(line) for line in lines]

    def set_labels(self, lines:list[str]) -> list[str]:
        # Removes the label lines from the list and changes @label with values and returns the list of lines
        lines = [line for line in lines if not line.strip()[-1] == ':']
        return [self.set_line_labels(line) for line in lines]

    def get_instruction_splitted(self, line:str) -> list[str]:
        #splits the instruction line into instruction name and parameters
        splittedLine = []
        if '[' not in line:
            splittedLine = line.replace(',', ' ').split()
        else:
            lastToAdd= line[line.index('['):line.index(']')+1]
            line = line.replace(lastToAdd, '')
            splittedLine = line.replace(',', ' ').split()
            splittedLine.append(lastToAdd)
        inst_name = splittedLine[0].upper()
        params =[param.lower() for param in splittedLine[1:]]
        return inst_name, params
        
    def convert_to_binary(self, line:str) -> str:
        insts = self.instructions
        inst_name, params = self.get_instruction_splitted(line)
        
        matched_params = {}
        inst_formats = insts[inst_name].get('formats') if insts[inst_name].get('formats') else [insts[inst_name].get('format')]
        for format in inst_formats:
            if len(params) == len(format):
                for i, param in enumerate(format):
                    matched_params[param] = params[i]  

        converted_regs = self.convert_matched_params(matched_params)
           
        binary_line = self.get_merged_instruction(inst_name, converted_regs)
        return binary_line

    def convert_matched_params(self, params:dict[str, str]) -> str:


        for param in list(params.keys()):
            if '[ra]' in param or '[ra, #imm16]' in param:
                params[param] = params[param].replace('[', '').replace(']', '').replace(',', ' ').split()
                # changes '[rx, #x]' to ['rx', '#x'] and '[rx]' to ['rx']
                if len(params[param]) == 2:
                    params['ra'] = params[param][0] # ra = ['rx', '#x'][0]
                    params['rb'] = params[param][1] # rb = ['rx', '#x'][1]
                elif len(params[param]) == 1 and '#' in params[param][0]:
                    params['rb'] = params[param][0]
                elif len(params[param]) == 1:
                    params['ra'] = params[param][0]
                del params[param]

        for param in list(params.keys()):
            params[param] = self.convert_register(params[param])
            if 'imm16' in param:
                params['rb'] = params.pop(param)

            if '-' in param:
                splitted = param.split('-')
                for i in splitted:
                    params[i] = params[param]
                del params[param]

        return params
    
    def convert_register(self, reg:str) -> str:
        if reg.lower().startswith('r'):
            return bin(int(reg[1:]))[2:].zfill(4)
        elif reg.startswith('#'):
            if '0x' in reg:
                return bin(int(reg[3:],16))[2:].zfill(16)
            elif '0b' in reg:
                return reg[3:].zfill(16)
            else:
                return bin(int(reg[1:]))[2:].zfill(16)

    
    def assemble_file(self, input_file:str, output_file:str=None, output_format:str='hex', input_format:str='asm'):
        self.set_defaults()
        lines = AssembleHelper.load_file(input_file)
        lines = self.clear_whitespace(lines)
        self.get_constants(lines)
        lines = self.set_constants(lines)
        self.get_labels(lines)
        lines = self.set_labels(lines)
        if output_format == 'hex':
            out_lines = [AssembleHelper.bin_to_hex(self.convert_to_binary(line))+'\n' for line in lines]
        elif output_format == 'bin':
            out_lines = [self.convert_to_binary(line)+'\n' for line in lines]
        if output_file == None:
            AssembleHelper.save_file(input_file.replace(f'.{input_format}', f'.{output_format}'), out_lines)
        else:
            AssembleHelper.save_file(output_file, out_lines)



def main():
    assembler = Assembler()
    lines = assembler.load_file('examples/screen.asm')
    lines = assembler.clear_whitespace(lines)
    assembler.get_constants(lines)
    lines = assembler.set_constants(lines)
    assembler.get_labels(lines)
    lines = assembler.set_labels(lines)
    
if __name__ == '__main__':
#main()
    assembler = Assembler()
    assembler.assemble_file('examples/screen.asm', output_format='bin')
    

        