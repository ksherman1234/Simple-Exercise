import sys


def input_taker(input):
    """Read user input into a list and eliminate blank lines"""
    with open(input) as f:
        lines = f.readlines()
    f.close()
    lines = [elem.strip() for elem in lines]

    for item in lines:
        #converts all items to a string
        item = str(item)
        if item[:1] == "#":
            lines.remove(item)
    lines = filter(None, lines)
    #removes empty lines
    for x in lines:
        print(x)
    return lines


def assign_labels_address(input_instructions):
    """Loops through list of instructions and maps labels to addresses"""
    labels = {}
    address = 0
    for line in input_instructions:
        items = line.split()
        if items[0][-1:] == ':' and items[0][:1] != "#":
            items[0] = items[0][:-1]
            labels[items[0]] = address
        address = address + 1
    return labels


def dat_command_helper(command):
    """Helper method for dealing with DAT instructions"""
    commandInt = int(command)
    if 0 <= commandInt and commandInt < 256:

        bit = '{0:08b}'.format(commandInt)
        return str(bit)
    else:
        print("Kevin, Simple Exercise, PLZ")


def get_address_from_label(opp_and_addr, label_list):
    """Matches labels to their address and returns address"""
    for key in label_list:
        extra = "tHiS Is ExtRa"
        opp_and_addr.append(extra)
        if opp_and_addr[1] == key or opp_and_addr[2] == key:
            return label_list[key]
    return


def command_match_helper(encoding_list, label_list, opp_and_addr):
    """Creates bits for all non DAT commands"""
    for key in encoding_list:
        if opp_and_addr[1] == key or opp_and_addr[0] == key:
            bit = encoding_list[key]
            address = get_address_from_label(opp_and_addr, label_list)
            if address == None:
                continue
            address_bit = '{0:04b}'.format(int(address))
            bit = bit + str(address_bit)
            return bit
    return


def byte_maker(input_list, label_list, encoding_list):
    """Given the input list, outputs list of byte string"""
    bytelist = []
    for item in input_list:
        opp_and_addr = item.split()

        if opp_and_addr[1] == "DAT":
            #deals with Data
            bit = dat_command_helper(opp_and_addr[2])
            bytelist.append(bit)
        else:
            bit = command_match_helper(encoding_list, label_list, opp_and_addr)
            bytelist.append(bit)
    return bytelist


def print_to_stdout(byte_list):
    """Conversts list of byte strings to bytecode and prints to stdout """
    bytes =[]
    for byte_string in byte_list:
        #Encodes string
        byte = byte_string.encode()
        bytes.append(byte)
    for byte in bytes:
        print(byte)


def main():
    """Main function. Takes in file name as command line argument and outputs bytes"""
    if len(sys.argv) != 2:
        print("Simple Exercise")
    #need if statement for bad command line arguments

    input = sys.argv[1]
    instruction_list = input_taker(input)
    # scram instruction bit pattern
    encoding = {
        "HLT": "0000", "LDA": "0001", "LDI": "0010",
        "STA": "0011", "STI": "0100", "ADD": "0101",
        "SUB": "0110", "JMP": "0111", "JMZ": "1000",
    }
    label_dict = assign_labels_address(instruction_list)
    byte_list = byte_maker(instruction_list, label_dict, encoding)
    print_to_stdout(byte_list)


if __name__ == "__main__":
    main()