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
    NUM2 '\n'
    SEPARATOR '\n'
    ;

HEADER
    : 'grammar bed;'
    ;

LINE
    : 'line\n' (
    '\t: (chrom SEPARATOR coordinate\'\\n\')+\n'
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

NUM2
    : 'NUM2\n'
    '\t: \'0\' .. \'2\';'
    ;

SEPARATOR
    : 'SEPARATOR\n'
    ('\t: \'\\t\' | \' \' \' \'+; ' | '\' \' \' \'+;' |
    | '\t: \'\\t\';' | '\t: \'\\t\';' |  '\t: \'\\t\';' |  '\t: \'\\t\';')
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
    'while chance < 0.999 and start > end:\n'
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
    : 'thickStart:\n'
    '{\n'
    'from random import randint, random\n'
    'chance = random()\n'
    'if chance < 0.999 and self.start <= self.end:\n'
    '    start = randint(self.start, self.end)\n'
    'else:\n'
    '    start = randint(0, 1e6)\n'
    'self.tStart = start\n'
    'current += self.create_node(UnlexerRule(src=str(start)))\n'
    '}\n'
    '\t;'
    ;

thickEnd
    : 'thickEnd:\n'
    '{'
    'from random import randint, random\n'
    'chance = random()\n'
    'if chance < 0.999 and self.tStart <= self.end:\n'
    '    end = randint(self.tStart, self.end)\n'
    'else:\n'
    '    end = randint(0, 1e6)\n'
    'self.tEnd = end\n'
    'current += self.create_node(UnlexerRule(src=str(end)))\n'
    '}\n'
    '\t;'
    ;

itemRgb
    : 'itemRgb\n'
    ('\t: \'0\'\n'
    '\t| NUM255 \',\' NUM255 \',\' NUM255;'
    | '\t: NUM255 \',\' NUM255 \',\' NUM255;')
    ;

blockCount
    : 'blockCount\n'
    ('\t: \'1\' .. \'4\'\n' | '\t" NUM\n')
    '{\n'
    'self.bCount = int(current)\n'
    '}\n'
    '\t;'
    ;

blockSizes
    : 'blockSizes:\n'
    (
    '{\n'
    'if self.unlexer.max_depth >= 2:\n'
    '    for _ in range(self.bCount - 1):\n'
    '        current += self.unlexer.NUMBER()\n'
    '        current += self.create_node(UnlexerRule(src=\',\'))\n'
    '}\n'
    '\tNUMBER\n'
    '{\n'
    'if self.bCount <= 1:\n'
    '    self.lastBlock = int(str(current))\n'
    'else:\n'
    '    self.lastBlock = int(str(current)[str(current).rfind(\',\') + 1:])\n'
    '}\n'
    ';'
    |
    '{\n'
    'if self.unlexer.max_depth >= 2:\n'
    '    for _ in range(self.bCount):\n'
    '        current += self.unlexer.NUMBER()\n'
    '        current += self.create_node(UnlexerRule(src=\',\'))\n'
    '}\n'
    '{\n'
    'if self.bCount == 1:\n'
    '    self.lastBlock = int(str(current))\n'
    'elif self.bCount == 0:\n'
    '    self.lastBlock = 0\n'
    'else:\n'
    '    self.lastBlock = int(str(current)[str(current).rfind(\',\') + 1:])\n'
    '}\n'
    ';'
    )
    ;

blockStarts
    : 'blockStarts:\n'
    '{\n'
    'if self.unlexer.max_depth >= 2:\n'
    '    for _ in range(self.bCount - 1):\n'
    '        current += self.unlexer.NUMBER()\n'
    '        current += self.create_node(UnlexerRule(src=\',\'))\n'

    'from random import random\n'
    'if random() < 0.999:\n'
    '    current += self.create_node(UnlexerRule(src=str(self.end - self.lastBlock)))\n'
    'else:\n'
    '    current += self.unlexer.NUM()\n'
    '}\n'
    ';'
    ;

chromName
    : 'chromName\n'
    ('\t: \'chr\' ( \'1\' .. \'9\' | \'1\' NUM | \'2\' NUM2 | (\'X\' | \'Y\' | \'M\'));'
    | '\t: \'chr\' ( \'1\' .. \'9\' | \'1\' NUM | \'2\' NUM2);')
    ;
