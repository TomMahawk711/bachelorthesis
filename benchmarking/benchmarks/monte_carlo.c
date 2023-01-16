#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

int main(int argc, char** argv){

    int n = 0;
    int num_threads = 1;

    if(argc < 3){
        printf("Usage: ./monte_carlo.out <number_of_calculations> <number_of_threads>\n");
        return EXIT_FAILURE;
    } else{
        n = atol(argv[1]);
        num_threads = atol(argv[2]);
    }

    unsigned int seed = 0;
    long total_inside = 0;
    omp_set_num_threads(num_threads);
    double start_time = omp_get_wtime();

    #pragma omp parallel private(seed)
    {
        long partial_inside = 0;
        seed = time(NULL);
        #pragma omp for schedule(static)
        for(int i = 0; i < n; i++){
            float x = ((float) rand_r(&seed) / (RAND_MAX));
            float y = ((float) rand_r(&seed) / (RAND_MAX));
            if((x*x + y*y)<= 1){
                partial_inside++;
            }
        }

        #pragma omp for schedule(static)
        for(int i = 0; i<num_threads; i++){
            #pragma omp atomic
                total_inside+=partial_inside;
        }
    }

    double end_time = omp_get_wtime();
    printf("sum: %f time: %2.6f \n", 4 * (float) total_inside / n, end_time-start_time);


    return EXIT_SUCCESS;
}