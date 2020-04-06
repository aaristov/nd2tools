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

`python -m segment dataset1.nd2 dataset2.nd2 ...`

```
python -m segment --help
Usage: __main__.py [OPTIONS] [PATH]...

Options:
  -o, --out_dir_suffix TEXT       Where to save the preview png for
                                  segmentation.  [default: _segment]

  -l, --len_range_px <INTEGER INTEGER>...
                                  min, max length of major axis in pixels
                                  [default: 50, 500]

  --log TEXT                      Logging level  [default: info]
  --help                          Show this message and exit.
```

#### Input:

- Folder:
  - D1: 
    - dataset.nd2

#### Output:

- Folder:
  - D1:
    - dataset.nd2
    - dataset_stats.csv <- table with columns (area, eccentricity, major_axis_length) all in pixels.
    - dataset_segment:
      - Pos_000.png
      - Pos_001.png

