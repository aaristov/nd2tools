![Python package](https://github.com/aaristov/nd2tools/workflows/Python%20package/badge.svg)

#  nd2 to tif conversion tools

# Installation

You can use local installation or Docker container

## Local installation using miniconda

1. Download and install [miniconda3](https://docs.conda.io/en/latest/miniconda.html)
2. Create new environment with python 3.8
  - `conda create -n nd2 python=3.8`
  - `conda activate nd2`
3. Install the package `pip install -U git+https://gitlab.pasteur.fr/aaristov/nd2shrink.git`
4. Optional. On Windows you will need C++ runtime binaries to use `pims`. Download and install it from [here](https://aka.ms/vs/16/release/vc_redist.x64.exe)

## Docker container

If using Mac or Linux it's highly recommended using preconfigured  Docker container.

In Windows Docker can't acceess remote volumes or Samba shares. But you can use it with local drives.

First, install [Docker Desktop](https://www.docker.com/products/docker-desktop), register and login.

Open terminal and run
```
docker run  -it -v /Volumes/Multicell:/Volumes/Multicell aaristov85/nd2tools
```
`-it` option makes shell interactive

`-v /Volumes/Multicell:/Volumes/Multicell` exposes local Multicell mount to the container with the same path. So, when you're inside the container, you can type `python -m nd2tif ` and then drag and drop any nd2 file from your datasets. It will add a valid path the command line, press Enter and enjoy.

In principle, you can insert your command right after container initialization:
```
docker run  -it -v /Volumes/Multicell:/Volumes/Multicell python -m nd2tif path_to_nd2
```

Remove `-it` option to run task in the background.

# How To Use CLI (comman line tools)

Package contains several independent modules

## nd2tif: convert multiwell nd2 dataset to tif stacks.

With binning and 16 to 8 bits conversion.

One position 'm' — one ImageJ-formatted tif stack with all channels and z planes.

### Use:

`python -m nd2tif path_to_nd2`

Available options:

```
python -m nd2tif --help
Usage: __main__.py [OPTIONS] PATH

Options:
  -b, --bin INTEGER          Image binning  [default: 4]
  --to_8bits                 converto to 8 bits  [default: False]
  --log TEXT                 Logging level  [default: info]
  -s, --start INTEGER RANGE  Start numbering from 000 or 001  [default: 0]
  -p, --prefix TEXT          Prefix for tif files  [default: Pos_]
  -c, --cpu INTEGER          Number of CPU  [default: 1]
  --help                     Show this message and exit.
```

#### Input:

- Folder:
  - experiment.nd2

#### Run:
`python -m nd2tif -b 4 --to_8bits -s 1 Folder/experiment.nd2`

#### Output:


- Folder:
  - experiment_binned_4x4_tifs
    - Pos_001.tif
    - Pos_002.tif
    - ...
  - experiment.nd2
  - experiment_meta.json


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

## segment: Segment organoids in bright field

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

