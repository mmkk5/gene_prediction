#translate nucleotides to amino acids

import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import generic_dna

if len(sys.argv) <=2:
    print >>sys.stderr, "please input: cds_exarct.py <input nuc fasta> <output aa fasta>"
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]
with open(input_file, "rU") as fin:
    with open(output_file,"w") as fout:
        for seq_record in SeqIO.parse(fin, "fasta"):
            cds = Seq(str(seq_record.seq), generic_dna)
            aa = cds.translate()
            seq = SeqIO.parse(str(aa), "fasta")
            #print str(seq_record.seq)
            SeqIO.write(seq, fout, "fasta")
