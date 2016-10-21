
aa = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','Y','W']

# for i in range(10,1000,10):
#     n = str(i).zfill(3)

with open("/home/jgcarvalho/zeca-results-all-cell/zeca-results-all-cell/Top8000-best_hom50_pdb_chain/rose_special_charged/run_10000/prob_g900") as f:
    for i in f.readlines():
        if i[2] in aa and i[8] in aa and i[14] in aa:
            print "{}{}{}, {}, {}".format(i[2],i[8],i[14],
            max(float(i[28:34]), float(i[40:46]), float(i[52:58]),float(i[64:70])),
            min(float(i[28:34]), float(i[40:46]), float(i[52:58]),float(i[64:70])))
    f.close()

# [ R+ ][ R+ ][ R+ ] -> { _ : 0.1060, * : 0.2526, | : 0.3688, ? : 0.2726 }
