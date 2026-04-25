import numpy as np

def calc_fccnogc(fccnogc, ric_op_mon = 0, cost_op_mon = 0, imp = 0, ammort = 0, mol = 0, rol = 0):
    if fccnogc is not None:
        return fccnogc
    elif ric_op_mon != 0 and cost_op_mon !=0:
        return ric_op_mon - cost_op_mon - imp
    elif mol != 0:
        return mol - imp
    elif rol != 0 and ammort != 0:
        return rol - imp + ammort
    else:
        raise ValueError("Insufficient Data")

def calc_rol(rol, ric_op_mon = 0, cost_op_mon = 0, ammort = 0, mol = 0):
    if rol is not None:
        return rol
    elif ric_op_mon != 0 and cost_op_mon !=0:
        return ric_op_mon - cost_op_mon - ammort
    elif mol != 0:
        return mol - ammort
    else:
        raise ValueError("Insufficient Data")

def calc_fcgc(fcgc, fccnogc, ccno):
    if fcgc is not None:
        return fcgc
    else:
        return fccnogc - ccno

def calc_fcid(fcid, inv, dis):
    if fcid is not None:
        return fcid
    else:
        return - inv + dis

def calc_fcfr(fcfr, rimb_cap, pat_net, deb_f):
    if fcfr is not None:
        return fcfr
    else:
        return + pat_net + deb_f - rimb_cap

def calc_fcrf(fcrf, of, div):
    if fcrf is not None:
        return fcrf
    else:
        return - of - div

def calc_var_liq(var_liq, fcgc, fcid, fcfr, fcrf):
    if var_liq is not None:
        return var_liq
    else:
        return fcgc + fcid + fcfr + fcrf

def calc_fcu(fcu, fcgc, fcid):
    if fcu is not None:
        return fcu
    else:
        return fcgc + fcid

def calc_fce(fce, fcu, fcfr, fcrf, rimb_cap, div):
    if fce is not None:
        return fce
    else:
        return fcu + fcfr - rimb_cap +fcrf - div

#fixed cost per period
def calc_npv(npv, fc, k, i_0, t, cost):
    if npv is not None:
        return npv
    else:
        pv = 0

        for i in range(len(fc)):
            fc_net = fc[i] - cost
            pv += fc_net / ((1 + k) ** t[i])

        result = pv - i_0
        return result
