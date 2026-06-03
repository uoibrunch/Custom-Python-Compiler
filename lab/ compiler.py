#MARIOS ELLINIDIS 4926


import re
class Token:
    def __init__(self , recognized_string , family , line_number):
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number

class LexError(Exception):
    pass

class Lex:
    keywords = ["main", "def" , "#def" , "#int" , "global" , "if" , "elif", "else" , "while" , "print" , "return" , "input" , "int" , "and" , "or" , "not"]

    states = { 0 : { "space"   :   0    , "letter"  :   1   , "digit"     :   2   , "operators" :   400   ,  "mulOperator" : 500 , "slash" : 5 , "smaller" : 6 , "larger" : 7 , "equal" : 8 , "mark" : 9 , "delimiter" : 900 , "groupSymbol" : 1000 , "sharp" : 12 , "other" : 101 , "EOF" : 0 },
            1 : { "letter"  :   1    ,  "digit"  :   1   , "other"     : 200 } ,
            2 : { "digit"   :   2    , "letter"  : 102   , "other"     : 300 } ,
            3 : { "digit"   :   2    ,  "other"  : 400 } ,
            5 : { "slash"   : 500    ,  "other"  : 109 } ,
            6 : { "equal"   : 700    ,  "other"  : 600 } ,
            7 : { "equal"   : 700    ,  "other"  : 600 } ,
            8 : { "equal"   : 700    ,  "other"  : 800 } ,
            9 : { "equal"   : 700    ,  "other"  : 103 } ,
            10 : { "letter"  :  10    ,  "other"  : 1200 } ,
            11 : { "other"  : 1000 }  , 
            12 : { "brace"   : 1000   ,   "sharp" : 13    ,     "letter" : 10      ,    "other" : 104  ,          "EOF" : 105} ,
            13 : { "other"   : 13     ,   "sharp" : 14    ,        "EOF" : 106}   ,
            14 : { "other"   : 13     ,   "sharp" : 1100  ,        "EOF" : 107},
            }
    
    Error_types = { 101 , 102 , 103 , 104 , 105 , 106 , 107 , 108 , 109}

    final_states = { 100 : "ERROR",
                    200 : "IDENTIFIER", 
                    300 : "NUMBER",
                    400 : "addOperator",
                    500 : "mulOperator",
                    600 : "relOperator",
                    700 : "doublerelOperator",
                    800 : "assignOperator",
                    900 : "delimiter",
                    1000 : "groupSymbol",
                    1100 : "COMMENT",
                    1200 : "possibleKeyword",
                    1300 : "KEYWORD"
                    }
    
    def __init__(self , file_name): 
        if not file_name.endswith(".cpy"):
            raise ValueError("Only .cpy files are supported. \n")
        self.file_name = file_name
        self.line_number = 1
        self.current_token = None
        self.source_code = None
        self.index = 0
        self.lastToken = "" 
    
    def _error(self , message , type):
        error_message = ""
        match type:
            case 100:
                error_message = "An illegal symbol was found: '"+message + "' in Line: " ,self.line_number
            case 101:
                error_message = "Cant read word: '"+message+"' in Line: " ,self.line_number
            case 102:
                error_message ="Illegal expression '"+message+"' in Line: " ,self.line_number,"Digit expected"
            case 103:
                error_message = "Illegal expression '"+message+"' in Line: " ,self.line_number,"Did you mean '!=' ?"
            case 104:
                error_message = "Illegal expression '"+message+"' in Line: " ,self.line_number,"\n\nWrong expression following '#' symbol\n"
            case 105:
                error_message = "Illegal expression '"+message+"' in Line: " ,self.line_number,"EOF"
            case 106:
                error_message = "Illegal expression '"+message+"' in Line: " ,self.line_number,"EOF , if your intention was to comment add '##' at the end of your comment"
            case 107:
                error_message = "Illegal expression '"+message+"' in Line: " ,self.line_number,"EOF , if your intention was to comment use '##' at the end of your comment"
            case 109:
                error_message = "Illegal expression '"+message+"' in Line: " ,self.line_number,"Did you mean '//' ?"
            case 110:
                error_message = "Illegal expression '"+message+"' in Line: " ,self.line_number,"\n\nIdentifier detected more than 30 characters, please reduce the number of characters"
            case 111:
                error_message = "Illegal expression '"+message+"' in Line: " ,self.line_number,"Supported numbers are between 32767 and -32767"
        raise LexError(error_message)

    def next_token(self):
        return_type = False
        with open(self.file_name, "r" , encoding="utf-8") as file:#delete encoding if necessary
                self.source_code = file.read()
                while self.index < len(self.source_code):
                    recognized_string = ""
                    current_state = 0
                    while current_state not in self.final_states and self.index < len(self.source_code):
                        char = self.source_code[self.index]
                        if self.index == len(self.source_code) - 1 and recognized_string!="":
                            category = "EOF"
                        elif char.isspace() and current_state == 0:
                            category = "space"
                            if char == '\n':
                                self.line_number +=1
                            self.index += 1
                            continue
                        elif char.isalpha():
                            category = "letter"
                        elif char.isdigit():
                            category = "digit"
                        elif char == "+" or char == "-":
                            category = "operators"
                        elif char == "*" or char == "%":
                            category = "mulOperator"
                        elif char == "/":
                            category = "slash"
                        elif char == "<":
                            category = "smaller"
                        elif char == ">":
                            category = "larger"
                        elif char == "=":
                            category = "equal"
                        elif char == "!":
                            category = "mark"
                        elif char == "," or char == ":":
                            category = "delimiter"
                        elif char == "(" or char == ")":
                            category = "groupSymbol"
                        elif char == "#":
                            category = "sharp"
                        elif char == "{" or char == "}":
                            category = "brace"
                            recognized_string += char
                        else: 
                            category = "other"
                            if not char.isspace(): #propably illegal symbol
                                category = "error"
                                recognized_string += char
                                self._error(recognized_string , 100)
                        if  current_state == 13 or current_state == 14: #check if comment is completed
                            if category != "sharp":
                                if category != "EOF":
                                    category = "other"
                                    current_state = self.states[current_state][category]
                        if category in self.states [current_state]: 
                            current_state = self.states[current_state][category]
                        elif category == "error":
                            current_state = 100
                        else:
                            category = "other"
                            if  current_state == 13 or current_state == 14: #adopt to the last character
                                self.index+=1
                            current_state = self.states[current_state][category]
                            self.index-=1 #repeat letter
                        if current_state in self.Error_types:#error detected , send a message
                                recognized_string += char
                                self._error(recognized_string , current_state)
                                current_state = 100   
                        self.index+=1
                        if current_state == 3: #if there was letter before its propably an operation and not digit
                            if self.lastToken == "IDENTIFIER":
                                category = "other"
                                current_state = self.states[current_state][category]
                                recognized_string += char      
                        if current_state == 700 or current_state == 500 or current_state == 900: #just accept and move on 
                            recognized_string += char

                        if current_state == 200: #check if more than 30 characters
                            if len(recognized_string) > 30:
                                self._error(recognized_string ,110)
                                current_state = 100

                        if current_state == 300: #check if its within the accepted numbers
                            if int(recognized_string) > 32767 or int(recognized_string) < -32767:
                                self._error(recognized_string ,111)
                                current_state = 100
                        if current_state == 1100:
                            current_state = 0
                            recognized_string = ""
                            continue
                        if current_state == 400:
                            recognized_string += char

                        if current_state == 200: #check if its keyword
                            if recognized_string in self.keywords:
                                current_state = 1300
                        
                        if current_state == 1200: #check if the word after # is an actual keyword 
                            if recognized_string in self.keywords:
                                current_state = 1300
                            else:
                                self._error(recognized_string, 104)
                                current_state = 100
                            
                        if current_state == 1000 and recognized_string == "":#imediate accept if the groupsymbol is complete
                            recognized_string += char

                        if current_state in self.final_states:
                            self.lastToken = self.final_states[current_state]
                            family = self.lastToken
                            self.current_token = Token(recognized_string, family , self.line_number)
                            return_type = True
                        if char == '\n':
                            self.line_number +=1
                        recognized_string += char
                        if return_type:
                            return self.current_token             
        return None

