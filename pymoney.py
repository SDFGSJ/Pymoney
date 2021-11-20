import sys

def initialize_categories():
    return ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]

def read_from_file():
    expenseList=[]
    costList=[]
    try:
        with open("myrecord.txt",'r') as fh:
            #check if the file is empty
            content=fh.readlines()
            #print("[debug]file content=",content)

            if len(content)==0:
                sys.stderr.write("myrecord.txt is empty.\nLoad failed.\n")
                return 0,[],[]  #default values

            #return the position to the beginning
            fh.seek(0)
            try:
                myMoney=int(fh.readline())
            except:
                sys.stderr.write("can't convert mymoney to int,set to 0 by default.\n")

            for rec in fh.readlines():
                single_record=rec.split()   #a list of str
                if len(single_record)==3:
                    try:
                        single_record[2]=int(single_record[2])  #change the price from str to int
                    except:
                        sys.stderr.write("can't convert to int.\n")
                    expenseList.append(tuple(single_record))   #have to convert to tuple so that deletion works
                    costList.append(single_record[2])
                else:
                    sys.stderr.write(f"failed to parse '{' '.join(single_record)}' due to unmatched length(it should be 3)\n")
                    sys.stderr.write(f"'{' '.join(single_record)}' will not be written into your record\n")
            print("Welcome back!")
            #print("[debug: in is_file_exist()]expense_list=",expense_list)
            #print("[debug: in is_file_exist()]cost_list=",cost_list)
    except FileNotFoundError:   #first time run this program
        try:
            #user input initial amount of money if first time use
            myMoney = int(input("How much money do you have? "))
        except ValueError:
            sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
            myMoney = 0
    except ValueError as v:
        sys.stderr.write(str(v))
        return 0,[],[]
    finally:
        return myMoney, expenseList, costList

def write_to_file(myMoney, expenseList):
    try:
        with open("myrecord.txt",'w') as fh:
            fh.write(str(myMoney))
            fh.write('\n')

            #since rec[1] is 'int',we have to convert to 'str' before join,or we'll get an error
            for rec in expenseList:
                tmp_list=[rec[0],rec[1], str(rec[2])]
                fh.write(' '.join(tmp_list))
                fh.write('\n')
    except FileNotFoundError:
        sys.stderr.write("[write to file]: can't found myrecord.txt\n")

def view_categories(categories,level=0):
    if type(categories) in {list,tuple}:
        for child in categories:
            view_categories(child,level+1)
    else:
        print(f"{' '*4*level+'-'}{categories}")

def is_category_valid(category,categories):
    if type(categories) in {list,tuple}:
        for item in categories:
            valid=is_category_valid(category,item)
            if valid:
                return True
    return category==categories

def flatten(l):
    if type(l)==list:
        result=[]
        for child in l:
            result.extend(flatten(child))
        return result
    else:
        return [l]

def find_subcategories(category,categories):
    if type(categories) in {list,tuple}:
        for v in categories:    #v = sublist
            p=find_subcategories(category,v)
            if p==True:
                idx=categories.index(v)
                if idx+1 < len(categories) and type(categories[idx+1])==list:
                    return flatten(categories[idx:idx+2])
                else:   #return itself only if it has no subcategories
                    return [v]
            if p!=[]:
                return p
    return True if category==categories else [] #return [] instead of False if not found

def find(mymoney, records, categories):
    try:
        category_query=input("Which category do you want to find? ")
    except:
        sys.stderr.write("invalid category.\n")
        return
    
    valid=is_category_valid(category_query,categories)
    if not valid:
        print("""The specified category is not in the category list.
You can check the category list by command "view categories".
Fail to add a record.
""")
        return

    query_result=find_subcategories(category_query,categories)
    print("[debug]query_result=",query_result)

    find_result=list(filter(lambda rec:rec[0] in query_result, records))
    tmp_cost_list=[c[2] for c in find_result]   #get the cost of each matched record

    print("[debug]tmp_cost_list=",tmp_cost_list)
    print("[debug]find_result=",find_result)

    print("Here's your expense and income records under category '{category_query}':")
    print(f"{'Category':<20}{'Description':^20}{'Amount':>20}")   #both record[0],[1],[2] are strings
    print("=" * 60)
    for f in find_result:
        print(f"{f[0]:<20}{f[1]:^20}{f[2]:>20}")   #both f[0],[1],[2] are strings
    print("=" * 60)
    print(f"The total amount above is {mymoney + sum(tmp_cost_list)}.")   #can pass an iterable to sum()



