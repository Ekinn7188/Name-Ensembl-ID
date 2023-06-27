# Name-Ensembl-ID
A script that turns a .csv of human Ensembl IDs to their respective gene name.

# Command Use Example

`hg38_RNAseq_edgeR.csv`:
|	 | logFC |	logCPM	| F |	PValue	| FDR
|---|---|---|---|---|---|
|ENSG00000135373.13	|7.514448524	|5.983961777	|6067.864362	|1.89E-23	|3.00E-19|
|ENSG00000164484.12 |	-3.437775851 |	6.250356347 |	4295.180526 |	3.69E-22 |	2.94E-18|
|ENSG00000113657.13	|-4.346349849	|5.642271462	|4039.171863	|6.27E-22	|3.33E-18|
|ENSG00000109511.12	|-4.854179787	|5.434638143	|3580.314399	|1.77E-21	|7.04E-18|
|...|...|...|...|...|...|...|

```bash
$ python3 Name_Gene.py hg38_RNAseq_edgeR.csv -o output.csv
Finding Gene Names
Done!
```

`output.csv`:
|	 | Gene name	| logFC |	logCPM	| F |	PValue	| FDR
|---|---|---|---|---|---|---|
|ENSG00000135373.13	|EHF	|7.514448524	|5.983961777	|6067.864362	|1.89E-23	|3.00E-19|
|ENSG00000164484.12 |	TMEM200A|	-3.437775851 |	6.250356347 |	4295.180526 |	3.69E-22 |	2.94E-18|
|ENSG00000113657.13	|DPYSL3	|-4.346349849	|5.642271462	|4039.171863	|6.27E-22	|3.33E-18|
|ENSG00000109511.12	|ANXA10	|-4.854179787	|5.434638143	|3580.314399	|1.77E-21	|7.04E-18|
|...|...|...|...|...|...|...|

As you can see, the gene name was added to the right of the ID. in the specified output file.

# Command Arguments
  | Argument | Description |
  | ---    |     ---     |
  |**input** |The .csv file, which contains a column with ensembl gene ids.
## Options:
  | Option | Description |
  | ---    |     ---     |
  |**-h, --help**|Show this help message and exit.
  |**-o OUTPUT, --output OUTPUT**|Output file. Defaults to ./output.csv.
  |**-n NAME, --name NAME**|Column name for ensmbl id list. Mutually exclusive with --index.
  |**-i INDEX, --index INDEX**|Column index for ensmbl id list. (1-indexed) Defaults to 1. Mutually exclusive with --name.

