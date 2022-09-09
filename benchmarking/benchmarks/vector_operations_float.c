#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <string.h>

#define REPETITIONS 1e6

void init_array(float*, int, float);
void calculate_array(float*, float*, float*, int);
void print_array(float*, int);
void print_output();

int main(int argc, char** argv){

    if(argc < 2){
        printf("usage: task1.out <vector_size>\n");
        return EXIT_FAILURE;
    }

    const int vector_size = strtol(argv[1], NULL, 0);

    float a[vector_size], b[vector_size], c[vector_size];
    init_array(a, vector_size, 0);
    init_array(b, vector_size, 1);
    init_array(c, vector_size, 2);

    calculate_array(a, b, c, vector_size);
    // print_array(a, vector_size);

    return EXIT_SUCCESS;
}

void init_array(float* arr, int vector_size, float init_num){
    for(int i = 0; i<vector_size; ++i){
        arr[i] = init_num;
    }
}

void calculate_array(float* a, float* b, float* c, int vector_size){
    for(int run = 0; run < REPETITIONS; run++){
        #pragma omp simd aligned(a, b, c : 16) simdlen(VECTORIZATION_SIZE)
        for(int i = 0; i<vector_size; ++i){
            a[i] += b[i] * c[i];
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
