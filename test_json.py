import json

my_dict = [{"username": "XYZ", "email": "xyz@gmail.com", "location":"Washington", "test":{"t":"d", "w":"w"},"name":[{"f":"1", "s":"2"}, {"t":"3"}]}, 
           {"username": "ABC", "email": "xyz@gmail.com", "location":"Washington", "test":{"t":"d", "w":"w"},"name":[{"f":"1", "s":"2"}, {"t":"3"}]}]
my_list = [{"k":"k"}, {"w":"w"}]
sub=[]
sub.append(my_list[0])
#my_dict["name"]=sub
#print(my_dict)
#print(my_dict["name"][0]["k"])
#print(my_dict["test"]["t"])
print(my_dict[0]["username"])

# with open('test.json', 'w+') as json_file:
#     json.dump(my_dict, json_file)
#     print("create")