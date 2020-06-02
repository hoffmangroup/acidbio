grammar bed;

line
    : (chrom '\t' coordinate '\t' name '\n')+
    | (chrom '\t' coordinate '\t' name '\t' score '\n')+
    | (chrom '\t' coordinate '\t' name '\t' score '\t' strand '\n')+
    ;

chrom
    : CHAR+ | chromName
    ;

coordinate
    : NUMBER '\t' NUMBER NUM
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

chromName
    : 'chr' (( NUM | '1' NUM | '2' NUM3) | 'X' | 'Y' | 'M')
    ;

CHAR
    : ('a' .. 'z') | ('A' .. 'Z') | '_' | NUM
    ;


NUMBER
    : NUM+
    ;

NUM
    : '0' .. '9'
    ;

NUM3
    : '0' .. '3'
    ;