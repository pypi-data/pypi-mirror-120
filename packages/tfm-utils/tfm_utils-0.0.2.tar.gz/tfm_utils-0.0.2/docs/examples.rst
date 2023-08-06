Examples
==========


`JASPAR <http://jaspar.genereg.net>`_ is a very highly-touted transcription factor motif database from which motif count
matrices can be downloaded for a large variety of organisms and transcription factors. There exist numerous other motif
databases as well (TRANSFAC, CIS-BP, MEME, HOMER, WORMBASE, etc), most of which use a relatively similar format
for their motifs. Typically, a motif file consists of four rows or columns with each position in a given row or column corresponding
to a base within the motif. Sometimes there is an comment line started with ``>``. The row or column order is always ``A, C, G, T``.
In this example, the motif consists of four rows corresponding to the 16 positions of the motif with counts for each base at each position.

>>> path = "MA0007.1.pfm"
>>> ! cat MA0007.1.pfm

>MA0007.1 Ar
  9.00   9.00  11.00  16.00   0.00  12.00  21.00   0.00  15.00   4.00   5.00   6.00   3.00   0.00   4.00  11.00   1.00   3.00   6.00   6.00  10.00   5.00
  7.00   2.00   3.00   1.00   0.00   6.00   2.00  24.00   0.00   9.00  11.00   9.00   5.00   0.00   0.00   5.00  22.00  16.00   7.00   5.00  11.00  11.00
  2.00   3.00   3.00   7.00  22.00   1.00   0.00   0.00   8.00   2.00   2.00   9.00   1.00  24.00   0.00   1.00   1.00   1.00   5.00   9.00   0.00   6.00
  6.00  10.00   7.00   0.00   2.00   5.00   1.00   0.00   1.00   9.00   6.00   0.00  15.00   0.00  20.00   7.00   0.00   4.00   6.00   4.00   3.00   2.00

>>> import tfm_utils
>>> m = tfmp.create_matrix("MA0045.pfm")
>>> tfmp.score2pval(m, 8.7737)
9.992625564336777e-06
>>> tfmp.pval2score(m, 0.00001)
8.773708000000001

This could also be done using pandas as follows

>>> import pandas as pd
>>> import tfm_utils
>>> df = pd.read_csv("tests/M08490_1.94d.txt", sep = "\t", index_col=0)
>>> df.head()
            A         C         G         T
Pos
1    0.215492  0.220404  0.340647  0.223457
2    0.534211  0.101312  0.330926  0.033551
3    0.000000  0.000191  0.000286  0.999523
4    0.014867  0.000000  0.756531  0.228601
5    0.999333  0.000000  0.000000  0.000667
>>> matrix = tfm_utils.df_to_matrix(df)
>>> matrix
<tfm_utils.pytfmpval.Matrix; proxy of <Swig Object of type 'Matrix *' at 0x7fc2f8bfa330> >
>>> tfm_utils.score2pval(matrix, 7.14)
3.516674041748047e-06

This also works by passing the DataFrame into the functions directly and works for any orientation:

>>> df.head()
Pos        1         2         3         4         5         6        7    8         9    10        11        12
A    0.215492  0.534211  0.000000  0.014867  0.999333  0.000000  0.03061  0.0  0.226232  1.0  0.035516  0.221931
C    0.220404  0.101312  0.000191  0.000000  0.000000  0.968450  0.00000  0.0  0.758146  0.0  0.328779  0.327673
G    0.340647  0.330926  0.000286  0.756531  0.000000  0.000508  0.96939  0.0  0.000000  0.0  0.101733  0.227845
T    0.223457  0.033551  0.999523  0.228601  0.000667  0.031042  0.00000  1.0  0.015622  0.0  0.533973  0.222551
>>> tfm_utils.score2pval(df, 7.14)
5.960464477539063e-08


If you are more used to R, this could also be done by creating a string for the matrix by concatenating the rows (or columns) and using the ``read_matrix()`` function.
This method is usually easier, as it allows the user to parse the motif file as necessary to ensure a proper input. It's also more fitting for high-throughput use.

>>> from tfm_utils import tfmp
>>> mat = (" 3  7  9  3 11 11 11  3  4  3  8  8  9  9 11  2"
...        " 5  0  1  6  0  0  0  3  1  4  5  1  0  5  0  7"
...	   " 4  3  1  4  3  2  2  2  8  6  1  4  2  0  3  0"
...	   " 2  4  3  1  0  1  1  6  1  1  0  1  3  0  0  5"
...	  )
>>> m = tfmp.read_matrix(mat)
>>> tfmp.pval2score(m, 0.00001)
8.773708000000001
>>> tfmp.score2pval(m, 8.7737)
9.992625564336777e-06