def myadd(expenseList, costList, categories):
    try:
        #user input a record (blank-seperated)
        user_input=input("Add an expense or income record with category, description, and amount (separate by spaces):").split()
        #print("[debug]user_input=",user_input) #it's a list of str

        #check its length
        if len(user_input)==3:
            #check its content
            try:
                user_input[2]=int(user_input[2])    #always convert the price to int before appending to cost_list
            except:
                sys.stderr.write("can't convert to int.\n")
        else:   #invalid length
            sys.stderr.write("invalid input format, should be '<category> <description> <price>'\n")
            return expenseList, costList

        #check if the category added by user is valid or not
        valid=is_category_valid(user_input[0],categories)
        if not valid:
            print("""The specified category is not in the category list.
You can check the category list by command "view categories".
Fail to add a record.
""")
            return expenseList, costList


        record_tuple=tuple(user_input)  #change to tuple to prevent mutation
        #print("[debug]record_tuple=",record_tuple)

        expenseList.append(record_tuple)
        costList.append(record_tuple[2])    #add money to costList
    except ValueError as v:
        sys.stderr.write(str(v) + "the format should be '<category> <description> <price>'\n")

    return expenseList, costList

def myview(myMoney, expenseList, costList):
    print("Here's your expense and income records:")
    print(f"{'Category':<20}{'Description':^20}{'Amount':>20}")   #both record[0],[1],[2] are strings
    print("=" * 60)
    for record in expenseList:
        #print(record[0],record[1],record[2])
        print(f"{record[0]:<20}{record[1]:^20}{record[2]:>20}")   #both record[0],[1],[2] are strings
    print("=" * 60)
    print(f"Now you have {myMoney + sum(costList)} dollars.")   #can pass an iterable to sum()

def mydelete(expenseList, costList):
    try:
        #user input a record he/she wants to delete(blank-seperated)
        user_input=input("Which record do you want to delete? ").split()    #it's a list of str
        #print("[debug]user_input=",user_input)

        #check its length
        if len(user_input)==3:
            #check its content
            try:
                user_input[2]=int(user_input[2])    #always convert the price to int
            except:
                sys.stderr.write("can't convert to int.\n")
        else:   #invalid length
            sys.stderr.write("invalid input format, should be '<category> <description> <price>'\n")
            return expenseList, costList


        delete_record_tuple=tuple(user_input)   #delete_record_tuple: (description('str'), cost('int'))
        #print("[debug]delete_record_tuple=", delete_record_tuple)

        to_be_deleted_list=[]   #record the index to be deleted
        #want to know the index to be deleted,so use enumerate()
        for rec in enumerate(expenseList): #rec is a tuple.(idx, (description('str'), cost('int')))
            #print(rec)
            if delete_record_tuple==rec[1]:
                to_be_deleted_list.append(rec[0])   #append the index to the list
        #print("[debug]to_be_delete_list=",to_be_deleted_list)
        #print("[debug]expenseList=",expenseList)
        #print("[debug]costList",costList)


        if len(to_be_deleted_list) == 0:  #the record to be deleted doesn't exist in expenseList
            #have to convert delete_record_tuple[1] to 'str' in order to join them together
            tmp_list=[delete_record_tuple[0], delete_record_tuple[1], str(delete_record_tuple[2])]  #just for output
            sys.stderr.write(f"there's no such record like '{' '.join(tmp_list)}'. delete failed!\n")
        elif len(to_be_deleted_list) == 1:  #exactly 1 record matched,simply pop the index
            expenseList.pop(to_be_deleted_list[0])
            costList.pop(to_be_deleted_list[0])
            sys.stderr.write("delete success!\n")
        else:
            tmp_list=[user_input[0], user_input[1], str(user_input[2])]
            print(f"there are {len(to_be_deleted_list)} records of '{' '.join(tmp_list)}',which one do you want to delete? ")

            #show all the matched content to the user
            for idx in to_be_deleted_list:
                print(f"'{' '.join(tmp_list)}' at index {idx}")

            try:
                idx=int(input("Enter the index to be deleted: "))    #user enter which idx to be deleted

                if idx not in to_be_deleted_list:
                    sys.stderr.write("invalid index! delete failed!\n")
                else:
                    expenseList.pop(idx)   #simply pop the index
                    costList.pop(idx)
                    sys.stderr.write("delete success!\n")
            except ValueError:
                sys.stderr.write("the index should be a number. Please try again!\n")
    except ValueError as v:
        #print("[debug]user_input=",user_input) #it's a list of str
        sys.stderr.write(str(v) + "the format should be '<category> <description> <price>'\n")
    
    return expenseList, costList


#expense_list => a list of (str,int) pair
#cost_list => a list of int
mymoney, expense_list, cost_list=read_from_file()    #read the data from myrecord.txt
categories=initialize_categories()

while True:
    operation=input("What do you want to do (add / view / delete / view categories / find / exit)?")

    if operation=="add":
        expense_list, cost_list = myadd(expense_list, cost_list, categories)
    elif operation=="view":
        myview(mymoney, expense_list, cost_list)
    elif operation=="delete":
        expense_list, cost_list = mydelete(expense_list, cost_list)
    elif operation=="view categories":
        view_categories(categories)
    elif operation=="find":
        find(mymoney, expense_list, categories)
    elif operation=="exit":
        #print("[debug]expense_list=",expense_list)
        #print("[debug]cost_list",cost_list)
        write_to_file(mymoney, expense_list) #write the data into myrecord before leaving
        break
    else:
        sys.stderr.write("Invalid command. Try again.\n")
    
    #print("[debug]expense_list=",expense_list)
    #print("[debug]cost_list",cost_list)