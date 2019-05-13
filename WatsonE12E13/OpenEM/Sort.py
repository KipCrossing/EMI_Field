 
f_openEM = open("results13.csv", "r")
f_output = open("OpenEM_output.csv","w")
print("Yes")

for line in f_openEM:
    if line.split(",")[1]:
        f_output.write(line)


f_openEM.close()
f_output.close()