
import argparse
from collections import Counter
from edit_distance import edit_distance
from matplotlib import pyplot as plt
import pandas as pd
import re
from scipy.cluster import hierarchy

def extract_soundcorrespondences(edits,language1,language2):
    for e in edits[(language1,language2)]:
        print(e)

def plot_lang_relationships(symlangdistance, method):
    df = pd.DataFrame.from_dict(symlangdistance)
    print(df.shape)
    if method == 'upgma':
        Z = hierarchy.linkage(df, 'average')
        plt.figure(figsize=(7, 4))
        hierarchy.dendrogram(Z, orientation='top', labels=df.index, leaf_rotation=90, distance_sort='descending', show_leaf_counts=False)
        plt.title('UPGMA Tree for Dravidian Languages')
        plt.ylabel('Distance')
        plt.xlabel('Languages')
        plt.tight_layout()
        plt.savefig('upgma-dravidian.pdf')
        plt.close()
    #Exercise below
    #if method == 'nj':
    #   Phylogenetic inference using neighbor joining method
    

def mean_symmetrify(lang_distance):
    symmetric_lang_distance = {}
    for k in lang_distance.keys():
        symmetric_lang_distance[k[0]] = symmetric_lang_distance.get(k[0],{})
        symmetric_lang_distance[k[0]][k[1]] = symmetric_lang_distance[k[0]].get(k[1],0.0)
        symmetric_lang_distance[k[0]][k[1]] = (lang_distance[k] + lang_distance[(k[1],k[0])]) / 2.0

    return symmetric_lang_distance

def interlang_comparison(dictionarytsv):
    df = pd.read_csv(dictionarytsv,sep='\t')
    languages = df.columns[1:]

    lang_distance = {}
    lang_edits = {}
    for l1 in languages:
        for l2 in languages:
            if l1 == l2:
                lang_distance[(l1,l2)] = 0.0
            else:
                cnt = 0
                dist = 0
                edits = []
                for w1, w2 in zip(df[l1].tolist(), df[l2].tolist()):
                    if w1 != 'n/a' and w2 != 'n/a': 
                        cnt += 1
                        min_dist = 0
                        min_edits = []
                        pairs = ((x,y) for x in str(w1).split(',') for y in str(w2).split(','))
                        for p in pairs:
                            d,e = edit_distance(p[0].split(), p[1].split())
                            if min_dist == 0 or min_dist > d: 
                                min_dist = d
                                min_edits = e
                        dist += min_dist
                        edits += min_edits
                    lang_distance[(l1,l2)] = float(dist) / cnt
                    lang_edits[(l1,l2)] = [str(e) for e in edits]

    return lang_distance, lang_edits

def main():
    parser = argparse.ArgumentParser(description='Diachronic Linguistics')
    parser.add_argument('--dictfile',help='path to dictionary file',required=True)
    parser.add_argument('--phylogeny',help='Method to infer linguistic phylogeny',choices=['upgma','nj'],default='upgma')
    parser.add_argument('--soundcorrespondences',help='List sound correspondences')
    args = parser.parse_args()
    langdistance, langedits = interlang_comparison(args.dictfile)
    if args.phylogeny != None:
        symlangdistance = mean_symmetrify(langdistance)
        plot_lang_relationships(symlangdistance,args.phylogeny)
    if args.soundcorrespondences != None:
        languages = args.soundcorrespondences.split(',')
        extract_soundcorrespondences(langedits,languages[0],languages[1])

if __name__ == "__main__":
    main()
