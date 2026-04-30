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


def _is_present(value):
    present = value is not None
    return present


def _as_list(value):
    if isinstance(value, (list, tuple)):
        out = list(value)
        return out
    out = [value]
    return out


# -----------------------
# OPERATING AREA
# -----------------------

def resolve_mol(mol=None, ric_op_mon=None, cost_op_mon=None):
    if mol is not None:
        result = mol
        return result

    if ric_op_mon is not None and cost_op_mon is not None:
        result = calc_mol(ric_op_mon, cost_op_mon)
        return result

    raise ValueError("Insufficient Data for MOL")


def resolve_rol(rol=None, mol=None, ric_op_mon=None, cost_op_mon=None, amortisat=None):
    if rol is not None:
        result = rol
        return result

    if mol is not None and amortisat is not None:
        result = calc_rol_from_mol(mol, amortisat)
        return result

    if ric_op_mon is not None and cost_op_mon is not None and amortisat is not None:
        mol_value = calc_mol(ric_op_mon, cost_op_mon)
        result = calc_rol_from_mol(mol_value, amortisat)
        return result

    raise ValueError("Insufficient Data for ROL")


def resolve_fccnogc(
    fccnogc=None,
    ric_op_mon=None,
    cost_op_mon=None,
    tax=None,
    mol=None,
    rol=None,
    amortisat=None,
):
    if fccnogc is not None:
        result = fccnogc
        return result

    if ric_op_mon is not None and cost_op_mon is not None and tax is not None:
        result = calc_fccnogc_from_revenue(ric_op_mon, cost_op_mon, tax)
        return result

    if mol is not None and tax is not None:
        result = calc_fccnogc_from_mol(mol, tax)
        return result

    if rol is not None and tax is not None and amortisat is not None:
        result = calc_fccnogc_from_rol(rol, tax, amortisat)
        return result

    if ric_op_mon is not None and cost_op_mon is not None and amortisat is not None and tax is not None:
        mol_value = calc_mol(ric_op_mon, cost_op_mon)
        rol_value = calc_rol_from_mol(mol_value, amortisat)
        result = calc_fccnogc_from_rol(rol_value, tax, amortisat)
        return result

    raise ValueError("Insufficient Data for FCCNOGC")


def resolve_ros(ros=None, rol=None, ric_op_mon=None):
    if ros is not None:
        result = ros
        return result

    if rol is not None and ric_op_mon is not None:
        if ric_op_mon == 0:
            raise ValueError("Revenue is zero, ROS error, division not possible")
        result = calc_ros_from_rol(rol, ric_op_mon)
        return result

    raise ValueError("Insufficient Data for ROS")


def resolve_cin(cin=None, patrimonio_netto=None, debiti_finanz=None, liquidity=None):
    if cin is not None:
        result = cin
        return result

    if patrimonio_netto is not None and debiti_finanz is not None and liquidity is not None:
        result = calc_cin(patrimonio_netto, debiti_finanz, liquidity)
        return result

    raise ValueError("Insufficient Data for CIN")


def resolve_roi(roi=None, rol=None, cin=None, patrimonio_netto=None, debiti_finanz=None, liquidity=None):
    if roi is not None:
        result = roi
        return result

    if rol is not None and cin is not None:
        if cin == 0:
            raise ValueError("CIN is zero, ROI error, division not possible")
        result = calc_roi_from_rol(rol, cin)
        return result

    if rol is not None and patrimonio_netto is not None and debiti_finanz is not None and liquidity is not None:
        cin_value = calc_cin(patrimonio_netto, debiti_finanz, liquidity)
        if cin_value == 0:
            raise ValueError("CIN is zero, ROI error, division not possible")
        result = calc_roi_from_rol(rol, cin_value)
        return result

    raise ValueError("Insufficient Data for ROI")


def resolve_net_profit(utile_netto=None, rol=None, oneri_finanz=None, tax=None):
    if utile_netto is not None:
        result = utile_netto
        return result

    if rol is not None and oneri_finanz is not None and tax is not None:
        result = calc_net_profit(rol, oneri_finanz, tax)
        return result

    raise ValueError("Insufficient Data for Net Profit")


