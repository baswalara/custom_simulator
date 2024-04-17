import sys

def positive_int(num):
    if num >= 0:
        return num
    else:
        return -1 * num

def add_binary(bin1, bin2):
    num1 = int(bin1, 2)
    num2 = int(bin2, 2)
    sum_decimal = num1 + num2
    sum_binary = bin(sum_decimal)[2:]
    return sum_binary

def u_type(r, REGISTERS_MEMORY, REGISTERS_VALUES, pc):
    if r[25:32] == "0110111" or r[25:32] == "0010111":
        if r[25:32] == "0110111":  # lui
            c_register = r[20:25]
            imm = r[0:20]
            e = REGISTERS_MEMORY[c_register]
            REGISTERS_VALUES[e] = imm
        elif r[25:32] == "0010111":  # auipc
            c_register = r[11:7:-1]
            imm = r[31:12:-1]
            e = REGISTERS_MEMORY[c_register]
            REGISTERS_VALUES[e] = add_binary(pc, imm)
    else:
        return

def j_type(r, REGISTERS_MEMORY, REGISTERS_VALUES, pc):
    if r[25:32] == "1101111":
        c_register = r[20:25]  # jal
        imm = r[0] + r[12:20] + r[11] + r[1:11]
        e = REGISTERS_MEMORY[c_register]
        REGISTERS_VALUES[e] = add_binary(pc, "100")
    else:
        return

def sign_extend(imm, bits):
    if imm[0] == '1':
        return (bin(int(imm, 2) - (1 << bits))[2:]).zfill(bits)
    else:
        return imm.zfill(bits)

def beq(rs1, rs2, imm, pc):
    r = False
    imm_value = sign_extend(imm, 12)
    if REGISTERS_VALUES[rs1] == REGISTERS_VALUES[rs2]:
        r = True
    if r == True:
        pc += int(imm_value)
    return pc, r, imm

def bne(rs1, rs2, imm, pc):
    r = False
    imm_value = sign_extend(imm, 12)
    if REGISTERS_VALUES[rs1] != REGISTERS_VALUES[rs2]:
        r = True
    if r == True:
        pc += imm_value
    return pc, r, imm

def blt(rs1, rs2, imm, pc):
    r = False
    imm_value = sign_extend(imm, 12)
    if REGISTERS_VALUES[rs1] < REGISTERS_VALUES[rs2]:
        r = True
    if r == True:
        pc += imm_value
    return pc, r, imm

def bge(rs1, rs2, imm, pc):
    r = False
    imm_value = sign_extend(imm, 12)
    if REGISTERS_VALUES[rs1] >= REGISTERS_VALUES[rs2]:
        r = True
    if r == True:
        pc += imm_value
    return pc, r, imm

def bltu(rs1, rs2, imm, pc):
    r = False
    imm_value = sign_extend(imm, 12)
    if REGISTERS_VALUES[rs1] < REGISTERS_VALUES[rs2]:
        r = True
    if r == True:
        pc += imm_value
    return pc, r, imm

def bgeu(rs1, rs2, imm, pc):
    r = False
    imm_value = sign_extend(imm, 12)
    if REGISTERS_VALUES[rs1] >= REGISTERS_VALUES[rs2]:
        r = True
    if r == True:
        pc += imm_value
    return pc, r, imm

def add(rd, rs1, rs2, REGISTERS_VALUES):
    rd_val = int(REGISTERS_VALUES[rs1], 2) + int(REGISTERS_VALUES[rs2], 2)
    REGISTERS_VALUES[rd] = format(rd_val, '032b')[-32:]

def sub(rd, rs1, rs2, REGISTERS_VALUES):
    if rs1 == "x0":
        rd_val = 0 - int(REGISTERS_VALUES[rs2], 2)
    else:
        rd_val = int(REGISTERS_VALUES[rs1], 2) - int(REGISTERS_VALUES[rs2], 2)
    REGISTERS_VALUES[rd] = format(rd_val, '032b')[-32:]

def slt(rd, rs1, rs2, REGISTERS_VALUES):
    if int(REGISTERS_VALUES[rs1], 2) < int(REGISTERS_VALUES[rs2], 2):
        REGISTERS_VALUES[rd] = '00000000000000000000000000000001'
    else:
        REGISTERS_VALUES[rd] = '00000000000000000000000000000000'

