import numpy as np

def calc_fccnogc(ric_op_mon = 0, cost_op_mon = 0, imp = 0, ammort = 0, mol = 0, rol = 0):
    if ric_op_mon != 0 and cost_op_mon !=0:
        return ric_op_mon - cost_op_mon - imp
    elif mol != 0:
        return mol - imp
    elif rol != 0 and ammort != 0:
        return rol - imp + ammort
    else:
        raise ValueError("Insufficient Data")

def calc_rol(ric_op_mon = 0, cost_op_mon = 0, ammort = 0, mol = 0):
    if ric_op_mon != 0 and cost_op_mon !=0:
        return ric_op_mon - cost_op_mon - ammort
    elif mol != 0:
        return mol - ammort
    else:
        raise ValueError("Insufficient Data")

def calc_fcgc(fccnogc, ccno):
    return fccnogc - ccno

def calc_fcid(inv, dis):
    return - inv + dis

def calc_fcfr(rimb_cap, pat_net, deb_f):
    return + pat_net + deb_f - rimb_cap

def calc_fcrf(of, div):
    return - of - div

def calc_var_liq(fcgc, fcid, fcfr, fcrf):
    return fcgc + fcif + fcfr + fcrf

def calc_fcu(fcgc, fcid):
    return fcgc + fcid

def calc_fce(fcu, fcfr, fcrf, rimb_cap, div):
    return fcu + fcfr - rim_cap +fcrf - div

def calc_npv(fc, k, i_0, t, cost):
    pv = 0
    
    for i in range(len(fc)):
        fc_net = fc[i] - cost  
        pv += fc_net / ((1 + k) ** t[i])
    
    result = pv - i_0
    return result


