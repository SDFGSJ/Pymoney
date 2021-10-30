import sys

expense_list=[] #a list of (str,int) pair
cost_list=[]    #a list of int
mymoney=0

def read_from_file():   #add return true,false
    global mymoney
    try:
        with open("myrecord.txt",'r') as fh:
            #check if the file is empty
            content=fh.readlines()
            #print("[debug]file content=",content)

            if len(content)==0:
                sys.stderr.write("[Load failed]:myrecord.txt is empty.\n")
                return False

            #return the position to the beginning
            fh.seek(0)
            print("Welcome back!")
            mymoney=int(fh.readline())
            for rec in fh.readlines():
                single_record=rec.split()   #a list of str

                if len(single_record)==2:
                    expense_list.append(tuple(single_record))   #have to convert to tuple so that deletion works
                    cost_list.append(int(single_record[1])) #remember to convert cost to int
                else:
                    sys.stderr.write("failed to parse the record due to unmatched length(it should be 2)\n")

            #print("[debug: in is_file_exist()]expense_list=",expense_list)
            #print("[debug: in is_file_exist()]cost_list=",cost_list)
    except FileNotFoundError:   #first time run this program
        try:
            #user input initial amount of money if first time use
            mymoney = int(input("How much money do you have? "))
        except ValueError:
            sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
            mymoney = 0
    except ValueError:
        sys.stderr.write("can't convert to int when parsing file\n")
        return False
    finally:
        return True

def write_to_file():
    try:
        with open("myrecord.txt",'w') as fh:
            fh.write(str(mymoney))
            fh.write('\n')

            #since rec[1] is 'int',we have to convert to 'str' before join,or we'll get an error
            for rec in expense_list:
                tmp_list=[rec[0], str(rec[1])]
                fh.write(' '.join(tmp_list))
                fh.write('\n')
    except FileNotFoundError:
        sys.stderr.write("[in write_to_file()]: can't found myrecord.txt\n")

def myadd():    #need to check if user enter nothing
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
            return

        record_tuple=tuple(user_input)  #change to tuple to prevent mutation
        #print("[debug]record_tuple=",record_tuple)

        expense_list.append(record_tuple)
        cost_list.append(record_tuple[1])    #add money to cost_list
    except ValueError:
        #print("[debug]user_input=",user_input) #it's a list of str
        sys.stderr.write(f"can't convert the price '{user_input[1]}' to int, the format should be '<description> <price>'\n")

def myview():
    print("Here's your expense and income records:")
    print("=" * 30)
    for record in expense_list:
        #print(record[0],record[1])
        print(f"{record[0]:<20}{record[1]:>10}")   #both record[0],record[1] are strings
    print("=" * 30)
    print(f"Now you have {mymoney + sum(cost_list)} dollars.")   #can pass an iterable to sum()

def mydelete():
    try:
        #user input a record he/she wants to delete(blank-seperated)
        user_input=input("Which record do you want to delete? ").split()
        #print("[debug]user_input=",user_input) #it's a list of str

        #check its length
        if len(user_input)==2:
            #check its content
            user_input[1]=int(user_input[1])    #always convert the price to int
        else:   #invalid length
            sys.stderr.write("invalid input format, should be '<description> <price>'\n")
            return


        delete_record_tuple=tuple(user_input)   #delete_record_tuple: (description('str'), cost('int'))
        #print("[debug]delete_record_tuple=", delete_record_tuple)

        to_be_deleted_list=[]   #record the index to be deleted
        #want to know the index to be deleted,so use enumerate()
        for rec in enumerate(expense_list): #rec is a tuple.(idx, (description('str'), cost('int')))
            #print(rec)
            if delete_record_tuple==rec[1]:
                to_be_deleted_list.append(rec[0])   #append the index to the list
        #print("[debug]to_be_delete_list=",to_be_deleted_list)
        #print("[debug]expense_list=",expense_list)
        #print("[debug]cost_list",cost_list)


        if len(to_be_deleted_list) == 0:  #the record to be deleted doesn't exist in expense_list
            #have to convert delete_record_tuple[1] to 'str' in order to join them together
            tmp_list=[delete_record_tuple[0], str(delete_record_tuple[1])]
            print(f"there's no such record like '{' '.join(tmp_list)}'")
            return False
        elif len(to_be_deleted_list) == 1:  #exactly 1 record matched,simply pop the index
            expense_list.pop(to_be_deleted_list[0])
            cost_list.pop(to_be_deleted_list[0])
            return True #delete success
        else:
            tmp_list=[user_input[0], str(user_input[1])]
            print(f"there are {len(to_be_deleted_list)} records of '{' '.join(tmp_list)}',which one do you want to delete? ")

            #show all the matched content to the user
            for idx in to_be_deleted_list:
                print(f"'{' '.join(tmp_list)}' at index {idx}")

            try:
                idx=int(input("Enter the index to be deleted: "))    #user enter which idx to be deleted

                if idx not in to_be_deleted_list:
                    print("invalid index!")
                    return False    #deletion failed
                else:
                    expense_list.pop(idx)   #simply pop the index
                    cost_list.pop(idx)
                    return True #delete success
            except ValueError:
                sys.stderr.write("the index should be a number. Please try again!\n")
    except ValueError:
        #print("[debug]user_input=",user_input) #it's a list of str
        sys.stderr.write(f"can't convert the price '{user_input[1]}' to int, the format should be '<description> <price>'\n")


#testcase:breakfast -50, lunch -70, dinner -100, salary 3500
if __name__=='__main__':
    isFileGood=read_from_file()    #read the data from myrecord.txt

    if isFileGood:  #myrecord.txt is not empty
        while True:
            operation=input("What do you want to do (add / view / delete / exit) ?")

            if operation=="add":
                myadd()
            elif operation=="view":
                myview()
            elif operation=="delete":
                success=mydelete()
                if success:
                    print("delete success!")
                else:
                    print("delete failed!")
            elif operation=="exit":
                #print("[debug]expense_list=",expense_list)
                #print("[debug]cost_list",cost_list)
                write_to_file() #write the data into myrecord before leaving
                break;
            else:
                print("Invalid command. Try again.")
            
            #print("[debug]expense_list=",expense_list)
            #print("[debug]cost_list",cost_list)