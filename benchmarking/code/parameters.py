class Parameters:
    def __init__(self, benchmark_names, start_time, iterations, limit_type, limits, thread_counts, vectorization_sizes, vector_sizes,
                 datatype, map_sizes):
        self.benchmark_names = benchmark_names
        self.start_time = start_time
        self.iterations = iterations
        self.limit_type = limit_type
        self.limits = limits
        self.thread_counts = thread_counts
        self.vectorization_sizes = vectorization_sizes
        self.vector_sizes = vector_sizes
        self.datatype = datatype
        self.map_sizes = map_sizes