def resolve_roe(roe=None, utile_netto=None, rol=None, oneri_finanz=None, tax=None, patrimonio_netto=None):
    if roe is not None:
        result = roe
        return result

    if utile_netto is not None and patrimonio_netto is not None:
        if patrimonio_netto == 0:
            raise ValueError("Equity is zero, ROE error, division not possible")
        result = calc_roe(utile_netto, patrimonio_netto)
        return result

    if rol is not None and oneri_finanz is not None and tax is not None and patrimonio_netto is not None:
        if patrimonio_netto == 0:
            raise ValueError("Equity is zero, ROE error, division not possible")
        utile_netto_value = calc_net_profit(rol, oneri_finanz, tax)
        result = calc_roe(utile_netto_value, patrimonio_netto)
        return result

    raise ValueError("Insufficient Data for ROE")


# -----------------------
# CASH FLOW AREA
# -----------------------

def resolve_var_ccno(var_ccno=None, ccno1=None, ccno2=None):
    if var_ccno is not None:
        result = var_ccno
        return result

    if ccno1 is not None and ccno2 is not None:
        result = calc_var_ccno(ccno1, ccno2)
        return result

    raise ValueError("Insufficient Data for variation of CCNO")


def resolve_fcgc(fcgc=None, fccnogc=None, var_ccno=None):
    if fcgc is not None:
        result = fcgc
        return result

    if fccnogc is not None and var_ccno is not None:
        result = calc_fcgc(fccnogc, var_ccno)
        return result

    raise ValueError("Insufficient Data for FCGC")


def resolve_inv(inv=None, acquisition_1=None, acquisition_2=None):
    if inv is not None:
        result = inv
        return result

    if acquisition_1 is not None and acquisition_2 is not None:
        result = calc_inv(acquisition_1, acquisition_2)
        return result

    raise ValueError("Insufficient Data for investments")


def resolve_vnc(vnc=None, valore_stor=None, ammo_ti=None, n_ammo_ti=None):
    if vnc is not None:
        result = vnc
        return result

    if valore_stor is not None and ammo_ti is not None and n_ammo_ti is not None:
        result = calc_vnc(valore_stor, ammo_ti, n_ammo_ti)
        return result

    raise ValueError("Insufficient Data for VNC")


def resolve_dis(dis=None, vnc=None, plus=None, minus=None):
    if dis is not None:
        result = dis
        return result

    if vnc is not None and plus is not None and minus is not None:
        result = calc_dis_from_vnc(vnc, plus, minus)
        return result

    raise ValueError("Insufficient Data for divestments")


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
    if fcid is not None:
        result = fcid
        return result

    if inv is None and acquisition_1 is not None and acquisition_2 is not None:
        inv = calc_inv(acquisition_1, acquisition_2)

    if dis is None and vnc is None and valore_stor is not None and ammo_ti is not None and n_ammo_ti is not None:
        vnc = calc_vnc(valore_stor, ammo_ti, n_ammo_ti)

    if dis is None and vnc is not None and plus is not None and minus is not None:
        dis = calc_dis_from_vnc(vnc, plus, minus)

    if dis is not None and inv is not None:
        result = calc_fcid_from_inv_dis(inv, dis)
        return result

    if inv is not None:
        zero_dis = 0
        result = calc_fcid_from_inv_dis(inv, zero_dis)
        return result

    raise ValueError("Insufficient Data for FCID")


def resolve_fcfr(fcfr=None, patrimonio_netto=None, debiti_finanz=None, quota_rimbors_capital=None):
    if fcfr is not None:
        result = fcfr
        return result

    if patrimonio_netto is not None and debiti_finanz is not None and quota_rimbors_capital is not None:
        result = calc_fcfr(patrimonio_netto, debiti_finanz, quota_rimbors_capital)
        return result

    raise ValueError("Insufficient Data for FCFR")


def resolve_fcrf(fcrf=None, oneri_finanziari=None, dividendi=None):
    if fcrf is not None:
        result = fcrf
        return result

    if oneri_finanziari is not None and dividendi is not None:
        result = calc_fcrf(oneri_finanziari, dividendi)
        return result

    raise ValueError("Insufficient Data for FCRF")


def resolve_var_liquidity(fcgc=None, fcid=None, fcfr=None, fcrf=None, var_liquidity=None):
    if var_liquidity is not None:
        result = var_liquidity
        return result

    if fcgc is not None and fcid is not None and fcfr is not None and fcrf is not None:
        result = calc_var_liquidity(fcgc, fcid, fcfr, fcrf)
        return result

    raise ValueError("Insufficient Data for liquidity variation")


