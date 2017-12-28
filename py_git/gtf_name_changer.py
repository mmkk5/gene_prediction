#coding:utf-8
#input
#JXYK01000001.1 Trichosporon faecale strain JCM 2941 scaffold_0001, whole genome shotgun sequence        GeneMark.hmm    exon    1070    2551    0       -       .       gene_id "1_g"; transcript_id "1_t";
#JXYK01000001.1 Trichosporon faecale strain JCM 2941 scaffold_0001, whole genome shotgun sequence        GeneMark.hmm    stop_codon      1070    1072    .       -       0       gene_id "1_g"; transcript_id "1_t";
#JH977535.1 Trichosporon asahii var. asahii CBS 2479 unplaced genomic scaffold scaffold00002, whole genome shotgun sequence      GeneMark.hmm    exon    290     425     0       -       .       gene_id "1_g"; transcript_id "1_t";

import sys
import re

#python [このファイル名] tfaecale.gtf(入力ファイル) tfaecale_e.gtf(出力ファイル)
if len(sys.argv) <=2:
    print >>sys.stderr, "please input: gtf_name_changer.py <input file> <output file>"
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

pat1 = re.compile(r'Trichosporon\s([a-z]*?)\s')
pat2 = re.compile(r'(scaffold[0-9]*?).\s')
pat3 = re.compile(r'scaffold_([0-9]*?).\s')
pat4 = re.compile(r'gene_id\s\"([0-9]*?)_g\";\s')
with open(input_file, "r") as fin:
    with open(output_file,"w") as fout:
        for l in fin.readlines():
            a = []
            a = l.split("\t")
            match1 = pat1.search(a[0])
            match2 = pat2.search(a[0])  #scaffold0002 for tasahii
            match3 = pat3.search(a[0])  #0002 except for tasahii
            match4 = pat4.search(a[8])
            if match2 != None and a[2] == "CDS":    #for tasahii
                a[0] = "t" + match1.group(1) + "_" + match2.group(1)
                a[2] = "t" + match1.group(1) + "_" + match2.group(1) + "_gene" + match4.group(1) + "_" + a[6]
                print >> fout, ('\t'.join(a)),
            elif match3 != None and a[2] == "CDS":   #except for tasahii
                a[0] = "t" + match1.group(1) + "_scaffold" + match3.group(1)
                a[2] = "t" + match1.group(1) + "_scaffold" + match3.group(1) + "_gene" + match4.group(1) + "_" + a[6]
                print >> fout, ('\t'.join(a)),
