import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

if len(sys.argv) <=2:
    print >>sys.stderr, "please input: fasta_concatenator.py <input fasta file> <output fasta file>"
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

ex_id = ""
nuc = []
with open(input_file, "r") as fin:
    with open(output_file,"w") as fout:
        for seq_record in SeqIO.parse(fin, "fasta"):
            curr_id = seq_record.id
            if curr_id == ex_id:
                nuc.append(str(seq_record.seq))
                continue
            elif "+" in ex_id:
                ex_seq = "".join(nuc)
                print >> fout, (">" + ex_id + "\n" + ex_seq)
                ex_id = curr_id
                nuc = []
                nuc.append(str(seq_record.seq))
                continue
            elif "-" in ex_id:
                nuc.reverse()
                ex_seq = "".join(nuc)
                print >> fout, (">" + ex_id + "\n" + ex_seq)
                ex_id = curr_id
                nuc = []
                nuc.append(str(seq_record.seq))
                continue
            else:
                ex_id = curr_id
                nuc.append(str(seq_record.seq))
        if "+" in curr_id:
            last_seq = "".join(nuc)
            print >> fout, (">" + curr_id + "\n" + last_seq)
        elif "-" in curr_id:
            nuc.reverse()
            last_seq = "".join(nuc)
            print >> fout, (">" + curr_id + "\n" + last_seq)
