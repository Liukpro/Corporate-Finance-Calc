#Cash Flow and Ratio Analysis, ANALISI STORICA
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
        raise ValueError("Revenue is zero, ROS error, division not possible")
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
            raise ValueError("CIN is zero, ROI error, division not possible")
        return rol / cin
    else:
        raise ValueError("Insufficient Data")

def calc_roe(roe, rol = None, of = None, imp = None, pat_net = None):
    if roe is not None:
        return roe
    elif pat_net == 0:
        raise ValueError("Equity is zero, ROE error, division not possible")
    elif rol is not None and of is not None and imp is not None and pat_net is not None:
        ut_net = rol - of - imp
        return ut_net / pat_net
    else:
        raise ValueError("Insufficient Data")

#nel nuovo file qui non ho inserito il calcolo della variazione di ccno, attenzione in futuro!!
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

    # Calcolo investimenti totali
    if inv is not None:
        inv_final = inv
    else:
        inv_final = (acqui_1 or 0) + (acqui_2 or 0)

    # Calcolo disinvestimenti - SOLO SE ESPLICITAMENTE RICHIESTO
    if dis is not None:
        # dis già fornito direttamente
        pass
    elif vnc is not None:
        # dis calcolato da vnc
        dis = vnc + (plus or 0) - (minus or 0)
    elif val_sto is not None and ammo_ti is not None and n_ammo is not None:
        # dis calcolato da valore storico
        vnc_calc = val_sto - (ammo_ti * n_ammo)
        dis = vnc_calc + (plus or 0) - (minus or 0)
    else:
        # Nessun dato sui disinvestimenti
        dis = None

    # Risultato finale
    if dis is not None:
        return dis - inv_final
    elif inv_final != 0:
        return 0 - inv_final
    else:
        raise ValueError("Insufficient data: provide at least investments or divestments")

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
    elif fcu is not None and fcfr is not None and rimb_cap is not None and fcrf is not None and div is not None:
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
    
def calc_yield_to_mat_zero(k, va, vn, dur):
    if k is not None:
        return k
    if va !=0 and vn != 0 and dur != 0:
        return (vn / va) ** (1/dur) - 1
    else:
        raise ValueError("Insufficient Data")

def calc_va_ced_bond(va_ced, vn_ced, k_ced, t_ced, k_merk):
    if va_ced is not None:
        return va_ced
    elif vn_ced is not None and k_ced is not None and t_ced is not None and k_merk is not None:
        ced = vn_ced * k_ced
        va_ced = 0.0
        n = int(t_ced)
        f = t_ced - n
        for i in range(n):
            va_ced += ced / ((1 + k_merk) ** (i + 1))
        if f > 0:
            if k_merk != -1:
                va_ced += ced * f / ((1 + k_merk) ** t_ced)
        va_ced += vn_ced / ((1 + k_merk) ** t_ced)
        return va_ced
    else:
        raise ValueError("Insufficient Data")


def calc_stock_price(stock_price=None, k=None, g=None, b=None,
                     dividend_1=None, earnings_t0=None,
                     retention_ratio=None, roe=None,
                     model="gordon"):

    if stock_price is not None:
        return stock_price

    # growth
    if g is None:
        if retention_ratio is not None and roe is not None:
            g = retention_ratio * roe
        elif b is not None and roe is not None:
            g = b * roe

    # dividend
    if dividend_1 is None:
        if earnings_t0 is not None and b is not None:
            dividend_1 = earnings_t0 * (1 - b)
        else:
            raise ValueError("Insufficient data for dividend")

    # no growth
    if model == "no_growth":
        if k is None:
            raise ValueError("k required")
        return dividend_1 / k

    # gordon
    if model == "gordon":
        if k is None or g is None:
            raise ValueError("k and g required")
        if k <= g:
            raise ValueError("k must be > g")
        return dividend_1 / (k - g)

    raise ValueError("Unknown model")
    
def calc_vaoc(stock_price_grow=None, stock_price_no_grow=None):
    if stock_price_grow is not None and stock_price_no_grow is not None:
        vaoc = stock_price_grow - stock_price_no_grow
        return vaoc
    else:
        raise ValueError("Insufficient Data for VAOC")

def calc_capital_share(mortgage, n):
    """
    Quota capitale costante:
    C = M / n
    """
    if mortgage is not None and n is not None and n != 0:
        return mortgage / n
    raise ValueError("Insufficient Data for capital share")


def calc_residual_debt(mortgage, n, t):
    """
    Debito residuo al tempo t:
    D_t = M * (1 - t/n)
    """
    if mortgage is not None and n is not None and t is not None:
        return mortgage * (1 - t / n)
    raise ValueError("Insufficient Data for residual debt")


