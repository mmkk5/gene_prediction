#coding:utf-8
import sys
import re

if len(sys.argv) <=2:
    print >>sys.stderr, "please input: scaffold_counter.py <input file> <output file>"
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

scaffold = "s"
length = 0
with open(input_file, "r") as fin:
    with open(output_file,"w") as fout:
        d = {}
        #以下のpatはassembly nameに合わせて使い分けて。
        pat = re.compile(r'(scaffold_[0-9]*?),')
        #pat = re.compile(r'(scaffold[0-9]*?),')
        for l in fin.readlines():
            if ">" in l:
                print >>fout, (scaffold + "\t" + str(length))
                length = 0
                scaffold = pat.search(l).group(0)
                continue
            else:
                length += len(l.rstrip())
                continue
        print >>fout, (scaffold + "\t" + str(length))
    fout.close()
fin.close()