def resolve_fcu(fcu=None, fcgc=None, fcid=None):
    if fcu is not None:
        result = fcu
        return result

    if fcgc is not None and fcid is not None:
        result = calc_fcu(fcgc, fcid)
        return result

    raise ValueError("Insufficient Data for FCU")


def resolve_fce(
    fce=None,
    fcu=None,
    fcfr=None,
    quota_rimbors_capital=None,
    fcrf=None,
    dividendi=None,
):
    if fce is not None:
        result = fce
        return result

    if fcu is not None and fcfr is not None and quota_rimbors_capital is not None and fcrf is not None and dividendi is not None:
        result = calc_fce(fcu, fcfr, quota_rimbors_capital, fcrf, dividendi)
        return result

    raise ValueError("Insufficient Data for FCE")


# -----------------------
# NPV AREA
# -----------------------

def resolve_fc_series(fc=None, fcu=None, fce=None):
    if fc is not None:
        series = _as_list(fc)
        source = "FC"
        return series, source

    if fcu is not None:
        series = _as_list(fcu)
        source = "FCU"
        return series, source

    if fce is not None:
        series = _as_list(fce)
        source = "FCE"
        return series, source

    raise ValueError("No cash flow source available")


def resolve_discount_rate(source, k=None, k_t=None, wacc=None, ke=None):
    if source == "FCU":
        rate = wacc if wacc is not None else k
        if rate is None:
            raise ValueError("Missing WACC for FCU valuation")
        return rate, "constant" if k_t is None else "variable"

    if source == "FCE":
        rate = ke if ke is not None else k
        if rate is None:
            raise ValueError("Missing Ke for FCE valuation")
        return rate, "constant" if k_t is None else "variable"

    rate = k
    if rate is None and k_t is None:
        raise ValueError("Missing discount rate for FC valuation")
    return rate, "constant" if k_t is None else "variable"


def resolve_npv(
    fc=None,
    fcu=None,
    fce=None,
    cost=0,
    t=None,
    i_0=None,
    k=None,
    k_t=None,
    wacc=None,
    ke=None,
):
    fc_series, source = resolve_fc_series(fc=fc, fcu=fcu, fce=fce)
    rate, rate_kind = resolve_discount_rate(source=source, k=k, k_t=k_t, wacc=wacc, ke=ke)

    t_series = _as_list(t) if t is not None else list(range(1, len(fc_series) + 1))

    if len(fc_series) != len(t_series):
        raise ValueError("The numbers of cash flows and periods should be equal")

    pv_list = []

    if rate_kind == "variable":
        k_series = _as_list(k_t)
        if len(k_series) != len(fc_series):
            raise ValueError("The numbers of rates and periods should be equal")

        for fc_i, k_i, t_i in zip(fc_series, k_series, t_series):
            fc_net = calc_fc_net(fc_i, cost)
            df = calc_df_variable(k_i, t_i)
            pv = calc_pv(fc_net, df)
            pv_list.append(pv)
    else:
        for fc_i, t_i in zip(fc_series, t_series):
            fc_net = calc_fc_net(fc_i, cost)
            df = calc_df_constant(rate, t_i)
            pv = calc_pv(fc_net, df)
            pv_list.append(pv)

    total_pv = calc_total_pv(pv_list)

    if i_0 is None:
        raise ValueError("Missing initial investment i_0")

    npv_value = calc_npv(total_pv, i_0)
    return npv_value


# -----------------------
# BOND ZERO COUPON AREA
# -----------------------

def resolve_bond_zero_va(va=None, k=None, vn=None, dur=None):
    if va is not None:
        result = va
        return result

    if k is not None and vn is not None and dur is not None:
        df = calc_bond_zero_discount_factor(k, dur)
        result = calc_bond_zero_va(vn, df)
        return result

    raise ValueError("Insufficient Data for zero coupon bond VA")


def resolve_bond_zero_yield_to_maturity(k=None, va=None, vn=None, dur=None):
    if k is not None:
        result = k
        return result

    if va is not None and vn is not None and dur is not None:
        if va == 0 or vn == 0 or dur == 0:
            raise ValueError("Insufficient Data")
        mont = calc_bond_zero_mont(vn, va)
        factor = calc_bond_zero_factor(dur)
        result = calc_bond_zero_yield_to_maturity(mont, factor)
        return result

    raise ValueError("Insufficient Data for zero coupon bond YTM")
