#include <omp.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void* calculate_partial_monte_carlo(void*);

struct thread_args {
	unsigned int seed;
	long* fract_n;
};

int main(int argc, char** argv) {

	int number_of_threads = 1;
	long n = 0;

	if(argc < 3) {
		printf("Usage: ./monte_carlo_par.out <n> <number_of_threads>\n");
		return EXIT_FAILURE;
	} else {
		number_of_threads = atoi(argv[2]);
		n = atol(argv[1]);
	}

	long fract_n = n / number_of_threads;
	long total_inside_points = 0;
	pthread_t threads[number_of_threads - 1];
	void* ret_vals[number_of_threads];
	struct thread_args t_args[number_of_threads];

	for(int i = 0; i < number_of_threads - 1; i++) {
		t_args[i].fract_n = &fract_n;
		t_args[i].seed = time(NULL);
		pthread_create(&threads[i], NULL, calculate_partial_monte_carlo, (void*)&t_args[i]);
	}

	t_args[number_of_threads-1].fract_n = &fract_n;
	t_args[number_of_threads-1].seed = time(NULL);
	ret_vals[number_of_threads - 1] = calculate_partial_monte_carlo((void*)&t_args);
	total_inside_points += *(long*)ret_vals[number_of_threads - 1];
	free(ret_vals[number_of_threads - 1]);

	for(int i = 0; i < number_of_threads - 1; i++) {
		pthread_join(threads[i], &ret_vals[i]);
		total_inside_points += *(long*)ret_vals[i];
		free(ret_vals[i]);
	}

	return EXIT_SUCCESS;
}

void* calculate_partial_monte_carlo(void* n_part) {
	struct thread_args args = *(struct thread_args*)n_part;
	long total_inside = 0;
	for(int i = 0; i < *args.fract_n; i++) {
		float x = ((float)rand_r(&args.seed) / (RAND_MAX));
		float y = ((float)rand_r(&args.seed) / (RAND_MAX));
		if((x * x + y * y) <= 1) {
			total_inside++;
		}
	}

	long* retptr = malloc(sizeof(long));
	*retptr = total_inside;
	return (void*)retptr;
}