import itertools
import string
import os
import re
import time

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

printable = '0123456789abcdefghijklmnopqrstuvwxyzàáâäãåæçéèêëíìîïñóòôöõœúùûüABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÄÃÅÆÇÉÈÊËÍÌÎÏÑÓÒÔÖÕŒÚÙÛÜ!"#$%&\'()*+,-./:;?@[\\]^_`{|}~ \t\n\r\x0b\x0c'

# xor fonction
def xor(data, key):
    return bytes(a ^ b for a, b in zip(data, itertools.cycle(key)))

def findkey(name,cipher_file):
    chars = string.ascii_lowercase # abcdefghijklmnopqrstuvwxyz
    i = 0
    for item in itertools.product(chars, repeat=6):
        i += 1
        key = "".join(item)
        if(i%10000 == 0):
            print(key)
        if tryDecrypt(name,cipher_file,bytes(key, encoding="ansi")):
            return key
    return None

def hasNonPrintable(text_decrypt):
    for char in text_decrypt:
        if char not in printable:
            return True
    return False

def isFrench(text_decrypt, name):
    if hasNonPrintable(text_decrypt):
        return False
    if not verifDico(text_decrypt):
        return False
    return True

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
                wcount += 1
                if wcount == 4:
                    dico.close()
                    print(colors.OKGREEN+ "[+] Key found" + colors.RESET)
                    dico.close()
                    return True
    dico.close()
    return False

def readFile(cipher_file,key,nb_chars=0):
    try:
        with open(cipher_file, 'rb') as encrypt:
            if nb_chars != 0:
                cipher_text = encrypt.read(nb_chars)
            else:
                cipher_text = encrypt.read()
            text = xor(cipher_text, key)
            text = text.decode(encoding="ansi")
            encrypt.close()
            return text
    except NameError as error:
        print(error)
        print(colors.FAIL + "[-] File doesn't  seems to exist" + colors.RESET)

def tryDecrypt(name, cipher_file, key):

    text = readFile(cipher_file, key,100)
    if isFrench(text, name):
        print(colors.OKGREEN+"[+] The key is: ' "+ key.decode() + " '" + colors.RESET)
        writeDecipher(name, text)
        return True

    return False


#Write in file the decrypt text
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
            key = findkey(name, cipher_file)
            if key != None:
                tryDecrypt(name,cipher_file, key)
                break

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))