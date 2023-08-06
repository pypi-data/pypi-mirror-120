//
// Created by jorge on 12/16/20.
//
#include "include/Dataset.h"
#include "MergerTask.h"
#include "MergerTasksList.h"
#include <boost/log/core.hpp>
#include <boost/log/trivial.hpp>
#include <boost/log/expressions.hpp>
#include <boost/thread.hpp>

namespace logging = boost::log;

size_t
Dataset::getMetricNames(std::vector<std::string> & metrics) {
    if (chunkVector.size() > 0) {
        chunkVector[0]->getMetricNames(metrics);
        return metrics.size();
    }
    else {
        metrics = metricNames;
        return metricNames.size();
    }
}

void
Dataset::addChunk(Chunk *pChunk) {

    // Critical section
    mu.lock();
    this->chunkVector.emplace_back(pChunk);

    // total size of samplesInDataset
    samplesInDataset += pChunk->getSamplesCount();

    // Append metrics here.
    mu.unlock();
}


void
Dataset::addMergedMetric(std::basic_string<char, std::char_traits<char>, std::allocator<char>> metricName, std::vector<uint64_t> *data ) {

    // Critical section
    mu.lock();
    hashMapMetrics.emplace( metricName, data);
    // Append metrics here.
    mu.unlock();
}

void
Dataset::sortChunks() {
    struct {
        bool operator()(Chunk *a, Chunk *b) const { return a->getId() < b->getId(); }
    } compare;
    std::sort(chunkVector.begin(), chunkVector.end(), compare);
}




int
 MergerTaskConsumerThread(MergerTasksList *mergerTasks, Dataset *dataSet) {

    while (!mergerTasks->empty()) {
        MergerTask  *task = mergerTasks->pop();

        std::vector<uint64_t> *fullMetric = new std::vector<uint64_t >;
        fullMetric->reserve(dataSet->getMetricLength());

        size_t chunkNumber = 0;
        size_t chunkMax = dataSet->getChunkVector().size()-1;

        for (auto &chunk: dataSet->getChunkVector() ) {
            auto m = chunk->getMetric(task->getIndex());
            auto start = m->values;
            int count = (chunkNumber == chunkMax)  ? dataSet->getMetricLength() - (300*chunkNumber) : 300;
            fullMetric->insert(fullMetric->end(), start, start+count);
            ++chunkNumber;
        }
        dataSet->addMergedMetric(task->getMetricName(), fullMetric);
    }
    return 0;
}

int
Dataset::mergeChunkMetrics() {

    BOOST_LOG_TRIVIAL(info) << "Sorting chunks";
    sortChunks();

    // Get names to a permanent vector
    // TODO: Find why this vector already has values.
    metricNames.clear();
    getMetricNames(metricNames);

    hashMapMetrics.clear();

    MergerTasksList mergerTasks;

    // Allocate metrics
    BOOST_LOG_TRIVIAL(info) << "Reallocating " << metricNames.size() << " metrics, " << samplesInDataset << " samples each.";

    int metricIndex = 0;
    for (auto metricName : metricNames) {
        mergerTasks.push(metricName, metricIndex);
        ++metricIndex;
    }

#if 1
    // Thread pool
    size_t numThreads =  boost::thread::hardware_concurrency();
    boost::thread_group threads;
    for (size_t i = 0; i < numThreads; ++i)
        threads.add_thread( new boost::thread(MergerTaskConsumerThread, &mergerTasks, this));

    // Wait for threads to finish
    threads.join_all();

#else
    MergerTaskConsumerThread(&mergerTasks, this);
#endif

    BOOST_LOG_TRIVIAL(info) << "Done with reallocation.";
    return 0;
}


void Dataset::releaseChunks() {

    for (auto c : chunkVector) {
        delete c;
    }
    chunkVector.clear();
}

void Dataset::FileParsed() {

    int metricsNameLen = 0;
    for (auto chunk : chunkVector) {

        auto currMetricLen = chunk->getMetricsCount();
        if (metricsNameLen != 0  && metricsNameLen!=currMetricLen) {
            BOOST_LOG_TRIVIAL(debug) << "Number of metrics differ from chunk to chunk:" << metricsNameLen << "!= " << currMetricLen;
        }

        if (metricsNameLen!=currMetricLen) {
            metricNames.clear();
            chunk->getMetricNames(metricNames);
            metricsNameLen = currMetricLen;
        }
    }
}
