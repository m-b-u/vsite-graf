import numpy as np


def clear_framebuffer(A):
    assert(A.ndim == 2) 
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i][j] = 0
    
def clear_framebuffer_1D(A_):
    assert(A_.ndim == 1)
    for i in range(len(A)):
        A_[i] = 0
    # shorter: A[:] = 0


if __name__=='__main__':
    M = 20
    N = 10
    A = np.empty( (N, M), dtype=np.uint8 )

    clear_framebuffer(A)

    A[3][15] = 9
    
    print(A)

    A[3, 15] = 8

    print(A)

    A_ = A.ravel()

    assert (A_.base is A)

    A_[3*M + 15] = 7

    print(A)

    print('#' * 40)

    print(A_)

    print("A.strides: ", A.strides)
