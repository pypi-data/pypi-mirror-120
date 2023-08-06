# Introduction

DLTrainer is an easy to use framework for quickly setting up deep learning experiments. This includes CPU, single GPU and distributed GPU experiments. Currently, this package only supports PyTorch.

This packages is primarily designed for running experiments from the command line, so that workloads can be easily ran in the cloud.

# Installation

```sh
pip install DLTrainer
```

# Usage

You can get started running your experiment with the following setup. This is just a short overview, the examples folder can be used for an example of an actual setup. 

An example folder structure is shown below. It is fine to deviate from this structure, however, you will need to ensure your run.py file can import your custom models, datasets and metrics. Additionally, you can put your data folder anywhere so long as your set the `--data_dir` argument correctly. You must specify how to load your data in your custom Dataset class, therefore, you may name these files however you like.
    
      ├── your_project
          ├── your_data
              ├──train.pkl      # your training set
              ├──dev.pkl        # your dev set
          ├── model.py        # your custom model class
          ├── dataset.py      # your custom dataset specific to your task (see https://pytorch.org/tutorials/beginner/basics/data_tutorial.html) for more details
          ├── metrics.py      # functions to calculate your task specific metrics
          ├── run.py  
            
A quick example of run.py using the above file structure.

```python
from DLTrainer.pytorch import DLTrainer

# custom file imports
from model import your_config_class, your_model_class
from dataset import your_dataset_class
from metrics import your_metrics_func

MODELS = {
    'my_model': (your_config_class, your_model_class, your_dataset_class),
}

if __name__ == "__main__":
    trainer = DLTrainer(MODELS, metrics_fn=calculate_metrics)
```

The following command will execture training using this script for 1 training epoch.

```sh
python run.py --model my_model --data_dir data --run-name sample_run --do_train --num_train_epochs 1
```

To see a see a full list of DLTrainer input arguments run:

```sh
python run.py --help
```



