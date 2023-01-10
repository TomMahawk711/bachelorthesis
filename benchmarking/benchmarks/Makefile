VECTORIZATION_SIZE?=2
OPTIMIZATION_FLAG?=O1

CC=gcc
CFLAGS=-std=gnu11 -Wall -Wextra -pedantic -march=native -fopenmp -$(OPTIMIZATION_FLAG)

all: monte_carlo heat_stencil
vector_operations: vector_operations_SSE_double vector_operations_SSE_single vector_operations_SSE2_double vector_operations_SSE2_single vector_operations_AVX_double vector_operations_AVX_single vector_operations_AVX512_double vector_operations_AVX512_single

clean:
	$(RM) *.out

monte_carlo: 
	$(CC) $(CFLAGS) monte_carlo.c -o monte_carlo.out

heat_stencil:
	$(CC) $(CFLAGS) heat_stencil.c -o heat_stencil.out

vector_operations_SSE_double:
	$(CC) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector_operations_SSE_double.c -o vector_operations_SSE_double.out

vector_operations_SSE_single:
	$(CC) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector_operations_SSE_single.c -o vector_operations_SSE_single.out

vector_operations_SSE2_double:
	$(CC) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector_operations_SSE2_double.c -o vector_operations_SSE2_double.out

vector_operations_SSE2_single:
	$(CC) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector_operations_SSE2_single.c -o vector_operations_SSE2_single.out

vector_operations_AVX_double:
	$(CC) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector_operations_AVX_double.c -o vector_operations_AVX_double.out

vector_operations_AVX_single:
	$(CC) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector_operations_AVX_single.c -o vector_operations_AVX_single.out

vector_operations_AVX512_double:
	$(CC) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector_operations_AVX512_double.c -o vector_operations_AVX512_double.out

vector_operations_AVX512_single:
	$(CC) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector_operations_AVX512_single.c -o vector_operations_AVX512_single.out