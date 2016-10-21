
helix = []
strand = []
coil = []
other = []
result = "/home/jgcarvalho/zeca-apply-results/chameleonic-10/rose_special_charged/run_10000/outres/2LHC_002"
with open(result) as f:
    f.readline()
    for i in f.readlines():
        l = i.strip().split("\t")
        helix.append(l[2])
        strand.append(l[3])
        coil.append(l[4])
        other.append(l[5])
    f.close()


pdb = "/home/jgcarvalho/Downloads/2lhc.pdb"
c = 0
cur_res = 1
with open(pdb) as f:
    for i in f.readlines():
        if i[0:4] == "MODE":
            c=0
            cur_res=1
        if i[0:4] == "ATOM":
            if int(i[22:27]) == cur_res:
                # print int(i[22:27]), cur_res,
                l = i[:62] + other[c] + i[67:]
            else:
                c+=1
                cur_res += 1
                l = i[:62] + other[c] + i[67:]
            print l,
        else:
            print i,
