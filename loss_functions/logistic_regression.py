import scipy
import numpy as np

import numpy.linalg as la
from sklearn.utils.extmath import row_norms, safe_sparse_dot

from .loss_oracle import Oracle
from .utils import safe_sparse_add, safe_sparse_multiply, safe_sparse_norm

MAX_SMOOTHNESS_DIM = 1000


def logsig(x):
    """
    Compute the log-sigmoid function component-wise.
    See http://fa.bianp.net/blog/2019/evaluate_logistic/ for more details.
    """
    out = np.zeros_like(x)
    idx0 = x < -33
    out[idx0] = x[idx0]
    idx1 = (x >= -33) & (x < -18)
    out[idx1] = x[idx1] - np.exp(x[idx1])
    idx2 = (x >= -18) & (x < 37)
    out[idx2] = -np.log1p(np.exp(-x[idx2]))
    idx3 = x >= 37
    out[idx3] = -np.exp(-x[idx3])
    return out


class LogisticRegression(Oracle):
    """
    Logistic regression oracle that returns loss values, gradients and Hessians.
    """
    def __init__(self, A, b, store_mat_vec_prod=True, *args, **kwargs):
        super(LogisticRegression, self).__init__(*args, **kwargs)
        self.A = A
        b = np.asarray(b)
        if (np.unique(b) == [1, 2]).all():
            # Transform labels {1, 2} to {0, 1}
            self.b = b - 1
        elif (np.unique(b) == [-1, 1]).all():
            # Transform labels {-1, 1} to {0, 1}
            self.b = (b+1) / 2
        else:
            assert (np.unique(b) == [0, 1]).all()
            self.b = b
        self.n, self.dim = A.shape
        self.store_mat_vec_prod = store_mat_vec_prod
        self.x_last = 0#np.zeros(self.dim)
        self.mat_vec_prod = 0#np.zeros(self.n)
    
    def value(self, x):
        z = self.mat_vec_product(x)
        regularization = self.l1*safe_sparse_norm(x, ord=1) + self.l2/2*safe_sparse_norm(x)**2
        return np.mean(safe_sparse_multiply(1-self.b, z)-logsig(z)) + regularization
    
    def gradient(self, x):
        z = self.mat_vec_product(x)
        activation = scipy.special.expit(z)
        grad = safe_sparse_add(self.A.T@(activation-self.b)/self.n, self.l2*x)
        if scipy.sparse.issparse(x):
            grad = scipy.sparse.csr_matrix(grad).T
        return grad
    
    def hessian(self, x):
        z = self.mat_vec_product(x)
        activation = scipy.special.expit(z)
        weights = activation * (1-activation)
        A_weighted = safe_sparse_multiply(self.A.T, weights)
        return A_weighted@self.A/self.n + self.l2*np.eye(self.dim)
    
    def stochastic_gradient(self, x, idx=None, batch_size=1, replace=False):
        if idx is None:
            idx = np.random.choice(self.n, size=batch_size, replace=replace)
        z = self.mat_vec_product(x)
        activation = scipy.special.expit(z)        
        stoch_grad = safe_sparse_add(self.A[idx].T@(activation-self.b[idx])/len(idx), self.l2*x)
        return stoch_grad
    
    def mat_vec_product(self, x):
        if not self.store_mat_vec_prod or safe_sparse_norm(x-self.x_last) != 0:
            z = self.A @ x
            if scipy.sparse.issparse(z):
                z = z.toarray().ravel()
            if self.store_mat_vec_prod:
                self.mat_vec_prod = z
                self.x_last = x.copy()
        
        return self.mat_vec_prod
    
    def norm(self, x):
        return safe_sparse_norm(x)
        
    def smoothness(self, use_eigen_if_large=False):
        if self.dim < MAX_SMOOTHNESS_DIM or use_eigen_if_large:
            covariance = self.A.T@self.A/self.n
            if scipy.sparse.issparse(covariance):
                covariance = covariance.toarray()
            return 0.25*np.max(la.eigvalsh(covariance)) + self.l2
        else:
            print(
            """The dimension is {}, which might be too large 
            for computing the largest eigenvalue of
            the covariance matrix, so an estimate is returned.
            Set use_eigen_if_large=True to compute anyway """.format(self.dim)
            )
            return self.average_smoothness()
    
    def max_smoothness(self):
        max_squared_sum = row_norms(self.A, squared=True).max()
        return 0.25*max_squared_sum + self.l2
    
    def average_smoothness(self):
        ave_squared_sum = row_norms(self.A, squared=True).mean()
        return 0.25*ave_squared_sum + self.l2
    
    def density(self, x):
        if hasattr(x, "toarray"):
            dty = float(x.nnz) / (x.shape[0]*x.shape[1])
        else:
            dty = 0 if x is None else float((x!=0).sum()) / x.size
        return dty
