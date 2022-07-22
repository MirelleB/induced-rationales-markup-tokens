# induced-rationales-markup-tokens
Paper reproduction code: <b>Induced Natural Language Rationales and Interleaved Markup Tokens Enable Extrapolation in Large Language Models.</b>

We provide the necessary notebooks for playback in both tasks: SCAN and Addition

Description of folder contents:

## SCAN
### few-shot-text-davinci-002
Experiment with prompt composed of explanations and markup tokens
> Experiment-rationales+markups.ipynb

Experiment with prompt consisting of only explanations
> Experiment-rationales-only.ipynb

Experiment with prompt composed of only the markup tokens
> Experiment-rationales-only.ipynb

In the outputs/ directory it is possible to check the output of the model in each of the above scenarios.

Note: Due to costs, the ablation tests (rationales/markups only) were performed with 200 samples.
### finetuning-ada-curie-davinci

Experiment with fine tuning on GPT-3 models (Ada, Curie, Davinci)
> fine-tuning-GPT3-ada-20-epochs.ipynb

> fine-tuning-GPT3-curie-3-epochs.ipynb

> fine-tuning-GPT3-davinci-3-epochs.ipynb

Each experiment was trained using the SCAN Training dataset (16,990) and converted to jsonl format (train_prepared.jsonl)
The evaluation was done with the test set (3,920) it was also converted into the jsonl format (test_prepared.jsonl)

In notebooks test_* has the code used in the test step of the models.
In the /outputs/ folder making the model output available in each scenario tried.

## Addition
Experiment with prompt composed of explanations and markup tokens
> Experiment-rationales+markups.ipynb

Experiment with prompt consisting of only explanations
> Experiment-rationales-only.ipynb

Experiment with prompt composed of only the markup tokens
> Experiment-rationales-only.ipynb

In the outputs/ directory it is possible to check the output of the model in each of the above scenarios.

Note: Due to costs, the ablation tests (rationales/markups only) were performed with 200 samples.

# Generating the datasets
In both SCAN and Addition tasks, the dataset went through some pre-processing. The same configuration with the following steps:

1. Download SCAN dataset:
> wget https://raw.githubusercontent.com/facebookresearch/meta_seq2seq/master/data/tasks_train_length.txt

> wget https://raw.githubusercontent.com/facebookresearch/meta_seq2seq/master/data/tasks_test_length.txt

> sed 's/IN:\ //' tasks_train_length.txt | sed 's/\ OUT:\ /\t/' > train.tsv

>sed 's/IN:\ //' tasks_test_length.txt | sed 's/\ OUT:\ /\t/' > test.tsv

2. Run the script <b>generate_dataset.py</b>
> python generate_dataset.py --file_name=random_400_test --output_path=SCAN/ --task=SCAN

 > python3 generate_dataset.py --file_name=addition_random_400_test
 --min_digits=4
 --max_digits=14
 --output_path=addition_task/ --task=addition