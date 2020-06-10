grammar bed;

line
    : (chrom SEPARATOR coordinate)+
    | (chrom SEPARATOR coordinate SEPARATOR name '\n')+
    | (chrom SEPARATOR coordinate SEPARATOR name SEPARATOR score '\n')+
    | (chrom SEPARATOR coordinate SEPARATOR name SEPARATOR score SEPARATOR strand '\n')+
    | (chrom SEPARATOR coordinate SEPARATOR name SEPARATOR score SEPARATOR strand SEPARATOR thickStart '\n')+
    | (chrom SEPARATOR coordinate SEPARATOR name SEPARATOR score SEPARATOR strand SEPARATOR thickStart SEPARATOR thickEnd'\n')+
    | (chrom SEPARATOR coordinate SEPARATOR name SEPARATOR score SEPARATOR strand SEPARATOR thickStart SEPARATOR thickEnd SEPARATOR itemRgb '\n')+
    | (chrom SEPARATOR coordinate SEPARATOR name SEPARATOR score SEPARATOR strand SEPARATOR thickStart SEPARATOR thickEnd SEPARATOR itemRgb SEPARATOR blockCount SEPARATOR blockSizes '\n')+
    | (chrom SEPARATOR coordinate SEPARATOR name SEPARATOR score SEPARATOR strand SEPARATOR thickStart SEPARATOR thickEnd SEPARATOR itemRgb SEPARATOR blockCount SEPARATOR blockSizes SEPARATOR blockStarts'\n')+
    ;

chrom
    : CHAR+ | chromName
    ;

coordinate
    : 
{ 
from random import randint, random
start, end = randint(0, 1e6), randint(0, 1e6)
chance = random()
while chance < 0.999 and start > end:
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
    : CHAR+
    ;

score
    : NUM | NUM NUM | NUM NUM NUM | '1000'
    ;

strand
    : '+' | '-' | '.'
    ;

thickStart
    :
{
from random import randint, random
chance = random()
if chance < 0.999:
    start = randint(self.start, self.end)
else:
    start = randint(0, 1e6)
self.tStart = start
current += self.create_node(UnlexerRule(src=str(start)))
}
    ;

thickEnd
    : 
{
from random import randint, random
chance = random()
if chance < 0.999:
    end = randint(self.tStart, self.end)
else:
    end = randint(0, 1e6)
self.tEnd = end
current += self.create_node(UnlexerRule(src=str(end)))
}
    ;

itemRgb
    : '0'
    | NUM255 ',' NUM255 ',' NUM255
    ;

blockCount
    : NUM
{
self.bCount = int(current)
}
    ;

blockSizes
    :
{
if self.unlexer.max_depth >= 2:
    for _ in range(self.bCount - 1):
        current += self.unlexer.NUMBER()
        current += self.create_node(UnlexerRule(src=','))
}
    NUMBER
{
if self.bCount <= 1:
    self.lastBlock = int(str(current))
else:
    self.lastBlock = int(str(current)[str(current).rfind(',') + 1:])
}
    ;

blockStarts
    : 
{
if self.unlexer.max_depth >= 2:
    for _ in range(self.bCount - 1):
        current += self.unlexer.NUMBER()
        current += self.create_node(UnlexerRule(src=','))

from random import random
if random() < 0.999:    
    current += self.create_node(UnlexerRule(src=str(self.end - self.lastBlock)))
else:
    current += self.unlexer.NUM()
}
    ;

chromName
    : 'chr' (NUM | '1' NUM | '2' NUM3 | ('X' | 'Y' | 'M'))
    ;

CHAR
    : ('a' .. 'z') | ('A' .. 'Z') | '_' | NUM
    ;


NUMBER
    : NUM+
    ;

NUM255
    : NUM | NUM NUM | ('2' NUM '0' .. '4' | '25' '0' .. '5')
    ;

NUM
    : '0' .. '9'
    ;

NUM3
    : '0' .. '3'
    ;

SEPARATOR
    : '\t'
    ;