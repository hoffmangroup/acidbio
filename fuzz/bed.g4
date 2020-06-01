grammar bed;

chrom
    : CHAR+ | ('chr' NUMBER)
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