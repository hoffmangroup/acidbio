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
    : NUMBER SEPARATOR NUMBER
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
    : NUMBER
    ;

thickEnd
    : NUMBER
    ;

itemRgb
    : '0'
    | NUM255 ',' NUM255 ',' NUM255
    ;

blockCount
    : NUM
    ;

blockSizes
    : (NUMBER ',')* NUMBER
    ;

blockStarts
    : (NUMBER ',')* NUMBER
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