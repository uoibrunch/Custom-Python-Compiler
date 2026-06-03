 ##MARIOS ELLINIDIS 4926##

#int accountBalance
def deposit(amount):
#{
    global accountBalance 
    if amount > 0:
        #{
            accountBalance = accountBalance + amount
            return accountBalance + amount
        #}
    else:
        return -1
    
#}
        
def withdraw(amount):
#{
    global accountBalance
    if amount > 0 and amount <= accountBalance:
        #{
            accountBalance = accountBalance - amount
            print(accountBalance)
        #}
    elif amount > accountBalance:
        return 0
    else:
        return -1   
#}


#def main
#int choice, amount
accountBalance = 0

choice = int(input())
amount = int(input())
if choice == 1:
    print(deposit(amount))
elif choice == 2:
    print(withdraw(amount))
