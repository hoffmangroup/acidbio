import random

write_file = open("bigFile.bed", 'w')

for num in range(1, 23):
    start = 1
    end = 1
    for i in range(115000):
        end += random.randint(5, 20)
        write_file.write("chr"+str(num)+"\t"+str(start)+"\t"+str(end)+"\n")
        start = end

write_file.close()
