f = open("/home/kermit/Desktop/Coding/CO Project evaluation framework Apr2 (copy 1)/SimpleSimulator/input.txt", "r")
lines = f.readlines()
if not lines:
    print("Error: Input file is empty")
    exit()

for line in lines:
    line = line.strip()
nums = len(lines)

instruction_type={
    'add':'R',
    'sub':'R',
    'sll':'R',
    'slt':'R',
    'sltu':'R',
    'xor':'R',
    'srl':'R',
    'or':'R',
    'and':'R',
    'addi':'I',
    'lw':'I',
    'sltiu':'I',
    'jalr':'I',
    'sw':'S',
    'beq':'B',
    'bne':'B',
    'blt':'B',
    'bge':'B',
    'bltu':'B',
    'bgeu':'B',
    'lui':'U',
    'auiprogramCounter':'U',
    'jal':'J'
}

registerValue={
'00000': 0 ,
'00001': 0 ,
'00010': 0 ,
'00011': 0 ,
'00100': 0 ,
'00101': 0 ,
'00110': 0 ,
'00111': 0 ,
'01000': 0 ,
'01001': 0 ,
'01010': 0 ,
'01011': 0 ,
'01100': 0 ,
'01101': 0 ,
'01110': 0 ,
'01111': 0 ,
'10000': 0 ,
'10001': 0 ,
'10010': 0 ,
'10011': 0 ,
'10100': 0 ,
'10101': 0 ,
'10110': 0 ,
'10111': 0 ,
'11000': 0 ,
'11001': 0 ,
'11010': 0 ,
'11011': 0 ,
'11100': 0 ,
'11101': 0 ,
'11110': 0 ,
'11111': 0 
}

instructionBinary={
    'add':'0110011',
    'sub':'0110011',
    'sll':'0110011',
    'slt':'0110011',
    'sltu':'0110011',
    'xor':'0110011',
    'srl':'0110011',
    'or':'0110011',
    'and':'0110011',
    'addi':'0010011',
    'lw':'0000011',
    'sltiu':'0010011',
    'jalr':'1100111',
    'sw':'0100011',
    'beq':'1100011',
    'bne':'1100011',
    'blt':'1100011',
    'bge':'1100011',
    'bltu':'1100011',
    'bgeu':'1100011',
    'lui':'0110111',
    'auiprogramCounter':'0010111',
    'jal':'1101111'
}

instructionLabels={
    '0110011':'R',
    '0000011':'I',
    '0010011':'I',
    '1100111':'I',
    '0100011':'S',
    '1100011': 'B',
    '0110111':'U',
    '0010111':'U',
    '1101111':'J'
}

memoryValue={
    '0x00010000' :0,
    '0x00010004' :0,
    '0x00010008':0,
    '0x0001000c':0,
    '0x00010010':0,
    '0x00010014':0,
    '0x00010018':0,
    '0x0001001c':0,
    '0x00010020':0,
    '0x00010024':0,
    '0x00010028':0,
    '0x0001002c':0,
    '0x00010030':0,
    '0x00010034':0,
    '0x00010038':0,
    '0x0001003c':0,
    '0x00010040':0,
    '0x00010044':0,
    '0x00010048':0,
    '0x0001004c':0,
    '0x00010050':0,
    '0x00010054':0,
    '0x00010058':0,
    '0x0001005c':0,
    '0x00010060':0,
    '0x00010064':0,
    '0x00010068':0,
    '0x0001006c':0,
    '0x00010070':0,
    '0x00010074':0,
    '0x00010078':0,
    '0x0001007c':0
}


nums = len(lines)
programCounter = {}

for i in range(0, nums * 4, 4):
    line_index = i // 4
    line = lines[line_index]
    programCounter[i] = line
if not programCounter:
    print("Error: programCounter dictionary is empty")
    exit()
OUTPUTS=[]
r=open("/home/kermit/Desktop/Coding/CO Project evaluation framework Apr2 (copy 1)/SimpleSimulator/output.txt",'w')
def bin32(num):
    binary = bin(num)[2:]
    binary = binary.zfill(32)
    return binary

def bintodec(binary_str):
    decimal_value = int(binary_str, 2)
    return (decimal_value)

def sext(value, bits):
    if value & (1 << (bits - 1)):
        return value - (1 << bits)
    else:
        return value
    
def unsigned(value, bits):
    return value & ((1 << bits) - 1)

def rtype(instruction, rd, rs1, rs2,func3,func7):
    if func3=='000' and func7=='0000000': 
        registerValue[rd] = registerValue[rs1] + registerValue[rs2]
    elif func3=='000' and func7=='0100000':
        registerValue[rd] = registerValue[rs1] - registerValue[rs2]
    elif func3=='001' and func7=='0000000': 
        registerValue[rd] = registerValue[rs1] << (registerValue[rs2] & 0b11111)
    elif func3=='010' and func7=='0000000': 
        registerValue[rd] = 1 if registerValue[rs1] < registerValue[rs2] else 0
    elif func3=='011' and func7=='0000000': 
        registerValue[rd] = 1 if (registerValue[rs1] & 0xFFFFFFFF) < (registerValue[rs2] & 0xFFFFFFFF) else 0
    elif func3=='100' and func7=='0000000': 
        registerValue[rd] = registerValue[rs1] ^ registerValue[rs2]
    elif func3=='101' and func7=='0000000': 
        registerValue[rd] = registerValue[rs1] >> (registerValue[rs2] & 0b11111)
    elif func3=='110' and func7=='0000000': 
        registerValue[rd] = registerValue[rs1] | registerValue[rs2]
    elif func3=='111' and func7=='0000000': 
        registerValue[rd] = registerValue[rs1] & registerValue[rs2]
    else:
        raise ValueError("Unsupported R-type instruction")
