import re
from timeit import default_timer
import xmltodict
import yaml

start = default_timer()

def n_tabdef(i):
    n_tab = 0
    for t in i:
        if t == ' ' or t == '-':
            n_tab += 1
        else:
            break
    return n_tab

with open("text.yaml", mode="r", encoding="utf-8") as infile:
    yam = yaml.safe_load(infile)
    with open("Tuelib.xml", mode='w', encoding='utf-8') as fileout:
        fileout.write(xmltodict.unparse(yam, pretty=True))
        end2 = default_timer()

with open("text.yaml", mode="r", encoding="utf-8") as file:
    infilelist = open("text.yaml", mode="r", encoding="utf-8").read().split('\n')
    n_tab = 0
    closes = {}
    outfile = ''
    count = 0
    for i in file.readlines():
        if count < len(infilelist):
            count += 1
        if re.fullmatch(r'.+\s', i, re.DOTALL):
            n_tab = n_tabdef(i)
            if n_tab // 2 in closes:
                outfile += '\t' * (n_tab // 2) + '</' + closes[n_tab // 2] + '>' + '\n'
                closes[n_tab] = ''
            if re.fullmatch(r'[^:]+:\s', i):
                teg = i[n_tab:len(i) - 2]
                if re.fullmatch(r'- .+', teg, re.DOTALL):
                    teg = teg[2:]
                outfile += '\t' * (n_tab // 2) + '<' + teg + '>' + '\n'
                closes[n_tab // 2] = teg
            else:
                teg = i[n_tab:i.index(':')]
                if re.fullmatch(r'- .+', teg, re.DOTALL):
                    teg = teg[2:]
                outfile += '\t' * (n_tab // 2) + '<' + teg + '>' + i[i.index(':') + 2:].rstrip('\n') + '</' + \
                           teg + '>' + '\n'
            n_tab = 0
    for i in list(closes)[::-1]:
        if closes[i]:
            outfile += '\t' * i + '</' + closes[i] + '>' + '\n'
            end3 = default_timer() - end2
    with open("text.xml", mode='w', encoding='utf-8') as fileout:
        fileout.write(outfile)

print(end2)
print(end3)

with open("text.yaml", mode="r", encoding="utf-8") as infile:
    yam = yaml.safe_load(infile)
    with open("Tue_csv.xml", mode='w', encoding='utf-8') as fileout:
        for item, doc in yam.items():
            fileout.write(item)
            fileout.write('\n')
            fileout.write('"' + str(doc) + '"')
