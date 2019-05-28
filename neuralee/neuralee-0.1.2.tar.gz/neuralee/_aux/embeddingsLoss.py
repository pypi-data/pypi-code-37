import torch
from .gradient import gradient_ee


class ELoss(torch.autograd.Function):

    @staticmethod
    def forward(ctx, X, Lp, Wn, lam):
        ctx.X, ctx.Lp, ctx.Wn, ctx.lam = X, Lp, Wn, lam
        return torch.tensor(0)

    def backward(ctx, grad_output):
        X, Lp, Wn, lam = ctx.X, ctx.Lp, ctx.Wn, ctx.lam
        return gradient_ee(X, Lp, Wn, lam), None, None, None


def eloss(X, Lp, Wn, lam):
    return ELoss.apply(X, Lp, Wn, lam)
