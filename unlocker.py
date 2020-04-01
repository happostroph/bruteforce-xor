import itertools
import string
import os
import re

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0;0m'

# xor fonction
def xor(data, key):
    return bytes(a ^ b for a, b in zip(data, itertools.cycle(key)))

def genkey():
    chars = string.ascii_lowercase # abcdefghijklmnopqrstuvwxyz
    for item in itertools.product(chars, repeat=6):
        print( "".join(item))

#def findWord(w, t):
    #return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def verifDico(text_decrypt):
    wcount = 0
    try:
        with open("liste_francais.txt", "r") as dico:
            words = [line.rstrip() for line in dico]
    except:
        print(colors.FAIL + "[-] Dictionnary doesn't  seems to exist" + colors.RESET)
    
    for word in words:
        reg = re.compile(r'\b' + re.escape(word) + r'\b', flags=re.IGNORECASE)
        if len(word) > 3:
            if reg.search(text_decrypt):
                print(colors.OKGREEN+"[+] Word found: "+ word + colors.RESET)
                wcount += 1
                if wcount == 10:
                    dico.close()
                    print(colors.OKGREEN+ "[+] Key found" + colors.RESET)
                    dico.close()
                    return True
     
    print(colors.WARNING+ "[?] Not enought word found :"+ str(wcount) + " ,change the file to test " + colors.RESET)
    dico.close()
    return False

def tryDecrypt(name, cipher_file, key = b'diidju'):
    try:
        with open(cipher_file, 'rb') as encrypt:
            cipher_text = encrypt.read()
            text = xor(cipher_text, key)
            text = text.decode(encoding="ansi")
            encrypt.close()

            print(colors.OKBLUE+ "[+] file " + cipher_file + " tried" + colors.RESET)

            if verifDico(text):
                print(colors.OKGREEN+"[+] The key is: ' "+ key.decode() + " '" + colors.RESET)
                writeDecipher(name, text)
    except:
        print(colors.FAIL + "[-] File doesn't  seems to exist" + colors.RESET)

def writeDecipher(name, decipher_text):
    file_to_write = "decode/decode_"+ name
    try:
        with open(file_to_write, 'wb') as decrypt:
            decrypt.write(decipher_text.encode(encoding="ansi"))
            print(colors.OKGREEN+"[+] Text "+ name +" decrypt "+ colors.RESET)
            decrypt.close()
    except:
        print(colors.FAIL + "[-] Fail to right decoded file" + colors.RESET)

def main():
    for root, dirs, files in os.walk("fichier"):
        for name in files:
            cipher_file = os.path.join(root, name)

            decipher_text = tryDecrypt(name, cipher_file)

if __name__ == "__main__":
    main()