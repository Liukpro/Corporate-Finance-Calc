import streamlit as st
from formulas import (calc_fccnogc, calc_rol, calc_fcgc, calc_fcid,
                      calc_fcfr, calc_fcrf, calc_var_liq, calc_fcu,
                      calc_fce, calc_npv, calc_va_bond_zero, calc_ros, 
                      calc_roi, calc_roe)

# Configurazione Pagina
st.set_page_config(page_title="Corporate Finance Calc", layout="wide")

st.title("Corporate Finance Calc")
st.caption("v2.1 - Fail-Fast Philosophy Implementation")
st.caption("If the program crashes with a TypeError, it means that the input or the import of the data required for the calculation was unsuccessful (incomplete).")

st.sidebar.markdown("""
**License:** Apache 2.0  
**Source code:** [GitHub](https://github.com/Liukpro/Corporate-Finance-Calc)
""")

# Inizializzazione Session State
keys_to_init = [
    'fccnogc', 'rol', 'fcgc', 'fcid', 'fcfr', 'fcrf', 'fcu', 'fce',
    'ros', 'roi', 'roe', 'pat_net', 'deb_f', 'liq', 'pos_fin_net', 'cin',
    'ric_op_mon', 'cost_op_mon', 'ammort', 'mol', 'of', 'imp', 'ut_net',
    'ccno', 'rimb_cap', 'div'
]
for key in keys_to_init:
    if key not in st.session_state:
        st.session_state[key] = None
      
if st.sidebar.button("Reset Session"):
    for key in keys_to_init:
        st.session_state[key] = None
    st.rerun()
  
st.sidebar.title("Tools")
page = st.sidebar.radio("Select one", [
    "Cash Flow Analysis",
    "Ratio Analysis",
    "NPV",
    "Bond Evaluation - in progress",
    "Coming Soon..."
])

