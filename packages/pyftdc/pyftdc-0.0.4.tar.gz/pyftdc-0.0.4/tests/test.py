# -*- coding: utf-8 -*-
import pyftdc

# Create a parser object
p = pyftdc.FTDCParser()

diagnostics_path = '/Volumes/Ext2TB/test_data/diagnostic.data_40'

# Parse a test directory
status = p.parse_dir(diagnostics_path)
if status == 0:
    print(f"Parsed sample data dir")
    meta = p.metadata
    print(meta[0])
    print(f"metadata has {len(meta)} elements")

    ts = p.timestamps()
    print(f"There are {len(ts)} timestamps")

    metrics = p.metric_names
    print(f"There are {len(metrics)} metrics")

    #
    m = p.get_metric( metrics[37] )
    #print(f"Metric values {m}")
    n = p.get_metric(metrics[73])
    #print(f"Another metric  {n}")

    # As Numpy ndarray
    s = p.get_metric_numpy(metrics[15])
    type_of_var = str(type(s))
    print(f"Metric '{metrics[15]}' is a {type_of_var} with {len(s)} elements")

    metric_list = [metrics[15],metrics[16], metrics[17],metrics[18] ]
    ss = p.get_metrics_list_numpy(metric_list)
    type_of_var = str(type(ss))
    print(f"Metric list '{metric_list}' is a {type_of_var} with {len(ss)} elements")

    i = 0
    for element in ss:
        type_of_var = str(type(element))
        print(f"\t{metric_list[i]}type {type_of_var} with {len(element)} elements")

        i += 1



else:
    print(f"foo: status is {status}")


