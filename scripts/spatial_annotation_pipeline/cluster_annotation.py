import pandas as pd
import requests, sys
import time

import pandas as pd
import requests, sys
import time

#k = features; #v = their features

d = { 'gene':['gene_id','start', 'end', 'biotype', 'description'],
      'transcript': ['transcript_id', 'start', 'end', 'Parent', 'biotype', 'description'],
      'exon': ['id', 'start', 'end','Parent', 'ensembl_phase', 'ensembl_end_phase'],
      'repeat': ['description', 'start', 'end'],
      'simple': ['logic_name', 'start', 'end'],
      'variation': ['id', 'start', 'end', 'consequence_type', 'clinical_significance', 'alleles'],
      'somatic_variation': ['id', 'start', 'end', 'consequence_type', 'clinical_significance'],
      'structural_variation': ['id', 'start', 'end'],
      'somatic_structural_variation': ['id', 'start', 'end']
    }

d_big = { 'gene':['gene_id','start', 'end', 'biotype', 'description'],
      'transcript': ['transcript_id', 'start', 'end', 'Parent', 'biotype', 'description'],
      'exon': ['id', 'start', 'end','Parent', 'ensembl_phase', 'ensembl_end_phase'],
      'repeat': ['description', 'start', 'end'],
      'simple': ['logic_name', 'start', 'end'],
      'variation': ['id', 'start', 'end', 'consequence_type', 'clinical_significance', 'alleles'],
      'somatic_variation': ['id', 'start', 'end', 'consequence_type', 'clinical_significance'],
      'structural_variation': ['id', 'start', 'end'],
      'somatic_structural_variation': ['id', 'start', 'end'],   
      'regulatory': ['id', 'start', 'end', 'description'],
      'motif': ['stable_id', 'start', 'end', 'transcription_factor_complex', 'binding_matrix_stable_id'],
      'peak': ['id', 'start', 'end', 'description', 'epigenome', 'score'],
      'array_probe': ['probe_name',  'start', 'end', 'probe_set', 'microarray', 'probe_length']
    }

def API_cl(chrom, start, end, di, species):

    for k in d.keys():     
        answer = ''
        
        while True:
            try:
                server = "https://rest.ensembl.org"
                ext = "/overlap/region/" + species + "/" + chrom + ':' + start + "-" + end + '?feature=' + k
                print(ext)
                r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
                break
                
            except requests.exceptions.Timeout:
                time.sleep(10)
                continue
                
        if r.status_code == 200:
            print('200')
            
        else:
            print(r.status_code)            
            time.sleep(10)
            
            while True:
                try:
                    server = "https://rest.ensembl.org"
                    ext = "/overlap/region/arabidopsis_thaliana/" + chrom + ':' + start + "-" + end + '?feature=' + k
                    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
                    break

                except requests.exceptions.Timeout:
                    time.sleep(10)
                    continue
                   
        decoded = r.json()
               
        
        
        if len(decoded) != 0:
            for r in range(len(decoded)):
                rec = decoded[r]
                s = ''

                for f in d[k][3:]:
                    add = str(f) + ':' + str(rec[f]) + ','
                    s += add

                s = str(rec[d[k][0]]) + ':' + str(rec[d[k][1]]) + '-' + str(rec[d[k][2]]) + ',' + str(s)
                s = s[:-1]

                answer += s
                answer += ';'

            di[k] = answer
     
        else:

            answer = 'None'
            di[k] = answer           

#file with clusters
with open('../all_data/clusters/cl_at_eu.txt') as clfile:
    cl_data = clfile.readlines()
    
#create dataframe
columns_clusters = ['Chr', 'Start', 'End', 'Seq', 'LIMEid']
cc = columns_clusters + list(d.keys())

df_clusters = pd.DataFrame(columns=cc)


#annotation
for i in range(1, len(cl_data)):
    
    cluster = cl_data[i].split('\t') 
    d_c = {}
    
    chrom = cluster[0]
    start = cluster[1]
    end = cluster[2]
    
    d_c['Chr'] = chrom
    d_c['Start'] = start
    d_c['End'] = end 
    d_c['Seq'] = cluster[3]
    d_c['LIMEid'] = str(cluster[4].strip()[1:-1].split(':'))
    
    API_cl(chrom, start, end, d_c, 'arabidopsis_thaliana')
      
    df_clusters.loc[i] = d_c
    
df_clusters.to_csv('../all_data/tables/cl_at_eu_ann.csv')
