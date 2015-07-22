#!/usr/bin/env python3

import argparse, csv, sys

from common import *

if len(sys.argv) == 1:
    sys.argv.append('-h')


parser = argparse.ArgumentParser()

parser.add_argument('-t', '--threshold', type=int, default=int(10))
parser.add_argument('csv_path', type=str)
parser.add_argument('out_path', type=str)
args = vars(parser.parse_args())

#不包含gbdt特征，只利用其数值分箱，频繁类别筛选

#出现频率超过10次的特征值集合
frequent_feats = read_freqent_feats(args['threshold'])

header=True
with open(args['out_path'], 'w') as f :

    for line,row in enumerate(csv.DictReader(open(args['csv_path']))):
        feats = []
        for feat in gen_feats(row):
            field = feat.split('-')[0]
            type, field = field[0], int(field[1:])
            #type=I Or C ,Field=1~39
            if type == 'C' and feat not in frequent_feats:
                feat = feat.split('-')[0]+'-less'
            #生成特征如 C1less、C2less
            if type == 'C':
                field += 13
            feats.append((field, feat))

        if(header==True):
            f.write('Label,Id,'+','.join(['{0}'.format(feat.split('-')[0]) for (field,feat) in feats])+'\n')
            header=False

        f.write(row['Label'] + ','+row['Id'] + ','+','.join(['{0}'.format(feat.split('-')[1]) for (field,feat) in feats])+'\n')
