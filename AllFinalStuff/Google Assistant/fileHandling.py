import  json
# Program to show various ways to read and
# write data in a file.
dict = {"USERNAME":"SOURABH"}
file1 = open("myfile.txt", "w")
file1.write(str(dict))
file1.close()  # to change file access modes

file1 = open("myfile.txt", "r+")
string_value = file1.read()
dict = eval(string_value)
if "USERNAME" in dict:
    print (dict["USERNAME"])
