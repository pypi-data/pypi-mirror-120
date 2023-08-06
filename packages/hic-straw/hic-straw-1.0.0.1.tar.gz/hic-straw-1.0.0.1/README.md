
# Straw: rapidly stream data from .hic files

Straw is library which allows rapid streaming of contact data from .hic files. Besides Python, there are C++, R, Matlab, Java and Javascript versions of Straw.

- For the Python, C++, R, Matlab versions of Straw, see: https://github.com/aidenlab/straw
- For the Java version of Straw, see: https://github.com/aidenlab/java-straw/
- For the Javascript version of Straw, see: https://github.com/igvteam/hic-straw/


## Quick Start Python

To install Straw type: pip install straw

Then import the module via **import straw** and run it using either **straw.straw** or **straw.strawC**.

### API Usage

straw.straw("observed/oe/expected", "normalization", "hicFile(s)", "region1", "region2", "units", "binsize")

1. observed/oe/expected - observed, expected or observed/expected (oe) contacts between loci pairs
2. normalization - string indicating normalization scheme. Available options are: NONE, VC, VC_SQRT or KR.
3. hicFile(s) - the hic file(s) to query. They can be either local or remote (eg on S3)
4. region 1 - genomic region "chr1:x1:x2" in base pair or fragment units. Interval convention is zero based 1/2 open
5. region 2 - genomic region "chr2:y1:y2"
6. units -- "BP" for base pairs
7. binSize -- size of each bin in base pair or fragment units. Bins are square

### Example

    import straw
    result = straw.straw('observed', 'KR', 'HIC001.hic', '1:109050000:109055000', '1:109105000:109110000', 'BP', 5000)
    for i in range(len(result)):
        print("{0}\t{1}\t{2}".format(result[i].binX, result[i].binY, result[i].counts))

