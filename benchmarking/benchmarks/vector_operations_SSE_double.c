#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <xmmintrin.h>

#define REPETITIONS 1e6

void init_array(double*, int, double);
void calculate_array(double*, double*, double*, int);
void print_array(double*, int);
void print_output();

int main(int argc, char** argv){

    int size = 0;

	if(argc < 2) {
		printf("usage: task3.out <vector_size>\n");
		return EXIT_FAILURE;
	} else {
		size = atol(argv[1]);
	}

	double a[size], b[size], c[size];
	init_array(a, size, 0);
	init_array(b, size, 1);
	init_array(c, size, 2);

	//double start_time = omp_get_wtime();
	calculate_array(a, b, c, size);
	//double end_time = omp_get_wtime();

	// print_output(start_time, end_time, a, size);

	return EXIT_SUCCESS;
}

void init_array(double* arr, int vector_size, double init_num){
    for(int i = 0; i<vector_size; ++i){
        arr[i] = init_num;
    }
}

void calculate_array(double* a, double* b, double* c, int size){
    __m128 a_128;
	__m128 b_128;
	__m128 c_128;

	for(int run = 0; run < REPETITIONS; ++run) {
		for(int i = 0; i < size; i += 4) {
			a_128 = _mm_load_ps(&a[i]);
			b_128 = _mm_load_ps(&b[i]);
			c_128 = _mm_load_ps(&c[i]);
			a_128 = _mm_add_ps(a_128, _mm_mul_ps(b_128, c_128));
			_mm_store_ps(&a[i], a_128);
		}
	}
}

void print_array(double* arr, int vector_size){
    printf("[ ");
    for(int i = 0; i<vector_size; i++){
        printf("%.2f ", arr[i]);
    }
    printf("]\n");
}