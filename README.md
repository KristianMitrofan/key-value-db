# key-value-db
In this project we will be creating a simple version of a distributed, fault-tolerant, Key-Value (KV) database (or store), with a few tweaks. From Wikipedia: a key–value database, or key–value store, is a data storage paradigm designed for storing, retrieving, and managing associative arrays, and a data structure more commonly known today as a dictionary or hash table. Dictionaries contain a collection of objects, or records, which in turn have many different fields within them, each containing data. These records are stored and retrieved using a key that uniquely identifies the record, and is used to find the data within the database. In our case, we will be using a Trie instead of a hash table for storing the keys.

Data Creation

createData.py is used for this task and it can be run as:
e.g. python createData.py -k keyFile.txt -n 1000 -d 3 -l 4 -m 5
where:
    -n indicates the number of lines (i.e. separate data) that we would like to generate (e.g. 1000)
    -d is the maximum level of nesting (i.e. how many times in a line a value can have a set of key :
    values). Zero means no nesting, i.e. there is only one set of key-values per line (in the value of the
    high level key)
    M111 - Big Data - Spring 2021 - Programming Assignment
    Deadline: April 16th 2021, 23:59
    -m is the maximum number of keys inside each value.
    -l is the maximum length of a string value whenever you need to generate a string. For example 4
    means that we can generate Strings of up to length 4 (e.g. “ab”, “abcd”, “a”). We should not generate
    empty strings (i.e. “” is not correct). Strings can be only letters (upper and lowercase) and numbers. No
    symbols.
    -k keyFile.txt is a file containing a space-separated list of key names and their data types that we

KV Broker
The kv Broker NEEDS to be run after all of the servers in serverFile.txt are up.
e.g. python kvBroker.py -s serverFile.txt -i dataToIndex.txt -k 2
where:
    -s is a space separated list of server IPs and their respective ports that will be listening for queries and indexing commands
    -i is a file containing data that was output from the previous part of the project that was generating the data.
    -k is the replication factor, i.e. how many different servers will have the same replicated data

KV Server
The kv Server needs to start at a specific IP and port from the serverFile.txt and will be serving queries coming from the kv Broker.
e.g. kvServer -a ip_address -p port
