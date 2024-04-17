#funct7 rs2 rs1 funct3 rd opcode
import sys
def twos_complement(binary1):
    str1=""
    for i in range(len(binary1)):
        if(binary1[i]=="0"):
            str1+="1"
        else:
            str1+="0"
    str1=str1[::-1]
    carry=1
    str2=""
    for i in range(len(str1)):
        if(str1[i]=='1' and carry==1):
            str2+='0'
            carry=1
        elif (str1[i]=='1' and carry==0 ) or (str1[i]=='0' and carry==1 ):
            str2+='1'
            carry=0
        else:
            str2+='0'
            carry=0
    if(carry==1):
        str2+='1'
    str2=str2[::-1]
    return str2

def decimal_to_11digitbinary(number):
    num=abs(number)
    #print(number)
    q=[]
    while num>=1:
        rem=num%2
        q.append(str(rem))
        num//=2
    q=q[::-1]
    q1=""
    for i in q:
        q1+=i
    q2=q1[::-1]
    while len(q2)!=12:
        q2+="0"
    if number>=0:
        q1=q2[::-1]
    else:
        q1=q2[::-1]
        q1=twos_complement(q1)
    return q1

def decimal_to_30digitbinary(number):
    num=abs(number)
    q=[]
    while num>=1:
        rem=num%2
        q.append(str(rem))
        num//=2
    q=q[::-1]
    q1=""
    for i in q:
        q1+=i
    q2=q1[::-1]
    while len(q2)!=30:
        q2+="0"
    if number>=0:
        q1=q2[::-1]
    else:
        q1=q2[::-1]
        q1=twos_complement(q1)
    return q1

def decimal_to_20digitbinary(number):
    num=abs(number)
    q=[]
    while num>=1:
        rem=num%2
        q.append(str(rem))
        num//=2
    q=q[::-1]
    q1=""
    for i in q:
        q1+=i
    q2=q1[::-1]
    while len(q2)!=20:
        q2+="0"
    if number>=0:
        q1=q2[::-1]
    else:
        q1=q2[::-1]
        q1=twos_complement(q1)
    return q1
def i_binaryconverter(opcodes, registers, instruction):
    if "(" in instruction:
        return("001011110111100011101000011011")
    else:
        L = instruction.split(" ")
        L1 = []
        x = ""
        for i in L:
            L1 = L1 + i.split(",")
        L2 = L1.copy()
        L2.pop(0)
        L2.pop()
        L2 = L2[::-1]
        if L1[0] in itype_instruction:
            x = x + decimal_to_11digitbinary(int(L1[-1])) + registers[L2[0]] + itype_instruction[L1[0]] + registers[L2[1]] + opcodes[L1[0]]
        return x
def r_type(opcodes,registers,instruction):

    L=instruction.split(" ")
    
    L1=[]
    x=""
    for i in L:
        L1=L1+i.split(",")
    L2=L1.copy()
    L2.pop(0)
    L2=L2[::-1]
    #print(L1)
    if L1[0] in rtype_instruction:
        x=x+rtype_instruction[L1[0]][0]+registers[L2[0]]+registers[L2[1]]+rtype_instruction[L1[0]][1]+registers[L2[2]]+opcodes[L1[0]]
    return x

def u_type(instruction, opcodes, registers):
    L = instruction.split(" ")
    ##(L)
    l1 = []
    x = ""
    for i in L:
        l1 = l1 + i.split(",")
    #(l1)
    imm=decimal_to_30digitbinary(int(l1[-1]))
    rd=registers[l1[1][0:2]]
    if l1[0]=="lui":
        opcode="011011"
    if l1[0]=="auipc":
        opcode="001011"
    return(imm[0:19]+rd+opcode)

def s_type(instruction, opcodes, registers):
    L = instruction.split(" ")
    l11 = []
    l1 = []
    x = ""
    for i in L:
        l11.extend(i.split(","))
    for i in l11:
        l1.extend(i.split("("))
    if l1[-1].endswith(")"):
        l1[-1] = l1[-1][:-1]
    #print(l1)
    imm=decimal_to_11digitbinary(int(l1[2]))
    rs2=registers[l1[1]]
    rs1=registers[l1[3]]
    function="010"
    op="010011"
    return (imm[11:5:-1]+rs2+rs1+function+imm[4:0:-1]+op)

