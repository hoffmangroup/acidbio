# Test cases that should not raise errors

## Simpler Cases:

- #1: A file with annotations that should be irrelevant to main functions (intersect, merge, complement)
- #2: A file with unsorted entries should still work under complement, intersect
- #3: A file with no data in it should still work
- #4: tagAlign file format should still work (because it's a subset of BED)
- #5: broadPeak should work
- #6: gappedPeak should work so long as it's specified. It does have 3 extra features over regular BED
- #7: narrowPeak should work
- #8: A big file ~50 MB should work. Don't know how to move files onto mordor
so no file will exist here right now

