from Multi_path_DAG import (
    calc_mol,
    calc_rol_from_mol,
    calc_fccnogc_from_revenue,
    calc_fccnogc_from_mol,
    calc_fccnogc_from_rol,
    calc_ros_from_rol,
    calc_cin,
    calc_roi_from_rol,
    calc_net_profit,
    calc_roe,
    calc_var_ccno,
    calc_fcgc,
    calc_inv,
    calc_vnc,
    calc_dis_from_vnc,
    calc_fcid_from_inv_dis,
    calc_fcfr,
    calc_fcrf,
    calc_var_liquidity,
    calc_fcu,
    calc_fce,
    calc_fc_net,
    calc_df_constant,
    calc_df_variable,
    calc_pv,
    calc_total_pv,
    calc_npv,
    calc_bond_zero_discount_factor,
    calc_bond_zero_va,
    calc_bond_zero_mont,
    calc_bond_zero_factor,
    calc_bond_zero_yield_to_maturity,
)



def _as_list(x):
    if isinstance(x, (list, tuple)):
        return list(x)
    return [x]

def _present(x):
    return x is not None


def resolve_mol(mol=None, ric_op_mon=None, cost_op_mon=None):
    if _present(mol):
        return mol
    if _present(ric_op_mon) and _present(cost_op_mon):
        return calc_mol(ric_op_mon, cost_op_mon)
    raise ValueError("Insufficient data for MOL")


def resolve_rol(rol=None, mol=None, ric_op_mon=None, cost_op_mon=None, amortisat=None):
    if _present(rol):
        return rol

    if _present(mol) and _present(amortisat):
        return calc_rol_from_mol(mol, amortisat)

    if _present(ric_op_mon) and _present(cost_op_mon) and _present(amortisat):
        mol_value = calc_mol(ric_op_mon, cost_op_mon)
        return calc_rol_from_mol(mol_value, amortisat)

    raise ValueError("Insufficient data for ROL")


def resolve_ros(ros=None, rol=None, ric_op_mon=None):
    if _present(ros):
        return ros

    if _present(rol) and _present(ric_op_mon):
        if ric_op_mon == 0:
            raise ValueError("Division by zero in ROS")
        return calc_ros_from_rol(rol, ric_op_mon)

    raise ValueError("Insufficient data for ROS")


def resolve_net_profit(utile_netto=None, rol=None, oneri_finanz=None, tax=None):
    if _present(utile_netto):
        return utile_netto

    if _present(rol) and _present(oneri_finanz) and _present(tax):
        return calc_net_profit(rol, oneri_finanz, tax)

    raise ValueError("Insufficient data for Net Profit")


def resolve_roe(roe=None, utile_netto=None, rol=None, oneri_finanz=None, tax=None, patrimonio_netto=None):
    if _present(roe):
        return roe

    if _present(utile_netto) and _present(patrimonio_netto):
        if patrimonio_netto == 0:
            raise ValueError("Division by zero in ROE")
        return calc_roe(utile_netto, patrimonio_netto)

    if _present(rol) and _present(oneri_finanz) and _present(tax) and _present(patrimonio_netto):
        utile = calc_net_profit(rol, oneri_finanz, tax)
        return calc_roe(utile, patrimonio_netto)

    raise ValueError("Insufficient data for ROE")


# CASH FLOW OPERATIVO


def resolve_fcgc(fcgc=None, fccnogc=None, var_ccno=None):
    if _present(fcgc):
        return fcgc
    if _present(fccnogc) and _present(var_ccno):
        return calc_fcgc(fccnogc, var_ccno)
    raise ValueError("Insufficient data for FCGC")


def resolve_var_ccno(var_ccno=None, ccno1=None, ccno2=None):
    if _present(var_ccno):
        return var_ccno
    if _present(ccno1) and _present(ccno2):
        return calc_var_ccno(ccno1, ccno2)
    raise ValueError("Insufficient data for CCNO variation")

#INVESTIMENTI, VNC, DISINVESTIMENTI, FCID

def resolve_inv(inv=None, acquisition_1=None, acquisition_2=None):
    if _present(inv):
        return inv
    if _present(acquisition_1) and _present(acquisition_2):
        return calc_inv(acquisition_1, acquisition_2)
    raise ValueError("Insufficient data for investments")


