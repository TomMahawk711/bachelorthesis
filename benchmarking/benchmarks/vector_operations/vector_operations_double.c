#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <string.h>

#define REPETITIONS 1e6

#define VECTORIZATION_SIZE 4u

void init_array(double*, int, double);
void calculate_array(double*, double*, double*, int);
void print_array(double*, int);
void print_output();

int main(int argc, char** argv){

    if(argc < 2){
        printf("usage: task1.out <vector_size>\n");
        return EXIT_FAILURE;
    }

    const int vector_size = strtol(argv[1], NULL, 0);

    double a[vector_size], b[vector_size], c[vector_size];
    init_array(a, vector_size, 0);
    init_array(b, vector_size, 1);
    init_array(c, vector_size, 2);

    double start_time = omp_get_wtime();
    calculate_array(a, b, c, vector_size);
    double end_time = omp_get_wtime();

    print_output(start_time, end_time, a, vector_size);

    return EXIT_SUCCESS;
}

void init_array(double* arr, int vector_size, double init_num){
    for(int i = 0; i<vector_size; ++i){
        arr[i] = init_num;
    }
}

void calculate_array(double* a, double* b, double* c, int vector_size){
    for(int run = 0; run < REPETITIONS; run++){
        #pragma omp simd aligned(a, b, c : 16) simdlen(8)
        for(int i = 0; i<vector_size; ++i){
            a[i] += b[i] * c[i];
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

void print_output(double start_time, double end_time, double* arr, int vector_size){
    printf("time: %.4f ", end_time - start_time);
    // print_array(arr, vector_size);
}