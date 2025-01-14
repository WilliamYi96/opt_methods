import numpy as np

from optmethods.optimizer import Optimizer


class Bfgs(Optimizer):
    """
    Broyden–Fletcher–Goldfarb–Shanno algorithm. See
        https://arxiv.org/pdf/2004.14866.pdf
    for a convergence proof and see
        https://en.wikipedia.org/wiki/BFGS
    for a general description.
    
    Arguments:
        L (float, optional): an upper bound on the smoothness constant
            to initialize the Hessian estimate
        hess_estim (float array of shape (dim, dim), optional): initial Hessian estimate
        lr (float, optional): stepsize (default: 1)
    """
    
    def __init__(self, L=None, hess_estim=None, lr=1, store_hess_estimate=False, *args, **kwargs):
        super(Bfgs, self).__init__(*args, **kwargs)
        if L is None and hess_estim is None:
            L = self.loss.smoothness
            if L is None:
                raise ValueError("Either smoothness constant L or Hessian estimate must be provided")
        self.L = L
        self.B = hess_estim
        self.lr = lr
        self.store_hess_estimate = store_hess_estimate
        
    def step(self):
        self.grad = self.loss.gradient(self.x)
        x_new = self.x - self.lr * self.B_inv @ self.grad
        if self.line_search is not None:
            x_new = self.line_search(self.x, x_new)
        
        s = x_new - self.x
        grad_new = self.loss.gradient(x_new)
        y = grad_new - self.grad
        self.grad = grad_new
        
        y_s = y @ s
        if self.store_hess_estimate:
            Bs = self.B @ s
            sBs = s @ Bs
            self.B += np.outer(y, y)/y_s - np.outer(Bs, Bs)/sBs
        if y_s > 0:
            B_inv_y = self.B_inv @ y
            y_B_inv_y = y @ B_inv_y
            self.B_inv += (y_s + y_B_inv_y) * np.outer(s, s) / y_s**2
            self.B_inv -= (np.outer(B_inv_y, s) + np.outer(s, B_inv_y)) / y_s
        self.x = x_new
    
    def init_run(self, *args, **kwargs):
        super(Bfgs, self).init_run(*args, **kwargs)
        if self.B is None:
            if self.store_hess_estimate:
                self.B = self.L * np.eye(self.loss.dim)
            self.B_inv = 1 / self.L * np.eye(self.loss.dim)
        else:
            self.B_inv = np.linalg.pinv(self.B)
        self.grad = self.loss.gradient(self.x)
