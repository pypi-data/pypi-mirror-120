# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/


__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "20/09/2021"

import logging

import numpy

from darfix.decomposition.nica import NICA
from .base import Base

_logger = logging.getLogger(__file__)


class NICA_NMF(Base):
	"""
    Non-negative matrix factorization with non-negative ICA (NICA)
    initialization.

    Under the linear generative model x = A * s, where x is a p-dimensional
    observable random vector, s is the latent non-negative random vector of
    length num_components and A is a fixed (but unknown) non-negative matrix,
    this function tries to determine both s and A. The data matrix X is
    assumed to hold n samples of x, stacked in rows (shape(X) = (n, p)) or
    columns (shape(X) = (p, n)), which can be specified by the rowvar parameter.
    In practice, if shape(X) = (p, n) (resp. shape(X) = (n, p)) this function
    solves X = A * S (resp. X = S.T * A.T) both for S and A, where A is the
    so-called mixing matrix, with shape (p, num_components), and S is a
    (num_components, n) matrix which contains n samples of the latent source
    vector, stacked in columns.

    The non-uniqueness (non-convexity) property of NMF implies that the
    solution depends on the initial factor matrices.
    This function implements the idea presented in:
    `Efficient initialization for nonnegative matrix factorization based on
    nonnegative independent component analysis´
    (https://ieeexplore.ieee.org/document/7602947)
    which suggests that a good initialization is based on the factorization
    given by non-negative ICA.
	"""
	def __init__(self, data, num_components, chunksize=None, lr=0.03,
				 max_iter=5000, tol=1e-8):        

		nica = NICA(data, num_components, chunksize, lr, max_iter, tol)

        X = self.X
        # We assume rowvar is True throughout the algorithm
        if not rowvar:
            X = X.transpose()
            S = S.transpose()

        # Initial NMF factorization: X = F0 * G0
        F0 = numpy.abs(A)
        G0 = numpy.abs(S)

        W0 = G0.transpose().copy()  # Make array C-contiguous
        H0 = F0.transpose()

        nmf = NMF(n_components=min(num_components, S.shape[0]), init='custom')
        W = nmf.fit_transform(X.transpose(), W=W0, H=H0)
        H = nmf.components_

        A = H.transpose()
        S = W.copy()

        if rowvar:
            S = W.transpose()

        return S, A