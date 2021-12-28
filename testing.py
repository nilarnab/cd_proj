import time


class Analyzer:
    def __init__(self, ALPHABETS, RULES, FIRST, STRING):
        self.alphabets = ALPHABETS
        self.rules = RULES
        self.starting = FIRST
        self.string = STRING
        self.parsing_table = self.make_parsing_table()

    def find_terminals(self):
        """
        Finding terminals
        :return: dict(): all the terminals of the rules
        """
        terminals = dict()
        for variable in self.rules:
            for rules in self.rules[variable]:
                for el in rules:
                    if not el.isupper():
                        terminals[el] = True

        return terminals

    def make_parsing_table(self):

        # first make a blank table
        # n(rows) = n(variables)
        # n(cols) = n(terminals)

        terminals = list(self.find_terminals().keys())
        variables = self.find_variables()

        terminals.sort()
        variables.sort()

        n_terminals = len(terminals)
        n_variables = len(variables)

        parsing_table = [[None] * n_terminals for i in range(n_variables)]

        # making a dictionary for terminal_to_index
        term_to_index = dict()

        for i in range(len(terminals)):
            term_to_index[terminals[i]] = i

        # making a dictionary for variable to index
        var_to_index = dict()
        for i in range(len(variables)):
            var_to_index[variables[i]] = i

        # #print("TERM TO INDEX AT make parsing table", term_to_index)

        # #print("TERM TO INDEX", term_to_index)
        # #print("VAR TO INDEX", var_to_index)

        # start filling the parsing table
        for variable in self.rules:
            for rule in self.rules[variable]:

                # #print("VARIABLE", variable, "RULE", rule)
                first_finder = FindFirst(self.alphabets, self.rules, rule)
                first = first_finder.first

                # #print("First :", first)

                for symbol in first:

                    if symbol != '^':

                        # #print("Trying to put", [variable, rule], "in", var_to_index[variable], term_to_index[symbol])
                        # if symbol == 'a':
                        #     #print("<><>PUTTTING a in ", (var_to_index[variable], term_to_index[symbol]), "rule", rule)
                        if parsing_table[var_to_index[variable]][term_to_index[symbol]] is None:
                            parsing_table[var_to_index[variable]][term_to_index[symbol]] = [variable, rule]

                        else:
                            #print("!!!!!!!!!The place here is already filled with",
                                  # parsing_table[var_to_index[variable]][term_to_index[symbol]])
                            time.sleep(5)
                            exit(1)

                    else:
                        follow_finder = FindFollow(self.alphabets, self.rules, self.starting, variable)

                        #print("FOLLOW OF", variable, 'is', follow_finder.find_follow())

                        for symbol_1 in follow_finder.find_follow():

                            # #print("Trying to put (after eps)", [variable, rule], "in", [variable],
                            # term_to_index[symbol_1])
                            if symbol_1 == '$':
                                symbol_1 = '^'
                            if parsing_table[var_to_index[variable]][term_to_index[symbol_1]] is None:
                                parsing_table[var_to_index[variable]][term_to_index[symbol_1]] = [variable, rule]
                            else:
                                #print("!!!!!!!!!!The place is already filled with",
                                      # parsing_table[var_to_index[variable]][term_to_index[symbol_1]])
                                time.sleep(5)
                                exit(1)

        return parsing_table, var_to_index, term_to_index

    def get_follow(self):
        '''
        FUNCITON MADE FOR TESTING
        :return:
        '''
        follow_finder = FindFollow(self.alphabets, self.rules, self.starting, grammar)
        return follow_finder.find_follow()

    def find_variables(self):

        return list(set([key for key in self.rules]))

    def display_table(self, table):

        terminals = list(self.find_terminals().keys())
        terminals.sort()

        #print("DISPLAYING TABLE")
        for terminal in terminals:
            #print(terminal, end=" | ")
            pass
        #print('')

        for row in table:
            #print(row)
            pass

    def find_reason_of_error(self, stack, input):

        if input[0] == '}':
            return {'id': 1, 'type': 'missing bracket', 'message': '}'}

        if stack[-1] == '}':
            return {'id': 1, 'type': 'missing bracket', 'message': '{'}

        return {'id': 2, 'type': 'no match', 'message': 'parsing failed, no good match'}

    def analyze_string(self):

        """

        JSON
            {
                id: 0 / 1 / 2
                type: successful/ missing bracket / parsing failed, no good match
                message: None/ (, )/ None # type of bracket unbalanced
            }

        :return:
        """

        # #print(">>>>> starting analysis")
        stack = ['$', self.starting]
        input = list(self.string)
        input.append('$')

        parsing_table, var_to_index, term_to_index = self.parsing_table

        #print("TERM TO INDEX AT analyze string", term_to_index, var_to_index)

        self.display_table(parsing_table)
        # exit(1)

        while True:

            #print("STACK:", stack, "INPUT", input)

            # reduce
            while stack and input:
                if stack[-1] == input[0]:
                    stack.pop(-1)
                    input.pop(0)
                else:
                    break

            if not stack and not input:
                print("PARSING SUCCESSFUL")
                exit(0)
                pass

            # action
            # #print("TRYING TO HANDLE", stack, input)
            # #print("finding at", var_to_index[stack[-1]], term_to_index[input[0]])

            initial = input[0]
            if input[0] == '$':
                input[0] = '^'

            if stack[-1] == '$':
                print("!!!! PARSING FAILED, when", stack, input, "stack exhausted")
                return self.find_reason_of_error(stack, input)
                exit(0)

            if self.is_terminal(stack[-1]):
                print("!!!! PARSING FAILED, Could not find a possible match when STACK:", stack, "INPUT", input)
                return self.find_reason_of_error(stack, input)
                exit(0)

            if parsing_table[var_to_index[stack[-1]]][term_to_index[input[0]]] is None:
                print("NO MATCH FOUND FOR", stack[-1], input[0])
                return self.find_reason_of_error(stack, input)
                exit(0)

            try:
                action = [el for el in parsing_table[var_to_index[stack[-1]]][term_to_index[input[0]]]]
            except KeyError:
                print("!!! KEY ERROR when STACK", stack, "INPUT", input)
                return self.find_reason_of_error(stack, input)
                exit(1)
            except:
                print("!!!! UNANTICIPATED SITUATION when", stack, input)
                return self.find_reason_of_error(stack, input)

            if action is None:
                print("!!!! PARSING FAILED, could not find a possible action when STACK:", stack, "INPUT:", input)
                return self.find_reason_of_error(stack, input)
                exit(0)

            input[0] = initial

            # #print("ACTION:", action)

            # fill the stack
            # if action is None:
                # #print("STACK", stack, "INPUT", input)
                # #print("Could not find a match")

                # exit(1)

            rule = [el for el in action[1]]
            stack.pop(-1)
            while rule:
                temp = rule.pop(-1)

                if temp != '^':
                    stack.append(temp)

        pass

    def is_terminal(self, alphabet):

        return alphabet in self.find_terminals()


