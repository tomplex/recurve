#!/usr/bin/python

import json
import sys
import os
import argparse


def get_arg_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-j', '--json', required=True, help="input JSON. can either be a path to a file or text.")
    parser.add_argument('-s', '--sep', required=False, default=',', help='seperator for output ids')
    parser.add_argument('-i', '--id', required=False, default='feature_id', help="id field to search for, defaults to feature_id")
    parser.add_argument('--help', action='help')
    return parser


def parse_arguments(args):
    parser = get_arg_parser()
    
    if len(args) < 1:
        parser.print_help()
        sys.exit(1)
        
    parsed_args = parser.parse_args(args)
    
    return parsed_args

def recursive_get_feature_ids(id_field_name, json_blob):
    if type(json_blob) == list:
        for item in json_blob:
            for feat_id in recursive_get_feature_ids(id_field_name, item):
                yield feat_id
    elif type(json_blob) == dict:
        for key, value in json_blob.items():
            if key == 'feature_id':
                yield value
            elif type(value) in (dict, list):
                for feat_id in recursive_get_feature_ids(id_field_name, value):
                    yield feat_id
            else:
                continue


def main():
    args = parse_arguments(sys.argv[1:])
    if os.path.isfile(args.json):
        with open(args.json) as f:
            json_blob = json.load(f)
    else:
        json_blob = json.loads(args.json)
    all_ids = []
    for feat_id in recursive_get_feature_ids(args.id, json_blob):
        all_ids.append(feat_id)

    print(str(args.sep).join([str(i) for i in all_ids])) 


if __name__ == '__main__':
    main()

