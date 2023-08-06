#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include <FTDCParser.h>
#include <vector>
#include <filesystem>
#include <boost/log/core.hpp>
#include <boost/log/trivial.hpp>
#include <boost/log/expressions.hpp>

#include <pybind11-numpy.h>

namespace py = pybind11;

typedef std::vector<uint64_t>* Metrics;
typedef std::vector<std::string> MetricNames;

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)



// helper function to avoid making a copy when returning a py::array_t
// author: https://github.com/YannickJadoul
// source: https://github.com/pybind/pybind11/issues/1042#issuecomment-642215028
template <typename Sequence>

inline py::array_t<typename Sequence::value_type>
as_pyarray(Sequence &&seq) {
    auto size = seq.size();
    auto data = seq.data();
    std::unique_ptr<Sequence> seq_ptr = std::make_unique<Sequence>(std::move(seq));
    auto capsule = py::capsule(seq_ptr.get(), [](void *p) { std::unique_ptr<Sequence>(reinterpret_cast<Sequence*>(p)); });
    seq_ptr.release();
    return py::array(size, data, capsule);
}

inline py::array_t<uint64_t >
as_pyarray(Metrics m) {
    auto size = m->size();
    auto data = m->data();
    std::unique_ptr<Metrics> seq_ptr = std::make_unique<Metrics>(std::move(m));
    auto capsule = py::capsule(seq_ptr.get(),
                               [](void *p) { std::unique_ptr<Metrics>(reinterpret_cast<Metrics *>(p)); });
    seq_ptr.release();
    return py::array(size, data, capsule);
}

struct ParserClass {
    FTDCParser *pParser;
    std::vector<std::string> metadata;

    MetricNames metric_names;

    explicit ParserClass() {
        pParser = new FTDCParser();
    };

    int parseFile(std::string file) {
        namespace logging = boost::log;
        logging::core::get()->set_filter(logging::trivial::severity >  logging::trivial::error);
        int n = pParser->parseFiles(file, false, false);
        return n;
    }

    int parseDir(std::string dir) {

        // if it exists an it is a directory, pop and push contents
        if (std::filesystem::exists(dir) && std::filesystem::is_directory(dir)) {

            std::vector<std::string> fileList;
            for (auto&& fileInPath : std::filesystem::directory_iterator(dir))
                fileList.push_back(fileInPath.path().string());

            // Not really necessary.
            std::sort(fileList.begin(), fileList.end());
            int n = pParser->parseFiles(fileList, false, false);

            metadata = pParser->getMetadata();

            // metric names
            metric_names = pParser->getMetricsNames();

            return n;
        }
        return -1;
    }
    Metrics  timestamps() {
        return pParser->getMetric("start");
    }
    Metrics  getMetric(std::string metricName) {
        return pParser->getMetric(metricName);
    }
    uint64_t getMetricSampleCount() {
        return pParser->getMetricLength();
    }
    py::array_t<unsigned long>  getMetricAsNumpyArray(std::string metricName) {
        auto m = pParser->getMetric(metricName);
        return as_pyarray(m);
    }

    std::vector<py::array_t<unsigned long>> getMetricListAsNumpyArray(std::vector<std::string> metricNames) {
        std::vector<py::array_t<unsigned long>> metricList;

        for(auto name : metricNames) {
            auto element = as_pyarray( pParser->getMetric(name));
            metricList.emplace_back(element);
        }
        return metricList;
    }

};



PYBIND11_MODULE(_core, m) {

    m.doc() = R"pbdoc(
        MongoDB FTDC files parser library.
        -----------------------

        .. currentmodule:: pyftdc

        .. autosummary::
           :toctree: _generate

           parse_dir
           parse_file
           get_metric
           get_metric_sample_count
           get_metric_names
           timestamps
           metadata
    )pbdoc";



  py::class_<ParserClass>(m, "FTDCParser")
        .def(py::init<>())
        .def("parse_dir", &ParserClass::parseDir)
        .def("parse_file", &ParserClass::parseFile)
        .def("get_metric", &ParserClass::getMetric)
        .def("get_metric_sample_count", &ParserClass::getMetricSampleCount)
        .def_readonly("metric_names", &ParserClass::metric_names)
        .def_readonly("metadata", &ParserClass::metadata)
        .def("timestamps", &ParserClass::timestamps)

        .def("get_metric_numpy", &ParserClass::getMetricAsNumpyArray)
        .def("get_metrics_list_numpy", &ParserClass::getMetricListAsNumpyArray)
        ;

#if 0
  py::class_<MetricsMatrix>(m, "MetricsMatrix", py::buffer_protocol())
           .def_buffer([](MetricsMatrix &m) -> py::buffer_info {
               return py::buffer_info(
                       m.data(),                              // Pointer to buffer
                       sizeof(uint64_t),                      // Size of one scalar
                       py::format_descriptor<uint64_t>::format(), // Python struct-style format descriptor
                       2,                                // Number of dimensions
                       { m.rows(), m.cols() },        // Buffer dimensions
                       { sizeof(float) * m.cols(),   // Strides (in bytes) for each index
                         sizeof(uint64_t) }
               );
           })
           ;
#endif

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
