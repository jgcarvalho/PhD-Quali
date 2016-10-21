
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import matplotlib.font_manager as font_manager
import seaborn as sns
from glob import glob
from os.path import basename
import cPickle
from sys import argv
matplotlib.style.use('ggplot')
from sklearn import metrics
from ggplot import *


data = {}
colors = {'C':'green','E':'yellow','H':'red','?':'Grey'}

if len(argv) > 1:
    print "Loading data"
    file_data = open(argv[1],'r')
    data = cPickle.load(file_data)

else:
    # tmp = 0
    print "Loading files"
    for fn in glob("/home/jgcarvalho/zeca-apply-results/chameleonic-10/simple/run_10000/outres/*"):
        f_result = fn
        f_ss = "/home/jgcarvalho/zeca-apply-results/chameleonic-10/simple/run_10000/dssp/"+basename(fn)
        f_dssp = "/home/jgcarvalho/sync/data/dsspdb/chameleonic/"+basename(fn)+".dssp"

        ss = ""
        with open(f_ss) as f:
            f.readline()
            ss = f.readline()
            f.close()

        angles = []
        with open(f_dssp) as f:
            l = f.readline()
            while l[2] != '#':
                l = f.readline()
            for i in f.readlines():
                angles.append((float(i[103:109]),float(i[109:115]) ))
                # print "*"+i[97:103]+"*"+i[103:109]+"*"
            f.close()

        lines = []
        with open(f_result) as f:
            f.readline()
            for i in f.readlines():
                l = i.strip().split("\t")
                lines.append(l)
            f.close()

        count = 0
        for i in range(len(ss)):
            if ss[i] != '?':
                lines[i].append(angles[count][0])
                lines[i].append(angles[count][1])
                count += 1
            else:
                lines[i].append(360.0)
                lines[i].append(360.0)
        data[basename(fn)] = pd.DataFrame(lines, columns=['AA','pred_ss','helix','strand','coil','other','entropy', 'true_ss','phi','psi'])

        # tmp += 1
        # if tmp >100:
        #     break

    file_data = open('./all_data.txt', 'w')
    cPickle.dump(data, file_data)



def plot_rama_all(df):
    df.plot.scatter(x='phi', y='psi', title="All", xlim=[-180,180], ylim=[-180,180], c=all_data['true_ss'].apply(lambda x: colors[x]), s=5)
    plt.savefig('./figure_rama_all.pdf')

def plot_rama_per_ss_and_pred(df):
    true_coil = df.loc[df['true_ss'] == 'C']
    true_coil.plot.scatter(x='phi', y='psi', title='Coil', xlim=[-180,180], ylim=[-180,180], c=true_coil['pred_ss'].apply(lambda x: colors[x]), s=5)
    plt.savefig('./figure_rama_coil.pdf')

    true_helix = df.loc[df['true_ss'] == 'H']
    true_helix.plot.scatter(x='phi', y='psi', title='Helix', xlim=[-180,180], ylim=[-180,180], c=true_helix['pred_ss'].apply(lambda x: colors[x]), s=5)
    plt.savefig('./figure_rama_helix.pdf')

    true_strand = df.loc[df['true_ss'] == 'E']
    true_strand.plot.scatter(x='phi', y='psi', title='Strand', xlim=[-180,180], ylim=[-180,180], c=true_strand['pred_ss'].apply(lambda x: colors[x]), s=5)
    plt.savefig('./figure_rama_strand.pdf')
    