class FindFirst(Analyzer):

    def __init__(self, ALPHABETS, RULES, grammar):

        self.alphabets = ALPHABETS
        self.rules = RULES

        # #print(self.find_terminals())
        self.first = self.find_first(grammar)

    def find_terminals(self):
        """
        Finding terminals
        :return: dict(): all the terminals of the rules
        """
        terminals = dict()
        for variable in self.rules:
            for rules in self.rules[variable]:
                for el in rules:
                    if not el.isupper():
                        terminals[el] = True

        return terminals

    def find_first(self, grammar):

        # #print("Finding first of", grammar)

        if len(grammar) == 0:
            # #print("returning ^")
            return ['^']

        if self.is_terminal(grammar[0]):
            return [grammar[0]]
        elif grammar[0] == '^':
            return ['^']
        else:
            temp = []
            # the first symbol of alpha is a variable
            if self.has_epsilon(grammar[0]):
                extra = self.find_first(grammar[1:])
                for el in extra:
                    temp.append(el)

            for el in self.productions_starting_with_terminal(grammar[0]):
                temp.append(el)

            for el in self.find_variable_dependence(grammar[0]):
                # #print("VARIABLE DEPENDENCY", el)

                if el[0] != grammar[0]:
                    # #print("Trying to find the first of", el)
                    for extra in self.find_first(el):
                        if extra != '^':
                            temp.append(extra)
                        else:
                            # #print("found epsilon", el)
                            form_eps = self.find_first(el[1:])

                            for el_eps in form_eps:
                                temp.append(el_eps)

            return list(set(temp))

    def find_variable_dependence(self, variable):

        dependences = []

        for rule in self.rules[variable]:
            if rule[0] != '^':
                if not self.is_terminal(rule[0]):
                    dependences.append(rule)

        return dependences

    def has_epsilon(self, variable):

        for rule in self.rules[variable]:
            for symbol in rule:
                if symbol == '^':
                    return True

        return False

    def productions_starting_with_terminal(self, variable):

        terminals = []

        for rule in self.rules[variable]:

            if self.is_terminal(rule[0]):
                terminals.append(rule[0])

        return terminals

    def is_terminal(self, alphabet):

        return alphabet in self.find_terminals()


