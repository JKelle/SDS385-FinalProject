
#include <string>
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include <set>
#include "GCoptimization.h"

#define WIDTH 640
#define HEIGHT 360
#define MASK (1 << 8 - 1)

struct ForDataFn{
	int *data;
};


int smoothFn(int p1, int p2, int l1, int l2) {
	return l1 == l2 ? 0 : 1;
}

int dataFn(int p, int l2, void *data) {
	ForDataFn *myData = (ForDataFn *) data;
	int l1 = myData->data[p];

	int r1 = l1 >> 16;
	int g1 = l1 >> 8 & MASK;
	int b1 = l1 & MASK;

	int r2 = l2 >> 16;
	int g2 = l2 >> 8 & MASK;
	int b2 = l2 & MASK;

	return (r1 - r2)*(r1 - r2) + (g1 - g2)*(g1 - g2) + (b1 - b2)*(b1 - b2);
}


int compute_energy(GCoptimizationGridGraph *gc) {
	std::cout << "computing energy ..." << std::endl;
	return gc->compute_energy();
}

void write(int* result, int i, int lambda1, int lambda2) {
	char filename[100];
	sprintf(filename, "/Users/jkelle/Desktop/StatsProject/results/cartoon/color/color_%04d_%03d_%02d.txt", lambda1, lambda2, i);
	std::cout << "writing to output file " << filename << " ..." << std::endl;

	int label, r, g, b;
	std::ofstream file(filename);
	if (file.is_open()) {
		for (i = 0; i < WIDTH * HEIGHT; i++) {
			label = result[i];
			r = label >> 16;
			g = label >> 8 & MASK;
			b = label & MASK;
			file << r;
			file << "\n";
			file << g;
			file << "\n";
			file << b;
			file << "\n";
		}
		file.close();
		std::cout << "done writing to output file." << std::endl;
	}
	else {
		std::cout << "Unable to open file " << filename << std::endl;
	}
}


int main(int argc, char* argv[]) {
	int lambda1 = atoi(argv[1]);
	int lambda2 = atoi(argv[2]);
	int num_iterations = atoi(argv[3]);
	int num_pixels = WIDTH * HEIGHT;
	int label, r, g, b;
	int r1, g1, b1;

	// define label set
	std::cout << "reading image from cin ..." << std::endl;
	std::set<int> label_set;
	int* label_array = new int[num_pixels];
	for(int i = 0; i < num_pixels; i++) {
		std::cin >> r;
		std::cin >> g;
		std::cin >> b;
		label = (r << 16) | (g << 8) | b;
		label_set.insert(label);
		label_array[i] = label;
	}

	int num_labels = label_set.size();
	std::cout << "total of " << num_labels << " labels." << std::endl;

	int *result = new int[num_pixels];   // stores result of optimization

	try{
		std::cout << "constructing graph ..." << std::endl;
		GCoptimizationGridGraph *gc = new GCoptimizationGridGraph(WIDTH, HEIGHT, num_labels);

		// set up the needed data to pass to function for the data costs
		ForDataFn toFn;
		toFn.data = label_array;

		gc->setDataCost(&dataFn, &toFn);

		// smoothness comes from function pointer
		gc->setSmoothCost(&smoothFn);

		int energy = compute_energy(gc);
		int prev_energy = energy + 1;
		printf("before optimization, energy is %lld\n", energy);

		std::cout << "beginning optimization ..." << std::endl;
		for (int i = 1; i <= num_iterations && prev_energy != energy; i++) {
			std::cout << "running another iteration of alpha-expansion ..." << std::endl;
			gc->expansion(1);// run expansion for 1 iteration. For swap use gc->swap(num_iterations);
			prev_energy = energy;
			energy = compute_energy(gc);
			printf("after %lld iterations, energy is %lld\n", i, energy);

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

	delete [] label_array;
	delete [] result;

	return 0;
}
