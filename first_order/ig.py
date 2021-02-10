import numpy as np

from optimizer import Optimizer


class Ig(Optimizer):
    """
    Incremental gradient descent (IG) with decreasing or constant learning rate.
    
    For a formal description and convergence guarantees, see Section 10 in
        https://arxiv.org/abs/2006.05988
    
    The method is sensitive to finishing the final epoch, so it will terminate earlier 
    than it_max if it_max is not divisible by the number of steps per epoch.
    
    Arguments:
        prox_every_it (bool, optional): whether to use proximal operation every iteration 
            or only at the end of an epoch. Theory supports the latter. Only used if the loss includes
            a proximal regularizer (default: False)
        lr0 (float, optional): an estimate of the inverse smoothness constant, this step-size
            is used for the first epoch_start_decay epochs. If not given, it will be set
            with the value in the loss.
        lr_max (float, optional): a maximal step-size never to be exceeded (default: np.inf)
        lr_decay_coef (float, optional): the coefficient in front of the number of finished epochs
            in the denominator of step-size. For strongly convex problems, a good value
            is mu/3, where mu is the strong convexity constant
        lr_decay_power (float, optional): the power to exponentiate the number of finished epochs
            in the denominator of step-size. For strongly convex problems, a good value is 1 (default: 1)
        epoch_start_decay (int, optional): how many epochs the step-size is kept constant
            By default, will be set to have about 2.5% of iterations with the step-size equal to lr0
        batch_size (int, optional): the number of samples from the function to be used at each iteration
    """
    def __init__(self, prox_every_it=False, lr0=None, lr_max=np.inf, lr_decay_coef=0, lr_decay_power=1, 
                 epoch_start_decay=None, batch_size=1, *args, **kwargs):
        super(Ig, self).__init__(*args, **kwargs)
        self.prox_every_it = prox_every_it
        self.lr0 = lr0
        self.lr_max = lr_max
        self.lr_decay_coef = lr_decay_coef
        self.lr_decay_power = lr_decay_power
        self.epoch_start_decay = epoch_start_decay
        if epoch_start_decay is None and np.isfinite(self.epoch_max):
            self.epoch_start_decay = 1 + self.epoch_max // 40
        self.batch_size = batch_size
        
    def step(self):
        idx = np.arange(self.i, self.i + self.batch_size)
        idx %= self.loss.n
        self.i += self.batch_size
        self.i %= self.loss.n
        self.grad = self.loss.stochastic_gradient(self.x, idx=idx)
        denom_const = 1 / self.lr0
        lr_decayed = 1 / (denom_const + self.lr_decay_coef*max(0, self.finished_epochs-self.epoch_start_decay)**self.lr_decay_power)
        if lr_decayed < 0:
            lr_decayed = np.inf
        self.lr = min(lr_decayed, self.lr_max)
        self.x -= self.lr * self.grad
        end_of_epoch = self.it%self.steps_per_permutation == self.steps_per_permutation-1
        if self.prox_every_it and self.use_prox:
            self.x = self.loss.regularizer.prox(self.x, self.lr)
        elif end_of_epoch and self.use_prox:
            pass
    
    def init_run(self, *args, **kwargs):
        super(Ig, self).init_run(*args, **kwargs)
        if self.lr0 is None:
            self.lr0 = 1 / self.loss.batch_smoothness(batch_size)
        self.i = 0
