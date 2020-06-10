grammar metabed;


bed
    : HEADER '\n\n' LINE '\n'
    chrom '\n'
    coordinate '\n'
    name '\n'
    score '\n'
    strand '\n'
    thickStart '\n'
    thickEnd '\n'
    itemRgb '\n'
    blockCount '\n'
    blockSizes '\n'
    blockStarts '\n'
    chromName '\n'
    CHAR '\n'
    NUMBER '\n'
    NUM255 '\n'
    NUM '\n'
    NUM3 '\n'
    SEPARATOR '\n'
    ;

HEADER
    : 'grammar bed;'
    ;

LINE
    : 'line\n' (
    '\t: (chrom SEPARATOR coordinate)+\n'
    | '\t: (chrom SEPARATOR coordinate SEPARATOR name \'\\n\')+\n'
    | '\t: (chrom SEPARATOR coordinate SEPARATOR name SEPARATOR score \'\\n\')+\n'
    | '\t: (chrom SEPARATOR coordinate SEPARATOR name SEPARATOR score SEPARATOR strand \'\\n\')+\n'
    | '\t: (chrom SEPARATOR coordinate SEPARATOR name SEPARATOR score SEPARATOR strand SEPARATOR thickStart \'\\n\')+\n'
    | '\t: (chrom SEPARATOR coordinate SEPARATOR name SEPARATOR score SEPARATOR strand SEPARATOR thickStart SEPARATOR thickEnd \'\\n\')+\n'
    | '\t: (chrom SEPARATOR coordinate SEPARATOR name SEPARATOR score SEPARATOR strand SEPARATOR thickStart SEPARATOR thickEnd SEPARATOR itemRgb \'\\n\')+\n'
    )
    ';'
    ;

CHAR
    : 'CHAR\n'
    '\t:(\'a\' .. \'z\') | (\'A\' .. \'Z\') | \'_\' | NUM;'
    ;

NUMBER
    : 'NUMBER\n'
    '\t: NUM+;'
    ;

NUM255
    : 'NUM255\n'
    '\t: NUM | NUM NUM | (\'2\' NUM \'0\' .. \'4\' | \'25\' \'0\' .. \'5\');'
    ;

NUM
    : 'NUM\n'
    '\t: \'0\' .. \'9\';'
    ;

NUM3
    : 'NUM3\n'
    '\t: \'0\' .. \'3\';'
    ;

SEPARATOR
    : 'SEPARATOR\n'
    '\t: \'\\t\' | \' \'+; '
    ;

chrom
    : 'chrom\n'
    '\t: ' ('CHAR+' | 'chromName' | 'CHAR+ | chromName') ';'
    ;

coordinate
    : 'coordinate\n'
    '\t:'
'{\n'
'from random import randint, random\n'
'start, end = randint(0, 1e6), randint(0, 1e6)\n'
'chance = random()\n'
'while random < 0.999 and start > end:\n'
'    start, end = randint(0, 1e6), randint(0, 1e6)\n'
'current += self.create_node(UnlexerRule(src=str(start)))\n'
'}\n'
'\tSEPARATOR\n'
'{\n'
'current += self.create_node(UnlexerRule(src=str(end)))\n'
'self.start = start\n'
'self.end = end\n'
'}\n'
    '\t;'
    ;

name
    : 'name\n'
    '\t: CHAR+;'
    ;

score
    : 'score\n'
    '\t: ' (('NUM | NUM NUM | NUM NUM NUM | \'1000\'') | ('NUM | NUM NUM | NUM NUM NUM | \'1000\' | NUM \'.\' NUM+') | 'NUM*')
    ';'
    ;

strand
    : 'strand\n'
    '\t: ' ('\'+\' | \'-\' | \'.\'' | '\'+\' | \'-\'') ';'
    ;

thickStart
    : 'thickStart\n'
    '\t: NUMBER;'
    ;

thickEnd
    : 'thickEnd\n'
    '\t: NUMBER;'
    ;

itemRgb
    : 'itemRgb\n'
    ('\t: \'0\'\n'
    '\t| NUM255 \',\' NUM255 \',\' NUM255;'
    | '\t: NUM255 \',\' NUM255 \',\' NUM255;')
    ;

blockCount
    : 'blockCount\n'
    '\t: NUM;'
    ;

blockSizes
    : 'blockSizes\n'
    ('\t: (NUMBER \',\')* NUMBER'
    | '\t: (NUMBER \',\')+' )
    ';'
    ;

blockStarts
    : 'blockStarts\n'
    ('\t: (NUMBER \',\')* NUMBER'
    | '\t: (NUMBER \',\')+' )
    ';'
    ;

chromName
    : 'chromName\n'
    '\t: \'chr\' (( NUM | \'1\' NUM | \'2\' NUM3) | \'X\' | \'Y\' | \'M\');'
    ;