def plot_bar(df):

    true_coil = df.loc[df['true_ss'] == 'C']
    true_coil_coil = true_coil.loc[true_coil['pred_ss'] == 'C']
    true_coil_helix = true_coil.loc[true_coil['pred_ss'] == 'H']
    true_coil_strand = true_coil.loc[true_coil['pred_ss'] == 'E']
    true_coil_other = true_coil.loc[true_coil['pred_ss'] == '?']

    true_helix = df.loc[df['true_ss'] == 'H']
    true_helix_coil = true_helix.loc[true_helix['pred_ss'] == 'C']
    true_helix_helix = true_helix.loc[true_helix['pred_ss'] == 'H']
    true_helix_strand = true_helix.loc[true_helix['pred_ss'] == 'E']
    true_helix_other = true_helix.loc[true_helix['pred_ss'] == '?']

    true_strand = df.loc[df['true_ss'] == 'E']
    true_strand_coil = true_strand.loc[true_strand['pred_ss'] == 'C']
    true_strand_helix = true_strand.loc[true_strand['pred_ss'] == 'H']
    true_strand_strand = true_strand.loc[true_strand['pred_ss'] == 'E']
    true_strand_other = true_strand.loc[true_strand['pred_ss'] == '?']

    true_other = df.loc[df['true_ss'] == '?']
    true_other_coil = true_other.loc[true_other['pred_ss'] == 'C']
    true_other_helix = true_other.loc[true_other['pred_ss'] == 'H']
    true_other_strand = true_other.loc[true_other['pred_ss'] == 'E']
    true_other_other = true_other.loc[true_other['pred_ss'] == '?']

    tc = float(len(true_coil))
    th = float(len(true_helix))
    ts = float(len(true_strand))
    to = float(len(true_other))
    freq = [
        [len(true_coil_coil)/tc, len(true_coil_helix)/tc, len(true_coil_strand)/tc,  len(true_coil_other)/tc],
        [len(true_helix_coil)/th, len(true_helix_helix)/th, len(true_helix_strand)/th,  len(true_helix_other)/th],
        [len(true_strand_coil)/ts, len(true_strand_helix)/ts, len(true_strand_strand)/ts,  len(true_strand_other)/ts],
        [len(true_other_coil)/to, len(true_other_helix)/to, len(true_other_strand)/to,  len(true_other_other)/to]
        ]
    print freq
    print tc, th, ts, to
    df2 = pd.DataFrame(freq, columns=['Coil', 'Helix', 'Strand','Other'])
    ax = df2.plot.bar(stacked=True, color=['green','red','yellow','grey'], alpha=0.5)
    ax.xaxis.set_ticklabels(['Coil', 'Helix', 'Strand','Other'])
    # ax.tick_params(labelsize=30)
    plt.savefig('./figure_errors.pdf')
    
def roc_curve(df):
    # roc coil
    label_coil = [1.0 if x == 'C' else 0.0 for x in df['true_ss']]
    pred_coil = [float(x) for x in df['coil']]

    fpr_c,tpr_c,_=metrics.roc_curve(label_coil,pred_coil)
    auc_c = metrics.auc(fpr_c,tpr_c)

    df_coil = pd.DataFrame(dict(FPR=fpr_c, TPR=tpr_c))
    dfax = pd.DataFrame([[0.0,0.0],[1.0,1.0]])
    ax = dfax.plot.line(x=0, y=1,xlim=[0,1], ylim=[0,1], style='k--', legend=False)
    df_coil.plot.area(x='FPR', y='TPR',ax=ax, label='AUC = {0:.3f}'.format(auc_c), alpha=0.5, color='g')
    
    plt.savefig('./figure_roc_coil.pdf')

    # roc helix 
    label_helix = [1.0 if x == 'H' else 0.0 for x in df['true_ss']]
    pred_helix = [float(x) for x in df['helix']]

    fpr_h,tpr_h,_=metrics.roc_curve(label_helix,pred_helix)
    auc_h = metrics.auc(fpr_h,tpr_h)

    df_helix = pd.DataFrame(dict(FPR=fpr_h, TPR=tpr_h))
    ax = dfax.plot.line(x=0, y=1,xlim=[0,1], ylim=[0,1], style='k--', legend=False)
    df_helix.plot.area(x='FPR', y='TPR',ax=ax, label='AUC = {0:.3f}'.format(auc_h), alpha=0.5, color='r')
    plt.savefig('./figure_roc_helix.pdf')


    # roc strand
    label_strand = [1.0 if x == 'E' else 0.0 for x in df['true_ss']]
    pred_strand = [float(x) for x in df['strand']]

    fpr_s,tpr_s,_=metrics.roc_curve(label_strand,pred_strand)
    auc_s = metrics.auc(fpr_s,tpr_s)

    df_strand = pd.DataFrame(dict(FPR=fpr_s, TPR=tpr_s))
    ax = dfax.plot.line(x=0, y=1,xlim=[0,1], ylim=[0,1], style='k--', legend=False)
    df_strand.plot.area(x='FPR', y='TPR',ax=ax, label='AUC = {0:.3f}'.format(auc_s), alpha=0.5, color='y')
    plt.savefig('./figure_roc_strand.pdf')


def distribuicao_ss(df):
    plt.figure()
    dist = df.true_ss.value_counts().plot.bar(color=['grey','red','green','yellow'], alpha=0.5)
    dist.xaxis.set_ticklabels(['undefined', 'Helix', 'Coil','Strand'])
    plt.savefig('./figure_ss_count.pdf')

