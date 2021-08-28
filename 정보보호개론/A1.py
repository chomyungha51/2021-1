
#Encyption
def encyption(text, n):
    text = text.lower()
    res = ""
    for i in text:
        new = ord(i) + n
        if (new > 122):
            new -= 26
        res += chr(new)
    return res
        

#Decryption
def decryption(text, n):
    new = 0
    text = text.lower()
    res = ""
    for i in text:
        new = ord(i) - n
        if (new < 97):
            new += 26
        res += chr(new)
    return res
    
#Get plaintext and shift pattern
plainText = input("Enter the plaintext: ")
N = int(input("Enter the shift pattern: "))

#Print the ciphertext
ciphertext = encyption(plainText, N)
print(ciphertext)

#Print the plaintext
plaintext = decryption(ciphertext, N)
print(plaintext)
