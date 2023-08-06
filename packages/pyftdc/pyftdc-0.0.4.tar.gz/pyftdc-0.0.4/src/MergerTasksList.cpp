//
// Created by Jorge Imperial-Sosa on 9/19/21.
//

#include "MergerTasksList.h"

void
MergerTasksList::push(std::string & metricName, int  index){
    mu.lock();

    MergerTask *t = new MergerTask(metricName, index);

    mergerTasks.push(t);

    mu.unlock();
}


MergerTask *
MergerTasksList::pop(){

    mu.lock();
    auto p = mergerTasks.front();
    mergerTasks.pop();
    mu.unlock();
    return p;
}


bool
MergerTasksList::empty(){
    mu.lock();
    auto e = mergerTasks.empty();
    mu.unlock();
    return e;
}
