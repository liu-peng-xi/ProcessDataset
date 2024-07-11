#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <string>
#include <algorithm>

using namespace std;

// Function to load the graph from a file
unordered_map<int, unordered_set<int>> loadGraph(const string& filePath) {
    unordered_map<int, unordered_set<int>> adjacencyList;
    ifstream inputFile(filePath);
    string line;

    if (!inputFile.is_open()) {
        cerr << "Error opening file: " << filePath << endl;
        exit(EXIT_FAILURE);
    }

    while (getline(inputFile, line)) {
        istringstream iss(line);
        int src, dest;
        if (!(iss >> src >> dest)) {
            cerr << "Error parsing line: " << line << endl;
            continue;
        }
        adjacencyList[src].insert(dest);
    }

    inputFile.close();
    return adjacencyList;
}

// Function to process the operations and update the adjacency list
void processOperations(const string& operationsFilePath, unordered_map<int, unordered_set<int>>& adjacencyList, const string& outputFilePath, size_t bufferSize) {
    ifstream operationsFile(operationsFilePath);
    ofstream outputFile(outputFilePath);
    string line;
    vector<string> buffer;

    if (!operationsFile.is_open()) {
        cerr << "Error opening operations file: " << operationsFilePath << endl;
        exit(EXIT_FAILURE);
    }

    if (!outputFile.is_open()) {
        cerr << "Error opening output file: " << outputFilePath << endl;
        exit(EXIT_FAILURE);
    }

    while (getline(operationsFile, line)) {
        istringstream iss(line);
        int operation;
        iss >> operation;

        if (operation == 0) { // Insert edge operation
            int src, dest;
            if (!(iss >> src >> dest)) {
                cerr << "Error parsing line: " << line << endl;
                continue;
            }

            auto& neighbors = adjacencyList[src];
            if (neighbors.find(dest) != neighbors.end()) {
                buffer.push_back(to_string(src) + " " + to_string(dest) + " 0");
            } else {
                neighbors.insert(dest);
                buffer.push_back(to_string(src) + " " + to_string(dest) + " 1");
            }
        } else if (operation == 1) { // Delete node operation
            int node;
            if (!(iss >> node)) {
                cerr << "Error parsing line: " << line << endl;
                continue;
            }

            // Remove all outgoing edges
            auto it = adjacencyList.find(node);
            if (it != adjacencyList.end()) {
                for (const auto& neighbor : it->second) {
                    buffer.push_back(to_string(node) + " " + to_string(neighbor) + " 2");
                }
                adjacencyList.erase(it);
            }

            // Remove all incoming edges
            for (auto& [src, neighbors] : adjacencyList) {
                if (neighbors.erase(node)) {
                    buffer.push_back(to_string(src) + " " + to_string(node) + " 2");
                }
            }
        } else {
            cerr << "Unknown operation: " << operation << endl;
            continue;
        }

        // Write buffer to file if it reaches the buffer size
        if (buffer.size() >= bufferSize) {
            for (const string& bufferedLine : buffer) {
                outputFile << bufferedLine << endl;
            }
            buffer.clear();
        }
    }

    // Write any remaining operations in the buffer to file
    for (const string& bufferedLine : buffer) {
        outputFile << bufferedLine << endl;
    }

    operationsFile.close();
    outputFile.close();
}

int main(int argc, char* argv[]) {
    if (argc != 5) {
        cerr << "Usage: " << argv[0] << " <graph_file> <operations_file> <output_file> <buffer_size>" << endl;
        return EXIT_FAILURE;
    }

    string graphFilePath = argv[1];
    string operationsFilePath = argv[2];
    string outputFilePath = argv[3];
    size_t bufferSize = stoi(argv[4]);

    unordered_map<int, unordered_set<int>> adjacencyList = loadGraph(graphFilePath);

    processOperations(operationsFilePath, adjacencyList, outputFilePath, bufferSize);

    return EXIT_SUCCESS;
}
