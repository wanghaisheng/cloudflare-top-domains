
import modin.pandas as pd
import os
import time
import ray
# Look at the Ray documentation with respect to the Ray configuration suited to you most.
# ray.shutdown()
ray.init(ignore_reinit_error=True)
def merge_csv_files(file_paths, output_path):
    # Read all CSV files into a list of DataFrames
    dfs = []
    for file in file_paths:
        df = pd.read_csv(file)
        df['cfrank']=os.path.basename(file).replace('c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-','').replace('-20240617-20240624.csv')
      
        df['source_file'] = os.path.basename(file)  # Add a column to track the source file
        dfs.append(df[:1000000])
        print(f"File: {file}, Domains: {len(df)}")

    # Merge all DataFrames on the 'domain' column
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on='domain', how='outer', suffixes=('', f'_{df.source_file.iloc[0]}'))
    
    # Remove duplicate columns (if any)
    merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]
    
    # Sort by domain
    merged_df = merged_df.sort_values('domain')
    
    # Count domains present in each file
    for file in file_paths:
        file_name = os.path.basename(file)
        domains_in_file = merged_df[merged_df['source_file'] == file_name]['domain']
        print(f"Domains in {file_name}: {len(domains_in_file)}")
    
    # Count domains present in all files
    # domains_in_all = merged_df.groupby('domain').filter(lambda x: len(x) == len(file_paths))
    # print(f"Domains present in all files: {len(domains_in_all)}")
    
    # Remove the 'source_file' column before saving
    merged_df = merged_df.drop('source_file', axis=1)
    
    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(output_path, index=False)
    
    print(f"Merged CSV saved to {output_path}")
    print(f"Total number of unique domains in merged file: {len(merged_df)}")




l=[
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-1000000-20240617-20240624.csv',
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-500000-20240617-20240624.csv',
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-200000-20240617-20240624.csv',
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-100000-20240617-20240624.csv', 
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-50000-20240617-20240624.csv', 
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-20000-20240617-20240624.csv', 
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-10000-20240617-20240624.csv', 
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-5000-20240617-20240624.csv',
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-2000-20240617-20240624.csv',
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-1000-20240617-20240624.csv',
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-500-20240617-20240624.csv', 
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-200-20240617-20240624.csv']





output_path =r'D:\Download\audio-visual\a_ideas\cloudflare-radar-domains-top-1000000-rank.csv'



# merge_csv_files(l, output_path)
# import modin.pandas as pd
# df =pd.read_csv(output_path)
# count=df['domain']
# print(len(list(set(count))))
