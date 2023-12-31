# -*- coding: utf-8 -*-

# ********************************** #
# Author: kaanguney.keklikci@tum.de  #
# Date: 12.07.2023                   #
# ********************************** #

import numpy as np
import aomip
import tifffile
from abc import ABC


class Gradient(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lr = 1e-2

    def setlr(self, lr) -> None:
        self.lr = lr

    def update(self, x, gradient, **kwargs) -> np.ndarray:
        self.lr = kwargs.get("lr", self.lr)
        return x - self.lr * gradient


class GradientDescent(aomip.Optimization):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scheduler = Gradient()
        self.objective = aomip.leastSquares

    def optimize(self, n=100, **kwargs) -> tuple:
        x, loss = self.x0, 0.0
        history = []
        self.scheduler.lr = kwargs.get("lr", self.scheduler.lr)
        for i in range(n):
            if i % 10 == 0:
                print(f"Loss @ {i}-th iteration = {loss:.2f}")
            gradient = self.calculate_gradient(x)
            x = self.scheduler.update(x, gradient, lr=self.scheduler.lr)
            loss = self.objective(self.operator.apply(x), self.sino)
            history.append(loss)
        print(f"Completed, loss = {loss:.2f}")
        return x, history


class Subgradient(aomip.Optimization):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scheduler = Gradient()
        self.objective = aomip.leastSquares
        self.step = "constant"

    def optimize(self, n=100, beta=0.1, **kwargs) -> tuple:
        # backprojection as the initial guess
        A = self.operator
        backprojection = A.applyAdjoint(A.apply(self.target))
        x = backprojection.reshape(self.vol_shape, order="F")
        self.scheduler.lr = kwargs.get("lr", self.scheduler.lr)
        self.step = kwargs.get("step", self.step)
        grad = aomip.FirstDerivative()
        history, loss = [], 0.0
        for i in range(n):
            if i % 10 == 0:
                print(f"Loss @ {i}-th iteration = {loss:.2f}")
            prevx = x
            dx = grad.applyAdjoint(grad.apply(prevx))
            norm = np.linalg.norm(dx, ord=1)
            subgradient = np.sign(norm)
            # compute learning rate
            if self.step == "square_summable":
                self.scheduler.lr = 1 / (i + 1e3)
            elif self.step == "diminishing":
                self.scheduler.lr = 1 / np.sqrt(i + 1e6)
            elif self.step == "constant":
                self.scheduler.lr = self.scheduler.lr
            else:
                raise NotImplementedError
            x = self.scheduler.update(
                prevx, (dx + self.calculate_gradient(prevx)), lr=self.scheduler.lr
            )
            loss = self.objective(A.apply(x), self.sino) + norm
            history.append(loss)
        print(f"Completed, loss = {loss:.2f}")
        return x, history