def utype(instruction,  rd, imm, oprogramCounterode, pcExecution):
    imm_decimal = bintodec(imm)
    if oprogramCounterode=="0110111":
        registerValue[rd] = imm_decimal << 12
    elif oprogramCounterode=="0010111":
        registerValue[rd] = pcExecution + (imm_decimal << 12)
    else:
        raise ValueError("Unsupported U-type instruction")

def itype(instruction, rd, rs1, immediate,func3,oprogramCounterode,pcExecution):
    imm=bintodec(immediate)
    if func3=='000' and oprogramCounterode=='0010011': 
        registerValue[rd] = registerValue[rs1] + imm
    elif func3 == '010' and oprogramCounterode == '0000011': 
        address_decimal = registerValue[rs1] + imm
        address_hex = hex(address_decimal)
        registerValue[rd] = memoryValue.get(address_hex, 0)
    elif func3=='011' and oprogramCounterode=='0010011':
        registerValue[rd] = 1 if registerValue[rs1] < imm else 0
    elif func3=='000' and oprogramCounterode=='1100111': 
        registerValue[rd] = pcExecution + 4
        pcExecution = registerValue[rs1] + imm
    else:
        raise ValueError("Unsupported I-type instruction")

def stype(instruction,rs2,rs1,immediate,func3,oprogramCounterode,pcExecution):
    imm = bintodec(immediate)
    if func3 == "010":
            address = registerValue[rs1] + sext(imm,32)
            memoryValue[address] = registerValue[rs2]
         
    else:
        raise ValueError("Unsupported S-type instruction")        

def btype(instruction,rs1,rs2,immediate,func3,pcExecution):
    imm=bintodec(immediate)
    if  func3 =="000":
         offset = (imm << 1) | 0b0
         target_address = pcExecution + offset
         if rs1 == rs2:  
            return target_address, True  
         else:
            return pcExecution + 4, False
    if  func3 =="001":
         offset = (imm << 1) | 0b0  
         target_address = pcExecution + offset  
        
         if rs1 != rs2:  
            return target_address, True  
         else:
            return pcExecution + 4, False

    if  func3 =="100":
        offset = (imm << 1) | 0b0  
        target_address = pcExecution + offset 
        if sext(rs1, 32) >= sext(rs2, 32):
            return pcExecution + 4, False
        else:
            return target_address, True
    if  func3 =="110":
        offset = (imm << 1) | 0b0  
        target_address = pcExecution + offset 
        if unsigned(rs1, 32) >= unsigned(rs2, 32):
            return pcExecution + 4, False
        else:
            return target_address, True

    if  func3 =="101":
        offset = (imm << 1) | 0b10  
        target_address = pcExecution + offset 
        if sext(rs1, 32) < sext(rs2, 32):
            return pcExecution + 4, False
        else:
            return target_address, True

    if  func3 =="111":
        offset = (imm << 1) | 0b0  
        target_address = pcExecution + offset 
        if unsigned(rs1, 32) < unsigned(rs2, 32):
            return pcExecution + 4, False
        else:
            return target_address, True 


def jtype(instruction, rd, imm, oprogramCounterode, pcExecution):
    imm_decimal = bintodec(imm)
    registerValue[rd] = pcExecution + 4
    offset = ((int(imm) & 0b111111111111) << 1) | 0b0
    target_address = pcExecution + offset
    target_address &= 0xFFFFFFFE
    pcExecution = target_address
    
def execute_instruction(instruction,pcExecution):
    type = decodeInstructionType(instruction)
    if type == "R":
        rtype(instruction, instruction[20:25], instruction[12:17], instruction[7:12],instruction[17:20],instruction[0:7])
    elif type == "I":
        itype(instruction, instruction[20:25], instruction[12:17], instruction[0:12],instruction[17:20],instruction[25:32],pcExecution)
    elif type == "B":
        imm=instruction[0]+instruction[24]+instruction[1:7]+instruction[20:26]
        btype(instruction,instruction[12:17],instruction[20:25],imm,instruction[17:20],pcExecution)
    elif type == "S":
        imm = instruction[0:7] + instruction[20:25]
        stype(instruction, instruction[7:12], instruction[12:17], imm, instruction[17:20],instruction[25:31],pcExecution)
    elif type == "U":
        utype(instruction,instruction[20:25],instruction[0:20],instruction[25:32],pcExecution)
    elif type == "J":
        imm = instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11]
        jtype(instruction,instruction[20:25],imm,instruction[25:32],pcExecution)

def programCounterAndOuput(pcExecution):
    output = '0b'+ str(bin32(pcExecution)) + " " 
    register_bin_values = {}
    
    for key, value in registerValue.items():
        register_bin_values[key] = bin32(value)  
        output += "0b" + register_bin_values[key] + ' '
    output+='\n'
    OUTPUTS.append(output)
    
    return register_bin_values


def decodeInstructionType(instruction):
    OprogramCounterODE=instruction[-8:-1]
    INSTRUCTION_TYPE=instructionLabels[OprogramCounterODE]
    return INSTRUCTION_TYPE


pcEnd = max(programCounter.keys())
pcExecution = 0 

def memOutput():
    memoryValue_bin_values = {} 
    for key, value in memoryValue.items():
        
        memoryValue_bin_values[key] = bin32(value)  
        out = str(key) + ": " + "0b" + memoryValue_bin_values[key] +'\n'
        r.write(out)

while pcExecution < pcEnd:
    instruction = programCounter[pcExecution]  
    execute_instruction(instruction, pcExecution)
    programCounterAndOuput(pcExecution)
    pcExecution += 4

for i in OUTPUTS:
    r.write(i)
memOutput()
f.close()
r.close()
