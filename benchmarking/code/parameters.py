class Parameters:
    # add new parameters here, in benchmarking.save_config() and in data_processing.get_config()
    def __init__(self, benchmark_names, start_time, iterations, limit_type, limits, thread_counts, vectorization_sizes, vector_sizes,
                 precisions, map_sizes, optimization_flags, instruction_sets):
        self.benchmark_names = benchmark_names
        self.start_time = start_time
        self.iterations = iterations
        self.limit_type = limit_type
        self.limits = limits
        self.thread_counts = thread_counts
        self.vectorization_sizes = vectorization_sizes
        self.vector_sizes = vector_sizes
        self.precisions = precisions
        self.map_sizes = map_sizes
        self.optimization_flags = optimization_flags
        self.instruction_sets = instruction_sets
