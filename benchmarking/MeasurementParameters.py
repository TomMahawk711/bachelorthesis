class MeasurementParameters:
    def __init__(self, limits, iterations, limit_type, thread_counts, vectorization_sizes, vector_sizes, map_sizes, benchmark_names,
                 start_time):
        self.limits = limits
        self.iterations = iterations
        self.limit_type = limit_type
        self.thread_counts = thread_counts
        self.vectorization_sizes = vectorization_sizes
        self.vector_sizes = vector_sizes
        self.map_sizes = map_sizes
        self.benchmark_names = benchmark_names
        self.start_time = start_time
