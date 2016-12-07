Im = imread('/Users/jkelle/Desktop/StatsProject/data/cartoon/colorFrames/colorFrame000300.jpg');

kappa = 1.1;
for lambda = [0.002, 0.004, 0.008, 0.016, 0.032, 0.064, 0.128, 0.256, 0.512, 1.024]
    S = L0Smoothing(Im, lambda, kappa);
    path = sprintf('/Users/jkelle/Desktop/StatsProject/results/cartoon/color/gradmin_%0.4f_%0.2f.bmp', lambda, kappa);
    imwrite(S, path)
end