#===================================Syntax Analyzer=========================================
class SyntaxError(Exception):
    pass
    
class SyntaxAnalyzer:

    
    def match_type(self, expected_type):
        
        if self.current_token.family == expected_type:
            line_number = self.current_token.line_number
            #print("Expected type : '"+expected_type+ "' was succefull in line :" , self.current_token.line_number," \n")
            self.current_token = self.lexer.next_token()
            #print("next token ",  self.current_token.recognized_string)
            if self.current_token == None:
                recognized_string = ""
                family = "EOF"
                self.current_token = Token(recognized_string, family , line_number)
        else:
            found_type = self.current_token.family
            if expected_type == 'IDENTIFIER':
                expected_type = 'a statement'
            line_number = self.current_token.line_number
            word_found = self.current_token.recognized_string
            self._error(f"Expected {expected_type} but found {found_type} '{word_found}' in line: {line_number}\n")
    def match_word(self, expected_word):
        if self.current_token.recognized_string == expected_word:
            line_number = self.current_token.line_number
            #print("Expected word : '"+expected_word+ "' was succefull in line : ",self.current_token.line_number," \n")
            self.current_token = self.lexer.next_token()
            #print("next token ",  self.current_token.recognized_string)
            if self.current_token == None:
                recognized_string = ""
                family = "EOF"
                self.current_token = Token(recognized_string, family , line_number)
        else:
            if(expected_word == '#def'):
                print("\nmain is missing\n")
            found_word = self.current_token.recognized_string
            line_number  = self.current_token.line_number
            self._error(f"Expected '{expected_word}' but found '{found_word}' in line: {line_number}\n")

    def _error(self, message):
        raise  SyntaxError(f"\nSyntax error: {message}\n")
    
    def __init__(self , lexer , intermediate_code, symbol_table , final_code):
        self.lexer = lexer
        self.current_token = None
        self.intermediate_code = intermediate_code
        self.symbol_table = symbol_table
        self.scope = None
        self.final_code = final_code
        self.not_actiavated = False

    def parse(self):
        try:
            self.current_token = self.lexer.next_token()
            self.startRule()
        except LexError as lex_error:
            print("\n"+ str(lex_error))
        except SyntaxError as syntax_error:
            print("\n" + str(syntax_error))

    def startRule(self):
        self.final_code.produce("\t.data")
        self.final_code.produce('str_nl:.asciz "\\n"')
        self.final_code.produce("\t.text")
        self.final_code.produce("LO:")
        self.final_code.produce("\tj Lmain")
        self.main_part()
        self.final_code.produce("Lmain:")
        self.call_main_part()
        
    
    def main_part(self):
        Variables = []
        new_scope = Scope()
        self.scope = new_scope
        self.symbol_table.add_Scope(new_scope)
        Variables = self.declarations()
        for variable in Variables:
                entity = Variable(variable,"integer",new_scope.get_nextOffset())
                new_scope.add_Entity(entity)

        while self.current_token.recognized_string == 'def':
            self.scope= new_scope
            self.function()
            self.symbol_table.print_table()
            self.symbol_table.pop_scope()
            self.symbol_table.print_table()
        self.scope = new_scope

    def call_main_part(self):
        self.match_word('#def')
        name_of_function = self.current_token.recognized_string
        self.match_word('main')
        self.intermediate_code.begin_block(name_of_function)
        Variables = self.declarations()
        for variable in Variables:
                entity = Variable(variable,"integer",self.scope.get_nextOffset())
                self.scope.add_Entity(entity)
        self.main_statements()
        self.symbol_table.print_table()
        self.intermediate_code.halt()
        self.intermediate_code.end_block(name_of_function)
        self.final_code.transform_intermediate(name_of_function)

        
    def main_statements(self):
        while self.current_token.family != "EOF":
            if self.current_token.recognized_string == '#{':
                self.match_word('#{')
                self.statements()
                self.match_word('#}')
            self.statement()
        print("\ncompilation succefully completed")

    def function(self):
        Parameters = []
        Variables = []
        self.match_word('def')
        name_of_function = self.current_token.recognized_string
        
        function_entity = Function(name_of_function, "integer", None , None , None)
        self.scope.add_Entity(function_entity)
        self.symbol_table.print_table()

        new_scope = Scope()
        self.scope = new_scope
        self.symbol_table.add_Scope(new_scope)

        self.match_type('IDENTIFIER')
        self.match_word('(')
        Parameters = self.id_list()
        
        entities = []
        for parameter in Parameters:
       
            entity = FormalParameter(parameter,"integer","cv")
            entities.append(entity)

            entity = Parameter(parameter , "integer" , "cv" ,self.scope.get_nextOffset() )
            self.scope.add_Entity(entity)
        
        function_entity.add_formalParameters(entities)

        self.match_word(')')
        self.match_word(':')
        self.match_word("#{")
        Variables= self.declarations()

        for variable in Variables:
            entity = Variable(variable,"integer",self.scope.get_nextOffset())
            self.scope.add_Entity(entity)

        while self.current_token.recognized_string == 'def':
            self.function()
            
            self.symbol_table.print_table()
            self.symbol_table.pop_scope()
            self.symbol_table.print_table()
                
        label = self.intermediate_code.begin_block(name_of_function)
        label = int(label)
        label += 1
        function_entity.update_startingQuad(label)

        self.scope = new_scope
        self.declarations()
        if(self.current_token.recognized_string == '#}'):
            self._error(f" You should have at least one statement in Block , Line: {self.current_token.line_number}")
        
        self.statements()
        self.match_word("#}")
        framelength = len(self.scope.entities)*4
        function_entity.update_framelength(framelength)
        self.intermediate_code.end_block(name_of_function)
        self.final_code.transform_intermediate(name_of_function)
    
    def if_stat(self):
        Results = [None, None, None] 
        self.match_word('if')
        breaklist = self.intermediate_code.emptyList()
        Results = self.condition()
        Btrue = Results[1]
        Bfalse = Results[2]
        self.match_word(":")
        if self.current_token.recognized_string == '#{':
            self.intermediate_code.backpatch(Btrue , self.intermediate_code.nextQuad())
            self.match_word('#{')
            self.statements()
            ifList= self.intermediate_code.makeList(self.intermediate_code.nextQuad())
            self.intermediate_code.gen_quad("jump" , "_" , "_" , "_")
            breaklist=self.intermediate_code.mergeList(breaklist , ifList)
            self.intermediate_code.backpatch(Bfalse , self.intermediate_code.nextQuad())
            self.match_word('#}')
        else:
            self.intermediate_code.backpatch(Btrue , self.intermediate_code.nextQuad())
            self.statement()
            ifList= self.intermediate_code.makeList(self.intermediate_code.nextQuad())
            self.intermediate_code.gen_quad("jump" , "_" , "_" , "_")
            breaklist=self.intermediate_code.mergeList(breaklist , ifList)
            self.intermediate_code.backpatch(Bfalse , self.intermediate_code.nextQuad())
        if  self.current_token.recognized_string == 'elif':
            self.match_word('elif')
            Results = self.condition()
            Btrue = Results[1]
            Bfalse = Results[2]
            self.match_word(":")
            if self.current_token.recognized_string == '#{':
                self.match_word('#{')
                self.intermediate_code.backpatch(Btrue , self.intermediate_code.nextQuad())
                self.statemets()
                ifList= self.intermediate_code.makeList(self.intermediate_code.nextQuad())
                self.intermediate_code.gen_quad("jump" , "_" , "_" , "_")
                breaklist=self.intermediate_code.mergeList(breaklist , ifList)
                self.intermediate_code.backpatch(Bfalse , self.intermediate_code.nextQuad())
                self.match_word('#}')
            else:
                self.intermediate_code.backpatch(Btrue , self.intermediate_code.nextQuad())
                self.statement()
                ifList= self.intermediate_code.makeList(self.intermediate_code.nextQuad())
                self.intermediate_code.gen_quad("jump" , "_" , "_" , "_")
                breaklist=self.intermediate_code.mergeList(breaklist , ifList)
                self.intermediate_code.backpatch(Bfalse , self.intermediate_code.nextQuad())
            while self.current_token.recognized_string == 'elif':
                self.match_word('elif')
                self.condition()
                self.match_word(":")
                if self.current_token.recognized_string == '#{':
                    self.match_word('#{')
                    self.intermediate_code.backpatch(Btrue , self.intermediate_code.nextQuad())
                    self.statemets()
                    ifList= self.intermediate_code.makeList(self.intermediate_code.nextQuad())
                    self.intermediate_code.gen_quad("jump" , "_" , "_" , "_")
                    breaklist=self.intermediate_code.mergeList(breaklist , ifList)
                    self.intermediate_code.backpatch(Bfalse , self.intermediate_code.nextQuad())
                    self.match_word('#}')
                else:
                    self.intermediate_code.backpatch(Btrue , self.intermediate_code.nextQuad())
                    self.statement()
                    ifList= self.intermediate_code.makeList(self.intermediate_code.nextQuad())
                    self.intermediate_code.gen_quad("jump" , "_" , "_" , "_")
                    breaklist=self.intermediate_code.mergeList(breaklist , ifList)
                    self.intermediate_code.backpatch(Bfalse , self.intermediate_code.nextQuad())
        if self.current_token.recognized_string == 'else':
            self.match_word('else')
            self.match_word(":")
            if self.current_token.recognized_string == '#{':
                self.match_word('#{')
                self.statemets()
                self.intermediate_code.backpatch(breaklist, self.intermediate_code.nextQuad())
                self.match_word('#}')
            else:
                self.statement()
                self.intermediate_code.backpatch(breaklist, self.intermediate_code.nextQuad())
        else:
            self.intermediate_code.backpatch(breaklist, self.intermediate_code.nextQuad())
    
    
    
    def declarations(self):
        Variables = []
        while self.current_token.recognized_string == "#int" or self.current_token.recognized_string == "global" :
            Variable= self.declaration_line() 
            Variables = Variables + Variable
    
        return Variables
            
    
    def declaration_line(self):
        Variable = []
       
        if(self.current_token.recognized_string == '#int'):
            self.match_word("#int")
            Variable = self.id_list()
            
        elif(self.current_token.recognized_string == 'global'):
            self.match_word("global")

            Global_Variables = self.id_list()
            for global_variable in Global_Variables:
                global_entity = GlobalVariable(global_variable)
                self.scope.add_Entity(global_entity)
        return Variable
    
    def id_list(self):
        Variables = []
        if self.current_token.family == 'IDENTIFIER':
            Variables.append(self.current_token.recognized_string)
            self.match_type("IDENTIFIER")
        elif self.current_token.family == 'KEYWORD':
            self.match_type("KEYWORD")
        while self.current_token.recognized_string == ',':
            self.match_word(',')
            if self.current_token.family=='IDENTIFIER':
                Variables.append(self.current_token.recognized_string)
                self.match_type('IDENTIFIER')
            elif self.current_token.family=='KEYWORD':
                self.match_type
                ('KEYWORD')
        return Variables
            
    def statements(self):
        while self.current_token.recognized_string != "#}":
            self.statement()
            
    def statement(self):
        
        if self.current_token.recognized_string == 'if' or self.current_token.recognized_string == 'while':
            self.structured_statement()
        else:
            self.simple_statement()
       
       
    def structured_statement(self):
        if self.current_token.recognized_string == 'if':
            self.if_stat()

        elif self.current_token.recognized_string == 'while':
            self.while_stat()

    def condition(self):
     
        Results = self.logical_or_expression()
        return   Results
    
    def simple_statement(self):        
       
        if self.current_token.recognized_string == 'print':
            self.print_stat()
        elif self.current_token.recognized_string == 'return':
            self.return_stat()
        else:
            self.assignment_stat()
     
    
    def assignment_stat(self):
        target = self.current_token.recognized_string
        self.match_type("IDENTIFIER")
        self.match_word("=")
        if self.current_token.recognized_string == "int":
            self.match_word("int")
            self.match_word("(")
            self.match_word("input")
            self.match_word("(")
            self.match_word(")")
            self.match_word(")")

            w = self.intermediate_code.newTemp()
            self.intermediate_code.gen_quad("in" , w , "_" , "_" )
            self.intermediate_code.gen_quad(":=" , w , "_" , target )
            new_temp = TemporaryVariable(w,"integer",self.scope.get_nextOffset())
            self.scope.add_Entity(new_temp)

        else:
            source=self.expression()
            self.intermediate_code.gen_quad(":=" , source , "_" , target )
    
    def expression(self):
        Results = [None, None, None] 
        Results = self.logical_or_expression()
        Or = Results[0] 
        return Or 
        
    def logical_or_expression(self):
        Results = [None, None, None] 
        Results = self.logical_and_expression()
        Btrue = Results[1]
        Bfalse = Results [2]
        while self.current_token.recognized_string == 'or':
            self.match_word('or')
            self.intermediate_code.backpatch(Bfalse,self.intermediate_code.nextQuad())
            Results = self.logical_and_expression()
            Q2true = Results[1]
            Q2false = Results[2]
            Btrue = self.intermediate_code.mergeList(Btrue ,Q2true)
            Bfalse = Q2false
            Results[1] = Btrue
            Results[2] = Bfalse
        return Results
    
    def logical_and_expression(self):
        Results = [None, None, None] 
        Results = self.relational_expr()
        Qtrue = Results[1]
        Qfalse = Results[2]     
        while self.current_token.recognized_string == 'and':
            self.match_word('and')
            self.intermediate_code.backpatch(Qtrue,self.intermediate_code.nextQuad())
            Results = self.relational_expr()
            R2true = Results[1]
            R2false = Results[2]
            Qfalse = self.intermediate_code.mergeList(Qfalse , R2false)
            Qtrue = R2true
            Results[1] = Qtrue
            Results[2] = Qfalse
        return Results

    def relational_expr(self):
        Results = [None,None, None] 
        E = self.additive_expr()
        Results.append(E)
        Results[0] = E
        E1 = E
       
        while   self.current_token.family == 'doublerelOperator' or self.current_token.family == 'relOperator':
           
            if self.current_token.family == 'relOperator':
                relop = self.current_token.recognized_string
                self.match_type( 'relOperator')
                E = self.additive_expr()
                Results[0] = E
                E2 = E
            elif self.current_token.family == 'doublerelOperator':
                relop = self.current_token.recognized_string
                self.match_type('doublerelOperator')
                E = self.additive_expr()
                E2 = E
            Rtrue = self.intermediate_code.makeList(self.intermediate_code.nextQuad())
            self.intermediate_code.gen_quad(relop , E1 , E2 , "_")
            Results[1] = Rtrue
            Rfalse = self.intermediate_code.makeList(self.intermediate_code.nextQuad())
            self.intermediate_code.gen_quad("jump" , "_" , "_" , "_")
            Results[2] = Rfalse
            if(self.not_actiavated == True):
                Results[1] = Rfalse
                Results[2] = Rtrue
                self.not_actiavated = False
        return Results
      
    def additive_expr(self):
        T = self.multiplicative_expr()
        T1 = T
        while self.current_token.family == 'addOperator':
            symbol = self.current_token.recognized_string
            self.match_type('addOperator')
            T = self.multiplicative_expr()
            T2 = T
            w = self.intermediate_code.newTemp()
            new_temp = TemporaryVariable(w,"integer",self.scope.get_nextOffset())
            self.scope.add_Entity(new_temp)
            self.intermediate_code.gen_quad(symbol, T1, T2, w)
            T1 = w 
        return T1
           
    def multiplicative_expr(self):
        unary = self.unary_expr()
        F1 = unary
        while self.current_token.family == 'mulOperator':
            symbol = self.current_token.recognized_string
            self.match_type('mulOperator')
            unary = self.unary_expr()
            F2 = unary
            w = self.intermediate_code.newTemp()
            new_temp = TemporaryVariable(w,"integer",self.scope.get_nextOffset())
            self.scope.add_Entity(new_temp)
            self.intermediate_code.gen_quad(symbol, F1 , F2 , w)
            F1 = w
        return F1
           
    def unary_expr(self):
        unitary = None
        if self.current_token.recognized_string == 'not':
            self.match_word('not')
            self.not_actiavated = True
            unitary = self.unitary_prosthetic_expr()
        else:
            unitary = self.unitary_prosthetic_expr()
        return unitary
            
    def unitary_prosthetic_expr(self):
        sign_operator= None
        if self.current_token.family == 'addOperator':
            sign_operator = self.current_token.recognized_string
            self.match_type('addOperator')
            if self.current_token.family != 'NUMBER':
                self._error(self._error(f"Expected a number after the '{sign_operator}' in Line : {self.current_token.line_number}"))
        term = self.term() 
        if sign_operator != None:
            term = sign_operator + term
        return term
        
    def term(self):
        factor = self.factor()
        return factor

    def factor(self):
        F = None
        Results = []
        if self.current_token.family == 'NUMBER':
            F = self.current_token.recognized_string
            self.match_type("NUMBER")
        elif self.current_token.recognized_string == '(':
            self.match_word('(')
            F = self.expression()
            self.match_word(')')
            
        else:
            F = self.current_token.recognized_string
            self.match_type('IDENTIFIER')
            Results = self.idtail(F)
            if len(Results) > 0:
                F= Results[-1]
        return F
    
    def idtail(self,F):
        Parameters= []
        if self.current_token.recognized_string == '(':
            self.match_word('(')
            Parameters = self.actual_par_list()
            for parameter in Parameters:
                self.intermediate_code.gen_quad("par" , parameter , "CV" , "_")
            self.match_word(')')
            w = self.intermediate_code.newTemp()
            new_temp = TemporaryVariable(w,"integer",self.scope.get_nextOffset())
            self.scope.add_Entity(new_temp)
            Parameters.append(w)
            self.intermediate_code.gen_quad("par" , w, "RET" , "_")
            self.intermediate_code.gen_quad("call", F , "_" , "_")
        return Parameters
        
    def actual_par_list(self):
        Parameters = []
        if self.current_token.recognized_string != ")":
            parameter =self.expression()
            Parameters.append(parameter)
            while self.current_token.recognized_string == ",":
                self.match_word(',')
                parameter =self.expression()
                Parameters.append(parameter)
        return Parameters
                
    def print_stat(self):
        self.match_word('print')
        self.match_word('(')
        source= self.expression()
        self.match_word(')')
        self.intermediate_code.gen_quad("out" , source , "_" , "_")
    
    def return_stat(self):
        self.match_word('return')
        source =self.expression()
        self.intermediate_code.gen_quad("ret" , source , "_" , "_")

    def while_stat(self):
        self.match_word('while')
        Bquad = self.intermediate_code.nextQuad()
        Results = self.condition()
        Btrue = Results[1]
        Bfalse = Results[2]
        self.match_word(":")
        if self.current_token.recognized_string == '#{':
            self.match_word('#{')
            self.intermediate_code.backpatch(Btrue, self.intermediate_code.nextQuad())
            self.statements()
            self.intermediate_code.gen_quad("jump" , "_" , "_" , Bquad)
            self.intermediate_code.backpatch(Bfalse, self.intermediate_code.nextQuad())
            self.match_word('#}')
        else:
            self.intermediate_code.backpatch(Btrue, self.intermediate_code.nextQuad())
            self.statement()
            self.intermediate_code.gen_quad("jump" , "_" , "_" , Bquad)
            self.intermediate_code.backpatch(Bfalse, self.intermediate_code.nextQuad())
   