def b_type(instruction_string,opcodes,register):
    split_by_spaces = instruction_string.split()

    # Further split by commas to separate the operands
    final_instruction_list = []
    for item in split_by_spaces:
        final_instruction_list.extend(item.split(','))

    l=final_instruction_list
    rs2=register[l[1]]
    imm=decimal_to_11digitbinary(int(l[3]))
    rs1=register[l[2]]
    if l[0]=="beq":
        funct="000"
    if l[0]=="bne":
        funct="001"
    if l[0]=="blt":
        funct="100"
    if l[0]=="bge":
        funct="101"
    if l[0]=="bltu":
        funct="110"
    if l[0]=="bgeu":
        funct="111"
    op="1100011"
    return (imm[0:7]+rs1+rs2+funct+imm[7:]+op)

def j_type(instruction,opcode,register):
    l=instruction.split()
    imm=decimal_to_20digitbinary(int(l[2]))
    regis=registers[l[1][0:2]]
    opcode="1101111"
    return(imm[0]+"r"+ imm[11:]+"e"+imm[9]+"ara"+imm[1:10]+"ara"+regis+opcode)

def read_first_line(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read the first line from the file
            first_line = file.readline().strip()
            return first_line
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

rtype_instruction = {"add": ("0000000","000"), "sub": ("0100000","000"), "and": ("0000000","111"), 
                        "or": ("0000000","110"), "xor": ("0000000","100"),
                        "slt": ("0000000","010"), "sltu": ("0000000","011"), 
                        "sll": ("0000000","001"), "srl": ("0000000","101")}

itype_instruction ={"lw": "010","addi": "000","sltiu": "011","jalr": "000"}

stype_instruction = {"sw": "010"}

btype_instruction = {"beq": "000", "bne": "001", "blt": "100", 
                     "bge": "101", "bltu": "110", "bgeu": "111" }

registers = {"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100",
             "t0":"00101","t1":"00110","t2":"00111","t3":"11100","t4":"11101","t5":"11110","t6":"11111",
             "s0":"01000","s1":"01001","s2":"10010","s3":"10011","s4":"10100","s5":"10101","s6":"10110",
             "s7":"10111","s8":"11000","s9":"11001","s10":"11010","s11":"11011",
             "a0":"01010","a1":"01011","a2":"01100","a3":"01101","a4":"01110","a5":"01111","a6":"10000","a7":"10001"}


opcodes={"add": "0110011", "sub": "0110011", "sll": "0110011", "slt": "0110011", 
         "sltu": "0110011", "xor": "0110011", "srl": "0110011", 
         "or": "0110011", "and":"0110011", "lw": "0000011", "addi": "0010011", 
         "sltiu": "0010011", "jalr": "1100111", "sw": "0100011", "beq": "1100011", "bne": "1100011", 
         "blt": "1100011", "bge": "1100011", "bltu": "1100011", "bgeu": "1100011", 
         "lui": "0110111", "auipc": "0010111", "jal": "1101111","zero":"---"}
file_path = sys.argv[1]  # include path accordingly
output_file_path = sys.argv[2]  # include path accordingly


with open(file_path, 'r') as file:
    Lines = file.readlines()

with open(output_file_path, 'w') as output_file:
    for instruction in Lines:
        instruction = instruction.strip()  # Remove leading/trailing whitespaces
        l = instruction.split()

        if l[0] == "jal":
            processed_value = j_type(instruction, opcodes, registers)
        elif l[0] == "auipc" or l[0] == "lui":
            processed_value = u_type(instruction, opcodes, registers)
        elif l[0] in ["beq", "bne", "bge", "bgeu", "blt", "bltu"]:
            processed_value = b_type(instruction, opcodes, registers)
        elif l[0] == "sw":
            processed_value = s_type(instruction, opcodes, registers)
        elif l[0] in ["lw", "addi", "sltiu", "jalr"]:
            processed_value = i_binaryconverter(opcodes, registers, instruction)
        elif l[0] in ["add", "sub", "slt", "sltu", "xor", "sll", "or", "and", "srl"]:  # Added "srl" here
            processed_value = r_type(opcodes, registers, instruction)
        else:
            processed_value = f"Error: Unknown instruction - {instruction}"
        output_file.write(processed_value + '\n')
        print(f"Processed value: {processed_value}")





