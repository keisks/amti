#!/usr/bin/python
# -*- coding: utf-8 -*-

### This script extract essential information from batch-result (to be similar to the results file from mturk GUI)
### 
### example usage
### > python batch_results_to_csv.py ./PATH/TO/BATCH/batch-332e34db-xxxx-xxxx-xxx-3ed33d5647f4/

import os
import sys
import re
import json
import csv
from datetime import datetime
from xml.etree.ElementTree import fromstring
from collections import Counter


# util function by @csbhagav
# https://github.com/allenai/abductive-nli/blob/master/anli/utils/file_utils.py
def read_jsonl_lines(input_file):
    with open(input_file) as f:
        lines = f.readlines()
        return [json.loads(l.strip()) for l in lines]

# util function by @csbhagav
# https://github.com/allenai/abductive-nli/blob/master/anli/utils/crowdsourcing_utils.py
def read_amti_assignment(xml_str):
    e = fromstring(xml_str)
    qa_in_file = []
    for answer in e.getchildren():
        q_a_pair = answer.getchildren()
        hit_question = q_a_pair[0].text
        if q_a_pair[1].text is None:
            hit_answer = ''
        else:
            hit_answer = q_a_pair[1].text.replace('\t', ' ')
        hit_answer = re.sub('\s+', ' ', hit_answer).strip()
        qa_in_file.append(
            {
                'question': hit_question,
                'answer': hit_answer
            }
        )
    return qa_in_file


# core_columns are shared by all kinds of HITs (tasks).
core_columns = [
    "HITId",
    "AssignmentId",
    "WorkerId",
    "AcceptTime",
    "SubmitTime",
    "WorkTimeInSeconds",
]


# batch directory
results_dir = os.path.join(sys.argv[1], "results")
if not os.path.exists(results_dir):
    raise Exception("Batch directory not found")


# store batch results into the submission list
submissions = []
num_hits = 0
num_assignments = Counter()
for hits_dir in os.listdir(results_dir):
    num_hits += 1
    abs_hits_dir = os.path.join(results_dir, hits_dir)
    assignments_file = os.path.join(abs_hits_dir, "assignments.jsonl")
    assignments = read_jsonl_lines(assignments_file)

    i=0
    for assignment in assignments:
        record = {}
        i+=1
        record['WorkerId'] = assignment['WorkerId']
        record['AssignmentId'] = assignment['AssignmentId']
        record['HITId'] = assignment['HITId']
        record['AcceptTime'] = assignment['AcceptTime']
        record['SubmitTime'] = assignment['SubmitTime']
        end = datetime.strptime(record['SubmitTime'][11:19], "%H:%M:%S")
        start = datetime.strptime(record['AcceptTime'][11:19], "%H:%M:%S")
        record['WorkTimeInSeconds'] = (end - start).seconds
        for qa in read_amti_assignment(assignment['Answer']):
            record[qa['question']] = qa['answer']
        submissions.append(record)
    num_assignments[i] += 1


# convert the submissions into a csv format.
task_specific_columns = sorted(list(set(record.keys()).difference(set(core_columns))))
full_columns = core_columns + task_specific_columns

with open(os.path.join(sys.argv[1], "merged_results.csv"), 'w') as f:
    writer = csv.DictWriter(f, fieldnames=full_columns)
    writer.writeheader()

    for sub in submissions:
        if "doNotRedirect" in sub.keys():
            sub.pop("doNotRedirect", None)

        writer.writerow(sub)

print("merged_resutls.csv is created under " + sys.argv[1])
print("===== Short summary =====")
print("Number of HITs in the results: {}".format(num_hits))
for k, v in num_assignments.items():
    print("{} HITs have {} assignments.".format(v, k))


