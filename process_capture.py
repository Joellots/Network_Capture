import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('capture.csv')

# Drop rows with missing values
df.dropna(inplace=True)

# Define functions to compute additional metrics
def compute_metrics(df):
    df['same_srv_rate'] = df.apply(lambda row: compute_same_srv_rate(df, row['tcp.srcport']), axis=1)
    df['diff_srv_rate'] = df.apply(lambda row: compute_diff_srv_rate(df, row['tcp.srcport']), axis=1)
    df['dst_host_same_srv_rate'] = df.apply(lambda row: compute_dst_host_same_srv_rate(df, row['tcp.dstport']), axis=1)
    df['dst_host_srv_diff_host_rate'] = df.apply(lambda row: compute_dst_host_srv_diff_host_rate(df, row['tcp.dstport']), axis=1)
    df['dst_host_srv_serror_rate'] = df.apply(lambda row: compute_dst_host_srv_serror_rate(df, row['tcp.dstport']), axis=1)
    df['dst_host_rerror_rate'] = df.apply(lambda row: compute_dst_host_rerror_rate(df, row['tcp.dstport']), axis=1)
    df['dst_host_serror_rate'] = df.apply(lambda row: compute_dst_host_serror_rate(df, row['tcp.dstport']), axis=1)
    df['dst_host_srv_count'] = df.apply(lambda row: compute_dst_host_srv_count(df, row['tcp.dstport']), axis=1)
    df['dst_host_diff_srv_rate'] = df.apply(lambda row: compute_dst_host_diff_srv_rate(df, row['tcp.dstport']), axis=1)
    df['count'] = df.apply(lambda row: compute_count(df, row['tcp.dstport']), axis=1)
    df['src_bytes'] = df['tcp.srcport']  # This is just an example, adjust accordingly
    df['dst_bytes'] = df['tcp.dstport']  # This is just an example, adjust accordingly
    return df

# Define helper functions for metrics calculation
def compute_same_srv_rate(df, src_port):
    same_srv_connections = df[df['tcp.srcport'] == src_port]
    return len(same_srv_connections) / len(df)

def compute_diff_srv_rate(df, src_port):
    diff_srv_connections = df[df['tcp.srcport'] != src_port]
    return len(diff_srv_connections) / len(df)

def compute_dst_host_same_srv_rate(df, dst_port):
    same_srv_connections = df[df['tcp.dstport'] == dst_port]
    return len(same_srv_connections) / len(df)

def compute_dst_host_srv_diff_host_rate(df, dst_port):
    diff_srv_connections = df[df['tcp.dstport'] != dst_port]
    return len(diff_srv_connections) / len(df)

def compute_dst_host_srv_count(df, dst_port):
    srv_count = len(df[df['tcp.dstport'] == dst_port])
    return srv_count

def compute_dst_host_diff_srv_rate(df, dst_port):
    total_connections = len(df)
    dst_host_count = len(df[df['tcp.dstport'] == dst_port])
    if total_connections > 0:
        return (total_connections - dst_host_count) / total_connections
    else:
        return 0.0

def compute_dst_host_srv_serror_rate(df, dst_port):
    serror_connections = df[(df['tcp.dstport'] == dst_port) & (df['tcp.flags.syn'] == True)]
    return len(serror_connections) / len(df)

def compute_dst_host_rerror_rate(df, dst_port):
    rerror_connections = df[(df['tcp.dstport'] == dst_port) & (df['tcp.flags.reset'] == True)]
    return len(rerror_connections) / len(df)

def compute_dst_host_serror_rate(df, dst_port):
    serror_connections = df[(df['tcp.dstport'] == dst_port) & (df['tcp.flags.syn'] == True)]
    return len(serror_connections) / len(df)

def compute_count(df, dst_port):
    count_connections = df[df['tcp.dstport'] == dst_port]
    return len(count_connections)

# Compute the metrics
df_with_metrics = compute_metrics(df)

# Output the results (for demonstration purposes)
print(df_with_metrics)

# Save the results to a new CSV file if needed
df_with_metrics.to_csv('capture_with_metrics.csv', index=False)