#======================Intermediate code=======================

class Quad:
    def __init__(self, label, operator, operand1, operand2, result):
        self.label = label
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2
        self.result = result

class IntermediateCode :
    def __init__(self):
        self.quads = [] 
        self.next_quad = 1
        self.temp_count = 1

    def gen_quad(self , operator , operand1, operand2, result):
        quad = Quad(self.next_quad,operator,operand1,operand2 ,result)
        self.quads.append(quad)
        self.next_quad += 1

    def nextQuad(self):
        return self.next_quad
    
    def newTemp(self):
        temp_name = f"T_{self.temp_count}"
        self.temp_count += 1
        return temp_name
    
    def emptyList(self):
        return[]
    
    def mergeList(self , list1, list2):
        return list1+list2
    
    def makeList(self, label):
        return [label]

    def backpatch(self , quad_list , label):
        for quad_label in quad_list:
            for quad in self.quads:
                if quad.label == quad_label:
                    quad.result = label

    def begin_block(self,name):
        label = f"{self.next_quad}"
        self.gen_quad("begin_block", name , "_" , "_")
        return label
    

    def end_block(self,name):
        label = f"L{self.next_quad}"
        self.gen_quad("end_block",name,"_","_")
        
    def halt(self):
        label = f"L{self.next_quad}"
        self.gen_quad("halt" , "_" , "_" , "_")
   
    def print_code(self, output_file):
        with open(output_file, 'w') as f:
            for quad in self.quads:
                f.write(f"{quad.label}:\t{quad.operator}\t{quad.operand1}\t{quad.operand2}\t{quad.result}\n")

