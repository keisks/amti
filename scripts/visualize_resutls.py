import os
import sys
import csv

"""
create html file to show workers submissions
"""

header = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Bootstrap Example</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <style>
    .input-sentence {
        background-color: #d3f4ff;
        color: black;
        padding-left: 3px;
        padding-right: 3px;

    }

    .end1-sentence {
        background-color: #fff8c9;
        color: black;
        padding-left: 3px;
        padding-right: 3px;
       
    }

    .end2-sentence {
        background-color: #ffe2f9;
        color: black;
        padding-left: 3px;
        padding-right: 3px;

    }
  </style>
  </head>
  <body>
  <div class="container">
  <h1 align="center"> WSC for social CSK </h1>

"""
  
footer = """\
</div>
</body>
</html>
"""

DIR_PATH = sys.argv[1]
csv_file_path = os.path.join(DIR_PATH, "merged_results.csv")
csv_reader = csv.DictReader(open(csv_file_path, 'r'))
seed_dict = {}

# load merged_results file
for row in csv_reader:
    if not row["HITId"] in seed_dict.keys():

        seed_dict[row["HITId"]] = {}
        seed_dict[row["HITId"]]["end1"] = []
        seed_dict[row["HITId"]]["end2"] = []
    seed_dict[row["HITId"]]["seed"] = row["InputSentence"]
    seed_dict[row["HITId"]]["name1"] = row["InputName1"]
    seed_dict[row["HITId"]]["name2"] = row["InputName2"]
    seed_dict[row["HITId"]]["conj"] = row["InputConj"]
    seed_dict[row["HITId"]]["end1"].append(row["end1"])
    seed_dict[row["HITId"]]["end2"].append(row["end2"])


print(header)

# print table
table_head = """\
<table class="table table-bordered">
<thead>
<tbody>
<tr align="center">
<td colspan="2">
"""

for hitid, sentences in seed_dict.items():
    print(table_head)
    print('<span class="input-sentence">')
    print(sentences["seed"])
    print('</span>')

    print("</td></tr>")
    # print table header and seed
    print('<tr align="center">')
    col1 = '<td style="width:50%"> <span class="end1-sentence"><b>'
    col1 += " ".join([sentences["conj"], sentences["name1"]])
    col1 += '</b></span> </td>'
    print(col1)
    col2 = '<td style="width:50%"> <span class="end2-sentence"><b>'
    col2 += " ".join([sentences["conj"], sentences["name2"]])
    col2 += '</b></span> </td>'
    print(col2)
    print("</tr>")

    for e1, e2 in zip(sentences["end1"], sentences["end2"]):
        print("<tr>")
        print('<td style="width:50%">' + e1 + "</td>")
        print('<td style="width:50%">' + e2 + "</td>")
        print("</tr>")

    print("</tbody></thead></table>")
        

# read csv and add submissions

print(footer)

