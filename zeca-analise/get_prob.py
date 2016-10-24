aa = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','Y','W']

# for i in range(10,1000,10):
#     n = str(i).zfill(3)

with open("/home/jgcarvalho/rose_special_charged/run_10000/prob_g999") as f:
    for i in f.readlines():
        if i[2] in aa and i[8] in aa and i[14] in aa:
            print "{}{}{}, {}".format(i[2],i[8],i[14], float(i[52:58]))
            # max(float(i[28:34]), float(i[40:46]), float(i[52:58]),float(i[64:70])),
            # min(float(i[28:34]), float(i[40:46]), float(i[52:58]),float(i[64:70])))
    f.close()