#======================Symbolic Table=======================

class Entity:
    def __init__(self,name):
        self.name = name
        

class Scope:
    def __init__(self):
        self.offset = 12
        self.return_address = None
        self.access_link = None
        self.return_value_of_the_function = None
        self.entities = [self.return_address, self.access_link, self.return_value_of_the_function]
    
    def get_nextOffset(self):
        return_value = self.offset
        self.offset += 4
        return return_value

    def add_Entity(self , entity):
        self.entities.append(entity)

    def print_scope(self,file):
        file.write("\tEntities:\n")
        for entity in self.entities[3:]:
            file.write(f"\t\tName: {entity.name}\n")
            if isinstance(entity, Variable):
                file.write(f"\t\tDatatype: {entity.datatype}\n")
                file.write(f"\t\tOffset: {entity.offset}\n")
                file.write("\t\t------------------------\n")
            elif isinstance(entity, TemporaryVariable):
                file.write(f"\t\tDatatype: {entity.datatype}\n")
                file.write(f"\t\tOffset: {entity.offset}\n")
                file.write("\t\t------------------------\n")
            elif isinstance(entity, GlobalVariable):
                file.write("\t\t------------------------\n")
            elif isinstance(entity, Parameter):
                file.write(f"\t\tDatatype: {entity.datatype}\n")
                file.write(f"\t\tMode: {entity.mode}\n")
                file.write(f"\t\tOffset: {entity.offset}\n")
                file.write("\t\t----------------------\n")
            elif isinstance(entity, Function):
                file.write(f"\t\tDatatype: {entity.datatype}\n")
                if entity.framelength is not None:
                    file.write(f"\t\tFramelength: {entity.framelength}\n")
                if entity.startingQuad is not None:
                    file.write(f"\t\tStartingQuad: {entity.startingQuad}\n")
                if entity.formalParameters is not None:
                    file.write("\t\tFormalParameters:\n")
                    for formal_param in entity.formalParameters:
                        file.write(f"\t\t\t- Name: {formal_param.name}, Datatype: {formal_param.datatype}, Mode: {formal_param.mode}\n")
                file.write("\t\t-------------------------\n")
        file.write("End of Scope\n")
        