# --- PAGE: CASH FLOW ANALYSIS ---
if page == "Cash Flow Analysis":
    st.subheader("Cash Flow Calculation")

    op = st.selectbox("Select the Cash Flow to calculate:", 
                      ["FCCNOGC", "RO-L", "FCGC", "FCID", "FCFR", "FCRf", "Variazione Liquidità", "FCU", "FCE"])
    
    # Helper per mostrare valori calcolati in precedenza
    def show_dependency(key_name, label):
        if st.session_state[key_name] is not None:
            st.info(f"{label} from previous calculation: {st.session_state[key_name]:.2f}")
            return st.session_state[key_name]
        else:
            st.warning(f"{label} not calculated yet.")
            return st.number_input(f"Insert {label} manually", value=0.0)

    if op == "FCCNOGC":
        st.write("Formula: Multiple paths (Revenue-Costs-Taxes / MOL-Taxes / ROL-Taxes+Ammort)")
        c1, c2 = st.columns(2)
        with c1:
            ric = st.number_input("Operating Revenue", value=0.0)
            cost = st.number_input("Operating Costs", value=0.0)
            imp = st.number_input("Taxes (Income)", value=0.0)
        with c2:
            ammort = st.number_input("Amortisation", value=0.0)
            mol = st.number_input("MOL (EBITDA)", value=0.0)
            rol_input = st.number_input("RO-L (EBIT)", value=0.0)

        if st.button("Calculate FCCNOGC"):
            try:
                # Passiamo i valori. Se l'utente lascia 0.0, calc_fccnogc userà le sue logiche elif
                res = calc_fccnogc(None, ric_op_mon=ric, cost_op_mon=cost, imp=imp, ammort=ammort, mol=mol, rol=rol_input)
                st.session_state.fccnogc = res
                st.success(f"FCCNOGC = {res:.2f}")
            except ValueError as e:
                st.error(f"Error: {e}")

    elif op == "RO-L":
        c1, c2 = st.columns(2)
        with c1:
            ric = st.number_input("Operating Revenue", value=0.0)
            cost = st.number_input("Operating Costs", value=0.0)
        with c2:
            ammort = st.number_input("Amortisation", value=0.0)
            mol = st.number_input("MOL (EBITDA)", value=0.0)

        if st.button("Calculate RO-L"):
            try:
                res = calc_rol(None, ric_op_mon=ric, cost_op_mon=cost, ammort=ammort, mol=mol)
                st.session_state.rol = res
                st.success(f"RO-L = {res:.2f}")
            except ValueError as e:
                st.error(f"Error: {e}")

    elif op == "FCGC":
        fccnogc_v = show_dependency('fccnogc', 'FCCNOGC')
        ccno = st.number_input("Delta CCNO (Working Capital Variation)", value=0.0)
        if st.button("Calculate FCGC"):
            res = calc_fcgc(None, fccnogc=fccnogc_v, ccno=ccno)
            st.session_state.fcgc = res
            st.success(f"FCGC = {res:.2f}")

    elif op == "FCID":
        st.write("Calculation of Cash Flow from Investing Activities")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Disinvestment Data**")
            val_sto = st.number_input("Historical Value", value=0.0)
            ammo_ti = st.number_input("Annual Amort. Quota", value=0.0)
            n_ammo = st.number_input("Years of Amort.", value=0, step=1)
            plus = st.number_input("Capital Gain (Plusvalenza)", value=0.0)
            minus = st.number_input("Capital Loss (Minusvalenza)", value=0.0)
            dis_manual = st.number_input("Direct Disinvestment Value (if known)", value=0.0)
        with c2:
            st.markdown("**Investment Data**")
            inv_manual = st.number_input("Direct Investment Value", value=0.0)
            acq1 = st.number_input("Acquisition 1", value=0.0)
            acq2 = st.number_input("Acquisition 2", value=0.0)

        if st.button("Calculate FCID"):
            try:
                res = calc_fcid(fcid=None, inv=inv_manual if inv_manual != 0 else None, 
                                dis=dis_manual if dis_manual != 0 else None,
                                val_sto=val_sto if val_sto != 0 else None, 
                                ammo_ti=ammo_ti, n_ammo=n_ammo,
                                plus=plus, minus=minus, acqui_1=acq1, acqui_2=acq2)
                st.session_state.fcid = res
                st.success(f"FCID = {res:.2f}")
            except ValueError as e:
                st.error(str(e))

    elif op == "FCFR":
        rimb_cap = st.number_input("Repayment of Capital (Rimborso Quota Capitale)", value=0.0)
        pat_net = st.number_input("Equity (Patrimonio Netto)", value=0.0)
        deb_f = st.number_input("Financial Debt", value=0.0)
        if st.button("Calculate FCFR"):
            res = calc_fcfr(None, rimb_cap=rimb_cap, pat_net=pat_net, deb_f=deb_f)
            st.session_state.fcfr = res
            st.success(f"FCFR = {res:.2f}")

    elif op == "FCRf":
        of = st.number_input("Interest Expense (Oneri Finanziari)", value=0.0)
        div = st.number_input("Dividends", value=0.0)
        if st.button("Calculate FCRf"):
            res = calc_fcrf(None, of=of, div=div)
            st.session_state.fcrf = res
            st.success(f"FCRf = {res:.2f}")

    elif op == "FCU":
        v1 = show_dependency('fcgc', 'FCGC')
        v2 = show_dependency('fcid', 'FCID')
        if st.button("Calculate FCU"):
            res = calc_fcu(None, fcgc=v1, fcid=v2)
            st.session_state.fcu = res
            st.success(f"FCU = {res:.2f}")

    elif op == "FCE":
        fcu_v = show_dependency('fcu', 'FCU')
        fcfr_v = show_dependency('fcfr', 'FCFR')
        fcrf_v = show_dependency('fcrf', 'FCRf')
        rimb_cap = st.number_input("Capital Repayment", value=0.0)
        div = st.number_input("Dividends Paid", value=0.0)
        if st.button("Calculate FCE"):
            try:
                res = calc_fce(None, fcu=fcu_v, fcfr=fcfr_v, fcrf=fcrf_v, rimb_cap=rimb_cap, div=div)
                st.session_state.fce = res
                st.success(f"FCE = {res:.2f}")
            except ValueError as e:
                st.error(str(e))

    elif op == "Variazione Liquidità":
        v1 = show_dependency('fcgc', 'FCGC')
        v2 = show_dependency('fcid', 'FCID')
        v3 = show_dependency('fcfr', 'FCFR')
        v4 = show_dependency('fcrf', 'FCRf')
        if st.button("Calculate Delta Cash"):
            try:
                res = calc_var_liq(None, fcgc=v1, fcid=v2, fcfr=v3, fcrf=v4)
                st.success(f"Total Liquidity Variation = {res:.2f}")
            except ValueError as e:
                st.error(str(e))

