#coding:utf-8
#CDSをアッセンブリデータからfasta file formatで抜き出す
import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import generic_dna

if len(sys.argv) <=3:
    print >>sys.stderr, "please input: cds_exarct.py <assembly data file> <geneinfo file> <output file>"
    sys.exit(1)

input1_file = sys.argv[1]   #assembly
input2_file = sys.argv[2]   #seq range
output_file = sys.argv[3]

with open(input1_file, "rU") as fin1, open(input2_file, "r") as fin2:
    with open(output_file,"w") as fout:
        n = []            #>から始まるインデックスを除きnucleotide sequenceだけにする
        nuc = ""
        for l in fin1.readlines():
            if len(l) == 0:
                continue
            if ">" in l:
                continue
            else:
                n.append(l.rstrip())    #末尾の改行(\n)はrtripで取り除く
                continue
        for x in n:
            nuc += x
        nucleotide = Seq(nuc)
        nucleotide_r = SeqRecord(nucleotide)
        #print seq_r.seq    #seq表示

        #各geneinfo file についてfor loopを回す
        for m in fin2.readlines():
            g = []
            gen = ""
            m0 = m.rstrip().split("\t")          #["CDS gene 3", "1", "1,15,343,382,453,901,2042,2158,2323,2359"]
            gene_num = m0[0]            #gene_num = "CDS gene 3"
            m1 = m0[2].split(",")       #[1,15,343,382,453,901,2042,2158,2323,2359]
            for i in range(len(m1)):
                if i % 2 == 0:
                    start = int(m1[i])-1
                    stop = int(m1[i+1])
                    part = nucleotide_r.seq[start:stop]      #cds抜き出し
                    g.append(part)
            for y in g:
                gen += y
            gene = Seq(str(gen))
            gene_r = SeqRecord(gene)
            #print >> fout, (">" + gene_num + "\n" + gene_r.seq)
            if m0[1] == "0":
                print >> fout, (">" + gene_num + "\n" + gene_r.seq)
            elif m0[1] == "1":
                print >> fout, (">" + gene_num + "\n" + gene_r.reverse_complement().seq)
            else:
                print >> fout, ("error")
