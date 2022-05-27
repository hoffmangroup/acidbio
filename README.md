# Acidbio

> Niu YN, Roberts EG, Denisko D, Hoffman MM. 2022. [Assessing and assuring interoperability of a genomics file format](https://doi.org/10.1093/bioinformatics/btac327). *Bioinformatics*, btac327. [https://doi.org/10.1093/bioinformatics/btac327](https://doi.org/10.1093/bioinformatics/btac327)

The BED test harness runs tools with a command-line interface against a test suite of expected success and expected fail BED files.
The test suite aims to improve interoperability of software parsing the BED format as input.

## Installation

To run the test harness, Python 3.5+ is required. The PyYAML package is required for parsing the configuration file.
To install PyYAML, run `python3 -m pip install -r bed/requirements.txt`. 
Alternatively, PyYAML can also be installed using Conda by `conda install -c conda-forge pyyaml`.

For testing your own software, clone the repository.

For reproducing results from the 80 packages tested in *Assessing and assuring interoperability of a genomics file format*, download the repository from [Zenodo](
https://doi.org/10.5281/zenodo.5784763). The Zenodo contains the files in this repository along with the Conda environments used to test the 80 packages.
For reproducing the results, Conda is required as we tested tools found on Bioconda.

## Quickstart

To test your own software, set up the `config.yaml` file and run the test harness as described below.
Conda is not required for testing your own software.

### `config.yaml`

The `config.yaml` file is required to run the test harness.
The configuration file must be placed in the `bed` directory.

The configuration file used to test the 80 packages is provided in this repository as a template.

The test harness configuration contains three sections:

**`file-locations`**

This section of the configuration file describes where secondary files are located.
For example, if the tool requires a BAM file, then you may specify the location by

```YAML
settings:
    file-locations:
        BAM: data/toy.bam
```

If you are testing your own software, you do not have to use the files provided in the `bed/data` directory.
You can replace them with a file that best suites your needs.

Not all secondary files are uploaded to this repository. Namely, `hg38.fa` is too large but can be obtained using
```
wget http://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz
```
Then, unzip the file using
```
gunzip hg38.fa.gz
```
Finally, place `hg38.fa` into the `bed/data` directory.

**`tools`**

This section lists the tools for testing with its command-line interface.
In the command-line interface, replace instances of the input BED file with `FILE` and instances of other file formats with the corresponding macro from `file-locations`.
For tools that use multiple BED files, you may reuse the BED file by having `FILE` appear multiple times in the command-line interface.
Alternatively, there are other BED files availabe in the `bed/data` directory called `intersect_file03.bed` to `intersect_file12.bed` for each BED variant that have the same format as the standard BED file test case (`03-standard_chrom.bed`).
For tools that require an output directory, you should use `TEMPDIR/` as the directory.
The test harness will replace TEMPDIR with a temporary directory that is deleted after the tool finishes testing.

For example, Samtools has a tool called bedcov that uses a BAM file and BED file. It could be listed as:

```YAML
tools:
    - samtools:
        bedcov: samtools bedcov FILE BAM
```

**`conda-environment`**

This section maps each package to the Conda environment that the package is installed in.
If the tool is not installed in a Conda environment, then leave the value blank.
For example, if Samtools is installed in the environment "test_env", then it would be listed as:
```YAML
conda-environment:
    samtools: test_env
```

For a tool not installed in a Conda environment:
```YAML
conda-environment:
    my-tool: 
```

### Example
To run the test harness on Samtools, first create a new Conda environment using `conda create -n test_env` and activate it with `conda activate test_env`. Then, install Samtools using `conda install -c bioconda samtools`.
Finally, the use the configuration file below to specify the execution of Samtools from command line and save the file as `config.yaml` in the `bed` directory.
```YAML
settings:
    file-locations:
        BAM: data/toy.bam
tools:
    - samtools:
        bedcov: samtools bedcov FILE BAM
conda-environment:
    samtools: test_env
```


### Running the test harness

The test harness is run against one BED variant (BED03 to BED12).
You must specify which BED variant to run and directory to output the result files to.
First, navigate into the `bed` directory of the repository.
Within the `bed` directory, to run the test harness, run the following:

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
                        output binary results to file. If unspecified, no
                        binary results will be outputted.
  --failed-good GOOD_TESTS_FILENAME
                        output incorrect good test cases to file
  --passed-bad BAD_TESTS_FILENAME
                        output incorrect bad test cases to file
```

The `failed-good` output file contains the tested tool's output from expected pass test cases that the tool incorrectly failed. The `passed-bad` output file contains the tested tool's output from expected fail test cases that the tool incorrectly passed. The `results-array-file` is used only for collecting results for visualization.
For just testing a tool against the test suite, this option should not be specified.


### Troubleshooting

- If the software cannot run correctly, the test harness will always show that the software failed on each test case.
- If the test harness does not output anything, it could be because the current Conda environment and the Conda environment in `config.yaml` do not match.

## BED badge

After testing software on the test harness, you may display a GitHub badge to indicate your software's conformance to the BED specification.

Using [shields.io](https://shields.io/), you may configure a badge that describes which BED variants your software parses.
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
