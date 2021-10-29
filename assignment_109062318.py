expense_list=[]
cost_list=[]

def myadd():
    #user input a record(blank-seperated),change to tuple to prevent mutation
    record_tuple=tuple(input("Add an expense or income record with description and amount:").split())
    expense_list.append(record_tuple)
    cost_list.append(int(record_tuple[1]))    #add money to cost_list(convert to int)
    #print("[debug]expense_list=",expense_list)
    #print("[debug]cost_list",cost_list)

def myview(mymoney):
    print("Here's your expense and income records:")
    print("==================")
    for record in expense_list:
        #print(record[0],record[1])
        print(f"{record[0]:<20}{record[1]:>6}")   #both record[0],record[1] are strings
    print("==================")
    print(f"Now you have {mymoney + sum(cost_list)} dollars.")   #can pass an iterable to sum()

def mydelete():
    delete_record_tuple=tuple(input("Which record do you want to delete?(description cost) ").split())
    #print(delete_record_tuple)
    to_be_deleted_list=[]
    for rec in enumerate(expense_list): #rec is a tuple(idx,(description,cost))
        #print(rec)
        if delete_record_tuple==rec[1]:
            to_be_deleted_list.append(rec)

    #print("to_be_delete_list=",to_be_deleted_list)
    if len(to_be_deleted_list)==0:  #the record to be deleted doesnt exist in expense_list
        print("there's no such record")
        return False
    elif len(to_be_deleted_list)==1:
        expense_list.remove(to_be_deleted_list[0][1])
        cost_list.remove(int(to_be_deleted_list[0][1][1]))
        return True #delete successfully
    else:
        print(f"there are {len(to_be_deleted_list)} records,which one do you want to delete? ")
        idx_list=[]
        for rec in to_be_deleted_list:
            idx_list.append(rec[0])
            print(f"{' '.join(rec[1])} at index {rec[0]}")

        idx=int(input())    #user choose which idx to be deleted

        if idx not in idx_list:
            print("invalid index!")
            return False    #deletion failed
        else:
            expense_list.pop(idx)
            cost_list.remove(int(to_be_deleted_list[idx][1][1]))
            return True #delete successfully


#testcase:breakfast -50, lunch -70, dinner -100, salary 3500
if __name__=='__main__':
    mymoney = int(input("How much money do you have? "))    #user input initial amount of money
    while True:
        operation=input("What do you want to do (add / view / delete / exit) ?")
        if operation=="add":
            myadd()
        elif operation=="view":
            myview(mymoney)
        elif operation=="delete":
            success=mydelete()
            if success:
                print("delete successfully!")
            else:
                print("deletion failed!")
        elif operation=="exit":
            break;
        else:
            print("Unknown operation")