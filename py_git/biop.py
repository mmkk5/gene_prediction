#coding:utf-8
#CDSをアッセンブリデータからfasta file formatで抜き出す
#input1_file <assembly data>
#>JXYK01000001.1 Trichosporon faecale strain JCM 2941 scaffold_0001, whole genome shotgun sequence
#CGATGGAGGTGACGGAACTAAATCTACAAGACGGGAGCTTAATCACGTGATACGAGaatggcggcgatggccgtgAGAAA
#ACGACGGTTGTTACACTCCGGTAGCCTCATTGTGCTCTGGAAACCAATATTCCGGCACCCAGCATCCATCCTTCACCGGC
#input1_file <geneinfo>
#JCM 2941 scaffold_0018 gene_8617        0       2698,2765,3147,5124
#JCM 2941 scaffold_0018 gene_8618        1       5482,5484,5560,5807,6006,6107,6148,6445,6484,6545,6579,6643,6689,6831

import sys
import re
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

g= ""
pat = re.compile(r'([A-Z][A-Z][A-Z]\s[0-9]*?\sscaffold.[0-9]*)')
with open(input1_file, "rU") as fin1:
    with open(output_file,"w") as fout:
        for seq_record in SeqIO.parse(fin1, "fasta"):
            desc = seq_record.description
            seq = seq_record.seq
            with open(input2_file, "r") as fin2:
                for m in fin2.readlines():
                    m0 = m.rstrip().split("\t")     #["JCM 2941 scaffold_0018 gene_8617","0","2698,2765,3147,5124"]
                    match1 = pat.search(desc)
                    match2 = pat.search(m0[0])
                    if match1.group(1) == match2.group(1):
                    #if match1.group(1) in m0[0]:
                        gene_num = m0[0]
                        m1 = m0[2].split(",")
                    #[1,15,343,382,453,901,2042,2158,2323,2359]
                    #print >> fout, (match1.group(1))
                        for i in range(len(m1)):
                            if i % 2 == 0:
                                start = int(m1[i])-1
                                stop = int(m1[i+1])
                                part = seq[start:stop]      #cds抜き出し
                                g += part
                                gen = Seq(str(g))
                                gene = SeqRecord(gen)
                        if m0[1] == "0":
                            print >> fout, (">" + gene_num + "\n" + gene.seq)
                            #continue
                        elif m0[1] == "1":
                            print >> fout, (">" + gene_num + "\n" + gene.reverse_complement().seq)
                        break
