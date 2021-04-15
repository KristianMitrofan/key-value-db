#!/usr/bin/python
import random
import string
import sys

if __name__ == "__main__":
    #Some constant variables about the random data generated
    MAX_INT = 1000000
    MAX_FLOAT = 1000
    VOCABULARY = string.ascii_lowercase + string.digits
        
    #createData -k keyFile.txt -n 1000 -d 3 -l 4 -m 5
    #Assign some default values to be safe
    data_file = "dataToIndex.txt"
    key_file = "keyFile.txt"
    num_of_lines = 1000
    max_depth = 3
    max_length = 4
    max_keys = 5

    for i, arg in enumerate(sys.argv):
        if arg == "-k":
            key_file = sys.argv[i+1]
        elif arg == "-n":
            num_of_lines = int(sys.argv[i+1])
        elif arg == "-d":
            max_depth = int(sys.argv[i+1])
        elif arg == "-l":
            max_length = int(sys.argv[i+1])
        elif arg == "-m":
            max_keys = int(sys.argv[i+1])

    #The format we want to generate is very similar to python dictionaries
    def generate_value(main_value,max_depth,max_keys,key_dict):
        if max_depth == 0:
            return main_value
        else:
            num_of_keys = random.randrange(max_keys)

            for _k in range(0,num_of_keys): 
                key = random.choice(list(key_dict.keys()))
                key_type = key_dict[key]
                
                if key_type == "string":
                    main_value[key] = ''.join(random.choice(VOCABULARY) for i in range(random.randrange(1,max_length)))
                elif key_type == "int":
                    main_value[key] = str(random.randrange(MAX_INT))
                elif key_type == "float":
                    main_value[key] = str(round(random.uniform(0,MAX_FLOAT),2))
                #I have added another type called set which is specifically for key-set values
                elif key_type == "set":
                    main_value[key] = generate_value({},max_depth-1,max_keys,key_dict)
                else:
                    main_value[key] = {}

        return main_value


    #Read the file with the value names and types, and store it in a dictionary
    key_of = open(key_file, "r")
    data_of = open(data_file, "w")
    key_dict = {}
    for line in key_of:
        key_dict[line.split()[0]] = line.split()[1]

    key_of.close()

    #Generate the lines of data as requested
    #e.g. “person2” : { “name” : “Mary” ; “address” : { “street” : “Panepistimiou” ; “number” : 12 } }
    for line_num in range(0,num_of_lines):
        main_key = "\"person" + str(line_num) + "\""
        main_value = {}
        main_value = generate_value(main_value,max_depth+1,max_keys,key_dict)
        line = main_key + " : " + str(main_value).replace(",",";").replace("\'","\"") + "\n"
        data_of.write(line)

    data_of.close()