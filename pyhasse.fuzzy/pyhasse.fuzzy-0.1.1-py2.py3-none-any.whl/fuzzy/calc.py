# -*- coding: utf-8 -*-
import logging


class Fuzzy(object):
    """<= relation will be transformed into a subsethood matrix, sh,

    by the Kosko-approach. The sh-matrix will be modified to get
    first a relational matrix and from this the zeta-matrix
    more about this class...

    :prop: | **r** number of rows of the data matrix (dm)
           | **k** number of columns of dm
           | **dm** data matrix with labels for the objects and the attributes
           | **sh** so-called Kosko subsethood matrix
           | **relat** relational matrix
           | **crisp_zeta ** crisp zeta matrix (after user input of alpha-cut
    """

    def __init__(self, r, k, dm, obj, prop, ndec):
        self.logger = logging.getLogger(__name__)
        self.r = r
        self.k = k
        self.dm = dm
        self.obj = obj
        self.prop = prop
        self.ndec = ndec
        self.logger.info('All values initialized')
        self.rred = None

    def calc_matrixnorm(self, matrix, r, k):
        """ Columnwise normalization to [0,1],

        applying (x-min)/(max-min).
        :prop:
        |**matrix**: usually a data matrix
        |**r** number of rows of matrix
        |**k** number of columns of matrix
        |**dmn** normalized matrix
        """
        # initialization
        self.dmn = []
        for i in range(0, r):
            self.dmn.append(0)
            self.dmn[i] = []
            for j in range(0, k):
                self.dmn[i].append(0)
        # normalization
        for j in range(0, k):
            mini = 10 ** 20
            maxi = -10 ** 20
            for i in range(0, r):
                if matrix[i][j] < mini:
                    mini = matrix[i][j]
                if matrix[i][j] > maxi:
                    maxi = matrix[i][j]
            delta = 1.0 * (maxi - mini)
            for i in range(0, r):
                if delta != 0:
                    hilf = float((matrix[i][j] - mini)/delta)
                    self.dmn[i][j] = hilf
                else:
                    self.dmn[i][j] = 0.0     # 9.10.2014  Need a warning?
        return self.dmn

    def calc_koskomatrix(self, matrix, r, k):
        """fuzzy representation of less than by Kosko-method
        :prop:
        **matrix** data matrix (original or normalized)
        **r** number of rows of 'matrix'
        **k** number of coulmns of 'matrix'
        **sh** Kosko subsethood matrix
        1.step of the fuzzy-poset procedure
        see Van de Walle et al. 1995
        sh relational matrix Kosko (s ubset h ood)
        usually not transitivity closed"""
        self.sh = []
        for i1 in range(0, self.r):
            self.sh.append(0)
            self.sh[i1] = []
            sumh = 0
            sumnenner = 0
            for i2 in range(0, self.r):
                if i1 == i2:
                    self.sh[i1].append(1.0)
                else:
                    sumnenner = 0
                    sumh = 0
                    for j in range(0, self.k):
                        sumh += min(matrix[i1][j], matrix[i2][j])
                        sumnenner += matrix[i1][j]
                    if sumnenner > 0:
                        # change 8.2.09 see v.d.Walle,1995 p. 119
                        hilf = float(1.0 * sumh / (1.0 * sumnenner))
                        self.sh[i1].append(hilf)
                    else:
                        self.sh[i1].append(1.0)   # change 8.2.09
        return self.sh

    def comparematrices(self, a, b):
        """if the sum of all abs diff. of matrix entries < eps than

        the outcome of this routine is flag = 1 else 0"""
        # eps tolerance = 0.01
        # a, b two matrices will dynamically varied
        eps = 0.01  # Attention please!!!
        sumh = 0
        for i1 in range(0, self.r):
            for i2 in range(0, self.r):
                sumh += abs(a[i1][i2] - b[i1][i2])
        if sumh <= eps:
            self.flag = 1
        else:
            self.flag = 0
        return self.flag

    def fuzzymatmult(self, a, b):
        """2. step in fuzzy posets. Matrixmethod after de Baets.

        An approximation to obtain from sh the transitive hull,
        whereby the fuzzy transitivity axiom is to be fulfilled"""
        # preparatory step: c is a matrix
        c = []
        for i1 in range(0, self.r):
            c.append(0)
            c[i1] = []
            for i2 in range(0, self.r):
                c[i1].append(0)
        # formally like a matrix multiplication
        for i1 in range(0, self.r):
            for i2 in range(0, self.r):
                hilf = []
                for i3 in range(0, self.r):
                    hilf.append(min(a[i1][i3], b[i3][i2]))
                c[i1][i2] = round(max(hilf), self.ndec)
        return c

    def matcopy(self, a):
        """r*r-square matrix copied yielding b"""
        b = []
        for i1 in range(0, self.r):
            b.append(0)
            b[i1] = []
            for i2 in range(0, self.r):
                b[i1].append(a[i1][i2])
        return b

    def fuzzyproduct(self, subsethood):
        """2. step: see DeBaets,DeMeyer in Inf Sci 152, 2003, 167-179,

        sh will be multiplied with itself (fuzzymatmult) until
        the resulting matrices do no more differ than eps"""
        flag = 0
        zaehl = 0
        # an iteration starts
        # copy of sh
        self.q = []
        for i1 in range(0, self.r):
            self.q.append(0)
            self.q[i1] = []
        for i1 in range(0, self.r):
            for i2 in range(0, self.r):
                self.q[i1].append(subsethood[i1][i2])
        # Now the proper iteration
        while flag == 0:
            q1 = self.fuzzymatmult(self.q, self.q)
            flag = \
                self.comparematrices(q1, self.q)  # Hilbert sequence criterion
            self.q = self.matcopy(q1)
            zaehl += 1
            if zaehl > 20:  # to keep the PC quiet...
                break
            else:
                pass
            # the entries of self.q are the so-called alpha-values from...
            # ....which the user given acut may depend.
        return self.q

    def calc_crisp_matrix(self, matrix, acut):
        """3. step: depending on acut: from 'matrix' a crisp matrix
        acut is a user input. In order to simplify the decsision for an
        appropriate acut, the list of entries of self.q
        (after fuzzy-multiplication
        should be listed """
        self.crisp_matrix = []
        for i1 in range(0, self.r):
            self.crisp_matrix.append(0)
            self.crisp_matrix[i1] = []
            for i2 in range(0, self.r):
                if matrix[i1][i2] >= acut:
                    self.crisp_matrix[i1].append(1)
                else:
                    self.crisp_matrix[i1].append(0)
        return self.crisp_matrix

    def generate_reduced_matrix(self, matrix1, identifier_list):
        """ 4. step: row and coulumn corresponding to 'identifier_list'

        will be kept and a new -reduced- matrix is obtained.
        In general the identifier_list is objred
        (listobj of generate_representative_elements),
        the outcome of equivalence classes calculations """
        # matrix2 pre-formulated
        lil = len(identifier_list)
        self.matrix2 = []
        for i1 in range(0, lil):
            self.matrix2.append(0)
            self.matrix2[i1] = []
            for i2 in range(0, lil):
                self.matrix2[i1].append(0)
        # matrix2 entries filled with the remaining values
        z1 = 0
        for ob in identifier_list:
            iob = self.obj.index(ob)
            for i1 in range(0, self.r):
                if i1 == iob:
                    z2 = 0
                    for i2 in range(0, self.r):
                        if self.obj[i2] in identifier_list:
                            self.matrix2[z1][z2] = matrix1[i1][i2]
                            z2 += 1
                    z1 += 1
        return self.matrix2

    def generate_representative_elements(self, matrix):
        """ Needed to perform the 4th step.
        Matrix is the relational matrix with entries 0, 1 ,
        the list of representative elements (listob = objred) will be
        generated. Difference to inout: Here the equivalence is
        based on the relational matrix and  n o t  on the dm
        """
        gathering = []
        flagec = 0
        for i1 in range(0, self.r):
            for i2 in range(i1 + 1, self.r):
                sumtest = matrix[i1][i2] + matrix[i2][i1]
                if sumtest == 2:
                    flagec = 1
                    gathering.append(i2)
        self.listob = []
        for ob in self.obj:
            if self.obj.index(ob) not in gathering:
                self.listob.append(ob)
        return self.listob

    def generate_equivalenceclasses(self, matrix, r, k, ndec=None):
        """calculates from 'matrix' the list of equivalence classes
        adapted for the new PyHasse-core
        :prop:
        |**r**   number of rows (i.e. of objects)
        |**k** k: number of columns (i.e. of attributes)
        |**eqm** eqm: an irregular 2-dim field, i.e. lists
                    of different length within a list
        |**already_visited** list of visited object
                               indices in the i2-loop
        |** hilf**: list generated for any i1 not already visited
        """
        self.eqm = []
        if ndec:
            self.ndec = ndec
        for i in range(0, r):
            for j in range(0, k):
                matrix[i][j] = round(float(matrix[i][j]),
                                     self.ndec)
        # the proper block to calculate equivalence classes
        # idea: objects (their indices) already visited in the
        # second loop will no more visited by the first loop
        already_visited = []
        for i1 in range(0, r):
            if i1 not in already_visited:
                hilf = []
                hilf.append(i1)
                for i2 in range(i1+1, r):
                    if matrix[i1] == matrix[i2]:
                        hilf.append(i2)
                        already_visited.append(i2)
                self.eqm.append(hilf)
            self.rred = len(self.eqm)
        return self.eqm, self.rred

    def calc_countofK(self, eqm):
        """K measures the role of equivalence classes
        K is a maximum, when uniform distribution and a
        minimum (=0), when only singletons
        :prop:
        |**eqm** : list of equivalence classes as outcome of
                    the fuzzy-method 'generate_equivalence classes'.
        |**K**: sum N(i)*(N(i)-1) with N(i) being number of
                    elements in the ith equivalence class
                    called 'hilf' in the body of the method.
        """
        K = 0
        leq = len(eqm)
        for i1 in range(0, leq):
            hilf = len(eqm[i1])
            K += hilf * (hilf - 1)
        return K

    def calc_countofcomparab(self, matrix):
            """ computes the comparabilities
            based on square matrix (r rows, r columns).
            :prop:
            |** matrix**: zeta matrix (square matrix)
            |** r **: number of rows/columns
            """
            r = len(matrix)
            comparabilities = 0
            for i1 in range(0, r):
                for i2 in range(0, r):
                    if matrix[i1][i2] == 1 and i1 != i2:
                        comparabilities += 1
            return comparabilities

    def calc_countofincomp(self, matrix):
        """calculates the number of elements (x,y)
        x||y based on relational matrix 'matrix'.
        :prop:
        |**matrix** relational matrix (e.g. zeta matrix)
        |**u** number of elements (x,y) with x||y
        """
        r = len(matrix)
        u = 0
        for i1 in range(0, r):
            for i2 in range(0, r):
                if matrix[i1][i2] == 0 and matrix[i2][i1] == 0:
                    u += 0.5
        return int(u)



