# -*- coding: utf-8 -*-

# ********************************** #
# Author: kaanguney.keklikci@tum.de  #
# Date: 16.06.2023                   #
# ********************************** #

from .proximal_operator import ProximalOperator


class L2(ProximalOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def proximal(self, x, sigma, gradient, reg):
        return (x - sigma * gradient) / (1 + sigma * reg)
