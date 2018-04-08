import copy

EPS = 1e-10


def identity(n):
    M = matrix(n, n, 0)
    for i in range(n):
        M[i, i] = 1
    return M


def augment(A, B):
    AB = matrix(A.rows_, A.cols_+B.cols_)
    for i in range(AB.rows_):
        for j in range(AB.cols_):
            if j < A.cols_:
                AB[i, j] = A[i, j]
            else:
                AB[i, j] = B[i, j - B.cols_]
    return AB


class matrix:

    def __init__(self, arg_1, arg_2=0, arg_3=0.0):
        if isinstance(arg_1, list):
            self.rows_ = len(arg_1)
            self.cols_ = len(arg_1[0])
            self.__matrix = arg_1
            self.shape = (self.rows_, self.cols_)
        else:
            if isinstance(arg_1, int) and isinstance(arg_2, int):
                self.rows_ = arg_1
                self.cols_ = arg_2
                self.__matrix = [[arg_3] * arg_2 for i in range(arg_1)]
                self.shape = (arg_1, arg_2)
            else:
                raise TypeError("parameters wrong")

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.__matrix[index]
        elif isinstance(index, tuple):
            return self.__matrix[index[0]][index[1]]

    def __setitem__(self, index, value):
        if isinstance(index, int):
            self.__matrix[index] = copy.deepcopy(value)
        elif isinstance(index, tuple):
            self.__matrix[index[0]][index[1]] = value

    def __mul__(self, N):
        if isinstance(N, int) or isinstance(N, float):
            M = matrix(self.rows_, self.cols_)
            for i in range(self.rows_):
                for j in range(self.cols_):
                    M[i, j] = self[i, j] * N
        else:
            assert N.rows_ == self.cols_, "dimension not match"
            M = matrix(self.rows_, N.cols_)
            for i in range(self.rows_):
                for j in range(N.cols_):
                    tmp_sum = 0
                    for k in range(self.cols_):
                        tmp_sum += self[i, k] * N[k, j]
                    M[i, j] = tmp_sum
        return M

    def inner_list(self):
        return self.__matrix

    def row_append(self, N):
        assert N.cols_ == self.cols_, "dimension not match"
        self.rows_ += 1
        self.shape = (self.rows_, self.cols_)
        for i in range(N.rows_):
            tmp_list = []
            for j in range(N.cols_):
                tmp_list.append(N[i, j])
            self.__matrix.append(tmp_list)

    def col_append(self, N):
        assert self.rows_ == self.rows_, "dimension not match"
        self.cols_ += 1
        self.shape = (self.rows_, self.cols_)
        for i in range(N.rows_):
            self.__matrix[i].append(N[i, 0])

    def col_deque(self):
        self.cols_ -= 1
        self.shape = (self.rows_, self.cols_)
        self.__matrix = [self.__matrix[0][1:]]

    def show(self):
        for i in range(self.rows_):
            for j in range(self.cols_):
                print(self[i, j], end='  ')
            print()

    def transpose(self):
        M = matrix(self.cols_, self.rows_)
        for i in range(self.cols_):
            for j in range(self.rows_):
                M[i, j] = self[j, i]
        return M

    def swap_rows(self, r1, r2):
        temp = copy.deepcopy(self.__matrix[r1])
        self.__matrix[r1] = self.__matrix[r2]
        self.__matrix[r2] = temp

    def gaussian_row_reduce(self):
        M = matrix(self.__matrix)
        rows = M.rows_
        cols = M.cols_
        i = rows - 1
        j = cols - 2

        while i >= 0:
            k = j - 1
            while k >= 0:
                if M[i, k] != 0:
                    j = k
                k -= 1

            if M[i, j] != 0:
                for t in range(i - 1, -1, -1):
                    for s in range(0, cols):
                        if s != j:
                            M[t, s] = M[t, s] - M[i, s] * (M[t, j] / M[i, j])
                            if EPS > M[t, s] > -EPS:
                                M[t, s] = 0

                    M[t, j] = 0

                for k in range(j+1, cols):
                    M[i, k] = M[i, k] / M[i, j]
                    if -EPS < M[i, k] < EPS:
                        M[i, k] = 0

                M[i, j] = 1

            i -= 1
            j -= 1

        return M

    def gaussian_eliminate(self):
        AB = matrix(self.__matrix)
        rows = AB.rows_
        cols = AB.cols_
        Acols = cols - 1

        i = 0
        j = 0

        while i < rows:
            pivot_found = False
            while j < Acols and not pivot_found:
                if AB[i, j] != 0:
                    pivot_found = True
                else:
                    max_row = i
                    max_val = 0
                    for k in range(i+1, rows):
                        cur_abs = abs(AB[k, j])
                        if cur_abs > max_val:
                            max_row = k
                            max_val = cur_abs
                    if max_row != i:
                        AB.swap_rows(max_row, i)
                        pivot_found = True
                    else:
                        j += 1

            if pivot_found:
                for t in range(i+1, rows):
                    for s in range(j+1, cols):
                        AB[t, s] = AB[t, s] - AB[i, s] * (AB[t, j] / AB[i, j])
                        if -EPS < AB[t, s] < EPS:
                            AB[t, s] = 0
                    AB[t, j] = 0

            i += 1
            j += 1

        return AB

    def inverse(self):
        I = identity(self.rows_)
        AI = augment(self, I)
        U = AI.gaussian_eliminate()
        IAInverse = U.gaussian_row_reduce()
        AInverse = matrix(self.rows_, self.cols_)

        for i in range(AInverse.rows_):
            for j in range(AInverse.cols_):
                AInverse[i, j] = IAInverse[i, j+self.cols_]

        return AInverse