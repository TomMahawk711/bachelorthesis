VECTORIZATION_SIZE?=2
OPTIMIZATION_FLAG?=O1

CC=gcc
CFLAGS=-std=gnu11 -Wall -Wextra -pedantic -fopenmp -march=native
SSEFLAGS=-O1
AVXFLAGS=-O2
AVX512FLAGS=-O2
OFLAGS=-$(OPTIMIZATION_FLAG)


all: monte_carlo heat_stencil vector_operations

sse: vector_operations_SSE_single
sse2: vector_operations_SSE2_double
avx: vector_operations_AVX_single vector_operations_AVX_double
avx512: vector_operations_AVX512_single vector_operations_AVX512_double
vector_operations: sse sse2 avx


clean:
	$(RM) *.out

monte_carlo: 
	$(CC) $(CFLAGS) $(OFLAGS) monte_carlo.c -o monte_carlo.out

heat_stencil:
	$(CC) $(CFLAGS) $(OFLAGS) heat_stencil.c -o heat_stencil.out

vector_operations_SSE_single:
	$(CC) $(CFLAGS) $(SSEFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector_operations_SSE_single.c -o vector_operations_SSE_single.out

vector_operations_SSE2_double:
	$(CC) $(CFLAGS) $(SSEFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector_operations_SSE2_double.c -o vector_operations_SSE2_double.out

vector_operations_AVX_single:
	$(CC) $(CFLAGS) $(AVXFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector_operations_AVX_single.c -o vector_operations_AVX_single.out

vector_operations_AVX_double:
	$(CC) $(CFLAGS) $(AVXFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector_operations_AVX_double.c -o vector_operations_AVX_double.out

vector_operations_AVX512_single:
	$(CC) $(CFLAGS) $(AVX512FLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector_operations_AVX512_single.c -o vector_operations_AVX512_single.out

vector_operations_AVX512_double:
	$(CC) $(CFLAGS) $(AVX512FLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector_operations_AVX512_double.c -o vector_operations_AVX512_double.out
