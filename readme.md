<div align="center">
    <h1> Schema Reinforcement Learning </h1>
</div>

<div align="center">

</div>

## Data

SchemaBench is intended solely for research and educational purposes and should not be construed as reflecting the opinions or views of the creators, owners, or contributors of this dataset. Below is the statistics of the schemas used in SchemaBench:

<br>
<div align="center">
<img src="assets/stats.png" width="300px">
</div>
<br>

We crawled 40K+ real-world schema files from [JSON Schema Store](https://www.schemastore.org/json/) and GitHub, and constructed SchemaBench. Below we present our data cleaning and construction pipeline with common cases.

<br>
<div align="center">
<img src="assets/clean.png" width="800px">
</div>
<br>

### Data Release

 Please download our dataset. *Simply copy those data files into the same folders in the repo.*
The file structure is as follows:
```
├── /schemabench/
│  └── /data/
│     ├── /custom/                         // Custom Formats
│     ├── /schema/                         // Complex Schema
│     ├── custom_append.jsonl
│     └── translation_test.jsonl           // Escape Translation
├── /train/
│  └── /data/
│     ├── mix_train_no_collected_json.json // SFT - w/o collected json
│     ├── mix_train.json                   // SFT - w/ collected json
│     ├── train_with_tool_ToS.parquet      // SRL - training set
│     └── val_with_tool_ToS.parquet        // SRL - validation set
```

*Please make sure you have downloaded all data files and put them into the right directory.*

## Training

✨Here is an overview of our training pipeline.

<br>
<div align="center">
<img src="assets/train.png" width="800px">
</div>
<br>

### Install
Initialize the environment (python==3.11)
```bash
bash scripts/init_env.sh
```

### Data Preparation
Download the data files from the [Data Release](#data) section and put them into the right directory.

### Fine-Tuning
```bash
bash scripts/train_sft.sh
```
If you want to use the SFT data without collected JSON, please run the following command:
```bash
bash scripts/train_sft_no_collected_json.sh
```

### Schema Reinforcement Learning (SRL)
We use a modified version of PRIME for SRL, which is already included in this repo as a submodule. To train the SRL model, please run the following command:
```bash
bash scripts/train_srl.sh
```

You can find your trained models in the `train/results` directory by default.

## Evaluation
Before evaluating performance on the SchemaBench, you should initialize the config file for local models' inference.
To initialize the config file, first:
```bash
cp private_example.toml private.toml
```
Then fill in the `private.toml` with your api key and base url if needed. After that, you can run the following evaluation script:
```bash
bash scripts/test_schemabench.sh
```

If you need to run the evaluation on a subset of the SchemaBench, you can modify the `test_category` in `test_schemabench.sh` script. Currently you can choose from `['all', 'schema', 'reasoning']` and all single sub-tasks.
