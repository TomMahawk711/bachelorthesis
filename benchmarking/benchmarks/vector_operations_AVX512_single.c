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
    __m512 a_512;
	__m512 b_512;
	__m512 c_512;

	for(int run = 0; run < REPETITIONS; ++run) {
		for(int i = 0; i < size; i += 16) {
			a_512 = _mm512_load_ps(&a[i]);
			b_512 = _mm512_load_ps(&b[i]);
			c_512 = _mm512_load_ps(&c[i]);
			a_512 = _mm512_add_ps(a_512, _mm512_mul_ps(b_512, c_512));
			_mm512_store_ps(&a[i], a_512);
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