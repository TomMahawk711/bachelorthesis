VECTORIZATION_SIZE?=2
OPTIMIZATION_FLAG?=O1

CC=gcc
CFLAGS=-std=gnu11 -Wall -Wextra -pedantic -march=native -fopenmp -$(OPTIMIZATION_FLAG)

all: monte_carlo heat_stencil
vector_operations: vector_operations_float

clean:
	$(RM) *.out

monte_carlo: 
	$(CC) $(CFLAGS) monte_carlo.c -o monte_carlo.out

vector_operations_SSE_double:
	$(CC) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector_operations_SSE_double.c -o vector_operations_SSE_double.out

vector_operations_SSE_float:
	$(CC) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector_operations_SSE_float.c -o vector_operations_SSE_float.out

vector_operations_SSE2_double:
	$(CC) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector_operations_SSE2_double.c -o vector_operations_SSE2_double.out

vector_operations_SSE2_float:
	$(CC) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector_operations_SSE2_float.c -o vector_operations_SSE2_float.out

vector_operations_AVX:
	$(CC) $(CFLAGS) -DVECTORIZATION_SIZE=$(VECTORIZATION_SIZE) vector_operations_float.c -o vector_operations_float.out

heat_stencil: 
	$(CC) $(CFLAGS) heat_stencil.c -o heat_stencil.out
