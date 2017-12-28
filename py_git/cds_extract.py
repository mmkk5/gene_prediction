#coding:utf-8
#CDSをアッセンブリデータからfasta file formatで抜き出す
#CDS gene 3     1    1,15,343,382,453,901,2042,2158,2323,2359
#output:>CDS gene 3

#ATTENTION:ダウンロードした塩基配列のCDSを示す位置番号が、１から始まる前提でのスクリプトである。
#０から始まる場合などはstart, stopの位置を変更する必要がある。

import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna

if len(sys.argv) <=3:
    print >>sys.stderr, "please input: cds_exarct.py <assembly data file> <geneinfo file> <output file>"
    sys.exit(1)

input1_file = sys.argv[1]   #assembly
input2_file = sys.argv[2]   #seq range
output_file = sys.argv[3]

with open(input1_file, "r") as fin1, open(input2_file, "r") as fin2:
    with open(output_file,"w") as fout:
        list_of_seqs = []
        for seq_record in SeqIO.parse(fin1,"fasta"):
            #print(repr(seq_record.seq))
            list_of_seqs.append(repr(seq_record.seq))
            nuc_seq = sum(list_of_seqs, Seq("", generic_dna))
            print (nuc_seq)

        for m in fin2.readlines():
            gene = []
            #gene = ""
            m0 = m.split("\t")          #["CDS gene 3","1","1,15,343,382,453,901,2042,2158,2323,2359"]
            gene_num = m0[0]             #gene_num = "CDS gene 3"
            m1 = m0[2].split(",")       #[1,15,343,382,453,901,2042,2158,2323,2359]
            for i in range(len(m1)):
                if i % 2 == 0:
                    start = int(m1[i])-1
                    stop = int(m1[i+1])
                    part = nuc_seq[start:stop]      #cds抜き出し
                    cds = gene.append(repr(part))
            #for y in g:
            #   gene += y
            if m0[1] == 0:
                print >> fout, (">" + gene_num + "\n" + cds)
                continue
            elif m0[1] == 1:
                print >> fout, (">" + gene_num + "\n" + repr(cds.reversecomplement()))
                continue
