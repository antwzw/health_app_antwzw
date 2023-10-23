# This is a script written by clydechx to generate corresponding data file automatically from the provided file https://eecs485staff.github.io/p2-health-serverside/healthdb-dump.txt
# Run this file under the folder database_data_fetch/.
from collections import defaultdict
f = open("./healthdb-dump.txt", "r")
lines = f.readlines()
i = 0
out = open("out.txt", "w")
dict = {'comments': 4, 'users': 5, "posts": 3, "following": 2, "likes": 3}
field = {'comments': ["commentid", "owner", "postid", "text"], 'users': [
    "username", "fullname", "email", "filename", "password"],
    "posts": ["postid", "filename", "owner"], "following": ["username1", "username2"],
    "likes": ["likeid", "owner", "postid"]}


def insert(tablename):
    res = ""
    res += ("INSERT INTO {}(".format(tablename))
    for i in range(len(field[tablename])):
        if i != len(field[tablename])-1:
            res += (field[tablename][i]+",")
        else:
            res += (field[tablename][i]+")\n")
    outputdict[tablename].append(res)


outputdict = defaultdict(list)
i = 0
while (i < len(lines)):
    line = lines[i]
    tablename = "".join(list(line.split()[-1])[:-1])

    j = i+1
    while (j < len(lines) and lines[j][0] != '+'):
        insert(tablename)
        res = ""
        res += ("VALUES (")
        for incre in range(dict[tablename]):
            this_line = lines[j+incre]
            mylist = list(this_line.split("=")[-1])
            value = "".join(mylist[1:len(mylist)-1])
            if incre != dict[tablename]-1:
                res += ("'{}'".format(value)+",")
            else:
                res += ("'{}'".format(value)+");\n")
        outputdict[tablename].append(res)
        j += dict[tablename]+2
    i = j
# properly insert to avoid violating constrains.
for table in ["users", "posts", "following", "comments", "likes"]:
    for output in outputdict[table]:
        out.write(output)
