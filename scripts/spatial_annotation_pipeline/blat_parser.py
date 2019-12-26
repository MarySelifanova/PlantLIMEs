import pandas as pd

chrom_dict = {'NC_003074.8': '3',
             'NC_003075.7': '4',
             'NC_003071.7': '2',
             'NC_003070.9': '1',
             'NC_003076.8': '5',
             'NC_000932.1': 'Pt',
              'NC_037304.1': 'Mt'}

def blat_parser(filename):
    
    with open(filename) as inf:
        
        columns = ['matches', 'misMatches', 'repMatches', 'nCount', 'qNumInsert', 'qBaseInsert', 'tNumInsert', 'tBaseInsert', 'strand', 'LIMEid', 'LIMEsize', 'qStart', 'qEnd', 'Chr', 'Chr_Size', 'tStart', 'tEnd', 'blockCount', 'blockSizes', 'qStarts', 'tStarts']
        df = pd.DataFrame(columns=columns)
        
        inf = inf.readlines()
        for i in range(5, len(inf)):
            
            l = inf[i].split()
            d = {}
            for j in range(len(l)):
                
                key = columns[j]
                value = l[j]
                
                if key == 'Chr':
                    value = chrom_dict[value]
                    
                d[key] = value
            print(d)
            
            df.loc[i] = d                
    
    return df 

eu_df = blat_parser('../blat_output/eudicots.psl')
mono_df = blat_parser('../blat_output/monocots.psl')

def filter_m(df):
    filter_match = df['misMatches'] == df['LIMEsize']
    df = df.loc[filter_match]
    return df

filter_m(eu_df)
filter_m(mono_df)

seq_dict_eu = {}
seq_dict_mono = {}

def seqd(file, seq_dict):
    
    with open(file) as fasta:
        f_data = fasta.readlines()

        for f in range(len(f_data)):
            if f_data[f][0] == '>':
                key = f_data[f][1:-1]
            else:
                value = f_data[f][:-1]
                seq_dict[key] = value
    return seq_dict    
                
seqd('../input/eudicots.fasta', seq_dict_eu)
seqd('../input/monocots.fasta', seq_dict_mono)
          
            
def make_txt(file, df, seq_dict):
    
    with open(file, 'a') as outfile:

        outfile.write('#LimeID,Chr,Start,Length,Sequence,SequenceType\n')

        for index, row in df.iterrows():

            name = row['LIMEid']
            sequence = seq_dict[name]
            
            name = name.split(',')
            name = name[0] + ',' + row['Chr'] + ',' + row['tStart'] + ',' + name[3]

            seqtype = row['repMatches'] + '_' + row['strand']

            s = name + ',' + sequence + ',' + seqtype + '\n'

            outfile.write(s)
                
make_txt('../eudicots.txt', eu_df, seq_dict_eu)
make_txt('../monocots.txt', mono_df, seq_dict_mono)
            
            
