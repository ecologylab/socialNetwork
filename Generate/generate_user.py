import sys
import random
import linecache
import simplejson as json

a = range(1,5400)
b = range(1,88700)

while(1):
    if(len(sys.argv) > 1):
        tmp = int(sys.argv[1])
        if tmp > 5000 or tmp < 1:
            print("Please enter value between 1 and 500")
        else:
            n = tmp 
            break
    else:
        print("How many users do you want to generate(Between 1 and 5000)?")

first_pop = random.sample(a,n)
last_pop = random.sample(b,n)

first_names = []
last_names = []
user_data = []
pk_list = range(2,n+2) 

for i in first_pop:
    name = linecache.getline("first_names.txt",i)
    first_names.append(name.strip())

for j in last_pop:
    name = linecache.getline("last_names.txt",j)
    last_names.append(name.strip())

f = open("initial_data.json","w")

def generate_json():
    for first,last,pk in zip(first_names,last_names,pk_list):
        username = '%s_%s' % (first.lower(),last.lower())
        json_list = dict(model="auth.user",pk=pk,fields=dict(username=username,first_name=first,last_name=last,is_active="True",is_superuser="False",
                         is_staff="False",email='%s@example.com' % (username,),password="sha1$58ab4$c80250ca3c0e27ab651ab1f76411ce1418742d25"))  
        user_data.append(json_list)


if __name__ == "__main__":
    generate_json() 

try:    
    json.dump(user_data,f,sort_keys=True, indent=4 * ' ')
    print("Data generation successful!")
except:
    print("Data generation is not completed successfully")
