cat keys.txt | while IFS= read -r line; do echo "$line" | ./chall; done