class FindFollow(FindFirst):
    def __init__(self, ALPHABETS, RULES, FIRST, variable):
        self.alphabets = ALPHABETS
        self.rules = RULES
        self.starting = FIRST
        self.variable = variable

    def find_follow(self):

        temp = []

        if self.variable == self.starting:
            # it is a starting symbol
            temp.append('$')

        rights = self.find_variable_in_rhs()

        for beta in rights:

            firsts = self.find_first(beta[1])

            # #print("BETA", beta, "its firsts", firsts)

            for first in firsts:

                # #print("FIRST", first)

                if first != '^':
                    temp.append(first)

                else:
                    # #print("it is an eps")
                    if beta[0] != self.variable:
                        follow_finder = FindFollow(self.alphabets, self.rules, self.starting, beta[0])
                        follows = follow_finder.find_follow()
                        for el in follows:
                            temp.append(el)

        return list(set(temp))

    def find_variable_in_rhs(self):

        possibiles = []

        for var in self.rules:
            for rule in self.rules[var]:
                for i in range(len(rule)):

                    if rule[i] == self.variable:
                        possibiles.append([var, rule[i + 1:]])

        return possibiles


if __name__ == '__main__':
    ALPHABETS = [chr(i + ord('a')) for i in range(26)]
    STRING = "int anewvariable;int var = 10;tf(a>b){int var = 10;}"
    # STRING = "int var = 10"
    # STRING = '()()((()))'
    # STRING = '(a)'

    STARTING = 'A'

    """
    A: Declaration and iitialization construct
    B, C: [a-Z]*
    T: Gives <SPACE>*<MATH><SPACE>*<DIGIT>*
    M: Gives mathematical functions
    S: <SPACE>*

    """

    """
    BROKEN CONVENTIONS
    ___________________________

    1. if(..) => tf(..)

    """

    RULES = {
        'A': [['i', 'n', 't', ' ', 'B', 'T', ';', 'A'], ['c', 'h', 'a', 'r', ' ', 'B', ';'], ['I'], ['^']],
        'B': [['a', 'C'], ['b', 'C'], ['c', 'C'], ['d', 'C'], ['e', 'C'], ['f', 'C'], ['g', 'C'], ['h', 'C'],
              ['i', 'C'], ['j', 'C'], ['k', 'C'], ['l', 'C'], ['m', 'C'], ['n', 'C'], ['o', 'C'], ['p', 'C'],
              ['q', 'C'], ['r', 'C'], ['s', 'C'], ['t', 'C'], ['u', 'C'], ['v', 'C'], ['w', 'C'], ['x', 'C'],
              ['y', 'C'], ['z', 'C']
              ],
        'C': [['a', 'C'], ['b', 'C'], ['c', 'C'], ['d', 'C'], ['e', 'C'], ['f', 'C'], ['g', 'C'], ['h', 'C'],
              ['i', 'C'], ['j', 'C'], ['k', 'C'], ['l', 'C'], ['m', 'C'], ['n', 'C'], ['o', 'C'], ['p', 'C'],
              ['q', 'C'], ['r', 'C'], ['s', 'C'], ['t', 'C'], ['u', 'C'], ['v', 'C'], ['w', 'C'], ['x', 'C'],
              ['y', 'C'], ['z', 'C']
            , ['^']],
        'T': [['S', 'M', 'S', 'R'], ['^']],
        'R': [['0', 'R'], ['1', 'R'], ['2', 'R'], ['3', 'R'], ['4', 'R'], ['5', 'R'], ['6', 'R'], ['7', 'R'],
              ['8', 'R'], ['^']],

        'M': [['+'], ['-'], ['*'], ['/'], ['=']],

        'S': [[' ', 'W']],
        'W': [[' ', 'W'], ['^']],
        'E': [['B', '>', 'B']],
        # 'F': [['B', '<', 'B', ']],

        # # if construct
        'I': [['t', 'f', '(', 'E', ')', '{', 'A', '}']]
        # 'S': []
    }
    grammar = 'A'
    analyzer = Analyzer(ALPHABETS, RULES, STARTING, STRING)

    res = analyzer.analyze_string()
    print(res)
