//
// Created by jorge on 12/16/20.
//

#ifndef FTDCPARSER_DATASET_H
#define FTDCPARSER_DATASET_H

#include <string>
#include <vector>
#include <map>
#include <boost/thread/mutex.hpp>
#include "Chunk.h"
#include "MergerTasksList.h"

class Dataset {

public:
    Dataset() : samplesInDataset(0),  metricNames(0) {};

    void addChunk(Chunk *pChunk);
    void releaseChunks();
    int mergeChunkMetrics();

    size_t getChunkCount() { return chunkVector.size(); }
    Chunk *getChunk(size_t n) { return (n < chunkVector.size()) ? chunkVector[n] : nullptr; }
    std::vector<Chunk *> getChunkVector() { return chunkVector; }

    size_t getMetricNames(std::vector< std::string> & metricNames);
    size_t getMetricLength() { return samplesInDataset; }
    std::vector<uint64_t>*getMetric(std::string metricName) { return hashMapMetrics[metricName]; }
    std::map<std::string, std::vector<uint64_t>*> getHashMetrics() { return hashMapMetrics; }
    size_t getMetricNamesCount() { return metricNames.size(); }


    void FileParsed();

    void   addMergedMetric(std::basic_string<char, std::char_traits<char>, std::allocator<char>> metricName, std::vector<uint64_t> *data );

private:
    int mergeChunkMetricsMT();
    void sortChunks();

    std::vector<Chunk*> chunkVector;
    size_t samplesInDataset;
    boost::mutex mu;
    std::vector<std::string> metricNames;
    std::map<std::string, std::vector<uint64_t>*> hashMapMetrics;

};


#endif //FTDCPARSER_DATASET_H
