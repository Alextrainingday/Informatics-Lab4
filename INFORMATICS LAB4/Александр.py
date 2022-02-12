import re
from timeit import default_timer
import xmltodict
import yaml

def n_tabdef(i):
    n_tab = 0
    for t in i:
        if t == ' ' or t == '-':
            n_tab += 1
        else:
            break
    return n_tab

start = default_timer()
with open("text.yaml", mode="r", encoding="utf-8") as infile:
    infilelist = open("text.yaml", mode="r", encoding="utf-8").read().split('\n')
    outfile = ''
    closes = {}
    count = 0
    for i in infile.readlines():
        if count < len(infilelist):
            count += 1
        i = i.rstrip('\n')
        if i:
            n_tab = n_tabdef(i)
            if n_tab // 2 in closes and n_tab != n_tabdef(infilelist[count]):
                outfile += '\t' * (n_tab // 2) + '</' + closes[n_tab // 2] + '>' + '\n'
                closes[n_tab] = ''
            if i[-1] == ':':
                teg = i[n_tab:len(i) - 1]
                if teg[:2] == '- ':
                    teg = teg[2:]
                outfile += '\t' * (n_tab // 2) + '<' + teg + '>' + '\n'
                closes[n_tab // 2] = teg
            else:
                
                teg = i[n_tab:i.index(':')]
                if teg[:2] == '- ':
                    teg = teg[2:]
                outfile += '\t' * (n_tab // 2) + '<' + teg + '>' + i[i.index(':') + 2:] + '</' + teg + '>' + '\n'
            n_tab = 0
    for i in list(closes)[::-1]:
        if closes[i]:
            outfile += '\t' * i + '</' + closes[i] + '>' + '\n'
    end1 = default_timer() - start
    with open("text.xml", mode='w', encoding='utf-8') as fileout:
        fileout.write(outfile) 
print(end1)

