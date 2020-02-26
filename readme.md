#  nd2 to tif tools

## Compress nd2 to tif with 4x binning and 16 to 8 bits conversion

### Use:

`python -m nd2shrink path_to_nd2`

# combine several nd2 into tif time series

### Use

`python -m nd2_combine folder`

#### Input:

- Folder:
  - D1: 
    - condition1.nd2
    - condition2.nd2
  - D2:
    - condition1.nd2
    - condition2.nd2

#### Output:

- Folder:
  - Compressed:
    - condition1:
      - Pos_001.tif <- D1, D2 images for well 1
      - Pos_002.tif <- D1, D2 images for well 2



