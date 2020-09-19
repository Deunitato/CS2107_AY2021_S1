#!/bin/bash

for X1 in {a..z}; do
    for X2 in {a..z}; do
        for X3 in {a..z}; do
            for X4 in {a..z}; do
                for X5 in {a..z}; do
                    OUTPUT=`openssl enc -aes-128-ecb -d -a -nosalt -base64 -pass pass:$X1$X2$X3$X4$X5 -in flag.txt.enc -md sha256`
                    echo $X1$X2$X3$X4$X5
                    if [[ $OUTPUT == *"flag{"* ]]; then
                        echo $OUTPUT
                        echo $X0$X1$X2$X3$X4
                        break
                    fi
                done
            done
        done
    done
done
echo 1