for X in c{a..z}{a..z}{a..z}{a..z}; do
  OUTPUT=`openssl enc -aes-128-ecb -d -a -nosalt -base64 -pass pass:$X -in flag.txt.enc -md sha256 2> /dev/null`
  echo $X
  if [[ $OUTPUT == *"flag{"* ]]; then
    echo $OUTPUT
    echo $X
    echo 2
    break
  fi
done
echo 1