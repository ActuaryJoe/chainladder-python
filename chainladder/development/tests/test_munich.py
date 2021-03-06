import numpy as np
from chainladder.utils.cupy import cp
import chainladder as cl
from rpy2.robjects.packages import importr
from rpy2.robjects import r

CL = importr('ChainLadder')


def test_mcl_paid():
    df = r('MunichChainLadder(MCLpaid, MCLincurred)').rx('MCLPaid')
    p = cl.MunichAdjustment(paid_to_incurred=('paid','incurred')).fit(cl.Development(sigma_interpolation='mack').fit_transform(cl.load_sample('mcl'))).munich_full_triangle_[0,0,0,:,:]
    xp = cp.get_array_module(p)
    arr = xp.array(df[0])
    xp.testing.assert_allclose(arr, p, atol=1e-5)


def test_mcl_incurred():
    df = r('MunichChainLadder(MCLpaid, MCLincurred)').rx('MCLIncurred')
    p = cl.MunichAdjustment(paid_to_incurred=[('paid','incurred')]).fit(cl.Development(sigma_interpolation='mack').fit_transform(cl.load_sample('mcl'))).munich_full_triangle_[1,0,0,:,:]
    xp = cp.get_array_module(p)
    arr = xp.array(df[0])
    xp.testing.assert_allclose(arr, p, atol=1e-5)

def test_mcl_ult():
    mcl = cl.load_sample('mcl')
    dev = cl.Development().fit_transform(mcl)
    cl_traditional = cl.Chainladder().fit(dev).ultimate_
    dev_munich = cl.MunichAdjustment(paid_to_incurred=[('paid','incurred')]).fit_transform(dev)
    cl_munich = cl.Chainladder().fit(dev_munich).ultimate_

def test_mcl_rollforward():
    mcl = cl.load_sample('mcl')
    mcl_prior = mcl[mcl.valuation<mcl.valuation_date]
    munich = cl.MunichAdjustment(paid_to_incurred=[('paid','incurred')]).fit(mcl_prior)
    new = munich.transform(mcl)
    cl.Chainladder().fit(new).ultimate_
