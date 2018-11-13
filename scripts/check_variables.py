### A script to check the variable matches (and mismatches) 
### between HIT template (j2) and data files (jsonl).

import re
import json
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-t', '--template', type=argparse.FileType('r'),
        help='path to template (.j2) file', required=True)
arg_parser.add_argument('-d', '--data', type=argparse.FileType('r'),
        help='path to data (.jsonl) file', required=True)
args = arg_parser.parse_args()

keys_j2 = set()
keys_data = set()

j2_content = args.template.read()
for d in args.data.readlines():
    for k in json.loads(d):
        keys_data.add(k)

re_pattern = r"{{.*?}}"
match = re.findall(re_pattern, j2_content)
for m in match:
    keys_j2.add(m[2:-2].strip())

print("\n================================================================")
print("The following variable(s) matches between template and data.")
for x in sorted(keys_data.intersection(keys_j2)):
    print('\t' + x)
print("\n================================================================")
print("The following variable(s) appear only in the data (jsonl) file")
for x in sorted(keys_data.difference(keys_j2)):
    print('\t' + x)
print("\n================================================================")
print("The following variable(s) appear only in the template (j2) file")
for x in sorted(keys_j2.difference(keys_data)):
    print('\t' + x)
print("\n================================================================")


