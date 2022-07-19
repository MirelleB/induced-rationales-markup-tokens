import argparse
import string
import logging
import random
import pandas as pd

def scan_preprocess(sentence):
  _map = {
    'I_WALK': 'WALK',
    'I_JUMP': 'JUMP',
    'I_LOOK': 'LOOK',
    'I_TURN_RIGHT': 'RIGHT',
    'I_TURN_LEFT': 'LEFT',
    'I_RUN': 'RUN'}
  tokens = [_map[token] for token in sentence.split()]
  return " ".join(tokens)

def sample_dataset(n_examples, min_digits, max_digits):
  examples = []
  for _ in range(n_examples):
      example = []
      max_digits_1 = random.randint(min_digits, max_digits)
      max_digits_2 = random.randint(min_digits, max_digits_1)
      temp = [max_digits_1, max_digits_2]
      random.shuffle(temp)
      for max_digits_i in temp:
          min_number = int((max_digits_i - 1) * '9') + 1
          max_number = int(max_digits_i * '9')
          example.append(random.randint(min_number, max_number))
      examples.append(example)
  return examples

def operation_add(examples):
  instruction = []
  output = []
  alphabet_list = list(string.ascii_uppercase)
  for num1, num2 in examples:
    num1_map = list(map(int, str(num1)))
    num2_map = list(map(int, str(num2)))

    afnum1=" ".join([alfa+str(num) for alfa, num in zip(reversed(alphabet_list[0:len(num1_map)]), num1_map)])
    afnum2=" ".join([alfa+str(num) for alfa, num in zip(reversed(alphabet_list[0:len(num2_map)]), num2_map)])
    instruction.append("add the numbers "+ afnum1+" and "+afnum2)
    #sum
    output.append(num1+num2)
  return instruction, output

def handle_issue_with_space(list_instructions):
  for instruction in list_instructions:
    sep_sentences = instruction.split('add the numbers')
    numbers = sep_sentences[1].split('and')
    number1 = "".join(numbers[0].strip().split())
    number2="".join(numbers[1].strip().split())

    number1 = " ".join([char for char in number1])
    number2 = " ".join([char for char in number2])
    return 'add the numbers '+number1+' and '+number2

def remove_markups(list_instructions):
  for instruction in list_instructions:
    sep_sentences = instruction.split('add the numbers')
    numbers = sep_sentences[1].split('and')
    number1 = "".join(numbers[0].strip().split())
    number2="".join(numbers[1].strip().split())
    number1 = " ".join([char for char in number1 if char.isdigit()])
    number2 = " ".join([char for char in number2 if char.isdigit()])
    return 'add the numbers '+number1+' and '+number2

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_path",
        type=str,
        required=True,
        help="output path",
    )
    parser.add_argument(
        "--file_name",
        type=str,
        required=True,
        help="Name of the file to be saved",
    )
    parser.add_argument(
        "--task",
        type=str,
        required=True,
        help="tasks: SCAN or addition",
    )
    parser.add_argument(
        "--n_examples",
        type=int,
        default=400,
        help="number of examples generated",
    )
    parser.add_argument(
        "--min_digits",
        type=int,
        default=4
    )
    parser.add_argument(
        "--max_digits",
        type=int,
        default=14
    )
    args = parser.parse_args()
    try:
        if args.task=='addition':
            examples = sample_dataset(n_examples=args.n_examples, min_digits=args.min_digits, max_digits=args.max_digits)
            instructions, outputs = operation_add(examples)
            df = pd.DataFrame({'instruction':instructions,'output':outputs})
            df['instruction'] =  df['instruction'].map(lambda x: handle_issue_with_space([x]))

            df_no_markups =  pd.DataFrame({'instruction':instructions,'output':outputs})
            df_no_markups['instruction'] =  df['instruction'].map(lambda x: remove_markups([x]))

            df.to_csv(args.output_path+args.file_name+'.tsv', sep='\t',index=None)
            df_no_markups.to_csv(args.output_path+args.file_name+'-no_markups.tsv', sep='\t',index=None)
        else:
            df = pd.read_csv('test.tsv', sep='\t',names = ['instruction','output'])
            #randomly choose n samples
            df = df.sample(n=args.n_examples)
            df['output'] = df['output'].map(scan_preprocess)
            df.to_csv(args.output_path+args.file_name+'.tsv',sep='\t',index=None)

    except:
        raise RuntimeError(f'An error occurred during the file generation.')


if __name__ == "__main__":
    main()
