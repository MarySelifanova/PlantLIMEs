#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd


# In[19]:


df_main = pd.read_csv("../all_data/tables/cl_at_eu-mono_ann.csv",index_col=0)


# In[21]:


clan = []
chr_c = []
start_c = []
end_c = []
seq_c = []
LIMEid_c = []
gene_c = []
repeat_c = []

chr_f = []
start_f = []
end_f = []
seq_f = []
LIMEid_f = []
gene_f = []
repeat_f = []


# In[31]:


df_main.head(1)


# In[29]:


cluster_list = [i for i in range(1, 523)]


# In[35]:


clan_counter = 0

for index, row in df_main.iterrows():
    if index in cluster_list:
        
        cluster_list.remove(index)
        clan_counter += 1
        clan.append(clan_counter)
        chr_c.append(row['Chr'])
        start_c.append(row['Start'])
        end_c.append(row['End'])
        seq_c.append(row['Seq'])
        limes = row['LIMEid']
        print(limes)
        LIMEid_c.append(limes)
        gene_c.append(row['gene'])
        repeat_c.append(row['repeat'])
        
        for index_n, row_n in df_main.iterrows():
            
            if index_n in cluster_list and index_n > index:        
                if row_n['LIMEid'] == limes:
                    cluster_list.remove(index_n)
                    clan.append(clan_counter)
                    chr_c.append(row_n['Chr'])
                    start_c.append(row_n['Start'])
                    end_c.append(row_n['End'])
                    seq_c.append(row_n['Seq'])
                    LIMEid_c.append(limes)
                    gene_c.append(row_n['gene'])
                    repeat_c.append(row_n['repeat'])      


# In[36]:


print(len(clan))


# In[38]:


df_clan = pd.DataFrame({'Clan' : clan,
                       'Chr' : chr_c, 'Start': start_c, 'End' : end_c, 'Seq': seq_c, 'LIME': LIMEid_c, 'Gene': gene_c, 'Repeat': repeat_c})


# In[39]:


df_clan


# In[40]:


df_clan.to_csv('at_clans.csv')


# In[ ]:




