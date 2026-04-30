import streamlit as st
from formulas import (calc_fccnogc, calc_rol, calc_fcgc, calc_fcid,
                      calc_fcfr, calc_fcrf, calc_var_liq, calc_fcu,
                      calc_fce, calc_npv, calc_va_bond_zero, calc_ros, 
                      calc_roi, calc_roe, calc_va_ced_bond)


# Configurazione Pagina
st.set_page_config(page_title="Corporate Finance Calc", layout="wide")

st.title("Corporate Finance Calc")
st.caption("v2.1 - Fail-Fast Philosophy Implementation")

st.sidebar.markdown("""
**License:** Apache 2.0  
**Source code:** [GitHub](https://github.com/Liukpro/Corporate-Finance-Calc)
""")

# Inizializzazione Session State
keys_to_init = [
    # Cash Flow keys
    'fccnogc', 'rol', 'fcgc', 'fcid', 'fcfr', 'fcrf', 'fcu', 'fce',
    # Ratio keys
    'ros', 'roi', 'roe', 'pat_net', 'deb_f', 'liq', 'pos_fin_net', 'cin',
    'ric_op_mon', 'cost_op_mon', 'ammort', 'mol', 'of', 'imp', 'ut_net',
    'ccno', 'rimb_cap', 'div',
    # Bond keys
    'bond_zero_va', 'bond_zero_ytm', 'bond_coupon_va',
    # Stock keys
    'stock_price_gordon', 'stock_price_no_growth', 'vaoc',
    'dividend_1', 'g', 'retention_ratio', 'payout_ratio'
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
    "Bond Evaluation",
    "Stock Evaluation",
    "Coming Soon..."
])

#CASH FLOW ANALYSIS
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
        imp_v = st.number_input("Taxes", value=0.0)

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
elif page == "Bond Evaluation":
    st.subheader("Bond Valuation")
    sub_op = st.selectbox("Type", ["Zero Coupon Bond", "Coupon Bond"])
    
    if sub_op == "Zero Coupon Bond":
        st.markdown("### Zero Coupon Bond Valuation")
        col1, col2 = st.columns(2)
        with col1:
            vn = st.number_input("Face Value (VN)", value=100.0)
            k = st.number_input("Discount Rate (Market Rate)", value=0.03, format="%.4f")
        with col2:
            dur = st.number_input("Duration (years)", value=1.0)
            
        if st.button("Calculate Bond Value"):
            try:
                res = calc_va_bond_zero(None, k=k, vn=vn, dur=dur)
                st.success(f"Bond Present Value = {res:.2f}")
            except ValueError as e:
                st.error(str(e))
        
        if st.button("Calculate Yield to Maturity"):
            try:
                va = st.number_input("Current Bond Price", value=95.0, key="ytm_price")
                ytm = calc_yield_to_mat_zero(None, va=va, vn=vn, dur=dur)
                st.success(f"Yield to Maturity = {ytm:.4%}")
            except ValueError as e:
                st.error(str(e))
    
    else:  # Coupon Bond
        st.markdown("### Coupon Bond Valuation")
        col1, col2 = st.columns(2)
        with col1:
            vn_ced = st.number_input("Face Value (VN)", value=100.0, key="coupon_vn")
            k_ced = st.number_input("Coupon Rate (annual)", value=0.05, format="%.4f")
            t_ced = st.number_input("Time to Maturity (years)", value=5.0)
        with col2:
            k_merk = st.number_input("Market Discount Rate", value=0.04, format="%.4f")
            
        if st.button("Calculate Coupon Bond Value"):
            try:
                res = calc_va_ced_bond(None, vn_ced=vn_ced, k_ced=k_ced, t_ced=t_ced, k_merk=k_merk)
                st.success(f"Coupon Bond Present Value = {res:.2f}")
                
                # Mostra anche il valore della cedola annuale
                annual_coupon = vn_ced * k_ced
                st.info(f"Annual Coupon Payment = {annual_coupon:.2f}")
            except ValueError as e:
                st.error(str(e))

