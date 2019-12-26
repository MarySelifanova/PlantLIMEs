#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd


# In[10]:


def to_fasta(infile, outfile):
    outlist = []
    
    with open(infile) as inf:
        data = inf.readlines()[1:]
        
        for lime in range(len(data)):
            l = data[lime].split(',')
            seq = l[4]
            l = l[:4]
            name = '>' + ','.join(l)
            outlist.append(name)
            outlist.append('\n')
            outlist.append(seq)
            outlist.append('\n')
    with open(outfile, 'a') as out:
        for line in outlist:
            out.write(line)


# In[11]:


to_fasta('all_data/eudicots_complex.txt', 'all_data/eudicots.fasta')


# In[12]:


to_fasta('all_data/monocots_complex.txt', 'all_data/monocots_complex.fasta' )


# In[5]:


df_cl = pd.read_csv('../all_data/tables/cl_at_eu-mono_ann.csv',index_col=0)


# In[17]:


with open('cl_at.fasta', 'a') as outfile:
    for index, row in df_cl.iterrows():
        #print(type(row['gene']))
        outfile.write('>' + str(row['gene']) +'\n')
        outfile.write(row['Seq'] +'\n')

