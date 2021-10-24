mymoney = int(input("How much money do you have? "))
print('''Add some expense or income records with description and amount:
desc1 amt1, desc2 amt2, desc3 amt3, ...''')

expense = input().split(', ')   #expense is a list
print("Here's your expense and income records:")
for record in expense:
    print(record)

#parse the record,split every record into name and cost
expense = [record.split() for record in expense]
cost = [int(record[1]) for record in expense]   #record[1] is $
print(expense)
print(cost)
print(f"Now you have {mymoney + sum(cost)} dollars.")   #can pass an iterable to sum()

#testcase:breakfast -50, lunch -70, dinner -100, salary 3500