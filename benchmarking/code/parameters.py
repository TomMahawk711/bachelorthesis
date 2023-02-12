class Parameters:
    # add new parameters here, in benchmarking.save_config(), data_processing.get_config() and the list comprehensions in
    # data_processing._get_data_per_benchmark_per_system()
    def __init__(self, benchmark_names, start_time, iterations, limit_type, limits, thread_counts, vectorization_sizes, vector_sizes,
                 precisions, optimization_flags, instruction_sets, stream_array_sizes, map_sizes, dot_counts):
        self.benchmark_names = benchmark_names
        self.start_time = start_time
        self.iterations = iterations
        self.limit_type = limit_type
        self.limits = limits
        self.thread_counts = thread_counts
        self.vectorization_sizes = vectorization_sizes
        self.vector_sizes = vector_sizes
        self.precisions = precisions
        self.optimization_flags = optimization_flags
        self.instruction_sets = instruction_sets
        self.stream_array_sizes = stream_array_sizes
        self.map_sizes = map_sizes
        self.dot_counts = dot_counts
