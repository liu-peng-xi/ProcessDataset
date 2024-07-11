# ProcessDataset
第一步：把动态的插入边和删除点，保留时间戳和id，都remap到0->?然后转换成txt

python3 parquet_to_txt.py /data/SNB/interactive-updates-sf1/inserts/Person_knows_Person.parquet /data/SNB/interactive-updates-sf1/inserts/insert.txt /data/SNB/interactive-updates-sf1/inserts/Person_knows_Person_map.txt /data/SNB/interactive-updates-sf1/deletes/Person.parquet /data/SNB/interactive-updates-sf1/deletes/delete.txt

第二步：把两个文件按照时间戳顺序混合，一行放一个操作，并将时间戳删除只保留操作
并设置一个标记位，0来自插入，1来自删除

python3 merge_by_timestamp.py --file1 /data/SNB/interactive-updates-sf1/inserts/insert.txt --file2 /data/SNB/interactive-updates-sf1/deletes/delete.txt --output_file /data/SNB/interactive-updates-sf1/deletes/insert_delete_merged.txt

第三步：处理静态数据，remap一下

python3 csv_to_txt.py --input_file /data/SNB/social_network-sf1-CsvBasic-StringDateFormatter/dynamic/person_knows_person_0_0.csv --output_file /data/SNB/social_network-sf1-CsvBasic-StringDateFormatter/dynamic/person_knows_person_0_0.txt --mapping_output /data/SNB/social_network-sf1-CsvBasic-StringDateFormatter/dynamic/person_knows_person_0_0_map.txt

第四步：先把静态边load到内存里成邻接vector，之后就是每进行一个插入或删除操作就更新一下这个邻接vector，然后再进行下一个操作，最后把所有经过的操作按顺序写到一个新文件中

编译
g++ -o process_graph_operations process_graph_operations.cpp


# bufferSize 是操作的数量，也就是缓冲区中的操作行数，可以改大
# <graph_file> <operations_file> <output_file> <buffer_size>

./process_graph_operations /data/SNB/social_network-sf1-CsvBasic-StringDateFormatter/dynamic/person_knows_person_0_0.txt /data/SNB/interactive-updates-sf1/deletes/insert_delete_merged.txt /data/SNB/interactive-updates-sf1/deletes/graph_process.txt 100
