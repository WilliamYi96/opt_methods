# Optimization methods
This is a package containing implementations of different loss functions and optimization algorithms. The main goal of this package is to have a unified and easy-to-use comparison of iteration complexities of the algorithms, so the time comparison of methods is approximate. If you are interested in finding the best implementation of a solver for your problem, you may find the [BenchOpt package](https://benchopt.github.io/index.html) more useful.
## Structure
Currently, the methods are structured as follows: first-order, quasi-Newton, second-order, and stochastic first-order methods. A number of universal line search procedures is implemented.
### First-order
Gradient-based algorithms:  
[Gradient Descent (GD)](https://github.com/konstmish/opt_methods/blob/master/optmethods/first_order/gd.py), [Polyak's Heavy-ball](https://github.com/konstmish/opt_methods/blob/master/optmethods/first_order/heavy_ball.py), (https://github.com/konstmish/opt_methods/blob/master/optmethods/first_order/polyak.py), [Incremental Gradient (IG)](https://github.com/konstmish/opt_methods/blob/master/optmethods/first_order/ig.py), [Nesterov's Acceleration](https://github.com/konstmish/opt_methods/blob/master/optmethods/first_order/nesterov.py), [Nesterov's Acceleration with a special line search](https://github.com/konstmish/opt_methods/blob/master/optmethods/first_order/nest_line.py), [Nesterov's Acceleration with restarts (RestNest)](https://github.com/konstmish/opt_methods/blob/master/optmethods/first_order/rest_nest.py), [Optimized Gradient Method (OGM)](https://github.com/konstmish/opt_methods/blob/master/optmethods/first_order/ogm.py).  
Adaptive: [AdaGrad](https://github.com/konstmish/opt_methods/blob/master/optmethods/first_order/adagrad.py), [Adaptive GD (AdGD)](https://github.com/konstmish/opt_methods/blob/master/optmethods/first_order/adgd.py), [Accelerated AdGD (AdgdAccel)](https://github.com/konstmish/opt_methods/blob/master/optmethods/first_order/adgd_accel.py), [Polyak](https://github.com/konstmish/opt_methods/blob/master/optmethods/first_order/polyak.py).
### Quasi-Newton
[BFGS](https://github.com/konstmish/opt_methods/blob/master/optmethods/quasi_newton/bfgs.py), [DFP](https://github.com/konstmish/opt_methods/blob/master/optmethods/quasi_newton/dfp.py), [L-BFGS](https://github.com/konstmish/opt_methods/blob/master/optmethods/quasi_newton/lbfgs.py), [Shor's R](https://github.com/konstmish/opt_methods/blob/master/optmethods/quasi_newton/shorr.py), [SR1](https://github.com/konstmish/opt_methods/blob/master/optmethods/quasi_newton/sr1.py).
### Second-order
Algorithms that use second-order information (second derivatives) or their approximations.  
[Newton](https://github.com/konstmish/opt_methods/blob/master/optmethods/second_order/newton.py), [Cubic Newton](https://github.com/konstmish/opt_methods/blob/master/optmethods/second_order/cubic.py), and [Regularized (Global) Newton](https://github.com/konstmish/opt_methods/blob/master/optmethods/second_order/reg_newton.py).
### Stochastic first-order
[SGD](https://github.com/konstmish/opt_methods/blob/master/optmethods/stochastic_first_order/sgd.py), [Root-SGD](https://github.com/konstmish/opt_methods/blob/master/optmethods/stochastic_first_order/root_sgd.py), [Stochastic Variance Reduced Gradient (SVRG)](https://github.com/konstmish/opt_methods/blob/master/optmethods/stochastic_first_order/svrg.py), [Random Reshuffling (RR)](https://github.com/konstmish/opt_methods/blob/master/optmethods/stochastic_first_order/shuffling.py).
### Notebooks
1. [Deterministic first-order methods](https://github.com/konstmish/opt_methods/blob/master/notebooks/1.%201st-order%20methods.ipynb): GD, acceleration, adaptive algorithms.  
2. [Second-order methods and quasi-Newton algorithms](https://github.com/konstmish/opt_methods/blob/master/notebooks/2.%202nd-order%20and%20quasi-Newton.ipynb): Newton, Levenberg-Marquardt, BFGS, SR1, DFP.  
3. [Example of running the methods on log-sum-exp problem](https://github.com/konstmish/opt_methods/blob/master/notebooks/3.%20Log-sum-exp.ipynb): a hard problem where quasi-Newton methods may either outperform all first-order method or fail due to high nonsmoothness of the problem. One can change the problem difficulty by adjusting the smoothing parameters of the objective.  
To be added: benchmarking wall-clock time of some numpy and scipy operations to show how losses should be implemented.
