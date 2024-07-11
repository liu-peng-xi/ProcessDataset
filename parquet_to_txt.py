import pandas as pd
import sys

def remap_ids_and_remove_duplicates(parquet_file, txt_file, id_mapping_file):
    # 读取 Parquet 文件
    df = pd.read_parquet(parquet_file)
    
    # 只保留 Person1Id 和 Person2Id 列
    df = df[['creationDate', 'Person1Id', 'Person2Id']]
    
    # 获取所有唯一的 ID
    unique_ids = pd.concat([df['Person1Id'], df['Person2Id']]).unique()
    
    # 创建 ID 映射：从原始 ID 到新的连续整数 ID
    id_mapping = {id_: int(new_id) for new_id, id_ in enumerate(sorted(unique_ids))}
    
    # 替换原始 ID 为新的连续整数 ID
    df['Person1Id'] = df['Person1Id'].map(id_mapping).astype(int)
    df['Person2Id'] = df['Person2Id'].map(id_mapping).astype(int)
    
    # 删除重复的边
    df = df.drop_duplicates()
    
    # 将 DataFrame 写入到 txt 文件
    df.to_csv(txt_file, index=False, header=False, sep=' ')
    
    # 将 ID 映射写入到文件
    id_mapping_df = pd.DataFrame(list(id_mapping.items()), columns=['OriginalID', 'MappedID'])
    id_mapping_df.to_csv(id_mapping_file, index=False, sep=' ')
    
    # 输出顶点数和边数
    num_vertices = len(unique_ids)
    num_edges = len(df)
    print("动态")
    print(f"Number of vertices: {num_vertices}")
    print(f"Number of edges: {num_edges}")

def remap_deletion_ids(parquet_file, txt_file):
    # 读取 Parquet 文件
    df = pd.read_parquet(parquet_file)
    
    # 只保留 id 列
    df = df[['deletionDate', 'id']]

    # 获取所有唯一的 ID
    unique_ids = pd.concat([df['id']]).unique()
    
    # 创建 ID 映射：从原始 ID 到新的连续整数 ID
    id_mapping = {id_: int(new_id) for new_id, id_ in enumerate(sorted(unique_ids))}
    
    # 替换原始 ID 为新的连续整数 ID
    df['id'] = df['id'].map(id_mapping).astype(int)

    # 将 DataFrame 写入到 txt 文件，每行一个新的映射后 ID
    df.to_csv(txt_file, index=False, header=False, sep=' ')

    num_vertices = len(unique_ids)
    print("删除点的个数")
    print(f"Number of vertices: {num_vertices}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python remap_ids_and_remove_duplicates.py <inserts/Person_knows_Person.parquet> <insert.txt> <id_mapping_file> [deletes/Person.parquet] [delete.txt]")
        sys.exit(1)
    
    parquet_file = sys.argv[1]
    txt_file = sys.argv[2]
    id_mapping_file = sys.argv[3]
    
    remap_ids_and_remove_duplicates(parquet_file, txt_file, id_mapping_file)
    print(f"Parquet file '{parquet_file}' has been converted and saved to '{txt_file}'.")
    
    if len(sys.argv) == 6:
        deletion_parquet_file = sys.argv[4]
        deletion_txt_file = sys.argv[5]
        remap_deletion_ids(deletion_parquet_file, deletion_txt_file)
        print(f"Deletion Parquet file '{deletion_parquet_file}' has been converted and saved to '{deletion_txt_file}'.")