# --- PAGE: RATIO ANALYSIS ---
elif page == "Ratio Analysis":
    st.subheader("Profitability Ratios")
    c1, c2 = st.columns(2)
    with c1:
        ric_op = st.number_input("Operating Revenue", value=0.0)
        rol_v = st.number_input("RO-L (EBIT)", value=0.0)
        pat_n = st.number_input("Equity (Patrimonio Netto)", value=0.0)
    with c2:
        deb_f = st.number_input("Financial Debt", value=0.0)
        liq = st.number_input("Liquidity", value=0.0)
        of_v = st.number_input("Interest Expense", value=0.0)
        imp_v = st.number_input("Income Taxes", value=0.0)

    if st.button("Run Ratio Analysis"):
        try:
            ros = calc_ros(None, rol=rol_v, ric_op_mon=ric_op)
            roi = calc_roi(None, rol=rol_v, deb_f=deb_f, liq=liq, pat_net=pat_n)
            roe = calc_roe(None, rol=rol_v, of=of_v, imp=imp_v, pat_net=pat_n)
            
            st.markdown("---")
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("ROS", f"{ros:.2%}")
            col_b.metric("ROI", f"{roi:.2%}")
            col_c.metric("ROE", f"{roe:.2%}")
        except ValueError as e:
            st.error(str(e))
        except ZeroDivisionError:
            st.error("Mathematical Error: Division by zero.")

# --- PAGE: NPV ---
elif page == "NPV":
    st.subheader("Net Present Value (NPV)")
    k = st.number_input("Discount rate k (decimal, e.g. 0.08)", value=0.0, format="%.4f")
    i_0 = st.number_input("Initial investment I₀", value=0.0)
    cost = st.number_input("Fixed cost per period", value=0.0)
    n = st.number_input("Number of periods", min_value=1, step=1, value=1)

    fc_list = []
    t_list = []
    for i in range(int(n)):
        col1, col2 = st.columns(2)
        with col1:
            fc_list.append(st.number_input(f"Cash flow period {i+1}", key=f"fc_{i}", value=0.0))
        with col2:
            t_list.append(st.number_input(f"Time period {i+1}", key=f"t_{i}", value=float(i+1)))

    if st.button("Calculate NPV"):
        try:
            res = calc_npv(None, fc=fc_list, k=k, i_0=i_0, t=t_list, cost=cost)
            st.success(f"NPV = {res:.2f}")
            if res > 0: st.info("The project creates value.")
            elif res < 0: st.warning("The project destroys value.")
        except ValueError as e:
            st.error(str(e))

# --- PAGE: BOND ---
elif page == "Bond Evaluation - in progress":
    st.subheader("Bond Valuation")
    sub_op = st.selectbox("Type", ["Zero Coupon Bond", "Coupon Bond"])
    
    if sub_op == "Zero Coupon Bond":
        vn = st.number_input("Face Value (VN)", value=100.0)
        k = st.number_input("Discount Rate", value=0.03, format="%.4f")
        dur = st.number_input("Duration (years)", value=1.0)
        if st.button("Calculate VA"):
            res = calc_va_bond_zero(None, k=k, vn=vn, dur=dur)
            st.success(f"Bond Present Value = {res:.2f}")
    
    else:
        st.info("Coupon Bond logic implementation pending final review.")

elif page == "Coming Soon...":
    st.write("Stay tuned for Stock Evaluation, WACC, and Mortgage tools.")
