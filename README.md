# CycleGAN Project
*Henri Toivanen, Hermanni Rautiainen, Roope Korhonen, Antti Auvinen*

## Installation

Clone project:
```bash
  git clone git@github.com:henritoi/gan-ai-project.git
  
  cd gan-ai-project
```

## Download datasets

```bash
  python main.py --init
```

or

```bash
  ./download_data.sh
```

## Commands

- Download datasets using command (deletes all old datasets) `--init`
- List downloaded datasets using command `--list`
- Select method to be executed using command `-e` following the method from `train` and `test`
- Select dataset to be used in training using command `--data` following the dataset name which can be found using the `--list` command
- Help `-h` or `--help`
