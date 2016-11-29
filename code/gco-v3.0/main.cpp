
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
#define LAMBDA1 8
#define LAMBDA2 1

int compute_energy(GCoptimizationGridGraph *gc) {
	std::cout << "computing energy ..." << std::endl;
	return gc->compute_energy();
}

void write(int* result, int i) {
	char filename[20];
	sprintf(filename, "output%02d_%d.res", LAMBDA, i);
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


int main() {
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
			smooth[l1+l2*NUM_LABELS] = LAMBDA1 * std::min(LAMBDA2, abs(l1 - l2));

	int *result = new int[num_pixels];   // stores result of optimization

	try{
		std::cout << "constructing graph ..." << std::endl;
		GCoptimizationGridGraph *gc = new GCoptimizationGridGraph(WIDTH, HEIGHT, NUM_LABELS);
		gc->setDataCost(data);
		gc->setSmoothCost(smooth);

		int energy = compute_energy(gc);
		printf("before optimization, energy is %lld\n", energy);

		std::cout << "beginning optimization ..." << std::endl;
		for (int i = 1; i < 10; i++) {
			gc->expansion(1);// run expansion for 2 iterations. For swap use gc->swap(num_iterations);
			int energy = compute_energy(gc);
			printf("after %lld iterations, energy is %lld\n", i, energy);

			for (int i = 0; i < num_pixels; i++) {
				result[i] = gc->whatLabel(i);
			}
			write(result, i);
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
