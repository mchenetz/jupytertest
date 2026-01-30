import pandas as pd
import os

# Define our storage paths
nfs_path = '/home/jovyan/shared/data/processing_lake/raw_data.csv'
px_block_path = '/home/jovyan/processed_summary.csv'

print(f"--- Starting Data Processing Pipeline ---")

# 1. READ: Consuming data from the Portworx NFS Proxy
if os.path.exists(nfs_path):
    df = pd.read_csv(nfs_path)
    print(f"Successfully read {len(df)} rows from NFS Data Lake.")
    
    # 2. PROCESS: Identify critical sensor failures
    critical_events = df[df['status'] == 'CRITICAL']
    
    # 3. WRITE: Saving the 'Critical' report to Portworx Block storage
    critical_events.to_csv(px_block_path, index=False)
    print(f"Report generated! Saved {len(critical_events)} critical events to Portworx Block.")
else:
    print("Error: raw_data.csv not found in the NFS Data Lake!")
