VECTORIZATION_SIZE?=2
OPTIMIZATION_FLAG?=O1

CC=gcc
CFLAGS=-std=gnu11 -fopenmp -march=native
SSEFLAGS=-O1
AVXFLAGS=-O1
AVX512FLAGS=-O2
OFLAGS=-$(OPTIMIZATION_FLAG)


all: monte_carlo heat_stencil vector_operations

vector_operations: sse avx avx512 vector_operations_single vector_operations_double
sse: vector_operations_SSE_single vector_operations_SSE2_double
avx: vector_operations_AVX_single vector_operations_AVX_double
avx512: vector_operations_AVX512_single vector_operations_AVX512_double


clean:
	$(RM) *.out

monte_carlo: 
	$(CC) $(CFLAGS) $(OFLAGS) monte_carlo.c -o monte_carlo.out

heat_stencil:
	$(CC) $(CFLAGS) $(OFLAGS) heat_stencil.c -o heat_stencil.out

vector_operations_single:
	$(CC) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector-operations/vector_operations_single.c vector-operations/vector_operations_aux.c -o vector_operations_single.out

vector_operations_double:
	$(CC) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector-operations/vector_operations_double.c vector-operations/vector_operations_aux.c -o vector_operations_double.out

vector_operations_SSE_single:
	$(CC) $(SSEFLAGS) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector-operations/vector_operations_SSE_single.c vector-operations/vector_operations_aux.c -o vector_operations_SSE_single.out

vector_operations_SSE2_double:
	$(CC) $(SSEFLAGS) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector-operations/vector_operations_SSE2_double.c vector-operations/vector_operations_aux.c -o vector_operations_SSE2_double.out

vector_operations_AVX_single:
	$(CC) $(AVXFLAGS) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector-operations/vector_operations_AVX_single.c vector-operations/vector_operations_aux.c -o vector_operations_AVX_single.out

vector_operations_AVX_double:
	$(CC) $(AVXFLAGS) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector-operations/vector_operations_AVX_double.c vector-operations/vector_operations_aux.c -o vector_operations_AVX_double.out

vector_operations_AVX512_single:
	$(CC) $(AVX512FLAGS) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector-operations/vector_operations_AVX512_single.c vector-operations/vector_operations_aux.c -o vector_operations_AVX512_single.out

vector_operations_AVX512_double:
	$(CC) $(AVX512FLAGS) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector-operations/vector_operations_AVX512_double.c vector-operations/vector_operations_aux.c -o vector_operations_AVX512_double.out
