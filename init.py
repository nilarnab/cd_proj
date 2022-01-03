import analyzer_module
import threading
import time

from testing import Analyzer

SUCCESS = True
CONCERNS = []


class TopParser:

    def __init__(self, source_code):

        self.source_code = source_code

    def get_brackets(self, string, line_no):

        res = []

        for e in string:
            if e in ['{', '}']:
                res.append([line_no, e])

        return res

    def points_of_divisions(self, buffer, line_no):

        """

        buffer is a long line


        this gives output like
        [
            [string to be parsed, analyzer_name, chunk_id]
        ]


        phase one
        getting till tf or }



        ASSUMPTION
        tf is always at the starrting
        } is the only element in its line
        
        for loop construct is not in use

        """

        # print("RECIEVED", buffer)

        partitions = []
        pointer_1 = -1
        pointer_2 = len(buffer)

        for i in range(len(buffer)):
            # print("WORKING for", buffer, "now on", buffer[i])

            if i != len(buffer) - 1:
                if buffer[i: i + 2] == 'tf':
                    # partition 1 not required
                    break

            if buffer[i] == '}':
                # partition is required
                pointer_1 = i
                break

        if buffer:
            for i in range(len(buffer) - 1, pointer_1 - 1, -1):

                if buffer[i] == '}':
                    # partition 2 is not required
                    break

                if buffer[i: i + 2] == 'tf':
                    # partition 2 is required
                    pointer_2 = i
                    break

        # so the division is to be

        # [: pointer_1 + 1] [pointer_1 + 1: pointer_2] [pointer_2: ]

        # print("poitner 1", pointer_1, "pointer 2", pointer_2)

        res = [
            [
                buffer[: pointer_1 + 1],
                'OPEN_ANALYZE',
                [line_no, 'a']
            ],

            [
                buffer[pointer_1 + 1: pointer_2],
                'REGULAR_ANALYZE',
                [line_no, 'b']
            ],

            [
                buffer[pointer_2:],
                'CLOSE_ANALYZE',
                [line_no, 'c']
            ],
        ]

        return res

    def work_divider(self, line_no):
        global grievances

        print("Thread in line no", line_no)

        partitions = self.points_of_divisions(self.source_code, line_no)
        print("PREPARING CHUNKS")
        for chunk in partitions:


            # print("CHUNK", chunk)
            if chunk[1] == 'OPEN_ANALYZE':
                analyzer = Analyzer_open
                parser_name = chunk[1]

                if chunk[0]:
                    grievances.append([chunk[2], '}'])

            if chunk[1] == 'REGULAR_ANALYZE':
                analyzer = Analyzer_regular
                parser_name = chunk[1]
            if chunk[1] == 'CLOSE_ANALYZE':
                analyzer = Analyzer_close
                parser_name = chunk[1]

                if chunk[0]:
                    grievances.append([chunk[2], '{'])

            self.parser(chunk[0], analyzer, parser_name)

    def parser(self, work, Analyzer, parser_name):
        global grievances, SUCCESS
        print("PARSER AT WORK")

        if not work:
            return

        # print("work received for analyzer", work, "with parser", parser_name)
        resp = Analyzer.analyze_string(work)

        print("RESPONSE:", resp)

        if resp['id'] == 0:
            print("PARSER WORKED, SAYS", resp['type'])
            pass

        else:
            print("Parser did not work for", "WORK:", work, "ANALYZER NAME", parser_name)
            SUCCESS = False

            # resp = Analyzer_alt.analyze_string(work)
            print("RESPONSE:", resp)

            # if resp['id'] != 0:
            #     SUCCESS = False
            #     CONCERNS.append(line_no)
            #     print("FATAL ERROR in line number", line_no)
            #     # exit(0)
            # else:
            #     print("PARSER TWO WORKED, SAYS", resp['type'])

    def solve_greivances(self):
        global SUCCESS
        """
        {'id': 0/1, 'type': 'successful'/'missing bracket'}
        :return:
        """

        if not SUCCESS:
            return {'id': 1, 'type': 'did not work'}

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
            return {'id': 1, 'type': 'not a match, missing bracket'}


def time_counter():
    global permission
    permission = False
    time_d = 0
    while time_d:
        # print("COUNT DOWN TIMER", time_d)
        time_d -= 1
        time.sleep(1)

    permission = True


