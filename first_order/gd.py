from optimizer import Optimizer


class Gd(Optimizer):
    """
    Gradient descent with constant learning rate.
    
    Arguments:
        lr (float, optional): an estimate of the inverse smoothness constant
    """
    def __init__(self, lr=None, *args, **kwargs):
        super(Gd, self).__init__(*args, **kwargs)
        self.lr = lr
        
    def step(self):
        self.grad = self.loss.gradient(self.x)
        if self.line_search is None:
            self.x -= self.lr * self.grad
        else:
            self.x = self.line_search(x=self.x, direction=-self.grad)
    
    def init_run(self, *args, **kwargs):
        super(Gd, self).init_run(*args, **kwargs)
        if self.lr is None:
            self.lr = 1 / self.loss.smoothness()
