import random
import argparse

def process_edge_file(input_file, output_file):
    vertices = set()
    edges = []
    
    # 读取边文件，统计顶点数和边数，并存储边
    with open(input_file, 'r') as f:
        for line in f:
            src, dst = map(int, line.strip().split())
            vertices.add(src)
            vertices.add(dst)
            edges.append((src, dst))
    
    num_vertices = len(vertices)
    num_edges = len(edges)
    
    # 输出顶点数和边数到命令行
    print(f"顶点数: {num_vertices}")
    print(f"边数: {num_edges}")
    
    # 为每条边添加随机权重并写入新文件
    with open(output_file, 'w') as f:
        for src, dst in edges:
            weight = random.randint(0, 10000)
            f.write(f"{src} {dst} {weight}\n")

def main():
    parser = argparse.ArgumentParser(description="Process edge file and add random weights.")
    parser.add_argument('input_file', type=str, help="Input edge file")
    parser.add_argument('output_file', type=str, help="Output file with weights")
    
    args = parser.parse_args()
    
    process_edge_file(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
