# Data Provenance

The completed reproduction used the provided processed SynLeaF data archive. The archive itself is not included in this GitHub repository because it is large and contains the processed datasets required by training.

The verified SHA-256 recorded for `data.tar.gz` is:

```text
73a9fa252ab75c609ff76ecacc3ea5fa4dabc0204d4117e17c4362767b0400d1
```

The extracted dataset folders documented by the run are `BRCA`, `CESC`, `COAD`, `KIRC`, `LAML`, `LUAD`, `OV`, `SKCM`, and `pan`. The server evidence records an extracted processed-data size of approximately 4.3G. Obtain the processed data archive from the source/reproduction materials available for this project, verify the checksum, and extract it into the source checkout's expected `data/` location.

This project does not claim to have independently rebuilt the processed data from raw biological sources.
