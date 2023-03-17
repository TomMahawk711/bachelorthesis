from data_processing import process, get_config
from plotting_templates import create_heatmap, create_scatter_plot


def _create_vectorization_scatter_plots_r9_grouping_vector_sizes():
    folder_name = "R9-7900X_bigger-vectors"
    parameters = get_config(folder_name)
    benchmark_name = "vector-operations"
    grouping_metric = parameters.vector_sizes
    grouping_metric_label = [(e*8)/1024 for e in grouping_metric]

    energies, times = \
        process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="NO-SPECIFIC", precision="double", frequency=4700, vector_size=1024, thread_count=4)
    sse_energies, sse_times = \
        process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="SSE2", precision="double", frequency=4700, vector_size=1024, thread_count=4)
    avx_energies, avx_times = \
        process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="AVX", precision="double", frequency=4700, vector_size=1024, thread_count=4)
    avx512_energies, avx512_times = \
        process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="AVX512", precision="double", frequency=4700, vector_size=1024, thread_count=4)

    powers = [energy / time for energy, time in zip(energies, times)]
    sse_powers = [energy / time for energy, time in zip(sse_energies, sse_times)]
    avx_powers = [energy / time for energy, time in zip(avx_energies, avx_times)]
    avx512_powers = [energy / time for energy, time in zip(avx512_energies, avx512_times)]

    sse_speed_up = list()
    avx_speed_up = list()
    avx512_speed_up = list()

    for i in range(len(grouping_metric)):
        sse_speed_up.append(times[i]/sse_times[i])
        avx_speed_up.append(times[i]/avx_times[i])
        avx512_speed_up.append(times[i]/avx512_times[i])

    energies_data = [(grouping_metric_label, energies), (grouping_metric_label, sse_energies), (grouping_metric_label, avx_energies), (grouping_metric_label, avx512_energies)]
    times_data = [(grouping_metric_label, times), (grouping_metric_label, sse_times), (grouping_metric_label, avx_times), (grouping_metric_label, avx512_times)]
    powers_data = [(grouping_metric_label, powers), (grouping_metric_label, sse_powers), (grouping_metric_label, avx_powers), (grouping_metric_label, avx512_powers)]
    speed_up_data = [(grouping_metric_label, sse_speed_up), (grouping_metric_label, avx_speed_up), (grouping_metric_label, avx512_speed_up)]

    # relative_energies = [1 - (e1 / e2) for e1, e2 in zip(sse_energies_2100Mhz, avx_energies_2100Mhz)]

    create_scatter_plot(speed_up_data, "vector size [kiB]", "speed up", "Vectors: speed up of SSE, AVX and AVX512",
                        ["SSE - 4700 MHz", "AVX - 4700 MHz", "AVX512 - 4700 MHz"], "upper right", x_ticks=grouping_metric_label, x_scale='linear', x_rotation=45)
    create_scatter_plot(energies_data, "vector size [kiB]", "consumed energy [Joules]", "Vectors: energy consumption using different instruction sets and vector sizes",
                        ["None - 4700 MHz", "SSE - 4700 MHz", "AVX - 4700 MHz", "AVX512 - 4700 MHz"], "upper left", x_ticks=grouping_metric_label, x_scale='linear', x_rotation=45)
    create_scatter_plot(times_data, "vector size [kiB]", "time [s]", "Vectors: wall times using different instruction sets and vector sizes",
                        ["None - 4700 MHz", "SSE - 4700 MHz", "AVX - 4700 MHz", "AVX512 - 4700 MHz"], "upper left", x_ticks=grouping_metric_label, x_scale='linear', x_rotation=45)
    create_scatter_plot(powers_data, "vector size [kiB]", "power draw [W]", "Vectors: power draw using different instruction sets and vector sizes",
                        ["None - 4700 MHz", "SSE - 4700 MHz", "AVX - 4700 MHz", "AVX512 - 4700 MHz"], "upper left", x_ticks=grouping_metric_label, x_scale='linear', x_rotation=45)
    #create_bar_plot(grouping_metric, relative_energies, "frequencies [MHz]", "relative energy difference", "relative energy difference SSE/AVX")


