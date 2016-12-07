# SDS385-FinalProject

This is my final project for my SDS 385 STATISTICAL MODELS FOR BIG DATA class.
It covers spatial smoothing optimization for removing compression artifacts in cartoon images.
This repo cantains the final paper along with the code I used to run the experiments shown in the paper.

## About

This project investigates two statistical methods for removing noise from cartoon images caused by lossy compression. Both methods, alpha-expansion and L0 gradient minimization, frame this spatial smoothing task as an optimization problem.

The alpha-expansion method models the image as a graph and uses graph cuts to compute a labeling that approximately minimizes graph energy. The L0 gradient minimization method introduces auxiliary variables into the objective function and alternates solving smaller subproblems.

The paper describes both methods in moderate detail and applies them both to an example cartoon image and compares results.

## Related Links

Here are links to the publications that describe the two methods in full detail.

* alpha-expansion: http://www.csd.uwo.ca/~yuri/Papers/pami01.pdf

* L0 gradient minimization: http://www.cse.cuhk.edu.hk/~leojia/projects/L0smoothing/