#--- PAGE: stock---
elif page == "Stock Evaluation":
    st.subheader("Stock Valuation")
    
    model = st.selectbox("Valuation Model", ["Gordon Growth Model", "No Growth Model"])
    
    if model == "Gordon Growth Model":
        st.markdown("### Gordon Growth Model (Dividend Discount Model)")
        
        calc_method = st.radio("Input Method", 
                               ["Direct (Dividend₁, k, g)", 
                                "From Earnings (E₀, Payout, ROE, k)"])
        
        if calc_method == "Direct (Dividend₁, k, g)":
            col1, col2, col3 = st.columns(3)
            with col1:
                dividend_1 = st.number_input("Expected Dividend next year (D₁)", value=2.0)
            with col2:
                k = st.number_input("Required Return (k)", value=0.10, format="%.4f")
            with col3:
                g = st.number_input("Growth Rate (g)", value=0.05, format="%.4f")
            
            earnings_t0 = None
            payout_ratio = None
            retention_ratio = None
            roe = None
            
        else:  # From Earnings
            col1, col2 = st.columns(2)
            with col1:
                earnings_t0 = st.number_input("Current Earnings (E₀)", value=5.0)
                payout_ratio = st.number_input("Payout Ratio (dividends/earnings)", value=0.40, format="%.4f")
            with col2:
                k = st.number_input("Required Return (k)", value=0.10, format="%.4f")
                roe = st.number_input("Return on Equity (ROE)", value=0.15, format="%.4f")
            
            retention_ratio = 1 - payout_ratio
            g = retention_ratio * roe
            
            dividend_1 = None
            
            st.info(f"Calculated: Retention Ratio = {retention_ratio:.4f}, Growth Rate = {g:.4%}")
        
        if st.button("Calculate Stock Price"):
            try:
                price = calc_stock_price(
                    stock_price=None,
                    dividend=dividend_1,
                    k=k,
                    g=g,
                    dividend_1=dividend_1,
                    earnings_t0=earnings_t0,
                    payout_ratio=payout_ratio,
                    retention_ratio=retention_ratio,
                    roe=roe,
                    model="gordon"
                )
                st.success(f"Stock Price = {price:.2f}")
                
                # Calcolo VAOC se disponibili i dati per il modello no growth
                if earnings_t0 is not None and k is not None:
                    no_growth_price = earnings_t0 / k
                    vaoc = price - no_growth_price
                    st.info(f"Value of Growth Opportunities (VAOC) = {vaoc:.2f}")
                    st.caption(f"No-growth value: {no_growth_price:.2f} | Growth premium: {vaoc:.2f}")
                    
            except ValueError as e:
                st.error(str(e))
    
    else:  # No Growth Model
        st.markdown("### No Growth Model (Constant Dividend)")
        
        col1, col2 = st.columns(2)
        with col1:
            dividend = st.number_input("Constant Dividend", value=2.0)
        with col2:
            k = st.number_input("Required Return (k)", value=0.10, format="%.4f")
        
        if st.button("Calculate Stock Price"):
            try:
                price = calc_stock_price(
                    stock_price=None,
                    dividend=dividend,
                    k=k,
                    g=None,
                    model="no_growth"
                )
                st.success(f"Stock Price = {price:.2f}")
            except ValueError as e:
                st.error(str(e))
    
    # Sezione separata per VAOC diretto
    st.markdown("---")
    st.subheader("Value of Growth Opportunities (VAOC)")
    st.caption("Calculate the difference between growth and no-growth stock values")
    
    col1, col2 = st.columns(2)
    with col1:
        price_growth = st.number_input("Stock Price (with growth)", value=50.0, key="vaoc_growth")
    with col2:
        price_no_growth = st.number_input("Stock Price (no growth)", value=30.0, key="vaoc_no_growth")
    
    if st.button("Calculate VAOC"):
        try:
            vaoc = calc_vaoc(price_growth, price_no_growth)
            st.success(f"VAOC = {vaoc:.2f}")
            st.info("This represents the additional value created by growth opportunities.")
        except ValueError as e:
            st.error(str(e))

elif page == "Coming Soon...":
    st.write("Stay tuned for Stock Evaluation, WACC, and Mortgage tools.")
