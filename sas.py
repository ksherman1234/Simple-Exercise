import sys


def input_taker(input):
    """Read user input into a list and eliminate blank lines"""
    try:
        with open(input) as f:
            lines = f.readlines()
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit(0)

    lines = [elem.strip() for elem in lines]

    for item in lines:
        item = str(item)
        if item[:1] == "#":
            lines.remove(item)
    lines = list(filter(None, lines))
    return lines


def assign_labels_address(input_instructions):
    """Loops through list of instructions and maps labels to addresses"""
    labels = {}
    address = 0
    for line in input_instructions:
        items = line.split()
        if items[0][-1:] == ':' and items[0][:1] != "#":
            if (input_instructions.index(line) + 1 ==
                    len(input_instructions) and len(items) == 1):
                raise ValueError("Improper label location")
            items[0] = items[0][:-1]
            labels[items[0]] = address
        if len(items) == 1:
            continue
        else:
            address = address + 1
    return labels


def get_address_from_label(elems_in_each_line, label_list):
    """Matches labels to their address and returns address"""
    command = (
        elems_in_each_line[2] if (len(elems_in_each_line[1]) == 3 and
                                  elems_in_each_line[1].isupper())
        else elems_in_each_line[1])
    if command.isdigit():
        commandInt = int(command)
        if 0 <= commandInt and commandInt < 16:
            bit = '{0:04}'.format(commandInt)
            return str(bit)
        else:
            raise ValueError("Address can't be larger than 16 bits")
            exit(0)
    else:
        for key in label_list:
            if command == key:
                return label_list[key]
        return


def get_labeladdress_DAT(label, label_list):
    """Gets label address if op is DAT"""
    for key in label_list:
        if key == label:
            return label_list[key]
    return


def dat_command_helper(elems_in_each_line, label_list):
    """Helper method for dealing with DAT instructions"""
    command = (elems_in_each_line[2] if elems_in_each_line[1] == "DAT"
               else elems_in_each_line[1])
    if command.isdigit():
        commandInt = int(command)
        if 0 <= commandInt and commandInt < 256:
            bit = '{0:08b}'.format(commandInt)
            return str(bit)
        else:
            raise ValueError("Too high a number, can't be more than 16")
            exit(0)
    else:
        address = get_labeladdress_DAT(command, label_list)
        if address is None:
            raise ValueError("Invalid Input. Exiting program")
            exit(0)
        address_bit = '{0:08b}'.format(int(address))
        return str(address_bit)


def command_match_helper(encoding_list, label_list, opp_and_addr):
    """Creates bits for all non DAT commands"""
    for key in encoding_list:
        if opp_and_addr[1] == key or opp_and_addr[0] == key:
            bit = encoding_list[key]
            address = get_address_from_label(opp_and_addr, label_list)
            if address is None:
                raise ValueError("Invalid Input. Exiting program")
                exit(0)
            address_bit = '{0:04b}'.format(int(address))
            bit = bit + str(address_bit)
            return bit
    return


def byte_maker(input_list, label_list, encoding_list):
    """Given the input list, outputs list of byte string"""
    bytelist = []
    for item in input_list:
        opp_and_addr = item.split()

        if opp_and_addr[0] == "DAT":
            bit = dat_command_helper(opp_and_addr, encoding_list)
            bytelist.append(bit)
        elif opp_and_addr[0] == "HLT":
            bit = "00000000"
            bytelist.append(bit)
        else:
            bit = command_match_helper(encoding_list, label_list, opp_and_addr)
            bytelist.append(bit)
    return bytelist


def clear_comments(input):
    """Removes all comments"""
    new_list = []
    for line in input:
        new_line = line.split("#")
        new_list.append(new_line[0])
    return new_list


def address_opp_error_check(input):
    """Checks that there is an address for each operation"""
    for line in input:
        items = line.split()
        if len(items) != 2:
            if len(items) == 1 and items[0] == "HLT":
                continue
            else:
                raise ValueError(
                    "Each line must have an operation and an address")
        else:
            if items[0] == "HLT":
                raise ValueError("You can not have HLT with an address")
            else:
                continue


def label_errors(input):
    """removes labels to avoid errors"""
    new_list = []
    for line in input:
        items = line.split()
        if items[0][-1:] == ':':
            new_line = line.split(":")
            new_list.append(new_line[1])
        else:
            new_list.append(line)
    return new_list


def print_to_stdout(byte_list):
    """Conversts list of byte strings to bytecode and prints to stdout """

    for byte in byte_list:
        sys.stdout.buffer.write(bytes([int(byte, 2)]))


def main():
    """Main function. Takes in file name and outputs bytes"""
    if len(sys.argv) > 2:
        sys.argv[:2]

    try:
        input = sys.argv[1]
    except IndexError:
        print("Not enough arguments")
        exit(0)

    instruction_list = input_taker(input)
    if len(instruction_list) > 16:
        raise ValueError(("Too many instructions, can't be more than 16."))
        exit(0)

    clear_input_instructions = clear_comments(instruction_list)
    label_dict = assign_labels_address(clear_input_instructions)

    # scram instruction bit pattern
    encoding = {
        "HLT": "0000", "LDA": "0001", "LDI": "0010",
        "STA": "0011", "STI": "0100", "ADD": "0101",
        "SUB": "0110", "JMP": "0111", "JMZ": "1000",
    }
    final_input_instructions = label_errors(clear_input_instructions)
    address_opp_error_check(final_input_instructions)
    byte_list = byte_maker(final_input_instructions, label_dict, encoding)
    print_to_stdout(byte_list)


if __name__ == "__main__":
    main()
