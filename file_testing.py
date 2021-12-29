def points_of_divisions(buffer, line_no):
    

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

        print("Received", buffer)

        partitions = []
        pointer_1 = -1
        pointer_2 = len(buffer)

        for i in range(len(buffer) - 1):
            # print("working on", buffer[i])

            if buffer[i: i + 2] == 'tf':
                # partition 1 not required
                break
                
            if buffer[i] == '}':
                # partition is required
                pointer_1 = i
                break

        
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
                str(line_no) + '_' + 'a'
            ],

            [
                buffer[pointer_1 + 1: pointer_2],
                'REGULAR_ANALYZE',
                str(line_no) + '_' + 'b'
            ],

            [
                buffer[pointer_2: ],
                'CLOSE_ANALYZE',
                str(line_no) + '_' + 'c'
            ],
        ]

        return res

if __name__ == '__main__':

    source_code = open("input1.txt", "r")
    line_no = 1
    

    buffer = []
    for line in source_code:
       

        line = line.replace('\n', '').strip()  # removing obvious '\n'



        line_no += 1
        buffer.append(line)

        if line_no % 8 == 0:
            nw_buffer = ''.join(buffer)
            buffer = []
            res = points_of_divisions(nw_buffer, line_no)
            print("returned", res)

