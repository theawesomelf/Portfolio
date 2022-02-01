import pymongo
from pymongo import MongoClient
import pprint

client = MongoClient()

db = client.db_people
peeps = db.thePeople

# #Question1
# count=0
# for peep in peeps.find({"numChildren":7}):
#     print(peep)
#     count+=1
# print(count," objects found")

# #Question2
# count=0
# for peep in peeps.find({"numChildren":7},{"pid":1,"state":1,"children":1,"_id":0}):
#     print(peep)
#     count+=1
# print(count," objects found")

# #Question3
# count=0
# for peep in peeps.find({"numChildren":6,"state":"CA"}):
#     print(peep)
#     count+=1
# print(count," objects found")

#Question4
print("\nPrinting results for Question 4\n")
count=0
for peep in peeps.find({"numChildren":{ "$in": [6,7]},"state":"CA"}):
    print(peep)
    count+=1
print(count," objects found")

#Question5
print("\nPrinting results for Question 5\n")
count=0
for peep in peeps.find({"children":{ "$regex": "Bob A"}},{"_id":0,"pid":1,"children":1}):
    print(peep)
    count+=1
print(count," objects found")

# #Question6
# count=0
# for peep in peeps.aggregate([{"$group":{"_id":"$numChildren","numInGroup":{"$sum":1}}},{"$sort":{"_id":1}}]):
#     print(peep)
#     count+=1
# print(count," objects found")

# #Question7
# count=0
# for peep in peeps.aggregate([{"$group":{"_id":"$state","avgSalary":{"$avg":"$salary"},"numInGroup":{"$sum":1}}},{"$sort":{"_id":1}}]):
#     print(peep)
#     count+=1
# print(count," objects found")

# #Question8
# count=0
# for peep in peeps.aggregate([{"$match":{"state":"WA"}},{"$group":{"_id":"$state","avgSalary":{"$avg":"$salary"},"numInGroup":{"$sum":1}}},{"$sort":{"_id":1}}]):
#     print(peep)
#     count+=1
# print(count," objects found")

print("\nPrinting results for Question 9\n")
#Question9
count=0
for peep in peeps.aggregate([{"$match":{"state":{"$in":["ND","SD","NE","KS","MN","IA","MS","WI","IL","IN","MI","OH"]}}},{"$group":{"_id":"$state","avgSalary":{"$avg":"$salary"},"minSalary":{"$min":"$salary"},"maxSalary":{"$max":"$salary"},"numInGroup":{"$sum":1}}},{"$sort":{"_id":1}}]):
    print(peep)
    count+=1
print(count," objects found")

#Question10
print("\nPrinting results for Question 10\n")
count=0
for peep in peeps.aggregate([{"$group":{"_id":"$state","avgSalary":{"$avg":"$salary"},"numInGroup":{"$sum":1}}},{"$match":{"avgSalary":{"$gte":82000}}},{"$sort":{"_id":1}}]):
    print(peep)
    count+=1
print(count," objects found")

#Question11
print("\nPrinting results for Question 11\n")
count=0
for peep in peeps.aggregate([{"$match":{"state":{"$in":["ND","SD","NE","KS","MN","IA","MS","WI","IL","IN","MI","OH"]}}},{"$group":{"_id":"$state","avgSalary":{"$avg":"$salary"},"minSalary":{"$min":"$salary"},"maxSalary":{"$max":"$salary"},"numInGroup":{"$sum":1}}},{"$match":{"avgSalary":{"$gte":82000}}},{"$sort":{"_id":1}}]):
    print(peep)
    count+=1
print(count," objects found")

#PART2
print("\n\nPrinting results for Part 2\n")

print("\nPrinting results for update_one\n")
query={"pid":1425}
change={"$set":{"age":105}}
for peep in peeps.find(query,{"_id":0,"pid":1,"firstName":1,"lastName":1,"age":1,"birth":1}):
    print(peep)
print("\nUpdating...\n")
peeps.update_one(query,change)
for peep in peeps.find(query,{"_id":0,"pid":1,"firstName":1,"lastName":1,"age":1,"birth":1}):
    print(peep)

print("\nPrinting results for update_many\n")
query={"state":"NM","lastName":{"$in":["Brown","Takahashi","Wu"]}}
change={"$inc":{"salary":10000}}
for peep in peeps.find(query,{"_id":0,"pid":1,"firstName":1,"lastName":1,"age":1,"birth":1,"state":1,"salary":1}):
    print(peep)
print("\nUpdating...\n")
peeps.update_many(query,change)
for peep in peeps.find(query,{"_id":0,"pid":1,"firstName":1,"lastName":1,"age":1,"birth":1,"state":1,"salary":1}):
    print(peep)

print("\nPrinting results for delete_many\n")
query={"numChildren":0,"age":{"$gt":45}}
for peep in peeps.find(query,{"_id":0,"pid":1,"firstName":1,"lastName":1,"age":1,"numChildren":1,"birth":1,"state":1}):
    print(peep)
print("\nDeleting...\n")
peeps.delete_many(query)
for peep in peeps.find(query,{"_id":0,"pid":1,"firstName":1,"lastName":1,"age":1,"numChildren":1,"birth":1,"state":1}):
    print(peep)