def distribution(df):
    true_coil = df.loc[df['true_ss'] == 'C']
    true_coil_coil = true_coil.loc[true_coil['pred_ss'] == 'C']
    true_coil_helix = true_coil.loc[true_coil['pred_ss'] == 'H']
    true_coil_strand = true_coil.loc[true_coil['pred_ss'] == 'E']

    true_helix = df.loc[df['true_ss'] == 'H']
    true_helix_coil = true_helix.loc[true_helix['pred_ss'] == 'C']
    true_helix_helix = true_helix.loc[true_helix['pred_ss'] == 'H']
    true_helix_strand = true_helix.loc[true_helix['pred_ss'] == 'E']
    true_helix_other = true_helix.loc[true_helix['pred_ss'] == '?']

    true_strand = df.loc[df['true_ss'] == 'E']
    true_strand_coil = true_strand.loc[true_strand['pred_ss'] == 'C']
    true_strand_helix = true_strand.loc[true_strand['pred_ss'] == 'H']
    true_strand_strand = true_strand.loc[true_strand['pred_ss'] == 'E']
    true_strand_other = true_strand.loc[true_strand['pred_ss'] == '?']

    plt.figure()
    ax_dist_coil = sns.distplot(true_coil_coil.coil, hist=False, rug=True, color="g", rug_kws={"alpha":0.1}, kde_kws={"label":"TP Coil"})
    sns.distplot(true_coil_helix.coil, hist=False, rug=True, color="r", ax=ax_dist_coil, rug_kws={"alpha":0.1}, kde_kws={"ls":'--',"label":"FN Helix (Coil)"})
    sns.distplot(true_coil_strand.coil, hist=False, rug=True, color="y", ax=ax_dist_coil, rug_kws={"alpha":0.1}, kde_kws={"ls":'--',"label":"FN Strand (Coil)"})
    sns.distplot(true_helix_coil.coil, hist=False, rug=True, color="r", ax=ax_dist_coil, rug_kws={"alpha":0.1}, kde_kws={"ls":':',"label":"FP Coil (Helix)"})
    sns.distplot(true_strand_coil.coil, hist=False, rug=True, color="y", ax=ax_dist_coil, rug_kws={"alpha":0.1}, kde_kws={"ls":':',"label":"FP Coil (Strand)"})
    plt.xlim(0,1)
    plt.savefig('./figure_distribution_coil.pdf')

    plt.figure()
    ax_dist_helix = sns.distplot(true_helix_helix.helix, hist=False, rug=True, color="r", rug_kws={"alpha":0.1}, kde_kws={"label":"TP Helix"})
    sns.distplot(true_helix_coil.helix, hist=False, rug=True, color="g", ax=ax_dist_helix, rug_kws={"alpha":0.1}, kde_kws={"ls":'--',"label":"FN Coil (Helix)"})
    sns.distplot(true_helix_strand.helix, hist=False, rug=True, color="y", ax=ax_dist_helix, rug_kws={"alpha":0.1}, kde_kws={"ls":'--',"label":"FN Strand (Helix)"})
    sns.distplot(true_coil_helix.helix, hist=False, rug=True, color="g", ax=ax_dist_helix, rug_kws={"alpha":0.1}, kde_kws={"ls":':',"label":"FP Helix (Coil)"})
    sns.distplot(true_strand_helix.helix, hist=False, rug=True, color="y", ax=ax_dist_helix, rug_kws={"alpha":0.1}, kde_kws={"ls":':',"label":"FP Helix (Strand)"})
    plt.xlim(0,1)
    plt.savefig('./figure_distribution_helix.pdf')


    plt.figure()
    ax_dist_strand = sns.distplot(true_strand_strand.strand, hist=False, rug=True, color="y", rug_kws={"alpha":0.1}, kde_kws={"label":"TP Strand"})
    sns.distplot(true_strand_coil.strand, hist=False, rug=True, color="g", ax=ax_dist_strand, rug_kws={"alpha":0.1}, kde_kws={"ls":'--',"label":"FN Coil (Strand)"})
    sns.distplot(true_strand_helix.strand, hist=False, rug=True, color="r", ax=ax_dist_strand, rug_kws={"alpha":0.1}, kde_kws={"ls":'--',"label":"FN Helix (Strand)"})
    sns.distplot(true_coil_strand.helix, hist=False, rug=True, color="g", ax=ax_dist_strand, rug_kws={"alpha":0.1}, kde_kws={"ls":':',"label":"FP Strand (Coil)"})
    sns.distplot(true_helix_strand.helix, hist=False, rug=True, color="r", ax=ax_dist_strand, rug_kws={"alpha":0.1}, kde_kws={"ls":':',"label":"FP Strand (Helix)"})
    plt.xlim(0,1)
    plt.savefig('./figure_distribution_strand.pdf')




all_data = pd.concat(data.values())
all_data[['helix','strand','coil','other']] = all_data[['helix','strand','coil','other']].apply(pd.to_numeric)
# print all_data.dtypes
# plot_rama_all(all_data)
# plot_rama_per_ss_and_pred(all_data)
plot_bar(all_data )
# roc_curve(all_data)
# distribuicao_ss(all_data)
# distribution(all_data)


plt.show()