def run(BYTE_CHUNK):
    source_code = open("input.txt", "r")

    threads = []

    line_no = 0

    print("MAKING ANALYZERS")



    while not permission:
        time.sleep(1)
        print("WAITING FOR PERMISSION", permission)

    # starting analysis

    buffer = []

    LINE_CHUNK = 20


    print("starting ..")
    START_TIME = time.time()
    chunk_buffer = source_code.readlines(BYTE_CHUNK)
    # print(chunk_buffer)
    line_no = 0

    while chunk_buffer:
        line_no += 1
        # print("line nu", line_no)
        # chunk_buffer_var = [el.strip() for el in chunk_buffer]
        line = ''.join(chunk_buffer).replace('\n', '')
        # line = line.strip()
        # print("feeding", line)
        top_parser = TopParser(source_code=line)
        threads.append(threading.Thread(target=top_parser.work_divider, args=(line_no,)))

        chunk_buffer = source_code.readlines(BYTE_CHUNK)
        # print(chunk_buffer)

    print("starting threads")
    for thread in threads:
        thread.start()

    """
    for line in source_code:
        line = line.replace('\n', '').strip()  # removing obvious '\n'


        line_no += 1
        buffer.append(line)

        if line_no % 10 == 0:
            nw_buffer = ''.join(buffer)
            buffer = []
            # print("BUFFER NOW", nw_buffer)
            top_parser = TopParser(source_code=nw_buffer)
            # top_parser.work_divider()     # non threaded application
            threads.append(threading.Thread(target=top_parser.work_divider, args=(line_no,)))
            threads[-1].start()
        # top_parser = TopParser(source_code=line)
        # top_parser.work_divider(line_no)
    if buffer:
        nw_buffer = ''.join(buffer)
        buffer = []
        # print(":::::::::::: BUFFER NOW", nw_buffer)
        top_parser = TopParser(source_code=nw_buffer)
        # top_parser.work_divider()     # non threaded application
        threads.append(threading.Thread(target=top_parser.work_divider, args=(line_no,)))
        threads[-1].start()

    """
    # print(">>>>>>>>>>> COMING OUT OF FILE READING now buffer", buffer)

    for thread_id in threads:
        thread_id.join()
    top_parser = TopParser("")
    res = top_parser.solve_greivances()
    # analysis complete
    END_TIME = time.time()

    print("======================================================================")
    print("REPORT")
    print("-----------------")
    if res['id'] == 1:
        print("Final Response", res)
        print("Possible problems in line", CONCERNS)
    else:
        print("SUCCESS")
        print("Final", res)
    print("------------------")
    print("TIME TAKEN")
    print("------------------")

    print(END_TIME - START_TIME, "secs")

    return END_TIME - START_TIME


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

    2. for loop is for( , , ){ }

    3. there cannot be anytrhing in the line after a opening { 
        bracket and nothing before closing } bracket

        there cannot be more than one curly brackets in one line

        like tf(){
            here
        }
        
    4. No Indentation


    
    
    """

    """
    RUlES OF ANALYSIS
    ------------------------------------

    Apparantly the chunks can be of three types
    1. opening: expects an opening bracket
    2. regular: self sufficiet
    3. closing: expects a closing bracket
    
    """

    OPEN_ANALYZE_START = 'I_OPEN'

    OPEN_ANALYZE = {

        'A': [['i', 'n', 't', ' ', 'B', 'T', ';', 'A'], ['^']],
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
        'F': [['B', '<', 'B']],

        'I_OPEN': [['A', '}']],

        'OPENING': [['}']]
    }

    REGULAR_ANALYZE_START = 'A'

    REGULAR_ANALYZE = {
        'A': [['i', 'n', 't', ' ', 'B', 'T', ';', 'A'], ['I', 'A'],
              ['F', 'A'], ['^']],
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

        'F': [['f', 'o', 'r', '(', 'B', '=', 'R', ',', 'B', '<', 'R', ',', 'B', '+', '+', ')', '{', 'A', '}']]
    }

    CLOSE_ANALYZE_START = 'I_CLOSE'

    CLOSE_ANALYZE = {
        'A': [['i', 'n', 't', ' ', 'B', 'T', ';', 'A'], ['c', 'h', 'a', 'r', ' ', 'B', ';', 'A'], ['^']],
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
        'F': [['B', '<', 'B']],

        # if construct

        'I_CLOSE': [['t', 'f', '(', 'E', ')', '{', 'A']],

        'OPENING': [['}']]

    }
    """
    ----------------------------------------------------------------------------
    """

    try:
        Analyzer_open = analyzer_module.Analyzer(ALPHABETS, OPEN_ANALYZE, OPEN_ANALYZE_START)
        Analyzer_regular = analyzer_module.Analyzer(ALPHABETS, REGULAR_ANALYZE, REGULAR_ANALYZE_START)
        Analyzer_close = analyzer_module.Analyzer(ALPHABETS, CLOSE_ANALYZE, CLOSE_ANALYZE_START)
    except:
        print("COULD NOT MAKE PARSING TABLE")

    min_time = float('inf')
    chunk_size = 8000

    this_time = run(chunk_size)
    print("CHUNK SIZE", chunk_size, "TIME", this_time)

# 11.595202207565308


