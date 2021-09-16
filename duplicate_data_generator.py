import argparse
import json
import random
import string
import pandas as pd
from faker import Faker

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--columns', help='column configuration file', dest='column_file_path', required=True)
    parser.add_argument('--output', help='output csv file', dest='output_file_path', required=True)
    parser.add_argument('--rows', help='the total number of rows to generate', dest='total_row_cnt', type=int, required=True)
    parser.add_argument('--duprate', help='duplication rate', dest='duplication_rate', type=float, required=True)
    parser.add_argument('--localization', help='localization', dest='localization', default='en_US', required=False)
    parser.add_argument('--cores', help='the number of cores to use for mulitprocessing', dest='cores', default=1, required=False)
    parser.add_argument('--batchsize', help='the size of each batch to process', dest='batchsize', default=50000, required=False)
    config = vars(parser.parse_args()) 

    with open(config['column_file_path']) as column_file:
        col_config = json.load(column_file)

    config.update(col_config)
    fake_data = get_fake_data(config)
    fake_data.to_csv(config['output_file_path'])

def get_fake_data(config):
    num_of_initial_rows = int(config['total_row_cnt']) - int(config['total_row_cnt'] * config['duplication_rate'])
    num_duplicated_rows = int(config['total_row_cnt']) - num_of_initial_rows
    
    fake_gen = Faker(config['localization'])
    initial_fake_data = pd.DataFrame()

    for column in config['columns']:
        initial_fake_data[column['name']] = [get_fake_string(column['type'], fake_gen) for x in range(num_of_initial_rows)]

    known_duplicates = initial_fake_data.sample(num_duplicated_rows, replace=True)

    for column in config['columns']:
        if 'transposition_chars' in column and column['transposition_chars'] > 0:
            for i in range(column['transposition_chars']):
                known_duplicates[column['name']] = known_duplicates[column['name']].apply(transposition_chars)
        if 'mistype_chars' in column and column['mistype_chars'] > 0:
            for i in range(column['mistype_chars']):
                known_duplicates[column['name']] = known_duplicates[column['name']].apply(transposition_chars)

    output_data = initial_fake_data.append(known_duplicates)
    return output_data


def get_fake_string(fake_type, fake_gen):
    if fake_type == 'first_name':
        return fake_gen.first_name()
    elif fake_type == 'last_name':
        return fake_gen.last_name()
    elif fake_type == 'street_address':
        return fake_gen.street_address()
    elif fake_type == 'secondary_address':
        return fake_gen.secondary_address()
    elif fake_type == 'city':
        return fake_gen.city()
    elif fake_type == 'state':
        return fake_gen.state()
    elif fake_type == 'postcode':
        return fake_gen.postcode()
    elif fake_type == 'current_country':
        return fake_gen.current_country()
    elif fake_type == 'phone_number':
        return fake_gen.phone_number()
    elif fake_type == 'email':
        return fake_gen.email()
    elif fake_type == 'ssn':
        return fake_gen.ssn()
    elif fake_type == 'date_of_birth':
        return str(fake_gen.date_of_birth(minimum_age=18, maximum_age=95))

def transposition_chars(str_to_alter):
    first_char = random.randrange(len(str_to_alter)-1)
    second_char = first_char + 1
    split_str = split(str_to_alter)
    tmp = split_str[first_char]
    split_str[first_char] = split_str[second_char]
    split_str[second_char] = tmp
    str_to_alter = combine(split_str)
    return str_to_alter

def mistype_chars(str_to_alter):
    char_to_alter = random.randrange(len(str_to_alter))
    split_str = split(str_to_alter)
    split_str[char_to_alter] = random.choice(string.ascii_letters)
    str_to_alter = combine(split_str)
    return str_to_alter

def split(word):
    return [char for char in word]

def combine(chars):
    new_str = ''
    for char in chars:
        new_str += char
    return new_str


          
if __name__ == '__main__':
    main()