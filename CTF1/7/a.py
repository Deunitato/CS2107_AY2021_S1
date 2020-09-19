import os
import subprocess
from itertools import product
from string import ascii_lowercase

def main():
    for i in product(ascii_lowercase, repeat=4):
        x = 'f' + ''.join(i)
        password = 'pass:' + x
        print(password)
        MyOut = subprocess.Popen(['openssl', 'enc', '-d', '-aes-128-ecb', '-nosalt', '-base64', '-pass', password, '-in', 'flag.txt.enc', '-out', 'flag.txt', '-md', 'sha256'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout,stderr = MyOut.communicate()
        if b"bad" not in stdout:
            # Success
            f = open('flag.txt', 'r')     
            lines = f.readline()
            print(password)
            if "flag" in lines:
            	output = open('output.txt', 'a')
            	ans = 'password: ' + x + ' ' + lines + '\n'
            	print(ans)
            	output.write(ans)

if __name__ == "__main__":
    main()
