# Description
The BED test harness runs tools with a command-line interface against a test suite of expected success and expected fail BED files.
The test suite aims to improve interoperability of software parsing the BED format as input.

## `config.yaml`

The test harness configuration contains three sections:

**`file-locations`**

This section of the configuration file describes where secondary files are located.
For example, if the tool requires a BAM file, then you may specify the location by

```YAML
settings:
    file-locations:
        BAM: data/example.bam
```

Not all secondary files are uploaded to this repository. Namely, `hg38.fa` is too large but can be obtained on the [UCSC Website](https://hgdownload.cse.ucsc.edu/goldenpath/hg38/bigZips/).

**`tools`**

This section lists the tools for testing with its command-line interface.
In the command-line interface, replace instances of the input BED file with `FILE` and instances of other file formats with the corresponding macro from `file-locations`.
For example, Bazam, a tool that uses a BAM file and BED file, could be listed as:

```YAML
tools:
    - bazam:
        bazam: bazam -bam BAM -L FILE 
```

**`conda-environment`**

This section maps each package to the Conda environment that the package is installed in.
If the tool is not installed in a Conda environment, then leave the value blank.
For example, if Bazam is installed in the environment "test_env", then it would be listed as:
```YAML
conda-environment:
    bazam: test_env
```

The configuration file used to test the 80 packages is provided in this repository as a template.


## Running the test harness

The test harness is run against one BED variant (BED03 to BED12).
You must specify which BED variant to run and directory to output the result files to.
The basic execution of the test harness is:

```bash
python3 bedrunall.py BED03 ./
```
This will run the test harness on BED3 tests and log the outputs to the current directory.

The full usage of the test harness is:
```
usage: bedrunall.py [-h] [-V] [-v] [-t TOOL] [-e EXCLUDE]
                    [--results-array-file RESULTS_FILENAME]
                    [--failed-good GOOD_TESTS_FILENAME]
                    [--passed-bad BAD_TESTS_FILENAME]
                    bed-version outdir

Tests the tools in config.yaml to see if they appropriately throw warnings or
errors against a suite of BED files

positional arguments:
  bed-version           Which BED type to test. Must be one of BED03, BED04,
                        ..., BED12
  outdir                location where all output files go

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -v, --verbose         display all results
  -t TOOL, --tool TOOL  test a specific program. If unspecified, all tools in
                        config.yaml will be tested.
  -e EXCLUDE, --exclude EXCLUDE
                        test all tools except for this tool. If unspecified,
                        all tools will be tested
  --results-array-file RESULTS_FILENAME
                        output binary results to file
  --failed-good GOOD_TESTS_FILENAME
                        output incorrect good test cases to file
  --passed-bad BAD_TESTS_FILENAME
                        output incorrect bad test cases to file
```

The `failed-good` output file contains the tested tool's output from expected pass test cases that the tool incorrectly failed. The `passed-bad` output file contains the tested tool's output from expected fail test cases that the tool incorrectly passed. The `results-array-file` is used only for collecting results for visualization.
For just testing a tool against the test suite, this file should be ignored.

## BED badge

After testing software on the test harness, you may display a GitHub badge to indicate your software's conformance to the BED specification.

Using [shields.io](shields.io), you may configure a badge that describes which BED variants your software parses.
For example, the following badge indicates that the software parses BED3, BED4, or BED6 files.

![BED Parser](https://img.shields.io/badge/BED%20Parser-BED3%20%7C%20BED4%20%7C%20BED6-informational)

You may also add a badge that indicates your software's performance on the test suite.
For example, the following badges indicate differing levels of performance on BED6 tests.

![BED Performance BAD](https://img.shields.io/badge/BED6-61.5%25-red)
![BED Performance](https://img.shields.io/badge/BED6-80.7%25-yellow)
![BED Performance](https://img.shields.io/badge/BED6-100%25-success)


We suggest that performance of $\leq$ 70% be given `red` background color, performance between 70% and 100% be given `yellow` background color, and performance of 100% be given `success` background color.


# License
acidbio is free software: you can redistribute it and/or modify it under the terms of version 2 of the GNU General Public License as published by the Free Software Foundation.

acidbio is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.

# Contact
`michael.hoffman at utoronto dot ca`