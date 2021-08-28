from pwn import *

#Run the file "automation"
p = process("./automation")

#There are five levels
for i in range(5):
    
    #Read and show the problem
    problem = p.recvuntil('\n\n').decode()
    print(problem)

    #LV1:hex_to_int
    if (i == 0):
        #Find the start and end index of target hex string
        start = problem.rfind('0x')
        end = len(problem[start+7:]) - 4

        #Change the string to decimal number and casting to string
        num = str(int(problem[start+2:start+end], 16))

        #Send the answer
        p.sendline(num)

    #LV2:str_to_hex
    elif (i == 1):
        #Get the 8 characters from the text
        start = problem.rfind(' ')
        string = problem[start+6:start+14]

        #Change the characters to ASCII,cast into hex, and then concanate
        hexa = ""
        for j in string:
            hexa += hex(ord(j))[2:]

        #Send the answer
        p.sendline(hexa)
        
    #LV3:hex_to_str
    elif (i == 2):
        #Get the start and end index of the hex string
        start = problem.rfind('0x')
        end = len(problem[start+2:]) - 4
        string = ""
        pre = "0x"
        hexa = problem[start+2:start+end]

        #Casting digits into string
        for h in range(int(len(hexa)/2)):
            cur = ""
            cur = pre + hexa[2*h:2*h+2]
            string += str(chr(int(cur,16)))

        #Send the answer
        p.sendline(string)

    #LV4:overflow addition
    elif (i == 3):
        #Get two numbers from text
        start = problem.rfind(': ')
        end = len(problem[start+2:]) - 4
        
        numbers = problem[start+7:start+end].split('+')
        
        a = numbers[0]
        b = numbers[1]


        string = ""
        high = 0
        pre = False
        answer = int(a) + int(b)

        #Overflow Check
        while (answer < -2147483647 or answer > 2147483647):
            if (answer < -2147483647):
                diff = answer + 2147483647 - 1
                answer = 2147483647 - diff
            elif (answer > 2147483647):
                diff = answer - 2147483647 - 1
                answer = -2147483647 + diff
                
        #Send the answer
        p.sendline(str(answer))

    #LV5:
    else:
        point = problem.rfind(": ")
        temp = problem[point+7:-7],split(" ")
        temp = [int(i) for i in temp]
        temp.sort()
        for i in temp:
            var = str(i) + ' '
            p.send(val)
        print(p.recv().decode())
    

