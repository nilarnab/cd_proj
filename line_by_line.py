import analyzer_module
import threading
import time


class TopParser:

    def __init__(self, source_code):

        self.source_code = source_code

    def work_divider(self, line_no):

        print("Thread in line no", line_no, "WORK RECEIVED", self.source_code)

        # time to divide the work
        codes = self.source_code.split(';')

        for i in range(len(codes)):
            if i != len(codes) - 1:
                self.parser(codes[i] + ';')
            else:
                self.parser(codes[i])

    def parser(self, work):
        global grievances

        if not work:
            return

        resp = Analyzer.analyze_string(work)

        # print("RESPONSE:", resp)

        if resp['id'] == 0:
            print("PARSER WORKED, SAYS", resp['type'])

        if resp['id'] == 1:
            grievances.append([line_no, resp['message']])
        if resp['id'] == 2:
            print("PARSER ONE DIDNT WORK, SAYS", resp['message'])
            print("TYRING PARSER TWO")

            resp = Analyzer_alt.analyze_string(work)
            print("RESPONSE:", resp)

            if resp['id'] != 0:
                exit(0)
            else:
                print("PARSER TWO WORKED, SAYS", resp['type'])

    def solve_greivances(self):
        """
        {'id': 0/1, 'type': 'successful'/'missing bracket'}
        :return:
        """
        global grievances
        open_list = ["[", "{", "("]
        close_list = ["]", "}", ")"]

        print("GRIEVANCES", grievances)
        grievances.sort()

        grievances = [el[1] for el in grievances]

        stack = []
        for i in grievances:
            if i in open_list:
                stack.append(i)
            elif i in close_list:
                pos = close_list.index(i)
                if (len(stack) > 0 and
                        open_list[pos] == stack[len(stack) - 1]):
                    stack.pop()
                else:
                    return {'id': 1, 'type': 'missing bracket'}
        if len(stack) == 0:
            return {'id': 0, 'type': 'successful'}
        else:
            return {'id': 1, 'type': 'missing bracket'}


def time_counter():
    global permission
    permission = False
    time_d = 4
    while time_d:
        print("COUNT DOWN TIMER", time_d)
        time_d -= 1
        time.sleep(1)

    permission = True


if __name__ == '__main__':

    global grievances, permission
    grievances = []

    time_thread = threading.Thread(target=time_counter, args=())
    time_thread.start()

    ALPHABETS = [chr(i + ord('a')) for i in range(26)]
    # STRING = "int anewvariable;int var = 10;tf(a>b){int var = 10;}"
    # STRING = "int var = 10;}"
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

    """
    successful runs
    int a = 11;
    int b = 10;
    tf(a>b){
        a=10;
    }
    
    
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
        'I': [['t', 'f', '(', 'E', ')', '{', 'A', '}']],
        # 'S': []

    }

    STARTING_ASSIGNMENT = 'A'

    RULE_ASSIGNMENT = {
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
        'A': [['B', 'W', '=', 'W', 'R', ';']],
        'R': [['0', 'R'], ['1', 'R'], ['2', 'R'], ['3', 'R'], ['4', 'R'], ['5', 'R'], ['6', 'R'], ['7', 'R'],
              ['8', 'R'], ['^']],
        'W': [[' ', 'W'], ['^']],
    }

    source_code = open("input.txt", "r")

    threads = []

    line_no = 1

    print("MAKING ANALYZERS")

    try:
        Analyzer = analyzer_module.Analyzer(ALPHABETS, RULES, STARTING)
        Analyzer_alt = analyzer_module.Analyzer(ALPHABETS, RULE_ASSIGNMENT, STARTING)
    except:
        print("COULD NOT MAKE PARSING TABLE")

    while not permission:
        time.sleep(1)
        print("WAITING FOR PERMISSION", permission)

    START = time.time()
    
    for line in source_code:
        line = line.replace('\n', '').strip()  # removing obvious '\n'
        # print("Line:"+line)
        top_parser = TopParser(source_code=line)
        # top_parser.work_divider()     # non threaded application
        # threads.append(threading.Thread(target=top_parser.work_divider, args=(line_no,)))
        # threads[-1].start()
        top_parser.work_divider(line_no)
        line_no += 1

    for thread_id in threads:
        thread_id.join()

    res = top_parser.solve_greivances()

    END = time.time()

    print("FINAL", res)
    print("time taken", END - START)
