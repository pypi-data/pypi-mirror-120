//
// Created by Jorge Imperial-Sosa on 9/19/21.
//

#ifndef PYFTDC_MERGERTASK_H
#define PYFTDC_MERGERTASK_H

#include <string>

class MergerTask {

public:
    MergerTask(std::string metricName, int i);
    std::string getMetricName() { return metricName; }
    int getIndex() { return index; }
private:
    std::string metricName;
    int index;
};


#endif //PYFTDC_MERGERTASK_H
