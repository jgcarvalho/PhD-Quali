from glob import glob

def create_dic_aa():
    aa = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','Y','W']
    dic_aa = {}
    for a in aa:
        for b in aa:
            for c in aa:
                dic_aa[a+b+c] = [0,0,0,0,0,0,0,0]
    return dic_aa

dic_aa = create_dic_aa()

for fn in glob("/home/jgcarvalho/zeca-apply-results/Top8000-best_hom50_pdb_chain/rose_special_charged/run_10000/outres/*"):
    with open(fn) as f:
        f.readline()
        lines = f.readlines()
        for i in range(1, len(lines)-1):
            if lines[i][-2] != '?':
                if lines[i][2] == lines[i][-2]:
                    dic_aa[lines[i-1][0] + lines[i][0] +lines[i+1][0]][0] += 1
                else:
                    dic_aa[lines[i-1][0] + lines[i][0] +lines[i+1][0]][1] += 1
            if lines[i][-2] == 'H':
                if lines[i][2] == lines[i][-2]:
                    dic_aa[lines[i-1][0] + lines[i][0] +lines[i+1][0]][2] += 1
                else:
                    dic_aa[lines[i-1][0] + lines[i][0] +lines[i+1][0]][3] += 1
            if lines[i][-2] == 'E':
                if lines[i][2] == lines[i][-2]:
                    dic_aa[lines[i-1][0] + lines[i][0] +lines[i+1][0]][4] += 1
                else:
                    dic_aa[lines[i-1][0] + lines[i][0] +lines[i+1][0]][5] += 1
            if lines[i][-2] == 'C':
                if lines[i][2] == lines[i][-2]:
                    dic_aa[lines[i-1][0] + lines[i][0] +lines[i+1][0]][6] += 1
                else:
                    dic_aa[lines[i-1][0] + lines[i][0] +lines[i+1][0]][7] += 1
        f.close()


# for k in dic_aa.keys():
#     t = float(dic_aa[k][0] + dic_aa[k][1])
#     print "{}, {}, {}, {}, {}".format(k, dic_aa[k][0], dic_aa[k][1], dic_aa[k][0]/t, dic_aa[k][1]/t)

for k in dic_aa.keys():
    t = float(dic_aa[k][0] + dic_aa[k][1])
    th = dic_aa[k][2] + dic_aa[k][3]
    if th > 0:
        th = float(th)
        print "{}, {}, {}, {}, {}, {}, {}".format(k, dic_aa[k][2], dic_aa[k][3], dic_aa[k][2]/th, dic_aa[k][3]/th, th/t, th)

# for k in dic_aa.keys():
#     t = float(dic_aa[k][0] + dic_aa[k][1])
#     te = dic_aa[k][4] + dic_aa[k][5]
#     if te > 0:
#         te = float(te)
#         print "{}, {}, {}, {}, {}, {}, {}".format(k, dic_aa[k][4], dic_aa[k][5], dic_aa[k][4]/te, dic_aa[k][5]/te, te/t, te)

# for k in dic_aa.keys():
#     t = float(dic_aa[k][0] + dic_aa[k][1])
#     tc = dic_aa[k][6] + dic_aa[k][7]
#     if tc > 0:
#         tc = float(tc)
#         print "{}, {}, {}, {}, {}, {}, {}".format(k, dic_aa[k][6], dic_aa[k][7], dic_aa[k][6]/tc, dic_aa[k][7]/tc, tc/t, tc)