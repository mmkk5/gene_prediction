#coding:utf-8
import sys
import re
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import generic_dna

if len(sys.argv) <=2:
    print >>sys.stderr, "please input: thisFile.py <assembly data file> <output file>"
    sys.exit(1)

input_file = sys.argv[1]   #assembly
output_file = sys.argv[2]

pat1 = re.compile(r'Trichosporon\s([a-z]*?)\s')
pat2 = re.compile(r'(scaffold[0-9]*?).\s')
pat3 = re.compile(r'scaffold_([0-9]*?).\s')
with open(input_file, "rU") as fin:
    with open(output_file,"w") as fout:
        for seq_record in SeqIO.parse(fin, "fasta"):
            desc = seq_record.description
            match1 = pat1.search(desc)
            match2 = pat2.search(desc)  #scaffold0002 for tasahii
            match3 = pat3.search(desc)  #0002 except for tasahii
            if match2 != None:
                seq_record.description = ""
                seq_record.id = "t" + match1.group(1) + "_" + match2.group(1)
                SeqIO.write(seq_record, fout, "fasta")
            elif match3 != None:
                seq_record.description = ""
                seq_record.id = "t" + match1.group(1) + "_" + "scaffold" + match3.group(1)
                SeqIO.write(seq_record, fout, "fasta")
