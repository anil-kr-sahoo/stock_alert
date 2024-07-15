# name= input("enter name: ")
# age= int(input("enter age: "))
# mark= float(input("mark: "))
# print("welcome", name)
# print("age", age)
# print("mark", mark)


# first= int(input("enter first= "))
# second= int(input("enter second= "))
# print("sum= ", first+second)

# first= float(input("enter first= "))
# second= float(input("enter second= "))
# print("sum= ", first+second)

# side= int(input("side of the square= "))
# print("area of the square= ",side*side)
# side= float(input("side of the square= "))
# print("area of the square= ", side**2)
#
# a= float(input("enter first= "))
# b= float(input("enter second= "))
# print("average= ", (a+b)/2)

# a= int(input("enter first= "))
# b= int(input("enter second= "))
# print(a>=b)
# string1="my name is suchitra pani.\nanil kumar sahoo is my husband"
# print(string1)
# string2="i love you jerry.\nAlso hate you more."
# print(string2)

# name= input("enter your name= ")
# print("length of you name is= ",len(name))
# name= input("enter your name= ")
# print("length of your name= ",len(name))
# name=input("enter your name= ")
# print("length of your name= ", len(name))

# str= "hi am $.i have so many $"
# print(str.count("$"))
# str1= "hellow $.how are you $"
# print(str1.count("$"))

# num= int(input("enter the number= "))
# rem= num % 2
# if(rem==0):
#      print("num is even")
# else :
#      print("num is odd")
# num= int(input("enter the num= "))
# rem= num % 2
# if(rem==0):
#      print("even")
# else:
#      print("odd")

list
# marks=[90.7,78.6,46.8,86.7,95.3]
# print(marks)
# print(type(marks))
# print(marks[0])
# print(marks[3])
# print(marks[4])

# student=["suchitra",85.7,25,"delh["suchitra",85.7,25,"delhi"]
# print(student)
# print(student[0])
# print(student[2])
# print(student[5])
# student=["suchitra",85.7,25,"delhi"]
# print(student[0])
# student[0]= "anil"
# print(student)

# movies = []
# movies.append(input("enter the first movie= "))
# movies.append(input("enter the second movie= "))
# movies.append(input("enter the third movie= "))
# print(movies)

# grade =["c","d","a","a","b","b","a"]
# grade1= grade.count("a")
# print(grade1)

# grade  =["c","d","a","a","b","b","a"]
# grade.sort()
# print(grade)

# class_0=["a","s","a","d","b","c"]
# class_0.sort()
# print(class_0)
# dictionary
# info = {
#     "keys": "values",
#     "name": "suchitra",
#     "topics": ("dict", "set"),
#     "age": 34,
#     "subjects": ["python", "c+", "zava"],
#     "marks": 89.6,
#     34: 55.90}
# info["name"] = "sradhanjali"
# print(info)
# info["topics"]=("phy","chem","math")
# print(info)
# info.update({"city":"cuttack",})
# print(info)
# # nested dictionary
# students={
#      "name":"ramnarayan sahoo",
#      "marks":{
#          "phy":98,
#          "chem":78.5,
#          "math":67,}
# }
# print(students["marks"]["chem"])
# print(len(list(students.keys())))
# print(list(students.values()))
# print(list(students.items()))
# print(students.get("name"))
# students.update({"area":"delhi",})
# print(students)
# info={
#     "name":"ram pani",
#     "area":"delhi",
#     "marks":{
#         "phy":88.7,
#         "chem":65.8,
#         "math":98,
#
#     }
# }
# print(len(list(info)))
# print(info.get("marks"))
# info.update({"age":25,})
# print(info)
# collection={1,2,3,4,5,4,4,4,6,}
# print(type(collection))
# set={"hello","world","apnacollege","python"}
# print(set.pop())
# print(set.pop())
# collection=set()
# collection.add(1)
# collection.add(("college"))
# collection.add("python")
# print(collection)
# set1={1,2,3}
# set2={2,3,4,5,6}
# print(set1.union(set2))
# print(set1.intersection(set2))
# problem
# dictionary={
#     "table": ["a piece of forniture","list of facts and figure"],
#     "cat": "a small animal",
# }
# print(dictionary)
# classroom={"python","python","python","java","java","java","c++","c","javascripy"}
# print(len(classroom))
# dictionary={}
# x=int(input("enter phy= "))
# dictionary.update({"phy": x,})
# y=int(input("enter chem= "))
# dictionary.update({"chem": y,})
# z=int(input("enter math= "))
# dictionary.update({"math": z,})
# print(dictionary)
# values={9,"9.0",8.5}
# print(values)

# Create a list having following order from given string
#[date, info, credit/debit, time]
test = "15/7/24 12:01 - 20 Coins Credited as Welcome bonus"
x= test.split("-")
print(x[1].lower())