def sltu(rd, rs1, rs2, REGISTERS_VALUES):
    if int(REGISTERS_VALUES[rs1], 2) < int(REGISTERS_VALUES[rs2], 2):
        REGISTERS_VALUES[rd] = '00000000000000000000000000000001'
    else:
        REGISTERS_VALUES[rd] = '00000000000000000000000000000000'

def xor(rd, rs1, rs2, REGISTERS_VALUES):
    rd_val = positive_int(int(REGISTERS_VALUES[rs1], 2)) ^ positive_int(int(REGISTERS_VALUES[rs2], 2))
    REGISTERS_VALUES[rd] = format(rd_val, '032b')[-32:]

def sll(rd, rs1, rs2, REGISTERS_VALUES):
    shift_amount = int(REGISTERS_VALUES[rs2][-5:], 2)
    rd_val = int(REGISTERS_VALUES[rs1], 2) << shift_amount
    REGISTERS_VALUES[rd] = format(rd_val, '032b')[-32:]

def srl(rd, rs1, rs2, REGISTERS_VALUES):
    shift_amount = int(REGISTERS_VALUES[rs2][-5:], 2)
    rd_val = int(REGISTERS_VALUES[rs1], 2) >> shift_amount
    REGISTERS_VALUES[rd] = format(rd_val, '032b')[-32:]

def or_or(rd, rs1, rs2, REGISTERS_VALUES):
    rd_val = int(REGISTERS_VALUES[rs1], 2) | int(REGISTERS_VALUES[rs2], 2)
    REGISTERS_VALUES[rd] = format(rd_val, '032b')[-32:]

def and_and(rd, rs1, rs2, REGISTERS_VALUES):
    rd_val = int(REGISTERS_VALUES[rs1], 2) & int(REGISTERS_VALUES[rs2], 2)
    REGISTERS_VALUES[rd] = format(rd_val, '032b')[-32:]

def lw(rd, rs1, imm, REGISTERS_VALUES):
    address = int(REGISTERS_VALUES[rs1], 2) + int(imm, 2)
    mem_value = MEMORY[address]
    REGISTERS_VALUES[rd] = format(mem_value, '032b')[-32:]

def addi(rd, rs1, imm, REGISTERS_VALUES):
    rs1_value = int(REGISTERS_VALUES[rs1], 2)
    imm_value = int(imm, 2)
    result = rs1_value + imm_value
    REGISTERS_VALUES[rd] = format(result, '032b')[-32:]

def sltiu(rd, rs1, imm, REGISTERS_VALUES):
    rs1_value = int(REGISTERS_VALUES[rs1], 2)
    imm_value = int(imm, 2)
    if rs1_value < imm_value:
        REGISTERS_VALUES[rd] = '00000000000000000000000000000001'
    else:
        REGISTERS_VALUES[rd] = '00000000000000000000000000000000'

def jalr(rd, rs1, imm, REGISTERS_VALUES):
    pc = int(REGISTERS_VALUES["pc"], 2)
    REGISTERS_VALUES[rd] = format(pc + 4, '032b')[-32:]
    REGISTERS_VALUES["pc"] = format(int(REGISTERS_VALUES[rs1], 2) + int(imm, 2), '032b')[:-1]

def sw(rs1, rs2, imm, REGISTERS_VALUES):
    address = int(REGISTERS_VALUES[rs1], 2) + int(sign_extend(imm, 12), 2)
    value = REGISTERS_VALUES[rs2]
    MEMORY[address] = value

def r_type(s, REGISTERS_MEMORY, REGISTERS_VALUES):
    opcode = s[25:32]
    funct7 = s[0:7]
    y = s[7:12]
    x = s[12:17]
    rs1 = REGISTERS_MEMORY[x]
    rs2 = REGISTERS_MEMORY[y]
    func3 = s[17:20]
    rd = s[20:25]

def s_type(instruction, REGISTERS_MEMORY, REGISTERS_VALUES):
    imm = instruction[25:20] + instruction[7:12]
    rs2 = instruction[20:25]
    rs1 = instruction[15:20]
    func3 = instruction[12:15]
    if func3 == "010":
        sw(rs1, rs2, imm)

def i_type(s, REGISTERS_MEMORY, REGISTERS_VALUES):
    opcode = s[25:32]
    imm = s[0:12]
    rs1 = REGISTERS_MEMORY[s[12:17]]
    rd = s[20:25]
    func3 = s[17:20]

    if opcode == "0000011":
        lw(rd, rs1, imm)
    elif opcode == "0010011" and func3 == "000":
        addi(rd, rs1, imm)
    elif opcode == "0010011" and func3 == "011":
        sltiu(rd, rs1, imm)
    elif opcode == "1100111":
        jalr(rd, rs1, imm)

