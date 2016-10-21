from glob import glob
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

def occurrences(string, sub):
    count = start = 0
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count+=1
        else:
            return count

def create_dic_aa():
    aa = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','Y','W']
    dic_aa = {}
    for a in aa:
        for b in aa:
            for c in aa:
                dic_aa[a+b+c] = 0
    return dic_aa





dic_aa = create_dic_aa()

def create_dic_rose():
    rose = ['n','p']
    dic_rose = {}
    for a in rose:
        for b in rose:
            for c in rose:
                dic_rose[a+b+c] = {'*':0,'|':0,'_':0,'?':0}
    return dic_rose

def create_dic_rose_special():
    rose = ['n','p', 'G', 'P']
    dic_rose_special = {}
    for a in rose:
        for b in rose:
            for c in rose:
                dic_rose_special[a+b+c] = {'*':0,'|':0,'_':0,'?':0}
    return dic_rose_special

def create_dic_rose_special_charged():
    rose = ['n','p', 'G', 'P','+','-']
    dic_rose_special_charged = {}
    for a in rose:
        for b in rose:
            for c in rose:
                dic_rose_special_charged[a+b+c] = {'*':0,'|':0,'_':0,'?':0}
    return dic_rose_special_charged

dic_rose = create_dic_rose()
dic_rose_special = create_dic_rose_special()
dic_rose_special_charged = create_dic_rose_special_charged()

def count_hp(dic,ss,c):
    for i in range(1,len(ss)-1):
        dic[c[i-1]+c[i]+c[i+1]][ss[i]] += 1
                
count = 0
for fn in glob("/home/jgcarvalho/sync/data/multissdb/Top8000-best_hom50_pdb_chain/*"):
    # print fn
    with open(fn) as f:
        d = json.load(f)
        seq = ''.join(d['Seq'])
        rose_ss = ''.join([x[0] for x in d['All3HPRose']])
        rose_c = ''.join([x[1] for x in d['All3HPRose']])
        rose_special_ss = ''.join([x[0] for x in d['All3HPRoseSpecial']])
        rose_special_c = ''.join([x[1] for x in d['All3HPRoseSpecial']])
        rose_special_charged_ss = ''.join([x[0] for x in d['All3HPRoseSpecialCharged']])
        rose_special_charged_c = ''.join([x[1] for x in d['All3HPRoseSpecialCharged']])
        count_hp(dic_rose,rose_ss, rose_c)
        count_hp(dic_rose_special,rose_special_ss, rose_special_c)
        count_hp(dic_rose_special_charged,rose_special_charged_ss, rose_special_charged_c)
        for p in dic_aa.keys():
            dic_aa[p] += occurrences(seq, p)
        f.close()
    # count += 1
    # if count == 100:
    #     break

print dic_rose
print dic_rose_special
print dic_rose_special_charged



def count_aa(data):
    df = pd.DataFrame.from_dict(data, orient='index')
    df.columns = ['Count']
    df.sort(columns='Count').to_csv("count.csv")
    df.plot.hist(bins=615, xlim=[0,1700], legend=False)


count_aa(dic_aa)
plt.show()
