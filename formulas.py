import numpy as np # non sembra necessario per ora
#Tutto il file è impostato con filosofia fail-fast che verifica la corretta e precisa implementazione dei dati, qualora siano necessari.
#Se il programma crasha con un TypeError, vuol dire che l'input o l'importazione del dato non sono andati a buon fine.

#Cash Flow and Ratio Analysis
def calc_fccnogc(fccnogc, ric_op_mon = None, cost_op_mon = None, imp = None, ammort = None, mol = None, rol = None):
    if fccnogc is not None:
        return fccnogc
    elif ric_op_mon is not None and cost_op_mon is not None and imp is not None:
        return ric_op_mon - cost_op_mon - imp
    elif mol is not None and imp is not None:
        return mol - imp
    elif rol is not None and ammort is not None and imp is not None:
        return rol - imp + ammort
    else:
        raise ValueError("Insufficient Data")


def calc_rol(rol, ric_op_mon = None, cost_op_mon = None, ammort = None, mol = None):
    if rol is not None:
        return rol
    elif ric_op_mon is not None and cost_op_mon is not None and ammort is not None:
        return ric_op_mon - cost_op_mon - ammort
    elif mol is not None and ammort is not None:
        return mol - ammort
    else:
        raise ValueError("Insufficient Data")

def calc_ros(ros, rol = None, ric_op_mon = None):
    if ros is not None:
        return ros
    elif ric_op_mon == 0:
        raise ValueError("Revenue is zero, division not possible")
    elif rol is not None and ric_op_mon is not None:
        return rol / ric_op_mon
    else:
        raise ValueError("Insufficient Data")

def calc_roi(roi, rol = None, deb_f = None, liq = None, pat_net = None):
    if roi is not None:
        return roi
    elif rol is not None and deb_f is not None and liq is not None and pat_net is not None:
        pos_fin_net = deb_f - liq
        cin = pat_net + pos_fin_net
        if cin == 0:
            raise ValueError("CIN is zero, division not possible")
        return rol / cin
    else:
        raise ValueError("Insufficient Data")

def calc_roe(roe, rol = None, of = None, imp = None, pat_net = None):
    if roe is not None:
        return roe
    elif pat_net == 0:
        raise ValueError("Equity is zero, division not possible")
    elif rol is not None and of is not None and imp is not None and pat_net is not None:
        ut_net = rol - of - imp
        return ut_net / pat_net
    else:
        raise ValueError("Insufficient Data")

def calc_fcgc(fcgc, fccnogc = None, ccno = None):
    if fcgc is not None:
        return fcgc
    elif fccnogc is not None and ccno is not None:
        fcgc_a = fccnogc - ccno
        return fcgc_a
    else:
        raise ValueError("Insufficient Data")

#A bit complex FCID
def calc_fcid(fcid=None, inv=None, dis=None,
              vnc=None, val_sto=None, plus=None, minus=None,
              ammo_ti=None, n_ammo=None,
              acqui_1=None, acqui_2=None):

    if fcid is not None:
        return fcid

    inv_final = inv if inv is not None else ((acqui_1 or 0) + (acqui_2 or 0))


    if dis is None:
        temp_vnc = vnc
        if temp_vnc is None and val_sto is not None and ammo_ti is not None and n_ammo is not None:
            temp_vnc = val_sto - (ammo_ti * n_ammo)      
        if temp_vnc is not None:
            dis = temp_vnc + (plus or 0) - (minus or 0)

    if dis is not None:
        return dis - inv_final  
    elif inv is not None or acqui_1 is not None or acqui_2 is not None:
        return 0 - inv_final
    
    else:
        raise ValueError("Dati insufficienti: fornire almeno gli investimenti o i dati per il disinvestimento")

def calc_fcfr(fcfr, rimb_cap = None, pat_net = None, deb_f = None):
    if fcfr is not None:
        return fcfr
    elif pat_net is not None and deb_f is not None and rimb_cap is not None:
        return pat_net + deb_f - rimb_cap
    else:
        raise ValueError("Insufficient Data")

def calc_fcrf(fcrf, of = None, div = None):
    if fcrf is not None:
        return fcrf
    elif of is not None and div is not None:
        return - of - div
    else:
        raise ValueError("Insufficient Data")

def calc_var_liq(var_liq, fcgc = None, fcid = None, fcfr = None, fcrf = None):
    if var_liq is not None:
        return var_liq
    elif fcgc is not None and fcid is not None and fcfr is not None and fcrf is not None:
        return fcgc + fcid + fcfr + fcrf
    else:
        raise ValueError("Insufficient Data")

def calc_fcu(fcu, fcgc = None, fcid = None):
    if fcu is not None:
        return fcu
    elif fcgc is not None and fcid is not None:
        return fcgc + fcid
    else:
        raise ValueError("Insufficient Data")

def calc_fce(fce, fcu = None, fcfr = None, fcrf = None, rimb_cap = None, div = None):
    if fce is not None:
        return fce
    elif fcu is not None and fcfr is not none and rimb_cap is not None and fcrf is not None and div is not None
        return fcu + fcfr - rimb_cap + fcrf - div
    else:
        raise ValueError("Insufficient Data")
        
#NPV with variable fcs and fixed cost per period
def calc_npv(npv, fc, k, i_0, t, cost):
    if npv is not None:
        return npv
    if len(fc) != len(t):
        raise ValueError("The numbers of cash flows and periods should be equal")
    if k == -1:
        raise ValueError("Division by zero is not accepted")
    pv = 0
    for i in range(len(fc)):
        fc_net = fc[i] - cost
        pv += fc_net / ((1 + k) ** t[i])
    
    result = pv - i_0
    return result
    
#BONDS
def calc_va_bond_zero(va, k, vn, dur):
    if va is not None:
        return va
    
    if k is None or vn is None or dur is None:
        raise ValueError("Insufficient Data")

    return vn / ((1 + k) ** dur)
    
def yield_to_mat_zero(k, va, vn, dur):
    if k is not None:
        return k
    if va !=0 and vn != 0 and dur != 0:
        return (vn / va) ** (1/dur) - 1
    else:
        raise ValueError("Insufficient Data")

def calc_va_ced_bond(va_ced, vn_ced, k_ced, t_ced, k_merk):
    if va_ced is not None:
        return va_ced
    elif vn_ced is not None and k_ced !=0:
        ced = vn_ced * k_ced
        va_ced = 0.0
        n = int(t_ced)          
        f = t_ced - n           
        for i in range(n):
            va_ced += ced / ((1 + k_merk) ** (i + 1))
        if f > 0:
            if k_merk != -1: 
                va_ced += ced * f / ((1 + k_merk) ** t_ced)
            else:
                raise ValueError("market rate must be 0 or higher")
        va_ced += vn_ced / ((1 + k_merk) ** t_ced)
        return va_ced
    else:
        raise ValueError("Insufficient Data")



