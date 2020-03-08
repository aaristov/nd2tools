#  nd2 to tif conversion tools

## Installation

1. Download and install [miniconda3](https://docs.conda.io/en/latest/miniconda.html)
2. Create new environment with python 3.8
  - `conda create -n nd2 python=3.8`
  - `conda activate nd2`
3. Install the package `pip install -U git+https://gitlab.pasteur.fr/aaristov/nd2shrink.git`
4. Optional. On Windows you will need C++ runtime binaries to use `pims`. Download and install it from [here](https://aka.ms/vs/16/release/vc_redist.x64.exe)


## Compress nd2 to tif with 4x binning and 16 to 8 bits conversion

### Use:

`python -m nd2shrink path_to_nd2`

# Bin 16x stitched nd2:

### Use:
`python -m bin_stitched path_to_nd2`

Creates ImageJ-formatted tif file in the same folder. Can be opened by drag'n'drop in Fiji/ImageJ.

# Combine several nd2 into tif time series

### Use

`python -m nd2_combine path_to_folder`

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

# Segment organoids in bright field

### Use

`python -m segment dataset.nd2`

#### Input:

- Folder:
  - D1:
    - dataset.nd2

#### Output:

- Folder:
  - D1:
    - dataset.nd2
    - dataset_stats.csv <- table with columns (area, eccentricity, major_axis_length) all in pixels.
    - dataset:
      - Pos_000.png
      - Pos_001.png


## Multiwell intensity analysis (In development)

Allows to segment wells on microchip using bright field image and coount fluorescence intensities in time from fluorescent stack.

### API

```
import multiwell
from tifffile import imread
```
load stacks
```
bf_stack = imread('bf_stack.tif')
GFP_stack = imread('gfp_stack')
```
create mask using first image int he stack
```
mask = multiwell.get_mask(bf_stack)
```

get intensities from gfp stack. Returns pandas table with columns `['label', 'time', 'mean_intensity', 'max_intensity']`
```
gfp_intensity_table = multiwell.get_intensity_table(mask, GFP_stack)
```
Remove dark wells: selec last time point 'time = 16' where intinsities of dark wells and growing wells are well separated and select only those wells with intensitied higher than 'min_intensity'
```
gfp_intensity_table_grow = multicell.filter_table_by_min_intensity(gfp_intensity_table, time=16, min_intensity=200)
```

Show resulting track
```
multiwell.plot_intensity_vs_time(gfp_intensity_table_grow)
multiwell.plot_intensity_line(gfp_intensity_table_grow)
```


### TODO:
* simulator of brithfield wells and flurescence inside
* simulate drift and account for it
* normalize intensity by dark wells
* get correlation GFP(RFP) per well



