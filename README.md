# Layer Ensembles PyTorch

This repository contains a Pytorch implementation of Layer Ensembles (LEns) and image classification experiments for the [Layer Ensembles paper](https://arxiv.org/abs/2210.04882).

Deep Ensembles, as a type of Bayesian Neural Networks, can be used to estimate uncertainty on the prediction of multiple neural networks by collecting votes from each network and computing the difference in those predictions. In this paper, we introduce a method for uncertainty estimation that considers a set of independent categorical distributions for each layer of the network, giving many more possible samples with overlapped layers than in the regular Deep Ensembles. We further introduce an optimized inference procedure that reuses common layer outputs, achieving up to 19× speed up and reducing memory usage quadratically. We also show that the method can be further improved by ranking samples, resulting in models that require less memory and time to run while achieving higher uncertainty quality than Deep Ensembles.

## Run

Use `run_example.sh` to train and evaluate a single model on MNIST.
## Citation

If you use this work for your research, you can cite it as:
```
@article{oleksiienko2023lens,
    author = {{Oleksiienko}, Illia and {Iosifidis}, Alexandros},
    title = "{Layer Ensembles}",
    journal = {arXiv:2210.04882},
    year = {2023},
}
```

## Notes

This repository is based on the [Variational Neural Networks](https://doi.org/10.1016/j.simpa.2022.100431) PyTorch [implementation](https://github.com/iliiliiliili/variational-nn-pytorch) for the corresponding [paper](https://arxiv.org/abs/2207.01524).
Additionally, it contains implementations of Monte Carlo Dropout, Bayes By Backpropagation, Hypermodels and Deep Ensembles methods.