#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <immintrin.h>

#define REPETITIONS 1e6

void init_array(float*, int, float);
void calculate_array(float*, float*, float*, int);
void print_array(float*, int);
void print_output();

int main(int argc, char** argv){

    int size = 0;

	if(argc < 2) {
		printf("usage: task3.out <vector_size>\n");
		return EXIT_FAILURE;
	} else {
		size = atol(argv[1]);
	}

	float a[size], b[size], c[size];
	init_array(a, size, 0);
	init_array(b, size, 1);
	init_array(c, size, 2);

	//double start_time = omp_get_wtime();
	calculate_array(a, b, c, size);
	//double end_time = omp_get_wtime();

	// print_output(start_time, end_time, a, size);

	return EXIT_SUCCESS;
}

void init_array(float* arr, int vector_size, float init_num){
    for(int i = 0; i<vector_size; ++i){
        arr[i] = init_num;
    }
}

void calculate_array(float* a, float* b, float* c, int size){
    __m256 a_256;
	__m256 b_256;
	__m256 c_256;

	for(int run = 0; run < REPETITIONS; ++run) {
		for(int i = 0; i < size; i += 4) {
			a_256 = _mm256_load_ps(&a[i]);
			b_256 = _mm256_load_ps(&b[i]);
			c_256 = _mm256_load_ps(&c[i]);
			a_256 = _mm256_add_ps(a_256, _mm256_mul_ps(b_256, c_256));
			_mm256_store_ps(&a[i], a_256);
		}
	}
}

void print_array(float* arr, int vector_size){
    printf("[ ");
    for(int i = 0; i<vector_size; i++){
        printf("%.2f ", arr[i]);
    }
    printf("]\n");
}