def resolve_vnc(vnc=None, valore_stor=None, ammo_ti=None, n_ammo_ti=None):
    if _present(vnc):
        return vnc
    if _present(valore_stor) and _present(ammo_ti) and _present(n_ammo_ti):
        return calc_vnc(valore_stor, ammo_ti, n_ammo_ti)
    raise ValueError("Insufficient data for VNC")


def resolve_dis(dis=None, vnc=None, plus=None, minus=None):
    if _present(dis):
        return dis
    if _present(vnc) and _present(plus) and _present(minus):
        return calc_dis_from_vnc(vnc, plus, minus)
    raise ValueError("Insufficient data for disinvestments")


def resolve_fcid(
    fcid=None,
    inv=None,
    dis=None,
    vnc=None,
    valore_stor=None,
    plus=None,
    minus=None,
    ammo_ti=None,
    n_ammo_ti=None,
    acquisition_1=None,
    acquisition_2=None,
):

    if _present(fcid):
        return fcid

    inv_val = inv if _present(inv) else (
        calc_inv(acquisition_1, acquisition_2)
        if _present(acquisition_1) and _present(acquisition_2)
        else None
    )

    vnc_val = vnc if _present(vnc) else (
        calc_vnc(valore_stor, ammo_ti, n_ammo_ti)
        if _present(valore_stor) and _present(ammo_ti) and _present(n_ammo_ti)
        else None
    )

    dis_val = dis if _present(dis) else (
        calc_dis_from_vnc(vnc_val, plus or 0, minus or 0)
        if vnc_val is not None
        else None
    )

    if inv_val is not None and dis_val is not None:
        return calc_fcid_from_inv_dis(inv_val, dis_val)

    if inv_val is not None:
        return calc_fcid_from_inv_dis(inv_val, 0)

    raise ValueError("Insufficient data for FCID")


# FCFR, FCRF, VARIAZIONE LIQUIDITà


def resolve_fcfr(fcfr=None, patrimonio_netto=None, debiti_finanz=None, quota_rimbors_capital=None):
    if _present(fcfr):
        return fcfr
    if _present(patrimonio_netto) and _present(debiti_finanz) and _present(quota_rimbors_capital):
        return calc_fcfr(patrimonio_netto, debiti_finanz, quota_rimbors_capital)
    raise ValueError("Insufficient data for FCFR")


def resolve_fcrf(fcrf=None, oneri_finanziari=None, dividendi=None):
    if _present(fcrf):
        return fcrf
    if _present(oneri_finanziari) and _present(dividendi):
        return calc_fcrf(oneri_finanziari, dividendi)
    raise ValueError("Insufficient data for FCRF")


def resolve_var_liquidity(fcgc=None, fcid=None, fcfr=None, fcrf=None, var_liquidity=None):
    if _present(var_liquidity):
        return var_liquidity
    if all(map(_present, [fcgc, fcid, fcfr, fcrf])):
        return calc_var_liquidity(fcgc, fcid, fcfr, fcrf)
    raise ValueError("Insufficient data for liquidity")


# FCU/FCE 


def resolve_fcu(fcu=None, fcgc=None, fcid=None):
    if _present(fcu):
        return fcu
    if _present(fcgc) and _present(fcid):
        return calc_fcu(fcgc, fcid)
    raise ValueError("Insufficient data for FCU")


def resolve_fce(
    fce=None,
    fcu=None,
    fcfr=None,
    quota_rimbors_capital=None,
    fcrf=None,
    dividendi=None,
):
    if _present(fce):
        return fce

    if all(map(_present, [fcu, fcfr, quota_rimbors_capital, fcrf, dividendi])):
        return calc_fce(fcu, fcfr, quota_rimbors_capital, fcrf, dividendi)

    raise ValueError("Insufficient data for FCE")


# NPV LOGIC


def resolve_npv(npv=None, fc=None, k=None, i_0=None, t=None, cost=0):
    if _present(npv):
        return npv

    if not (_present(fc) and _present(k) and _present(i_0) and _present(t)):
        raise ValueError("Insufficient data for NPV")

    fc_list = _as_list(fc)
    t_list = _as_list(t)

    if len(fc_list) != len(t_list):
        raise ValueError("FC and T length mismatch")

    pv = 0

    for f, ti in zip(fc_list, t_list):
        fc_net = f - cost
        df = calc_df_constant(k, ti)
        pv += calc_pv(fc_net, df)

    return calc_npv(pv, i_0)
