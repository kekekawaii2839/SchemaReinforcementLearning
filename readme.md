<div align="center">
    <h1> SchemaBench </h1>
</div>

<div align="center">

</div>

<p align="center">
  <a href="#data">Data</a> •
  <a href="#model">Model</a> •
  <a href="#performance">Performance</a> •
  <a href="#training">Training</a> •
  <a href="#evaluation">Evaluation</a> •
  <a href="#paper">Paper</a> •
  <a href="#citation">Citation</a>

</p>

</div>

Welcome to the official repo for SchemaBench, containing the dataset, training scripts and evaluation code in our papar.

## What's New

- **[2025/02/25]** SchemaBench is now released!

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

## Model🤗
We release the [LLaMA-3.2 3B SRL](https://huggingface.co/HaolunLi/LLaMA-3.2-3B-SRL) for anyone who wants to use it.

## Performance📈
We evaluate the performance of several models on the SchemaBench. The results are shown below:
| Model                   | Complex | Custom | Escape | Overall | GSM8K | MATH500 | MMLU  | ARC-C |
|-------------------------|---------|--------|--------|---------|-------|---------|-------|-------|
| GPT-4o                  | 84.47   | 61.56  | 37.14  | 61.06   | 97.80 | 41.40   | 86.16 | 97.01 |
| GPT-4o-mini             | 68.86   | 46.17  | 16.89  | 43.98   | 86.13 | 31.80   | 49.41 | 77.65 |
| Qwen-2.5 7B             | 72.42   | 43.60  | 11.11  | 42.38   | 94.54 | 38.60   | 74.43 | 91.21 |
| MiniCPM-3 4B            | 53.88   | 20.29  | 9.13   | 27.77   | 69.22 | 33.40   | 66.58 | 88.31 |
| LLaMA-3.1 8B            | 64.26   | 33.07  | 12.02  | 36.45   | 95.91 | 85.60   | 71.83 | 84.98 |
| LLaMA-3.1 8B SFT        | 74.56   | 46.64  | 60.58  | 60.59   | 89.46 | 63.80   | 66.97 | 84.56 |
| - w/o Collected JSON    | 70.84   | 42.06  | 60.35  | 57.75   | 78.39 | 46.00   | 58.87 | 75.68 |
| LLaMA-3.2 3B            | 49.84   | 27.31  | 8.37   | 28.51   | 80.97 | 35.40   | 62.38 | 79.27 |
| LLaMA-3.2 3B SFT        | 71.71   | 45.52  | 52.21  | 56.48   | 82.94 | 44.40   | 61.50 | 78.41 |
| - w/o Collected JSON    | 72.42   | 42.83  | 54.82  | 56.69   | 78.85 | 36.20   | 59.11 | 75.68 |
| LLaMA-3.2 3B SRL        | 82.25   | 66.13  | 69.10  | 72.50   | 84.23 | 43.20   | 57.99 | 78.24 |


## Training

✨Here is an overview of our training pipeline.

<br>
<div align="center">
<img src="assets/train.png" width="800px">
</div>
<br>

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

If you need to run the evaluation on a subset of the SchemaBench, you can modify the `test_category` in `test_schemabench.sh` script. Currently you can choose from `['all', 'schema', 'reasoning']` and all single sub-tasks.

## Paper
The paper is currently under review. We will update the paper link once it is published.

## Citation
To be updated in the future.