class Table:
    def __init__(self, output_file):
        self.scopes = []
        self.output_file = output_file
    
    def add_Scope(self, scope):
        self.scopes.append(scope)

    def pop_scope(self):
        self.scopes.pop()


    def searchfor(self, name):
            current_level = len(self.scopes)-1
            nesting_level = len(self.scopes)
            global_declared = False
            for scope in reversed(self.scopes):
                nesting_level-= 1
                for entity in reversed(scope.entities):
                    if entity != None:
                        if entity.name == name:
                            if isinstance(entity, GlobalVariable) :
                                global_declared = True
                                continue
                            return entity , current_level , nesting_level , global_declared
            return None
    
    def print_table(self):
        f = self.output_file
        f.write("==========================NEW VIEW===========================\n")
        level = 0
        for scope in self.scopes:
            f.write(f"SCOPE LEVEL {level}\n")
            level += 1
            scope.print_scope(f)

class Variable(Entity):
    def __init__(self, name, datatype,offset):
        super().__init__(name)  
        self.datatype = datatype
        self.offset = offset

class TemporaryVariable(Entity):
    def __init__(self, name, datatype,offset):
        super().__init__(name)  
        self.datatype = datatype
        self.offset = offset

class GlobalVariable(Entity):
    def __init__(self, name):
        super().__init__(name)