def calc_residual_debt_prev(mortgage, n, t):
    """
    Debito residuo al tempo t-1:
    D_(t-1) = M * (1 - (t-1)/n)
    """
    if mortgage is not None and n is not None and t is not None:
        return mortgage * (1 - (t - 1) / n)
    raise ValueError("Insufficient Data for residual debt t-1")


def calc_interest_t(mortgage, n, t, k):
    """
    Interessi al tempo t:
    I_t = D_(t-1) * k
    """
    if mortgage is not None and n is not None and t is not None and k is not None:
        residual_prev = calc_residual_debt_prev(mortgage, n, t)
        return residual_prev * k
    raise ValueError("Insufficient Data for interest calculation")


def calc_mortgage_payment(capital_share, interest_share):
    """
    Rata:
    R_t = quota capitale + interessi
    """
    if capital_share is not None and interest_share is not None:
        return capital_share + interest_share
    raise ValueError("Insufficient Data for payment")


def calc_mortgage_payment_fr(debt, k, n):
    if debt is not None and n is not None:
        if k == 0:
            return debt / n
        if k is not None:
            return debt * (k * (1 + k) ** n) / ((1 + k) ** n - 1)
    raise ValueError("Insufficient Data for French payment")


def calc_residual_debt_fr(debt, k, n, t):
    if debt is not None and k is not None and n is not None and t is not None:
        return debt * ((1 + k) ** n - (1 + k) ** t) / ((1 + k) ** n - 1)
    raise ValueError("Insufficient Data for residual debt")


def calc_interest_fr(debt, k, n, t):
    if debt is not None and k is not None and n is not None and t is not None:
        residual_prev = debt * ((1 + k) ** n - (1 + k) ** (t - 1)) / ((1 + k) ** n - 1)
        return residual_prev * k
    raise ValueError("Insufficient Data for interest")


def calc_capital_share_fr(payment, interest):
    if payment is not None and interest is not None:
        return payment - interest
    raise ValueError("Insufficient Data for capital share")


def build_italian_table(mortgage, annual_rate, years):
    n = years * 12
    k = annual_rate / 12

    capital_share = calc_capital_share(mortgage, n)

    table = []

    for t in range(1, n + 1):
        # Interessi calcolati correttamente con D_(t-1)
        interest = calc_interest_t(mortgage, n, t, k)

        payment = capital_share + interest

        # Debito residuo dopo il pagamento (D_t)
        residual = calc_residual_debt(mortgage, n, t)

        table.append({
            "period": t,
            "year": (t - 1) // 12 + 1,
            "capital": capital_share,
            "interest": interest,
            "payment": payment,
            "residual": residual
        })

    return table


def build_french_table(debt, annual_rate, years):
    """Restituisce lista di dizionari con tabella completa"""
    months = years * 12
    monthly_rate = annual_rate / 12
    
    if monthly_rate == 0:
        constant_payment = debt / months
    else:
        constant_payment = debt * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    
    table = []
    residual = debt
    
    for t in range(1, months + 1):
        interest = residual * monthly_rate
        capital = constant_payment - interest
        
        if t == months:
            capital = residual
            constant_payment = capital + interest
        
        residual = debt * ((1 + monthly_rate) ** months - (1 + monthly_rate) ** t) / ((1 + monthly_rate) ** months - 1)
        
        table.append({
            "month": t,
            "year": (t - 1) // 12 + 1,
            "capital": round(capital, 2),
            "interest": round(interest, 2),
            "payment": round(constant_payment, 2),
            "residual": round(max(residual, 0), 2)
        })
    
    return table


# ============ WACC ============

def calc_wacc(re, rd, tc, equity, debt):
    if re is None or rd is None or tc is None or equity is None or debt is None:
        raise ValueError("Insufficient Data for WACC")
    total = equity + debt
    if total == 0:
        raise ValueError("Total capital cannot be zero")
    return re * (equity / total) + rd * (1 - tc) * (debt / total)


# ============ NPV FCU/FCE ============

def calc_npv_fcu(cash_flows, wacc, initial_investment, fixed_cost=0):
    """cash_flows è lista di float, wacc è float"""
    if not cash_flows:
        raise ValueError("No cash flows provided")
    pv = 0
    for t, cf in enumerate(cash_flows, start=1):
        net_cf = cf - fixed_cost
        pv += net_cf / ((1 + wacc) ** t)
    return pv - initial_investment


def calc_npv_fce(cash_flows, ke, initial_equity, fixed_cost=0):
    """cash_flows è lista di float, ke è float"""
    if not cash_flows:
        raise ValueError("No cash flows provided")
    pv = 0
    for t, cf in enumerate(cash_flows, start=1):
        net_cf = cf - fixed_cost
        pv += net_cf / ((1 + ke) ** t)
    return pv - initial_equity
