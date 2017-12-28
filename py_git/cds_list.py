#coding:utf-8
#biodata>Trichosporon RNASeqAnalysis>genemark>bio3801_geneinfo.txtの形式で抜き出す
#input:
#JXYK01000001.1 Trichosporon faecale strain JCM 2941 scaffold_0001, whole genome shotgun sequence        CDS     1070    2551    1       gene_id "1_g"; transcript_id "1_t";
#JXYK01000001.1 Trichosporon faecale strain JCM 2941 scaffold_0001, whole genome shotgun sequence        CDS     7552    7588    1       gene_id "1_g"; transcript_id "2_t";
#JH977535.1 Trichosporon asahii var. asahii CBS 2479 unplaced genomic scaffold scaffold00002, whole genome shotgun sequence      GeneMark.hmm    CDS     290     425     .       -       2       gene_id "1_g"; transcript_id "1_t";
#output:
#JCM 2941 scaffold_0001 gene_1      1       1070,2551,7552,7588
#CBS 2479 scaffold00002 gene_2      1       290,425

#input: CDS     49      2139     1    gene_id "8455_g"; transcript_id "8455_t"
#output: CDS gene1	　1	　1,15,343,382,453,901,2042,2158,2323,2359,2605


import sys
import re

#python [このファイル名] cds_tfaecale(入力ファイル) cds_list_tfaecale(出力ファイル)
if len(sys.argv) <=2:
    print >>sys.stderr, "please input: cds_list.py <input file> <output file>"
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "r") as fin:
    with open(output_file,"w") as fout:
        '''
        新規geneの場合：新しくリストをつくり、CDS位置情報を格納
        すでに辞書内にリストがある場合：既存のリストに位置情報を追加
        '''
        d = {}
        pat1 = re.compile(r'gene_id\s\"([0-9]*?)_g\"')
        pat2 = re.compile(r'([A-Z][A-Z][A-Z]\s[0-9]*?\sscaffold.*?[0-9]*?)\,')
        #pat2_tasahii = re.compile(r'[A-Z][A-Z][A-Z]\s[0-9]*?.*?\sscaffold([0-9]*?)\,')
        store_gene = 0       #gene number情報が更新される前にひとつ前のデータをとっておくため
        store_scaffold = ""
        store_strand = 0
        for l in fin.readlines():
            a = []
            a = l.split("\t")
            match1 = pat1.search(a[5])
            gene_num = match1.group(1)
            match2 = pat2.search(a[0])
            scaffold_num = match2.group(1)
            start = a[2]
            stop = a[3]
            if gene_num == store_gene and scaffold_num == store_scaffold:
                d[gene_num].append(start)
                d[gene_num].append(stop)
                continue
            elif gene_num == store_gene and scaffold_num != store_scaffold:
                break
            else:
            #if gene_num != store_num
                try:
                    seq = ','.join(map(str,d[store_gene]))
                    print >> fout,  (store_scaffold + " gene_" + store_gene + "\t" + store_strand + "\t" + seq)   #ひとつ前のデータはこの文より前で変更しないように
                except KeyError, e:
                    pass
                store_gene = gene_num
                store_scaffold = scaffold_num
                store_strand = a[4]
                d[gene_num] = []
                d[gene_num].append(start)
                d[gene_num].append(stop)
                continue
        last_seq = ','.join(map(str,d[gene_num]))
        print >> fout, (scaffold_num + " gene_" + gene_num + "\t" + a[4] + "\t" + last_seq)
    fout.close()
fin.close()
