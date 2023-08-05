# MAFIO

A minimalist Python package for reading and writing [MAF](https://docs.gdc.cancer.gov/Data/File_Formats/MAF_Format/#:~:text=Mutation%20Annotation%20Format%20(MAF)%20is,(or%20open-access).) files.

# Usage

## Read
```py
from mafio import MAFReader

reader = MAFReader("test.maf")

# for reading compressed file
reader = MAFReader("test.maf", compression='gzip')

data = reader.read()

print(reader.headers) # ['col1', 'col2', 'col3']
print(next(data)) # [[1,2,3], [4,5,6], [7,8,9]]

# return only certain columns
data = reader.read(use_cols=['col1','col3'])

print(reader.headers) # ['col1', 'col3']
print(next(data)) # [[1,3], [4,6], [7,9]]

# for big files use chunks
data = reader.read(chunk_size=2)

print(next(data)) #[[1,2,3], [4,5,6]]
print(next(data)) #[[7,8,9]]

```
## Write
```py
from mafio import MAFWriter

cols = ['col1', 'col2', 'col3']
row1 = [1,2,3]
row1 = [4,5,6]
row1 = [7,8,9]
data = [cols, row1, row2, row3]

writer = MAFWriter("test.maf")

# you can also compress the data
writer = MAFWriter("test.maf", compression='gzip')

writer.write(data)

# for appending the file
writer.write(data, append=True)
```