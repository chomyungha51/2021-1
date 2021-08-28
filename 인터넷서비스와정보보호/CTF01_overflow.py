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
        end = len(problem[start+2:]) - 4

        #Check if I found the right string
        #print(problem[start+2:start+end])

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
        
        numbers = problem[start+2:start+end].split('+')
        
        a = numbers[0]
        b= numbers[1]

        for i in a:
            print('a: ', i)

        for i in b:
            print('b: ', i)


        string = ""
        high = 0
        pre = False
        
        #Both are positive numbers
        if (a[0]!='-' and b[0]!='-'):
            if (len(a) > len(b)):
                longer = a
                shorter = b
            elif (len(a) <len(b)):
                longer = b
                shorter = a
            else:
                if (a[0] > b[0]):
                    longer = a
                    shorter = b
                else:
                    longer = b
                    shorter = a
                    
            s = len(shorter)-1
            l = len(longer)-1

            while (s >= 0 and l >= 0):
                if (s >= 0):
                    cur = int(shorter[s]) + int(longer[l]) + high
                    high = int(cur / 10)
                    cur = int(cur % 10)
                    string = str(cur) + string
                    s -= 1
                    l -= 1
                else:
                    cur = int(longer[l]) + high
                    high = int(cur / 10)
                    cur = int(cur % 10)
                    string = str(cur) + string
                    if (l == 0 and high != 0):
                        string = str(high) + string
                    l -= 1 
            
        #Both are negative numbers
        elif (a[0]=='-' and b[0]=='-'):
            pre = True
            if (len(a[1:]) > len(b[1:])):
                longer = a[1:]
                shorter = b[1:]
            elif (len(a[1:]) <len(b[1:])):
                longer = b[1:]
                shorter = a[1:]
            else:
                if (a[1] > b[1]):
                    longer = a[1:]
                    shorter = b[1:]
                else:
                    longer = b[1:]
                    shorter = a[1:]
                    
            s = len(shorter)-1
            l = len(longer)-1
            
            while(s >= 0 and l >= 0):
                if (s >= 0):
                    cur = int(shorter[s]) + int(longer[l]) + high
                    high = int(cur / 10)
                    cur = int(cur % 10)
                    string = str(cur) + string
                    s -= 1
                    l -= 1
                else:
                    cur = int(longer[l]) + high
                    high = int(cur / 10)
                    cur = int(cur % 10)
                    string = str(cur) + string
                    if (l == 0 and high != 0):
                        string = str(high) + string
                    l -= 1

        #A is positive, B is negative
        elif (a[0]!='-' and b[0]=='-'):
            if (len(a) > len(b[1:])):
                longer = a
                shorter = b[1:]
            elif (len(a) <len(b[1:])):
                longer = b[1:]
                shorter = a
                pre = True
            else:
                if (a[0] > b[1]):
                    longer = a
                    shorter = b[1:]
                else:
                    longer = b[1:]
                    shorter = a
                    pre = True
                    
            s = len(shorter)-1
            l = len(longer)-1

            while(s >= 0 and l >= 0):
                if (s >= 0):
                    cur = int(longer[l]) + int(shorter[s]) - high
                    if (cur < 0):
                        high = 1
                        cur += 10
                    else:
                        high = 0
                    string = str(cur) + string
                    l -= 1
                else:
                    cur = int(longer[l]) - high
                    if (cur < 0):
                        high = 1
                        cur += 10
                    else:
                        high = 0
                    if (l == 0 and high == 0):
                        break
                    string = str(cur) + string
                    l -= 1
                
            
        #A is negative, B is positive
        else:
            if (len(a[1:]) > len(b)):
                longer = a[1:]
                shorter = b
                pre = True
            elif (len(a[1:]) <len(b)):
                longer = b
                shorter = a[1:]
            else:
                if (a[1] > b[0]):
                    longer = a[1:]
                    shorter = b
                    pre = True
                else:
                    longer = b
                    shorter = a[1:]
                    
            s = len(shorter)-1
            l = len(longer)-1

            while(s >= 0 and l >= 0):
                if (s >= 0):
                    cur = int(longer[l]) + int(shorter[s]) - high
                    if (cur < 0):
                        high = 1
                        cur += 10
                    else:
                        high = 0
                    string = str(cur) + string
                    s -= 1
                    l -= 1
                else:
                    cur = int(longer[l]) - high
                    if (cur < 0):
                        high = 1
                        cur += 10
                    else:
                        high = 0
                    if (l == 0 and high == 0):
                        break
                    string = str(cur) + string
                    l -= 1
                    
        #Overflow Check
        if (len(string) >= 10 and string > '2147483647'):
            answer = ""
            high = 0
            s = 9
            l = len(string)-1
            '''
            while(s >= 0 and l >= 0):
                if (s >= 0):
                    cur = int(longer[l]) + int(shorter[s]) - high
                    if (cur < 0):
                        high = 1
                        cur += 10
                    else:
                        high = 0
                    answer = str(cur) + answer
                    s -= 1
                    l -= 1
                else:
                    cur = int(longer[l]) - high
                    if (cur < 0):
                        high = 1
                        cur += 10
                    else:
                        high = 0
                    if (l == 0 and high == 0):
                        break
                    answer = str(cur) + answer
                    l -= 1
            '''
            if(pre == False):
                answer = -2147483647 + int((int(string) - 2147483647)%2147483647) + 1
                answer = '-' + answer
            else:
                answer = 2147483647 + int((int(string) + 2147483647)%2147483647) + 1

        else:
            answer = string
            if(pre == True):
                answer = '-' + answer
                
        #Send the answer
        p.sendline(answer)

    #LV5:
    else:
        point = problem.rfind(": ")
        temp = problem[point:-6]
        print(temp)
        

#p.interactive()

