# 第一題
print("--task 1--")
def find_and_print(messages):
# write down your judgment rules in comments
    # the parameter is whomever mentioned the following keywords are likely to be at least 17 years old ("18 years old","college student","legal age in Taiwan","vote")
    # if they mentioned they are 18 years old, we assume them to be over 17 (assuming they are not speaking irony) > over 17 years old
    # legal age in Taiwan is 18 years old > over 17 years old
    # if they are able to vote, we assume they are legal age in US, which is 18 years old > over 17 years old
    # most students in college are 18 years old or more > over 17 years old
# your code here, based on your own rules

# Define judgement
    judgement=["18 years old","college student","legal age in Taiwan","vote"]

    for people in messages:
        for match in judgement:
            if match in messages[people]:
                print(people)

find_and_print({
"Bob":"My name is Bob. I'm 18 years old.",
"Mary":"Hello, glad to meet you.",
"Copper":"I'm a college student. Nice to meet you.",
"Leslie":"I am of legal age in Taiwan.",
"Vivian":"I will vote for Donald Trump next week",
"Jenny":"Good morning."
})

# 第二題
print("--task 2--")
def calculate_sum_of_bonus(data):
# write down your bonus rules in comments
    # Role: engineer: salary x 104%; CEO: x 109%; sales: x 106%
    # Performance: above average: salary x 113%; average: remain unchange; below average: x 90%
# your code here, based on your own rules

# 先把所有individual的資料抽出來
    for array in data:
        detail=data[array]
        # print(detail)

# 把每個人的dict拆出來獨立跑裏面的程式,把salary的貨幣和格式定好
    for profile in detail:
        num_string=str(profile["salary"])
        if "," in num_string:
            num_string=num_string.replace(",","")
        profile["salary"]=num_string

        if "USD" in num_string:
           TWD=int(num_string[slice(0,-3)])
           num_string=TWD*30
        # print(TWD)
        profile["salary"]=int(num_string)
        # print(profile["salary"])
    # print(detail)

# 算出原本salary的總和
    original=[]
    for pre in detail:
        original.append(int(pre["salary"]))

    og_salary=0
    for salary in original:
        og_salary+=salary

# 根據不同role制定salary
    for indi_role in detail:
        if indi_role["role"] == "Engineer":
            indi_role["salary"]=indi_role["salary"]*1.04
        
        elif indi_role["role"] == "CEO":
            indi_role["salary"]=indi_role["salary"]*1.09

        elif indi_role["role"] == "Sales":
            indi_role["salary"]=indi_role["salary"]*1.06

# 根據不同performance制定salary
    for confirmed_salary in detail:
        if "above" in confirmed_salary["performance"]:
            confirmed_salary["salary"]=confirmed_salary["salary"]*1.13

        elif "below" in confirmed_salary["performance"]:
            confirmed_salary["salary"]=confirmed_salary["salary"]*0.9

# 算出連bonus的salary總和
    total=[]
    for plus in detail:
        total.append(int(plus["salary"]))

    with_bonus_salary=0
    for bonus in total:
        with_bonus_salary+=bonus

# 算出今個月bonus的總數
    bonus_of_the_month=with_bonus_salary - og_salary 
    print(int(bonus_of_the_month))

calculate_sum_of_bonus({
"employees":[
{
"name":"John",
"salary":"1000USD",
"performance":"above average",
"role":"Engineer"
},
{
"name":"Bob",
"salary":60000,
"performance":"average",
"role":"CEO"
},
{
"name":"Jenny",
"salary":"50,000",
"performance":"below average",
"role":"Sales"
}
]
}) # call calculate_sum_of_bonus function


# 第三題
print("--task 3--")
def func(*data):
# your code here
    # 抽出列表裏所有的中間字
    middle_name={}
    for name in data:
        name=name[1]
        if name in middle_name:
            middle_name[name]+=1
        else:
            middle_name[name]=1
    # 查看中間字有沒有和其他人重複

    confirm=[]
    for i in middle_name:
        if middle_name[i]==1:
            confirm.append(i)
    
    if len(confirm)==0:
        print("沒有")
        return

    # 如果中間字對上就print
    for full in data:
        if full[1] in confirm:
            print(full)

func("彭⼤牆", "王明雅", "吳明") # print 彭⼤牆
func("郭靜雅", "王立強", "林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有

# 第四題
print("--task 4--")
def get_number(index):
# your code here
   
    arr=[0,4,3]
    if index<3:
        print(arr[index])
        return

    x=3
    for x in range(3,index+1):
        get = arr[x-1] + arr[x-2] - arr[x-3]
        arr.append(get)
    print(get)


get_number(1) # print 4
get_number(5) # print 10
get_number(10) # print 15