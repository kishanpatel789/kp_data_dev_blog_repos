
FILE="spells.txt"

sed '=' "$FILE" | head

sed 'a hello' "$FILE"

sed '1a i love you' "$FILE"

sed 'i hello' "$FILE"

sed '1,3d' $FILE | head

cat spells.txt | sed 's|Lumos|Lumos Maxima|' 

sed 's/^/Spell: /' spells.txt

cat spells_messy.txt
sed 's/\s*#.*// ; /^$/d ; s/^\s*//' spells_messy.txt

sed '/e/a blah' spells.txt

sed '/Exp/ p' spells.txt

sed -n '/Exp/ p' spells.txt

sed '=' spells.txt

sed '4s/.*/& FOREVER/' spells.txt

sed '3 d' spells.txt
sed '3! d' spells.txt

sed '1,3 d' spells.txt
cat spells.txt

sed -i '1,3 d' spells.txt
cat spells.txt

sed '/Expecto/ d' spells.txt

sed '4 q' spells.txt

sed '/Expelliarmus/ q' spells.txt

