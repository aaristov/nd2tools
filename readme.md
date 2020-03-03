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

# combine several nd2 into tif time series

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

