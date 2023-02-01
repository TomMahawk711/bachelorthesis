#include <stdio.h>
#include "vector_operations_aux.h"

#define REPETITIONS 1e6

void init_array_single_precision(float* arr, int vector_size, float init_num){
    for(int i = 0; i<vector_size; ++i){
        arr[i] = init_num;
    }
}

void init_array_double_precision(double* arr, int vector_size, double init_num){
    for(int i = 0; i<vector_size; ++i){
        arr[i] = init_num;
    }
}

void print_array_single_precision(float* arr, int vector_size){
    printf("[ ");
    for(int i = 0; i<vector_size; i++){
        printf("%.2f ", arr[i]);
    }
    printf("]\n");
}

void print_array_double_precision(double* arr, int vector_size){
    printf("[ ");
    for(int i = 0; i<vector_size; i++){
        printf("%.2f ", arr[i]);
    }
    printf("]\n");
}

void check_result_single_precision(float* arr, int vector_size){
    for(int i = 0; i < vector_size; ++i) {
        if(arr[i] != REPETITIONS*2){
            printf("invalid result\n");
            return;
        }
    }
    printf("valid result\n");
}

void check_result_double_precision(double* arr, int vector_size){
    for(int i = 0; i < vector_size; ++i) {
        if(arr[i] != REPETITIONS*2){
            printf("invalid result\n");
            return;
        }
    }
    printf("valid result\n");
}