class Function(Entity):  
    def __init__(self, name, datatype, framelength ,startingQuad , formalParameters):
        super().__init__(name)
        self.datatype = datatype
        self.startingQuad = startingQuad
        self.framelength = framelength
        self.formalParameters = formalParameters

    def add_formalParameters(self , formalParameters):
        self.formalParameters = formalParameters

    def update_framelength(self , framelength):
        self.framelength = framelength

    def update_startingQuad(self , startingQuad):
        self.startingQuad = startingQuad


class Parameter(Entity):
    def __init__(self, name, datatype, mode, offset):
        super().__init__(name)
        self.datatype = datatype
        self.mode = mode
        self.offset = offset
        

class FormalParameter(Entity):
    def __init__(self,name,  datatype, mode):
        super().__init__(name)
        self.datatype = datatype
        self.mode = mode

#==================================FINAL CODE =========================================
class FinalCode:
    def __init__(self ,intermediate_code , symbol_table ):
        self.intermediate_code = intermediate_code
        self.symbol_table = symbol_table
        self.final_code = []
  
        

    def gnlvcode(self , v):
        Results = []
        Results = self.symbol_table.searchfor(v)
        entity = Results[0]
        current_level = Results[1]
        level_of_variable = Results[2]
        if entity is  None:
            raise ValueError(f"The variable {v} wasnt found")
        for i in range(current_level - level_of_variable):
            if i == 0:
                self.produce("\tlw t0,-4(sp)")
            self.produce("\tlw t0,-4(t0)")
        self.produce(f"\taddi t0,t0,{entity.offset}")
    
    def loadvr(self, v , reg):
        Results = []
        entity = None
        current_level = None
        level_of_variable = None
        Results = self.symbol_table.searchfor(v)
        if v.isdigit() or (v.startswith('-') and v[1:].isdigit()):
            if v.startswith('-'):
                v = v[1:]
                self.produce(f"\tli {reg},-{v}")
                return
            self.produce(f"\tli {reg},{v}")
            return
        if Results !=None:
            entity = Results[0]
            current_level = Results[1]
            level_of_variable = Results[2]
            global_declared = Results[3]
            if current_level == level_of_variable:
                if isinstance(entity, Variable):
                    self.produce(f"\tlw {reg},-{entity.offset}(sp)")
                elif isinstance(entity, TemporaryVariable):
                    self.produce(f"\tlw {reg},-{entity.offset}(sp)")        
                elif isinstance(entity, Parameter):
                    self.produce(f"\tlw {reg},-{entity.offset}(sp)")
               
            elif global_declared == True:
                self.produce(f"\tlw {reg},-{entity.offset}(gp)")

            else:
                if isinstance(entity, Variable):
                    self.gnlvcode(v)
                    self.produce(f"\tlw {reg},(t0)")
                elif isinstance(entity, TemporaryVariable):
                    self.gnlvcode(v)
                    self.produce(f"\tlw {reg},(t0)")
                elif isinstance(entity, Parameter):
                    self.gnlvcode(v)
                    self.produce(f"\tlw {reg},(t0)")
        else:
            print(v ," wasn't found in symbol table")
               

    def storerv(self , reg,v):
        Results = []
        Results = self.symbol_table.searchfor(v)
        entity = Results[0]
        current_level = Results[1]
        level_of_variable = Results[2]
        global_declared = Results[3]
        if entity is None:
            raise ValueError(f"The variable {v} wasnt found")
        if current_level == level_of_variable:
            if isinstance(entity, Variable):
                self.produce(f"\tsw {reg},-{entity.offset}(sp)")
            elif isinstance(entity, TemporaryVariable):
                self.produce(f"\tsw {reg},-{entity.offset}(sp)")        
            elif isinstance(entity, Parameter):
                self.produce(f"\tsw {reg},-{entity.offset}(sp)")
        elif global_declared == True:
            self.produce(f"\tsw {reg},-{entity.offset}(gp)")
        else:
            if isinstance(entity, Variable):
                self.gnlvcode(v)
                self.produce(f"\tsw {reg},(t0)")
            elif isinstance(entity, TemporaryVariable):
                self.gnlvcode(v)
                self.produce(f"\tsw {reg},(t0)")
            elif isinstance(entity, Parameter):
                self.gnlvcode(v)
                self.produce(f"\tsw {reg},(t0)")
                

    def transform_intermediate(self, name_of_function):
        function_check = False
        parameter_quads=[]
        for quad in self.intermediate_code.quads:
            if quad.operator == "begin_block" and quad.operand1 == name_of_function:
                if (quad.operand1 == "main"):
                    self.produce(f"L{quad.label}:")
                    self.produce(f"\taddi,sp,sp,{(self.symbol_table.scopes[0].entities[-1]).offset +4}")
                    self.produce("\tmv gp,sp")
                    function_check = True
                else:
                    self.produce(f"L{quad.label}:")
                #  print("begin name ",name_of_function)
                    function_check = True
                    self.produce(f"\tsw ra,0(sp)")
                # print("function_check" ,function_check)
            if quad.operator == "end_block" and quad.operand1 == name_of_function:
                self.produce(f"L{quad.label}:")
                Results = []
                Results = self.symbol_table.searchfor(quad.operand1)
                if Results != None:
                    entity = Results[0]
                self.produce("\tlw ra,0(sp)")
                self.produce("\tjr ra")
                function_check = False
                #print("function_check" ,function_check)
            if quad.operator == "halt":
                self.produce(f"L{quad.label}:")
                self.produce("\tli a0,0")
                self.produce("\tli a7,93")
                self.produce("\tecall")

            
            if function_check == True:
                if quad.operator == ":=" :
                    self.produce(f"L{quad.label}:")
                    self.loadvr(quad.operand1 , "t0")
                    self.storerv("t0",quad.result)
                if quad.operator == "+":
                    self.produce(f"L{quad.label}:")
                    self.loadvr(quad.operand1 , "t1")
                    self.loadvr(quad.operand2 , "t2")
                    self.produce("\tadd t1,t1,t2")
                    self.storerv("t1" ,quad.result)
                if quad.operator == "-":
                    self.produce(f"L{quad.label}:")
                    self.loadvr(quad.operand1 , "t1")
                    self.loadvr(quad.operand2 , "t2")
                    self.produce("\tsub t1,t1,t2")
                    self.storerv("t1" ,quad.result)
                if quad.operator == "*":
                    self.produce(f"L{quad.label}:")
                    self.loadvr(quad.operand1 , "t1")
                    self.loadvr(quad.operand2 , "t2")
                    self.produce("\tmul t1,t1,t2")
                    self.storerv("t1" ,quad.result)
                if quad.operator == "//":
                    self.produce(f"L{quad.label}:")
                    self.loadvr(quad.operand1 , "t1")
                    self.loadvr(quad.operand2 , "t2")
                    self.produce("\tdiv t1,t1,t2")
                    self.storerv("t1" ,quad.result)
                if quad.operator == "%":
                    self.produce(f"L{quad.label}:")
                    self.loadvr(quad.operand1 , "t1")
                    self.loadvr(quad.operand2 , "t2")
                    self.produce("\trem t1,t1,t2")
                    self.storerv("t1" ,quad.result)
                if quad.operator == "jump":
                    self.produce(f"L{quad.label}:")
                    self.produce(f"\tj L{quad.result}")
                if quad.operator == "==":
                    self.produce(f"L{quad.label}:")
                    self.loadvr(quad.operand1, "t1")
                    self.loadvr(quad.operand2, "t2")
                    self.produce(f"\tbeq,t1,t2,L{quad.result}")
                if quad.operator == "<":
                    self.produce(f"L{quad.label}:")
                    self.loadvr(quad.operand1, "t1")
                    self.loadvr(quad.operand2, "t2")
                    self.produce(f"\tblt,t1,t2,L{quad.result}")
                if quad.operator == ">":
                    self.produce(f"L{quad.label}:")
                    self.loadvr(quad.operand1, "t1")
                    self.loadvr(quad.operand2, "t2")
                    self.produce(f"\tbgt,t1,t2,L{quad.result}")
                if quad.operator == "<=":
                    self.produce(f"L{quad.label}:")
                    self.loadvr(quad.operand1, "t1")
                    self.loadvr(quad.operand2, "t2")
                    self.produce(f"\tble,t1,t2,L{quad.result}")
                if quad.operator == ">=":
                    self.produce(f"L{quad.label}:")
                    self.loadvr(quad.operand1, "t1")
                    self.loadvr(quad.operand2, "t2")
                    self.produce(f"\tbge,t1,t2,L{quad.result}")
                if quad.operator == "!=":
                    self.produce(f"L{quad.label}:")
                    self.loadvr(quad.operand1, "t1")
                    self.loadvr(quad.operand2, "t2")
                    self.produce(f"\tbne,t1,t2,L{quad.result}")
                if quad.operator == "ret":
                    self.produce(f"L{quad.label}:")
                    self.loadvr(quad.operand1 , "t1")
                    self.produce("\tlw t0,-8(sp)")
                    self.produce("\tsw t1,0(t0)")
                if quad.operator == "in":
                    self.produce(f"L{quad.label}:")
                    self.produce("\tli a7,5")
                    self.produce("\tecall")
                    self.storerv("a0" ,quad.operand1)
                if quad.operator == "out":
                    self.produce(f"L{quad.label}:")
                    self.loadvr(quad.operand1,"t0")
                    self.produce("\tmv a0,t0")
                    self.produce("\tli a7,1")
                    self.produce("\tecall")
                    self.produce("\tla a0,str_nl")
                    self.produce("\tli a7,4")
                    self.produce("\tecall")
                if quad.operator == "par":
                    parameter_quads.append(quad)
                if quad.operator == "call":
                    Results = []
                    Results = self.symbol_table.searchfor(quad.operand1)
                    entity = Results[0]
                    current_level = Results[1]
                    level_of_variable = Results[2]
                    i = 0
                    for quad2 in parameter_quads:
                        self.produce(f"L{quad2.label}:")
                        if i==0:
                            self.produce(f"\taddi fp,sp,{entity.framelength}")
                        if quad2.operand2 == "CV":
                            offset= 12+(4*i)

                            self.loadvr(quad2.operand1,"t0")
                            self.produce(f"\tsw t0, -{offset}(fp)")
                            i+=1
                        if quad2.operand2 == "RET":
                            Results = []
                            Results = self.symbol_table.searchfor(quad2.operand1)
                            entity2 = Results[0]
                            self.produce(f"\taddi t0,sp,-{entity2.offset}")
                            self.produce("\tsw t0,-8(fp)")
                    if current_level == level_of_variable:
                        self.produce(f"L{quad.label}:")
                        self.produce("\tlw t0,-4(sp)")
                        self.produce("\tsw t0,-4(fp)")
                    else:
                        self.produce(f"L{quad.label}:")
                        self.produce("\tsw sp,-4(fp)")
                    self.produce(f"\taddi sp,sp,{entity.framelength}")
                    self.produce(f"\tjal L{entity.startingQuad-1}")
                    self.produce(f"\taddi sp,sp,-{entity.framelength}")
                    parameter_quads=[]
                    
    def produce(self, instructions):
       self.final_code.append(instructions)

                           
    def print_final_code(self, output_file):
        with open(output_file, 'w') as f:
            for line in self.final_code:
                f.write(line + '\n')


    

        
try:
    intermediate_code = IntermediateCode()
    file_name = input("\nGive me the name of the file : ")
    file_name_without_extension = file_name.split(".")[0]
    sym_output_file = file_name_without_extension + ".sym"
    int_output_file = file_name_without_extension + ".int"
    asm_output_file = file_name_without_extension + ".asm"
    with open(sym_output_file, 'w') as f:
        table = Table(f)
        lexer = Lex(file_name)
        final_code_generator = FinalCode(intermediate_code , table )
        parser = SyntaxAnalyzer(lexer , intermediate_code , table , final_code_generator)
        parser.parse()
    
    intermediate_code.print_code(int_output_file)
    
    final_code_generator.print_final_code(asm_output_file)
except ValueError as error:
    print("\n" + str(error))