def _create_vectorization_scatter_plots_r7_grouping_vector_sizes():
    folder_name = "R7-5800X_vectorization"
    parameters = get_config(folder_name)
    benchmark_name = "vector-operations"
    grouping_metric = parameters.vector_sizes[:-1]
    grouping_metric_label = [(e * 8) / 1024 for e in grouping_metric]

    energies, times = \
        process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="NO-SPECIFIC", precision="double", frequency=3800, vector_size=1024, thread_count=4)
    sse_energies, sse_times = \
        process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="SSE2", precision="double", frequency=3800, vector_size=1024, thread_count=4)
    avx_energies, avx_times = \
        process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="AVX", precision="double", frequency=3800, vector_size=1024, thread_count=4)

    powers = [energy / time for energy, time in zip(energies, times)]
    sse_powers = [energy / time for energy, time in zip(sse_energies, sse_times)]
    avx_powers = [energy / time for energy, time in zip(avx_energies, avx_times)]

    sse_speed_up = list()
    avx_speed_up = list()

    for i in range(len(grouping_metric)):
        sse_speed_up.append(times[i] / sse_times[i])
        avx_speed_up.append(times[i] / avx_times[i])

    energies_data = [(grouping_metric_label, energies), (grouping_metric_label, sse_energies), (grouping_metric_label, avx_energies)]
    times_data = [(grouping_metric_label, times), (grouping_metric_label, sse_times), (grouping_metric_label, avx_times)]
    powers_data = [(grouping_metric_label, powers), (grouping_metric_label, sse_powers), (grouping_metric_label, avx_powers)]
    speed_up_data = [(grouping_metric_label, sse_speed_up), (grouping_metric_label, avx_speed_up)]

    # relative_energies = [1 - (e1 / e2) for e1, e2 in zip(sse_energies_2100Mhz, avx_energies_2100Mhz)]

    create_scatter_plot(speed_up_data, "vector size [kiB]", "speed up", "Vectors: speed up of SSE and AVX",
                        ["SSE - 4700 MHz", "AVX - 4700 MHz"], "upper right", x_ticks=grouping_metric_label, x_scale='linear', x_rotation=45)
    create_scatter_plot(energies_data, "vector size [kiB]", "consumed energy [Joules]", "Vectors: energy consumption using different instruction sets and vector sizes",
                        ["None - 4700 MHz", "SSE - 4700 MHz", "AVX - 4700 MHz"], "upper left", x_ticks=grouping_metric_label, x_scale='linear', x_rotation=45)
    create_scatter_plot(times_data, "vector size [kiB]", "time [s]", "Vectors: wall times using different instruction sets and vector sizes",
                        ["None - 4700 MHz", "SSE - 4700 MHz", "AVX - 4700 MHz"], "upper left", x_ticks=grouping_metric_label, x_scale='linear', x_rotation=45)
    create_scatter_plot(powers_data, "vector size [kiB]", "power draw [W]", "Vectors: power draw using different instruction sets and vector sizes",
                        ["None - 4700 MHz", "SSE - 4700 MHz", "AVX - 4700 MHz"], "upper left", x_ticks=grouping_metric_label, x_scale='linear', x_rotation=45)
    # create_bar_plot(grouping_metric, relative_energies, "frequencies [MHz]", "relative energy difference", "relative energy difference SSE/AVX")


def _create_vectorization_scatter_plots_i7_grouping_vector_sizes():
    folder_name = "i7-3770_vectorization"
    parameters = get_config(folder_name)
    benchmark_name = "vector-operations"
    grouping_metric = parameters.vector_sizes[:-2]
    grouping_metric_label = [(e*8)/1024 for e in grouping_metric]

    energies, times = \
        process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="NO-SPECIFIC", precision="double", frequency=3600, vector_size=8192, thread_count=4)
    sse_energies, sse_times = \
        process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="SSE2", precision="double", frequency=3600, vector_size=8192, thread_count=4)
    avx_energies, avx_times = \
        process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="AVX", precision="double", frequency=3600, vector_size=8192, thread_count=4)

    powers = [energy / time for energy, time in zip(energies, times)]
    sse_powers = [energy / time for energy, time in zip(sse_energies, sse_times)]
    avx_powers = [energy / time for energy, time in zip(avx_energies, avx_times)]

    sse_speed_up = list()
    avx_speed_up = list()

    for i in range(len(grouping_metric)):
        sse_speed_up.append(times[i]/sse_times[i])
        avx_speed_up.append(times[i]/avx_times[i])

    energies_data = [(grouping_metric_label, energies), (grouping_metric_label, sse_energies), (grouping_metric_label, avx_energies)]
    times_data = [(grouping_metric_label, times), (grouping_metric_label, sse_times), (grouping_metric_label, avx_times)]
    powers_data = [(grouping_metric_label, powers), (grouping_metric_label, sse_powers), (grouping_metric_label, avx_powers)]
    speed_up_data = [(grouping_metric_label, sse_speed_up), (grouping_metric_label, avx_speed_up)]

    # relative_energies = [1 - (e1 / e2) for e1, e2 in zip(sse_energies_2100Mhz, avx_energies_2100Mhz)]

    create_scatter_plot(speed_up_data, "vector size [kiB]", "speed up", "Vectors: speed up of SSE and AVX",
                        ["SSE - 3600 MHz", "AVX - 3600 MHz"], "upper right", x_ticks=grouping_metric_label, x_scale='linear', x_rotation=45)
    create_scatter_plot(energies_data, "vector size [kiB]", "consumed energy [Joules]", "Vectors: energy consumption using different instruction sets and vector sizes",
                        ["None - 3600 MHz", "SSE - 3600 MHz", "AVX - 3600 MHz"], "upper left", x_ticks=grouping_metric_label, x_scale='linear', x_rotation=45)
    create_scatter_plot(times_data, "vector size [kiB]", "time [s]", "Vectors: wall times using different instruction sets and vector sizes",
                        ["None - 3600 MHz", "SSE - 3600 MHz", "AVX - 3600 MHz"], "upper left", x_ticks=grouping_metric_label, x_scale='linear', x_rotation=45)
    create_scatter_plot(powers_data, "vector size [kiB]", "power draw [W]", "Vectors: power draw using different instruction sets and vector sizes",
                        ["None - 3600 MHz", "SSE - 3600 MHz", "AVX - 3600 MHz"], "upper left", x_ticks=grouping_metric_label, x_scale='linear', x_rotation=45)
    # create_bar_plot(grouping_metric, relative_energies, "frequencies [MHz]", "relative energy difference", "relative energy difference SSE/AVX")


if __name__ == "__main__":
    _create_vectorization_scatter_plots_r9_grouping_vector_sizes()