def b_type(s, REGISTERS_MEMORY, REGISTERS_VALUES, pc):
    opcode = s[25:32]
    a = s[15:20]
    rs1 = REGISTERS_MEMORY[a]
    b = s[20:25]
    rs2 = REGISTERS_MEMORY[b]
    func3 = s[12:15]
    imm = s[0] + s[24] + s[1:7] + s[20:24] + s[7:12]
    if opcode == "1100011":  # B-type opcode
        if func3 == "000":  # beq
            pc, r, imm = beq(rs1, rs2, imm, pc)
        elif func3 == "001":  # bne
            pc, r, imm = bne(rs1, rs2, imm, pc)
        elif func3 == "100":  # blt
            pc, r, imm = blt(rs1, rs2, imm, pc)
        elif func3 == "101":  # bge
            pc, r, imm = bge(rs1, rs2, imm, pc)
        elif func3 == "110":  # bltu
            pc, r, imm = bltu(rs1, rs2, imm, pc)
        elif func3 == "111":  # bgeu
            pc, r, imm = bgeu(rs1, rs2, imm, pc)
    return pc, r, imm

memory_values = {}

# Define REGISTERS_MEMORY and REGISTERS_VALUES dictionaries
REGISTERS_MEMORY = {
    '00000': 'zero',
    '00001': 'ra',
    '00010': 'sp',
    '00011': 'gp',
    '00100': 'tp',
    '00101': 't0',
    '00110': 't1',
    '00111': 't2',
    '01000': 's0',
    '01001': 's1',
    '01010': 'a0',
    '01011': 'a1',
    '01100': 'a2',
    '01101': 'a3',
    '01110': 'a4',
    '01111': 'a5',
    '10000': 'a6',
    '10001': 'a7',
    '10010': 's2',
    '10011': 's3',
    '10100': 's4',
    '10101': 's5',
    '10110': 's6',
    '10111': 's7',
    '11000': 's8',
    '11001': 's9',
    '11010': 's10',
    '11011': 's11',
    '11100': 't3',
    '11101': 't4',
    '11110': 't5',
    '11111': 't6'
}

REGISTERS_VALUES = {
    "zero": "0",
    "ra": "0",
    "sp": "0",
    "gp": "0",
    "tp": "0",
    "t0": "0",
    "t1": "0",
    "t2": "0",
    "s0": "0",
    "s1": "0",
    "a0": "0",
    "a1": "0",
    "a2": "0",
    "a3": "0",
    "a4": "0",
    "a5": "0",
    "a6": "0",
    "a7": "0",
    "s2": "0",
    "s3": "0",
    "s4": "0",
    "s5": "0",
    "s6": "0",
    "s7": "0",
    "s8": "0",
    "s9": "0",
    "s10": "0",
    "s11": "0",
    "t3": "0",
    "t4": "0",
    "t5": "0",
    "t6": "0",
    "pc": "0"
}

MEMORY = memory_values

f = sys.argv[1]
with open(f, "r") as file:
    pc = 0
    for line in file:
        pc += 1
        s = line.strip()
        if s == "00000000000000000000000001100011":
            break
        opcode = s[25:32]
        pc = int(REGISTERS_VALUES["pc"], 2)
        if opcode[0] == '0':
            r_type(s, REGISTERS_MEMORY, REGISTERS_VALUES)
        elif opcode[0:2] == '01':
            i_type(s, REGISTERS_MEMORY, REGISTERS_VALUES)
        elif opcode == '1101111':
            j_type(s, REGISTERS_MEMORY, REGISTERS_VALUES, pc)
        elif opcode == '1100011':
            pc, r, i_b = b_type(s, REGISTERS_MEMORY, REGISTERS_VALUES, pc)
            if r == True:
                for j in range(int(i_b) - 1):
                    continue
        elif opcode == '0110111' or opcode == '0010111':
            u_type(s, REGISTERS_MEMORY, REGISTERS_VALUES, pc)
        else:
            s_type(s, REGISTERS_MEMORY, REGISTERS_VALUES)
        REGISTERS_VALUES["pc"] = format(pc + 4, '032b')[-32:]

r = sys.argv[2]
r = open(r, "w")
for register, value in REGISTERS_VALUES.items():
    print(f"{register}: {value}")
    r.write(f"{register}: {value}\n")