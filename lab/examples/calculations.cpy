##MARIOS ELLINIDIS 4926##
#int num1, num2 
    
def add(a , b):
#{
    return a + b
#}

def subtract(a , b):
#{
     return a - b
#}

def multiply(a , b):
#{
   return  a * b
#}
    
def divide ( a , b):
#{
    #int i
    def multiply(a , b):
    #{
        def subtract(a , b):
        #{
            return a - b
        #}
        return  a * b
    #}
    if b != 0:
        return a//b
#}
    
#def main
#int addResult, subtractResult, multiplyResult , divideResult
num1 = int(input())
num2 = int(input())
addResult = 0
subtractResult = 0
multiplyResult = 0
if num1 >= num2:
    subtractResult = subtract(num1 , num2)
elif num1 < num2:
    addResult = add(num1, num2)
else: 
    multiplyResult = multiply(num1, num2)

if multiplyResult > 0:
    while multiplyResult > 0:
    #{
        divideResult = divide(multiplyResult , 10)
        multiplyResult = multiplyResult - 1
        print(divideResult)
    #}
print(multiplyResult)
