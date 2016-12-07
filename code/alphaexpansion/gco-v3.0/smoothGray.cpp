
#include <string>
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include "GCoptimization.h"

#define WIDTH 640
#define HEIGHT 360
#define NUM_LABELS 256

int compute_energy(GCoptimizationGridGraph *gc) {
	std::cout << "computing energy ..." << std::endl;
	return gc->compute_energy();
}

void write(int* result, int i, int lambda1, int lambda2) {
	char filename[100];
	sprintf(filename, "/Users/jkelle/Desktop/StatsProject/results/cartoon/gray/gray_%04d_%03d_%02d.txt", lambda1, lambda2, i);
	std::cout << "writing to output file " << filename << " ..." << std::endl;

	std::ofstream file(filename);
	if (file.is_open()) {
		for (i = 0; i < WIDTH * HEIGHT; i++) {
			file << result[i];
			file << "\n";
		}
		file.close();
		std::cout << "done writing to output file." << std::endl;
	}
	else {
		std::cout << "Unable to open file " << filename << std::endl;
	}
}

/**
 * This program invokes alpha-expansion on a grayscale image.
 * Pixels of the input (noisey) grayscale image are read from stdin.
 * Pixels of the output (smoothed) grayscale are written to disk in a .txt file.
 *
 * D(ui, vi) = (ui - vi)^2
 * V(ui, uj) = lambda1 * min(lambda2, |ui - uj|)
 */
int main(int argc, char* argv[]) {
	int lambda1 = atoi(argv[1]);
	int lambda2 = atoi(argv[2]);
	int num_iterations = atoi(argv[3]);
	int num_pixels = WIDTH * HEIGHT;
	int label;

	// read image and define labels
	std::cout << "reading image from cin ..." << std::endl;
	int *data = new int[num_pixels * NUM_LABELS];
	for(int i = 0; i < num_pixels; i++) {
		// read label value
		std::cin >> label;

		// data energy function
		for (int l = 0; l < NUM_LABELS; l++ ) {
			data[i*NUM_LABELS + l] = (label - l)*(label - l);
		}
	}
	std::cout << "done reading image." << std::endl;

	// next set up the array for smooth costs
	int *smooth = new int[NUM_LABELS*NUM_LABELS];
	for (int l1 = 0; l1 < NUM_LABELS; l1++)
		for (int l2 = 0; l2 < NUM_LABELS; l2++)
			smooth[l1+l2*NUM_LABELS] = lambda1 * std::min(lambda2, abs(l1 - l2));

	int *result = new int[num_pixels];   // stores result of optimization

	try{
		std::cout << "constructing graph ..." << std::endl;
		GCoptimizationGridGraph *gc = new GCoptimizationGridGraph(WIDTH, HEIGHT, NUM_LABELS);
		gc->setDataCost(data);
		gc->setSmoothCost(smooth);

		int energy = compute_energy(gc);
		int prev_energy = energy + 1;
		printf("before optimization, energy is %lld\n", energy);

		std::cout << "beginning optimization ..." << std::endl;
		for (int i = 1; i <= num_iterations && prev_energy != energy; i++) {
			std::cout << "running another cycle of alpha-expansion ..." << std::endl;
			gc->expansion(1);  // run expansion for 1 cycle.
			prev_energy = energy;
			energy = compute_energy(gc);
			printf("after %lld cycles, energy is %lld\n", i, energy);

			for (int i = 0; i < num_pixels; i++) {
				result[i] = gc->whatLabel(i);
			}
			write(result, i, lambda1, lambda2);
		}


		delete gc;
	}
	catch (GCException e){
		e.Report();
	}

	delete [] result;
	delete [] smooth;
	delete [] data;

	return 0;
}
