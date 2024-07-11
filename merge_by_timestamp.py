import argparse

def read_file(file_path, label):
    with open(file_path, 'r') as file:
        lines = [line.strip().split(maxsplit=1) for line in file]
        return [(int(timestamp), label, rest) for timestamp, rest in lines]

def merge_files(file1_data, file2_data):
    merged_data = sorted(file1_data + file2_data, key=lambda x: x[0])
    return merged_data

def write_merged_file(merged_data, output_file):
    with open(output_file, 'w') as file:
        for _, label, rest in merged_data:
            file.write(f"{label} {rest}\n")

def main():
    parser = argparse.ArgumentParser(description='Merge two TXT files based on timestamp.')
    parser.add_argument('--file1', required=True, help='insert TXT file')
    parser.add_argument('--file2', required=True, help='delete input TXT file')
    parser.add_argument('--output_file', required=True, help='Output merge TXT file')

    args = parser.parse_args()

    file1_data = read_file(args.file1, 0)
    file2_data = read_file(args.file2, 1)

    merged_data = merge_files(file1_data, file2_data)
    write_merged_file(merged_data, args.output_file)

if __name__ == '__main__':
    main()
