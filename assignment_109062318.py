import sys

def read_from_file():
    expenseList=[]
    costList=[]
    try:
        with open("myrecord.txt",'r') as fh:
            #check if the file is empty
            content=fh.readlines()
            #print("[debug]file content=",content)

            if len(content)==0:
                sys.stderr.write("[Load failed]:myrecord.txt is empty.\n")
                return 0,[],[]  #default values

            #return the position to the beginning
            fh.seek(0)
            print("Welcome back!")
            myMoney=int(fh.readline())
            for rec in fh.readlines():
                single_record=rec.split()   #a list of str
                single_record[1]=int(single_record[1])  #change the price from str to int

                if len(single_record)==2:
                    expenseList.append(tuple(single_record))   #have to convert to tuple so that deletion works
                    costList.append(single_record[1])
                else:
                    sys.stderr.write("failed to parse the record due to unmatched length(it should be 2)\n")

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
        #sys.stderr.write("can't convert to int when parsing file\n")
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
                tmp_list=[rec[0], str(rec[1])]
                fh.write(' '.join(tmp_list))
                fh.write('\n')
    except FileNotFoundError:
        sys.stderr.write("[in write_to_file()]: can't found myrecord.txt\n")

def myadd(expenseList, costList):
    try:
        #user input a record (blank-seperated)
        user_input=input("Add an expense or income record with description and amount:").split()
        #print("[debug]user_input=",user_input) #it's a list of str

        #check its length
        if len(user_input)==2:
            #check its content
            user_input[1]=int(user_input[1])    #always convert the price to int before appending to cost_list
        else:   #invalid length
            sys.stderr.write("invalid input format, should be '<description> <price>'\n")
            return expenseList, costList

        record_tuple=tuple(user_input)  #change to tuple to prevent mutation
        #print("[debug]record_tuple=",record_tuple)

        expenseList.append(record_tuple)
        costList.append(record_tuple[1])    #add money to costList
    except ValueError:
        #print("[debug]user_input=",user_input) #it's a list of str
        sys.stderr.write(f"can't convert the price '{user_input[1]}' to int, the format should be '<description> <price>'\n")

    return expenseList, costList

def myview(myMoney, expenseList, costList):
    print("Here's your expense and income records:")
    print("=" * 30)
    for record in expenseList:
        #print(record[0],record[1])
        print(f"{record[0]:<20}{record[1]:>10}")   #both record[0],record[1] are strings
    print("=" * 30)
    print(f"Now you have {myMoney + sum(costList)} dollars.")   #can pass an iterable to sum()

def mydelete(expenseList, costList):
    try:
        #user input a record he/she wants to delete(blank-seperated)
        user_input=input("Which record do you want to delete? ").split()    #it's a list of str
        #print("[debug]user_input=",user_input)

        #check its length
        if len(user_input)==2:
            #check its content
            user_input[1]=int(user_input[1])    #always convert the price to int
        else:   #invalid length
            sys.stderr.write("invalid input format, should be '<description> <price>'\n")
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
            tmp_list=[delete_record_tuple[0], str(delete_record_tuple[1])]  #just for output
            sys.stderr.write(f"there's no such record like '{' '.join(tmp_list)}'. delete failed!\n")
        elif len(to_be_deleted_list) == 1:  #exactly 1 record matched,simply pop the index
            expenseList.pop(to_be_deleted_list[0])
            costList.pop(to_be_deleted_list[0])
            sys.stderr.write("delete success!\n")
        else:
            tmp_list=[user_input[0], str(user_input[1])]
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
    except ValueError:
        #print("[debug]user_input=",user_input) #it's a list of str
        sys.stderr.write(f"can't convert the price '{user_input[1]}' to int, the format should be '<description> <price>'\n")
    
    return expenseList, costList

#testcase:breakfast -50, lunch -70, dinner -100, salary 3500
#expense_list => a list of (str,int) pair
#cost_list => a list of int
mymoney, expense_list, cost_list=read_from_file()    #read the data from myrecord.txt

while True:
    operation=input("What do you want to do (add / view / delete / exit) ?")

    if operation=="add":
        expense_list, cost_list = myadd(expense_list, cost_list)
    elif operation=="view":
        myview(mymoney, expense_list, cost_list)
    elif operation=="delete":
        expense_list, cost_list = mydelete(expense_list, cost_list)
    elif operation=="exit":
        #print("[debug]expense_list=",expense_list)
        #print("[debug]cost_list",cost_list)
        write_to_file(mymoney, expense_list) #write the data into myrecord before leaving
        break
    else:
        sys.stderr.write("Invalid command. Try again.\n")
    
    #print("[debug]expense_list=",expense_list)
    #print("[debug]cost_list",cost_list)