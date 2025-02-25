<div align="center">
    <h1> SchemaBench </h1>
</div>

<div align="center">

</div>

<p align="center">
  <a href="#data">Data</a> •
  <a href="#training">Training</a> •
  <a href="#evaluation">Evaluation</a> •
  <a href="#paper">Paper</a> •
  <a href="#citation">Citation</a>

</p>

</div>

This repo provides all SFT and RL training data, complete training pipeline and evaluation scripts used in Schemabench. The dataset is using schema files crawled from [JSON Schema Store](https://www.schemastore.org/json/) and GitHub, then constructed automatically using fine-tuned LLaMA and [JSON Schema Faker](https://github.com/json-schema-faker/json-schema-faker).

## What's New

- **[2025/02/25]** SchemaBench is now released!

✨Here is an overview of our training pipeline.

<br>
<div align="center">
<img src="assets/train.png" width="800px">
</div>
<br>

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

 Please download our dataset using the following link: [Google Drive](https://drive.google.com/drive/folders/1NOx6xzS30HHRk5rikUdNOXvOT7UtwstR) or [Tsinghua Cloud](https://cloud.tsinghua.edu.cn/d/732f121b7b0044798190/). *Simply copy those data files into the same folders in the repo.*
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
### Install
Clone this repository and navigate to the SchemaBench folder.
```bash
git clone git@github.com:kekekawaii2839/SchemaBench.git
cd SchemaBench
```
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
We use [a modified version of PRIME](https://github.com/kekekawaii2839/PRIME) for SRL, which is already included in this repo as a submodule. To train the SRL model, please run the following command:
```bash
bash scripts/train_srl.sh
```

You can find your trained models in the `train/results` directory by default.

## Evaluation
Before evaluating performance on the SchemaBench, you should initialize the config file for local models' inference.
We use [CodeLinker](https://github.com/luyaxi/CodeLinker) for inference, which currently support any OpenAI compatible server for the evaluation. To initialize the config file, first:
```bash
mv private_example.toml private.toml
```
Then fill in the `private.toml` with your api key and base url if needed. After that, you can run the following evaluation script:
```bash
bash scripts/test_schemabench.sh
```

If you need to run the evaluation on a subset of the SchemaBench, you can modify the `test_category` in `test_schemabench.sh` script. Currently you can choose from `['all', 'schema', 'reasoning']` and single sub-tasks.

## Paper
The paper is currently under review. We will update the paper link once it is published.

## Citation
To be updated in the future.