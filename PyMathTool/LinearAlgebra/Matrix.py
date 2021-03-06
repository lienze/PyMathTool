__author__ = 'lienze'
# encoding=utf-8

'''
矩阵类
'''
class Mat:
    def __init__(self, *args):
        # 首先构造矩阵基础属性
        self.m = 0
        self.n = 0
        self.mat = []

        # 构造函数在这里分类
        if len(args) == 1:
            self.init3(args[0])
        elif len(args) == 2:
            # 构造函数有两个参数的时候，需要分析类型
            '''if isinstance(args[0], int) and isinstance(args[1], int):
                self.init2(args[0], args[1])
            elif isinstance(args[0], int) and isinstance(args[1], bool):
                self.init3(args[0], args[1])
            else:
                self.init0(args)'''
            if type(args[0]) is int and type(args[1]) is int:
                self.init2(args[0], args[1])
            elif type(args[0]) is int and type(args[1]) is bool:
                self.init3(args[0], args[1])
            else:
                self.init0(args)
        else:
            self.init0(args)

    def init0(self, args):
        # 首先检查类型
        count = 0
        max_list_len = 0
        for x in xrange(0, len(args)):
            # print args[x]
            if isinstance(args[x], list):
                count += 1
                if max_list_len < len(args[x]):
                    max_list_len = len(args[x])
            else:
                break

        if count == len(args):
            # 全部为list类型
            for i in args:
                # list基本单元先对齐
                if len(i) < max_list_len:
                    '''c = max_list_len - len(i)
                    while c > 0:
                        i.append(0)
                        c -= 1'''
                    # 这么改完, Pythonic 了许多
                    i.extend([0 for _ in xrange(1, max_list_len - len(i) + 1)])
                # 之后再添加
                self.mat.append(i)

            # 对象属性（行、列）初始化
            self.m = len(self.mat)
            self.n = len(self.mat[0])
        else:
            print u'初始化错误，list数量', count, u'参数数量', len(args)

    # 初始化为m*n矩阵
    def init2(self, m, n):
        self.m = m
        self.n = n
        self.mat = []
        for j in xrange(1, m + 1):
            xl = []
            for i in xrange(1, n + 1):
                xl.append(0)
            self.mat.append(xl)

    # 初始化为n阶单位矩阵或矩阵
    def init3(self, n, b_zero=False):
        self.mat = []
        for j in xrange(1, n + 1):
            xl = []
            for i in xrange(1, n + 1):
                if i == j and not b_zero:
                    xl.append(1)
                else:
                    xl.append(0)
            self.mat.append(xl)
        self.m = n
        self.n = n

    # 显示矩阵
    def show_mat(self):
        print ''
        for m in self.mat:
            print '(',
            for c in m:
                print c,
            print ')'

    '''
    功能：两个矩阵相加
    参数：matrix_a:矩阵A matrix_b:矩阵B
    返回值：相加后的矩阵(list)
    '''
    def __add__(self, other):
        return self.add_or_sub(self, other, 1)

    '''
    功能：两个矩阵相减
    参数：matrix_a:矩阵A matrix_b:矩阵B
    返回值：相加后的矩阵(list)
    '''
    def __sub__(self, other):
        return self.add_or_sub(self, other, 2)

    def add_or_sub(self, self_t, other_t, sign):
        matrix_a = self_t.mat
        matrix_b = other_t.mat
        # 确保两个矩阵的行数相同
        if len(matrix_a) != len(matrix_b):
            return -1

        # 接下来确保矩阵的列数相同
        na = []
        for la in matrix_a:
            if len(la) not in na:
                na.append(len(la))
        # print na

        nb = []
        for lb in matrix_b:
            if len(lb) not in nb:
                nb.append(len(lb))
        # print nb

        if len(na) != len(nb):
            if len(na) != 1 and len(nb) != 1:
                return -2

        # 之后进行两矩阵相加或相减
        if sign == 1:
            self.mat = [[x0 + y0 for x0, y0 in zip(x, y)] for x, y in zip(matrix_a, matrix_b)]
        elif sign == 2:
            self.mat = [[x0 - y0 for x0, y0 in zip(x, y)] for x, y in zip(matrix_a, matrix_b)]
        else:
            return -3
        return self

    '''
    功能：获取矩阵行数与列数
    参数：无
    返回值：[m, n] list类型
    '''
    def get_mn(self):
        m = len(self.mat)
        n = len(self.mat[0])
        return [m, n]

    '''
    功能：设置矩阵ij位置的值
    参数：i：矩阵中的行，j：矩阵中的列，x:值
    返回值：成功True或失败False
    '''
    def set_ij(self, i, j, x):
        self.mat[i-1][j-1] = x
        return True

    '''
    功能：获取矩阵ij位置的值
    参数：i：矩阵中的行，j：矩阵中的列
    返回值：返回ij位置的值
    '''
    def get_ij(self, i, j):
        return self.mat[i-1][j-1]

    '''
    功能：矩阵转置
    参数：无
    返回值：转置后的矩阵
    '''
    def convert_t(self):
        f_matrix = Mat(len(self.mat[0]), len(self.mat))
        for j in xrange(1, len(self.mat)+1):
            for i in xrange(1, len(self.mat[0])+1):
                f_matrix.set_ij(i, j, self.get_ij(j, i))
        return f_matrix

    '''
    功能：两个矩阵相乘 或 矩阵与整数相乘
    参数：other：另一个同阶矩阵
    返回值：相乘后的矩阵
    '''
    def __mul__(self, other):
        # 首先应该进行安全检查，此处先省略
        boo_k = False
        k = 0
        ca = 0
        if isinstance(self, int):
            # 矩阵与系数相乘的情况
            k = self
            ca = 1  # 系数的位置
            boo_k = True
        elif isinstance(other, int):
            # 矩阵与系数相乘的情况
            k = other
            ca = 2  # 系数的位置
            boo_k = True
        elif isinstance(self, Mat) and isinstance(other, Mat):
            # 矩阵与矩阵相乘的情况
            f_matrix = Mat(len(self.mat[0]), len(self.mat))
            for j in xrange(1, len(self.mat)+1):
                for i in xrange(1, len(self.mat[0])+1):
                    f_matrix.set_ij(i, j, self.get_ij(j, i) * other.get_ij(i, j))
            return f_matrix

        if boo_k:
            # 这里进行系数与矩阵相乘
            if ca == 1:
                mat_t = other
            elif ca == 2:
                mat_t = self
            else:
                return -2

            f_matrix = Mat(len(mat_t.mat[0]), len(mat_t.mat))

            for j in xrange(1, len(mat_t.mat)+1):
                for i in xrange(1, len(mat_t.mat[0])+1):
                    f_matrix.set_ij(i, j, mat_t.get_ij(i, j) * k)
            return f_matrix
        else:
            # 无类型匹配，返回-3
            return -3

    '''
    功能：矩阵第i行乘以k
    参数：i:第i行，k：系数
    返回值：处理之后的矩阵
    PS：第ir(row)行mul(乘)k
    '''
    def ir_mul_k(self, i, k):
        if i and i < len(self.mat):
            for x in xrange(0, len(self.mat[0])):
                self.mat[i-1][x] *= k
        return self

    '''
    功能：矩阵第j列乘以k
    参数：j：第j列，k：系数
    返回值：处理之后的矩阵
    PS：第jc(col)列mul(乘)k
    '''
    def jc_mul_k(self, j, k):
        if j and j < len(self.mat[0]):
            for x in xrange(0, len(self.mat)):
                self.mat[x][j-1] *= k
        return self

    '''
    功能：计算矩阵的秩
    参数：无
    返回值：秩
    '''
    def get_rank(self):
        # print self.m, self.n

        return self
