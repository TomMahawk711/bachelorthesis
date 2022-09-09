CC = gcc-12
CFLAGS = -std=gnu11 -Wall -Werror -Wextra -pedantic -fopenmp
VARIABLE = -DVECTORIZATION_SIZE=4

all: monte_carlo vector_operations_double vector_operations_float heat_stencil
vector_operations: vector_operations_double vector_operations_float

clean:
	$(RM) *.out

monte_carlo: 
	$(CC) $(CFLAGS) monte_carlo.c -o monte_carlo.out

vector_operations_double: 
	$(CC) $(CFLAGS) $(VARIABLE) vector_operations_double.c -o vector_operations_double.out

vector_operations_float:
	$(CC) $(CFLAGS) $(VARIABLE) vector_operations_float.c -o vector_operations_float.out

heat_stencil: 
	$(CC) $(CFLAGS) heat_stencil.c -o heat_stencil.out
