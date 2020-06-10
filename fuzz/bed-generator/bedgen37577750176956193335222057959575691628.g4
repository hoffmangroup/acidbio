grammar bed;

line
	: (chrom SEPARATOR coordinate SEPARATOR name SEPARATOR score '\n')+
;
chrom
	: CHAR+ | chromName;
coordinate
	:{
from random import randint, random
start, end = randint(0, 1e6), randint(0, 1e6)
chance = random()
while random < 0.999 and start > end:
    start, end = randint(0, 1e6), randint(0, 1e6)
current += self.create_node(UnlexerRule(src=str(start)))
}
	SEPARATOR
{
current += self.create_node(UnlexerRule(src=str(end)))
self.start = start
self.end = end
}
	;
name
	: CHAR+;
score
	: NUM | NUM NUM | NUM NUM NUM | '1000';
strand
	: '+' | '-' | '.';
thickStart
	: NUMBER;
thickEnd
	: NUMBER;
itemRgb
	: '0'
	| NUM255 ',' NUM255 ',' NUM255;
blockCount
	: NUM;
blockSizes
	: (NUMBER ',')* NUMBER;
blockStarts
	: (NUMBER ',')+;
chromName
	: 'chr' (( NUM | '1' NUM | '2' NUM3) | 'X' | 'Y' | 'M');
CHAR
	:('a' .. 'z') | ('A' .. 'Z') | '_' | NUM;
NUMBER
	: NUM+;
NUM255
	: NUM | NUM NUM | ('2' NUM '0' .. '4' | '25' '0' .. '5');
NUM
	: '0' .. '9';
NUM3
	: '0' .. '3';
SEPARATOR
	: '\t' | ' '+; 
