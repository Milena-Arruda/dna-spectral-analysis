import numpy as np
import random
from .read_files import *
from .write_files import *

def draw_samples(data, M, times, sd):
    results_drawn = dict()
    for t in range(times):
        count = 0
        random.seed(sd + t)
        draw = random.sample(range(len(data)), M)
        results_drawn[t] = {'voss':0, 'eiip':0, 'mem':0, 'qpsk':0, 'alg1':0, 'alg2':0}
        for idx in draw:
            gene = list(data.keys())[idx]
            if count < M:
                results_drawn[t] = {k: results_drawn[t].get(k) + data[gene].get(k) for k in results_drawn[t]}
                count += 1
    return results_drawn

def boxplot_information(results, methods):
    res = dict.fromkeys(methods, {})
    for mtd in methods:
        data = np.zeros(len(results))
        for tag in set(results):
            data[tag] = results[tag][mtd]

        median = np.quantile(data, 0.5)
        q1 = np.quantile(data, 0.25)
        q3 = np.quantile(data, 0.75)
        iqr = q3 - q1
        upper = q3 + 1.5*iqr
        lower = q1 - 1.5*iqr
        if min(data) > lower:
            lower = min(data)
        else:
            lower = sorted(set(data))[1]
        if max(data) < upper:
            upper = max(data)
        else:
            upper = sorted(set(data))[-2]
        res[mtd] = {'lower':lower, 'q1':q1, 'median':median, 'q3':q3, 'upper':upper}
    return res

def acc_sen_spe(TP, FP, args):
    res = dict.fromkeys(args.methods, {})
    for mtd in args.methods:
        acc = np.zeros(args.times)
        sen = np.zeros(args.times)
        spe = np.zeros(args.times)
        for idt in range(args.times):
            tp = TP[idt][mtd]
            fp = FP[idt][mtd]
            fn = args.M - tp
            tn = args.M - fp
            acc[idt] = (tp + tn) / (2*args.M) *100
            sen[idt] = tp / args.M *100
            spe[idt] = tn / args.M *100
        res[mtd] = {'accuracy':[round(np.mean(acc),2), round(np.std(acc),2)],
        'sensitivity':[round(np.mean(sen),2), round(np.std(sen),2)], 'specificity':[round(np.mean(spe),2), round(np.std(spe),2)]}
    return res

def roc(bxplt_TP, bxplt_FP, args):
    res = dict.fromkeys(args.methods, {})
    for mtd in args.methods:
        res[mtd] = {'TP':bxplt_TP[mtd]['median'], 'FP': bxplt_FP[mtd]['median']}
    return res

def statistics(args):
    res = {'bxplt_TP':None, 'bxplt_FP':None, 'roc':0, 'acc_sen_spe':0}
    data_cds = read_summarized_results(args.dir_statistics + 'results-summarized/cds.txt')
    TP = draw_samples(data_cds, args.M, args.times, args.seed)
    res['bxplt_TP'] = boxplot_information(TP, args.methods)

    data_intergenic = read_summarized_results(args.dir_statistics + 'results-summarized/intergenic.txt')
    FP = draw_samples(data_intergenic, args.M, args.times, args.seed)
    res['bxplt_FP'] = boxplot_information(FP, args.methods)

    res['roc'] = roc(res['bxplt_TP'], res['bxplt_FP'], args)

    res['acc_sen_spe'] = acc_sen_spe(TP, FP, args)

    _ = write_statistics(res, args.dir_statistics, args.methods)

    return None