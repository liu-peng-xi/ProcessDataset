import csv
import argparse

def read_id_pairs_from_csv(file_path):
    id_pairs = []
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='|')
        next(csvreader)  # 跳过标题行
        for row in csvreader:
            id_pairs.append((row[0], row[1]))
    return id_pairs

def create_id_mapping(id_pairs):
    unique_ids = sorted(set(id for pair in id_pairs for id in pair), key=int)
    id_mapping = {old_id: new_id for new_id, old_id in enumerate(unique_ids)}
    return id_mapping

def write_mapping_file(id_mapping, mapping_output):
    with open(mapping_output, 'w') as mapfile:
        for old_id, new_id in id_mapping.items():
            mapfile.write(f"{old_id} {new_id}\n")

def write_mapped_pairs(id_pairs, id_mapping, output_file):
    with open(output_file, 'w') as txtfile:
        for old_id1, old_id2 in id_pairs:
            txtfile.write(f"{id_mapping[old_id1]} {id_mapping[old_id2]}\n")

def main():
    parser = argparse.ArgumentParser(description='Process and map ID pairs from a CSV file.')
    parser.add_argument('--input_file', required=True, help='Input static graph CSV file with ID pairs')
    parser.add_argument('--output_file', required=True, help='Output TXT file for mapped ID pairs')
    parser.add_argument('--mapping_output', required=True, help='Output TXT file for ID mapping')

    args = parser.parse_args()

    id_pairs = read_id_pairs_from_csv(args.input_file)
    id_mapping = create_id_mapping(id_pairs)

    write_mapping_file(id_mapping, args.mapping_output)
    write_mapped_pairs(id_pairs, id_mapping, args.output_file)

if __name__ == '__main__':
    main()
