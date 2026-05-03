import pandas as pd
import streamlit as st
from numpy as np
from formulas import (calc_fccnogc, calc_rol, calc_fcgc, calc_fcid,
                      calc_fcfr, calc_fcrf, calc_var_liq, calc_fcu,
                      calc_fce, calc_npv, calc_va_bond_zero, calc_yield_to_mat_zero, calc_ros, 
                      calc_roi, calc_roe, calc_va_ced_bond, calc_stock_price, calc_vaoc, 
                      build_italian_table, build_french_table, calc_wacc, calc_npv_fcu, calc_npv_fce )


# Configurazione Pagina
st.set_page_config(page_title="Corporate Finance Calc", layout="wide")

st.title("Corporate Finance Calc")
st.caption("v3.0")

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
    'dividend_1', 'g', 'retention_ratio', 'payout_ratio',
    # Mortgage keys (NUOVE - Ammortamento Italiano)
    'mortgage_capital_share', 'mortgage_payment_it', 'mortgage_residual_debt_it',
    'mortgage_interest_t', 'mortgage_paid_off_debt',
    # Mortgage keys (NUOVE - Ammortamento Francese)
    'mortgage_payment_fr', 'mortgage_residual_debt_fr', 'mortgage_interest_fr',
    'mortgage_capital_share_fr', 'mortgage_paid_off_debt_fr',
    # WACC keys (NUOVE)
    'wacc', 'npv_fcu', 'npv_fce', 'total_pv_fcu', 'total_pv_fce',
    # Discount factor keys (NUOVE)
    'df_wacc', 'df_ke'
]
for key in keys_to_init:
    if key not in st.session_state:
        st.session_state[key] = None
      
#Reset Session
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
    "Mortgage",
    "WACC",
    "NPV with FCU/FCE",
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
            return st.number_input(f"Insert {label} manually", value=0.0, key=f"manual_{key_name}")

    if op == "FCCNOGC":
        st.write("Formula: Multiple paths")
        st.caption("Inserisci i dati per UNO dei seguenti metodi (gli altri lasciali vuoti)")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Metodo 1: Revenue - Costs - Taxes**")
            use_metodo1 = st.checkbox("Usa Metodo 1", key="fccnogc_use_met1")
            
            if use_metodo1:
                ric = st.number_input("Operating Revenue", value=0.0, key="fccnogc_ric")
                cost = st.number_input("Operating Costs", value=0.0, key="fccnogc_cost")
                imp = st.number_input("Taxes (Income)", value=0.0, key="fccnogc_imp")
            else:
                ric = cost = imp = None
                
            st.markdown("**Metodo 2: MOL - Taxes**")
            use_metodo2 = st.checkbox("Usa Metodo 2", key="fccnogc_use_met2")
            
            if use_metodo2:
                mol = st.number_input("MOL (EBITDA)", value=0.0, key="fccnogc_mol")
                imp2 = st.number_input("Taxes (Income)", value=0.0, key="fccnogc_imp2")
            else:
                mol = imp2 = None
                
        with col2:
            st.markdown("**Metodo 3: ROL - Taxes + Ammort**")
            use_metodo3 = st.checkbox("Usa Metodo 3", key="fccnogc_use_met3")
            if use_metodo3:
                rol_input = st.number_input("RO-L (EBIT)", value=0.0, key="fccnogc_rol")
                ammort = st.number_input("Amortisation", value=0.0, key="fccnogc_amm")
                imp3 = st.number_input("Taxes (Income)", value=0.0, key="fccnogc_imp3")
            else:
                rol_input = ammort = imp3 = None
                
        if st.button("Calculate FCCNOGC", key="btn_fccnogc"):
            try:
                res = calc_fccnogc(
                    ric_op_mon=ric,
                    cost_op_mon=cost,
                    imp=imp or imp2 or imp3,
                    ammort=ammort,
                    mol=mol,
                    rol=rol_input
                    )
                st.session_state.fccnogc = res
                st.success(f"FCCNOGC = {res:.2f}")
                
            except ValueError as e:
                st.error(f"Error: {e}")

    elif op == "RO-L":
        st.write("Formula: Revenue - Costs - Ammort  OR  MOL - Ammort")
        st.caption("Inserisci i dati per UNO dei seguenti metodi")
        
        col1, col2 = st.columns(2)
        with col1:
            use_metodo1 = st.checkbox("Usa Metodo 1: Revenue - Costs - Ammort", key="rol_use_met1")
            if use_metodo1:
                ric = st.number_input("Operating Revenue", value=0.0, key="rol_ric")
                cost = st.number_input("Operating Costs", value=0.0, key="rol_cost")
                ammort = st.number_input("Amortisation", value=0.0, key="rol_amm")
            else:
                ric = cost = ammort = None
                
        with col2:
            use_metodo2 = st.checkbox("Usa Metodo 2: MOL - Ammort", key="rol_use_met2") 
            if use_metodo2:
                mol = st.number_input("MOL (EBITDA)", value=0.0, key="rol_mol")
                ammort2 = st.number_input("Amortisation", value=0.0, key="rol_amm2")
                
            else:
                mol = ammort2 = None
                
        if st.button("Calculate RO-L", key="btn_rol"):
            try:
                res = calc_rol(
                ric_op_mon=ric,
                cost_op_mon=cost,
                ammort=ammort or ammort2,
                mol=mol
            )
                st.session_state.rol = res
                st.success(f"RO-L = {res:.2f}")
            except ValueError as e:
                st.error(f"Error: {e}")

    elif op == "FCGC":
        st.caption("Formula: FCGC = FCCNOGC - ΔCCNO")
        
        fccnogc_v = show_dependency('fccnogc', 'FCCNOGC')
        ccno = st.number_input("Delta CCNO (Working Capital Variation)", value=0.0, key="fcgc_ccno")
        if st.button("Calculate FCGC", key="btn_fcgc"):
            try:
                res = calc_fcgc(fccnogc=fccnogc_v, ccno=ccno)
                st.session_state.fcgc = res
                st.success(f"FCGC = {res:.2f}")
            except ValueError as e:
                st.error(str(e))

    elif op == "FCID":
        st.write("Cash Flow from Investing Activities")
        st.warning("Scegli UNO dei seguenti metodi (gli altri lasciali vuoti)")
        
        metodo = st.radio("Seleziona metodo:", 
                          ["FCID diretto", "Disinvestimenti - Investimenti", "Solo Investimenti (negativo)"],
                          key="fcid_method")
        
        if metodo == "FCID diretto":
            fcid_val = st.number_input("Valore FCID diretto", value=0.0, key="fcid_direct")
            
            if st.button("Calculate FCID", key="btn_fcid_direct"):
                try:
                    res = calc_fcid(fcid=fcid_val)
                    st.session_state.fcid = res
                    st.success(f"FCID = {res:.2f}")
                except ValueError as e:
                    st.error(str(e))
        
        elif metodo == "Disinvestimenti - Investimenti":
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Dati Disinvestimenti**")
                dis = st.number_input("Disinvestimenti (valore diretto)", value=0.0, key="dis_direct")
                
                st.markdown("---")
                st.markdown("**Oppure calcola disinvestimento da:**")
                vnc = st.number_input("VNC (Valore Netto Contabile)", value=0.0, key="vnc")
                val_sto = st.number_input("Valore storico", value=0.0, key="val_sto")
                ammo_ti = st.number_input("Quota ammortamento annuale", value=0.0, key="ammo_ti")
                n_ammo = st.number_input("Anni di ammortamento", value=0, step=1, key="n_ammo")
                plus = st.number_input("Plusvalenza", value=0.0, key="plus")
                minus = st.number_input("Minusvalenza", value=0.0, key="minus")
            
            with col2:
                st.markdown("**Dati Investimenti**")
                inv = st.number_input("Investimenti (valore diretto)", value=0.0, key="inv_direct")
                
                st.markdown("---")
                st.markdown("**Oppure somma di acquisizioni:**")
                acqui_1 = st.number_input("Acquisizione 1", value=0.0, key="acqui_1")
                acqui_2 = st.number_input("Acquisizione 2", value=0.0, key="acqui_2")
            
            if st.button("Calculate FCID", key="btn_fcid_dis_inv"):
                try:
                    params = {}
                    if inv != 0:
                        params["inv"] = inv
                    if dis != 0:
                        params["dis"] = dis
                    if vnc != 0:
                        params["vnc"] = vnc
                    if val_sto != 0:
                        params["val_sto"] = val_sto
                    if ammo_ti != 0:
                        params["ammo_ti"] = ammo_ti
                    if n_ammo != 0:
                        params["n_ammo"] = n_ammo
                    if plus != 0:
                        params["plus"] = plus
                    if minus != 0:
                        params["minus"] = minus
                    if acqui_1 != 0:
                        params["acqui_1"] = acqui_1
                    if acqui_2 != 0:
                        params["acqui_2"] = acqui_2
                    
                    res = calc_fcid(**params)
                    st.session_state.fcid = res
                    st.success(f"FCID = {res:.2f}")
                except ValueError as e:
                    st.error(str(e))
        
        else:  # Solo Investimenti
            inv = st.number_input("Investimenti", value=0.0, key="inv_only")
            
            if st.button("Calculate FCID", key="btn_fcid_inv_only"):
                try:
                    res = calc_fcid(inv=inv)
                    st.session_state.fcid = res
                    st.success(f"FCID = {res:.2f}")
                    st.caption(f"Calcolo: -{inv} (nessun disinvestimento)")
                except ValueError as e:
                    st.error(str(e))

    elif op == "FCRf":
        st.caption("Formula: FCRf = - Interest Expense - Dividends")
        
        col1, col2 = st.columns(2)
        with col1:
            of = st.number_input("Interest Expense (Oneri Finanziari)", value=0.0, key="fcrf_of")
        with col2:
            div = st.number_input("Dividends", value=0.0, key="fcrf_div")
            
        if st.button("Calculate FCRf", key="btn_fcrf"):
            try:
                res = calc_fcrf(of=of, div=div)
                st.session_state.fcrf = res
                st.success(f"FCRf = {res:.2f}")
            except ValueError as e:
                st.error(str(e))


    elif op == "FCFR":
        st.caption("Formula: FCRf = - Interest Expense - Dividends")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            pat_net = st.number_input("Equity (Patrimonio Netto)", value=0.0, key="fcfr_pat_net")       
        with col2:
            deb_f = st.number_input("Financial Debt", value=0.0, key="fcfr_deb_f")
        with col3:
            rimb_cap = st.number_input("Capital Repayment", value=0.0, key="fcfr_rimb_cap")
        if st.button("Calculate FCFR", key="btn_fcfr"):
            try:
                res = calc_fcfr(pat_net=pat_net, deb_f=deb_f, rimb_cap=rimb_cap)
                st.session_state.fcfr = res
                st.success(f"FCFR = {res:.2f}")
            except ValueError as e:
                st.error(str(e))

    elif op == "FCU":
        st.caption("Formula: FCU = FCGC + FCID")
        fcgc_val = show_dependency('fcgc', 'FCGC')
        fcid_val = show_dependency('fcid', 'FCID')
        
        if st.button("Calculate FCU", key="btn_fcu"):
            try:
                res = calc_fcu(fcgc=fcgc_val, fcid=fcid_val)
                st.session_state.fcu = res
                st.success(f"FCU = {res:.2f}")
            except ValueError as e:
                st.error(str(e))

    elif op == "FCE":
        st.caption("Formula: FCE = FCU + FCFR - RimborsoCapitale + FCRf - Dividends")
        fcu_val = show_dependency('fcu', 'FCU')
        fcfr_val = show_dependency('fcfr', 'FCFR')
        fcrf_val = show_dependency('fcrf', 'FCRf')
        
        col1, col2 = st.columns(2)
        with col1:
            rimb_cap = st.number_input("Capital Repayment", value=0.0, key="fce_rimb_cap")
        with col2:
            div = st.number_input("Dividends Paid", value=0.0, key="fce_div")
        
        if st.button("Calculate FCE", key="btn_fce"):
            
            try:
                res = calc_fce(fcu=fcu_val, fcfr=fcfr_val, fcrf=fcrf_val, rimb_cap=rimb_cap, div=div)
                st.session_state.fce = res
                st.success(f"FCE = {res:.2f}")
            except ValueError as e:
                st.error(str(e))

    elif op == "Variazione Liquidità":
        st.caption("Formula: ΔCash = FCGC + FCID + FCFR + FCRf")
        
        fcgc_val = show_dependency('fcgc', 'FCGC')
        fcid_val = show_dependency('fcid', 'FCID')
        fcfr_val = show_dependency('fcfr', 'FCFR')
        fcrf_val = show_dependency('fcrf', 'FCRf')
        
        if st.button("Calculate Delta Cash", key="btn_var_liq"):
            try:
                res = calc_var_liq(fcgc=fcgc_val, fcid=fcid_val, fcfr=fcfr_val, fcrf=fcrf_val)
                st.success(f"Total Liquidity Variation = {res:.2f}")
            except ValueError as e:
                st.error(str(e))
#RATIO ANALYSIS
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
            # Chiama le funzioni di formulas.py - NON riscrivere la logica
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

# NPV
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
            # Chiama la funzione di formulas.py - NON riscrivere il ciclo
            res = calc_npv(None, fc=fc_list, k=k, i_0=i_0, t=t_list, cost=cost)
            st.success(f"NPV = {res:.2f}")
          
            k_values = np.arange(0,0.5, 0.01)
            npv_values = []
            for k_val in k_values:
                npv_values.append(calc_npv(None, fc=fc_list, k=k_val, i_o = i_0, t = t_list, cost = cost))

            chart_npv = pd.DataFrame({"k": k_values, "NPV": npv_values})
            st.line_chart(chart_npv, x = "k", y= "NPV")
          
            if res > 0: 
                st.info("The project creates value.")
            elif res < 0: 
                st.warning("The project destroys value.")
        except ValueError as e:
            st.error(str(e))


#BONDs
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
                # Chiama la funzione
                res = calc_va_bond_zero(None, k=k, vn=vn, dur=dur)
                st.success(f"Bond Present Value = {res:.2f}")
            except ValueError as e:
                st.error(str(e))
        
        if st.button("Calculate Yield to Maturity"):
            try:
                va = st.number_input("Current Bond Price", value=95.0, key="ytm_price")
                # Chiama la funzione appena aggiunta
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
                # Chiama la funzione
                res = calc_va_ced_bond(None, vn_ced=vn_ced, k_ced=k_ced, t_ced=t_ced, k_merk=k_merk)
                st.success(f"Coupon Bond Present Value = {res:.2f}")
                annual_coupon = vn_ced * k_ced
                st.info(f"Annual Coupon Payment = {annual_coupon:.2f}")
            except ValueError as e:
                st.error(str(e))

#STOCKs
elif page == "Stock Evaluation":
    st.subheader("Stock Valuation")
    
    model = st.selectbox("Valuation Model", ["Gordon Growth Model", "No Growth Model"])
    
    if model == "Gordon Growth Model":
        st.markdown("### Gordon Growth Model (Dividend Discount Model)")
        st.warning("Richiede k > g (required return > growth rate)")
        
        calc_method = st.radio("Input Method", 
                               ["Direct (Dividend₁, k, g)", 
                                "From Earnings (E₀, Payout, ROE, k)"])
        
        if calc_method == "Direct (Dividend₁, k, g)":
            col1, col2, col3 = st.columns(3)
            with col1:
                dividend_1 = st.number_input("Expected Dividend next year (D₁)", value=2.0, min_value=0.0)
            with col2:
                k = st.number_input("Required Return (k)", value=0.10, format="%.4f", min_value=0.01)
            with col3:
                g = st.number_input("Growth Rate (g)", value=0.05, format="%.4f", min_value=0.0)
            
            earnings_t0 = None
            payout_ratio = None
            retention_ratio = None
            roe = None
            
        else:  # From Earnings
            col1, col2 = st.columns(2)
            with col1:
                earnings_t0 = st.number_input("Current Earnings (E₀)", value=5.0, min_value=0.0)
                payout_ratio = st.number_input("Payout Ratio", value=0.40, format="%.4f", min_value=0.0, max_value=1.0)
            with col2:
                k = st.number_input("Required Return (k)", value=0.10, format="%.4f", min_value=0.01)
                roe = st.number_input("Return on Equity (ROE)", value=0.15, format="%.4f", min_value=0.0)
            
            retention_ratio = 1 - payout_ratio
            g = None  # sarà calcolato dalla funzione
            dividend_1 = None
            
            st.info(f"Retention Ratio = {retention_ratio:.4f}")
        
        if st.button("Calculate Stock Price"):
            try:
                price = calc_stock_price(
                    stock_price=None,
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
                
                # VAOC usando calc_vaoc e calc_stock_price per no-growth
                if earnings_t0 is not None and k is not None:
                    no_growth_price = calc_stock_price(
                        stock_price=None,
                        dividend=earnings_t0,
                        k=k,
                        model="no_growth"
                    )
                    vaoc = calc_vaoc(price, no_growth_price)
                    st.info(f"VAOC = {vaoc:.2f} (Growth premium)")
                    st.caption(f"No-growth value: {no_growth_price:.2f} | Growth premium: {vaoc:.2f}")
                    
            except ValueError as e:
                st.error(str(e))
    
    else:  # No Growth Model
        st.markdown("### No Growth Model (Constant Dividend)")
        
        col1, col2 = st.columns(2)
        with col1:
            dividend = st.number_input("Constant Dividend", value=2.0, min_value=0.0)
        with col2:
            k = st.number_input("Required Return (k)", value=0.10, format="%.4f", min_value=0.01)
        
        if st.button("Calculate Stock Price"):
            try:
                price = calc_stock_price(
                    stock_price=None,
                    dividend=dividend,
                    k=k,
                    model="no_growth"
                )
                st.success(f"Stock Price = {price:.2f}")
            except ValueError as e:
                st.error(str(e))
    
    # VAOC diretto
    st.markdown("---")
    st.subheader("Value of Growth Opportunities (VAOC)")
    st.caption("Calculate the difference between growth and no-growth stock values")
    
    col1, col2 = st.columns(2)
    with col1:
        price_growth = st.number_input("Stock Price (with growth)", value=50.0, min_value=0.0, key="vaoc_growth")
    with col2:
        price_no_growth = st.number_input("Stock Price (no growth)", value=30.0, min_value=0.0, key="vaoc_no_growth")
    
    if st.button("Calculate VAOC"):
        try:
            vaoc = calc_vaoc(price_growth, price_no_growth)
            st.success(f"VAOC = {vaoc:.2f}")
            if vaoc > 0:
                st.info("Positive VAOC = growth creates value")
            elif vaoc < 0:
                st.warning("Negative VAOC = growth destroys value")
            else:
                st.info("VAOC = 0 = growth adds no value")
        except ValueError as e:
            st.error(str(e))
          
elif page == "Mortgage":
    st.subheader("Mutuo - Ammortamento")
    st.caption("Confronto tra ammortamento italiano (quota capitale costante) e francese (rata costante)")
    st.info("**Nota:** I calcoli sono basati su rate MENSILI.")
    
    mortgage_type = st.radio("Tipo di ammortamento", ["Italiano (Quota Capitale Costante)", "Francese (Rata Costante)"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        mortgage_debt = st.number_input("Debito iniziale (€)", value=100000.0, min_value=0.0, step=10000.0, key="mortgage_debt")
    with col2:
        annual_rate = st.number_input("Tasso di interesse annuo (%)", value=3.0, min_value=0.0, step=0.5, key="annual_rate") / 100
        monthly_rate = annual_rate / 12
        st.caption(f"Tasso mensile equivalente: {monthly_rate:.4%}")
    with col3:
        years = st.number_input("Durata (anni)", value=20, min_value=1, max_value=50, step=1, key="years")
        months = years * 12
        st.caption(f"Durata in mesi: {months}")
    
    st.markdown("---")
    
    # Display mode fuori dal bottone (con key per mantenere lo stato)
    display_mode = st.radio(
        "Visualizzazione", 
        ["Resa annuale (sintesi)", "Mensile (primi 12 mesi)", "Completa (tutti i mesi)"],
        key="mortgage_display_mode"
    )
    
    if mortgage_type == "Italiano (Quota Capitale Costante)":
        st.markdown("### Piano di Ammortamento Italiano")
        
        if st.button("Calcola Ammortamento Italiano", key="btn_italian"):
            table = build_italian_table(mortgage_debt, annual_rate, years)
            st.session_state['italian_table'] = table
        
        # Mostra la tabella se esiste in session_state
        if 'italian_table' in st.session_state:
            table = st.session_state['italian_table']
            
            total_interest = sum(row["interest"] for row in table)
            first_payment = table[0]["payment"]
            last_payment = table[-1]["payment"]
            
            col_a, col_b, col_c, col_d = st.columns(4)
            col_a.metric("Quota Capitale Mensile", f"€{table[0]['capital']:,.2f}")
            col_b.metric("Prima Rata", f"€{first_payment:,.2f}")
            col_c.metric("Ultima Rata", f"€{last_payment:,.2f}")
            col_d.metric("Totale Interessi", f"€{total_interest:,.2f}")
            
            st.info(f"**Totale pagato:** €{mortgage_debt + total_interest:,.2f}")
            
            if display_mode == "Resa annuale (sintesi)":
                annual_summary = []
                for year in range(1, years + 1):
                    year_rows = [r for r in table if r["year"] == year]
                    annual_summary.append({
                        "Anno": year,
                        "Capitale Pagato": sum(r["capital"] for r in year_rows),
                        "Interessi Pagati": sum(r["interest"] for r in year_rows),
                        "Totale Rata": sum(r["payment"] for r in year_rows),
                        "Debito Residuo": year_rows[-1]["residual"] if year_rows else 0
                    })
                st.dataframe(annual_summary, use_container_width=True)
            elif display_mode == "Mensile (primi 12 mesi)":
                st.dataframe(table[:12], use_container_width=True)
            else:
                st.dataframe(table, use_container_width=True)
    
    else:
        st.markdown("### Piano di Ammortamento Francese")
        
        if st.button("Calcola Ammortamento Francese", key="btn_french"):
            table = build_french_table(mortgage_debt, annual_rate, years)
            st.session_state['french_table'] = table
        
        # Mostra la tabella se esiste in session_state
        if 'french_table' in st.session_state:
            table = st.session_state['french_table']
            
            total_interest = sum(row["interest"] for row in table)
            constant_payment = table[0]["payment"] if table else 0
            
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Rata Mensile Costante", f"€{constant_payment:,.2f}")
            col_b.metric("Totale Interessi", f"€{total_interest:,.2f}")
            col_c.metric("Totale Pagato", f"€{mortgage_debt + total_interest:,.2f}")
            
            if display_mode == "Resa annuale (sintesi)":
                annual_summary = []
                for year in range(1, years + 1):
                    year_rows = [r for r in table if r["year"] == year]
                    annual_summary.append({
                        "Anno": year,
                        "Capitale Pagato": sum(r["capital"] for r in year_rows),
                        "Interessi Pagati": sum(r["interest"] for r in year_rows),
                        "Totale Rata": sum(r["payment"] for r in year_rows),
                        "Debito Residuo": year_rows[-1]["residual"] if year_rows else 0
                    })
                st.dataframe(annual_summary, use_container_width=True)
            elif display_mode == "Mensile (primi 12 mesi)":
                st.dataframe(table[:12], use_container_width=True)
            else:
                st.dataframe(table, use_container_width=True)


# WACC
elif page == "WACC":
    st.subheader("WACC - Weighted Average Cost of Capital")
    st.caption("Formula: WACC = r_e × (E/V) + r_d × (1 - t_c) × (D/V)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Costo del Capitale Proprio**")
        cost_of_equity = st.number_input("r_e (Costo dell'Equity)", value=0.12, min_value=0.0, max_value=1.0, step=0.01, format="%.4f")
        equity = st.number_input("E (Equity - Patrimonio Netto)", value=500000.0, min_value=0.0, step=10000.0)
    
    with col2:
        st.markdown("**Costo del Debito**")
        cost_of_debt = st.number_input("r_d (Costo del Debito)", value=0.05, min_value=0.0, max_value=1.0, step=0.01, format="%.4f")
        debt = st.number_input("D (Debito Finanziario)", value=300000.0, min_value=0.0, step=10000.0)
        tax_rate = st.number_input("t_c (Aliquota Fiscale)", value=0.24, min_value=0.0, max_value=0.5, step=0.01, format="%.4f")
    
    if st.button("Calcola WACC"):
        try:
            wacc = calc_wacc(cost_of_equity, cost_of_debt, tax_rate, equity, debt)
            st.session_state.wacc = wacc
            
            st.markdown("---")
            st.metric("WACC", f"{wacc:.2%}")
            
            with st.expander("Vedi calcolo dettagliato"):
                total = equity + debt
                st.write(f"E/V = {equity:,.0f} / {total:,.0f} = {equity/total:.2%}")
                st.write(f"D/V = {debt:,.0f} / {total:,.0f} = {debt/total:.2%}")
                st.write(f"r_e × (E/V) = {cost_of_equity:.2%} × {equity/total:.2%} = {cost_of_equity * equity/total:.2%}")
                st.write(f"r_d × (1-t_c) × (D/V) = {cost_of_debt:.2%} × {1-tax_rate:.2%} × {debt/total:.2%} = {cost_of_debt * (1-tax_rate) * debt/total:.2%}")
        except ValueError as e:
            st.error(str(e))


# NPV with FCU/FCE
elif page == "NPV with FCU/FCE":
    st.subheader("NPV - Due Approcci")
    st.caption("NPV con logica del capitale investito (FCU) vs logica dell'azionista (FCE)")
    
    approach = st.radio("Seleziona approccio", ["FCU (Free Cash Flow to Firm)", "FCE (Free Cash Flow to Equity)"])
    
    if approach == "FCU (Free Cash Flow to Firm)":
        st.markdown("### NPV con FCU (WACC come tasso di sconto)")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.get('wacc') is not None:
                st.info(f"WACC calcolato in precedenza: {st.session_state.wacc:.2%}")
                use_saved_wacc = st.checkbox("Usa WACC salvato", value=True)
                if use_saved_wacc:
                    wacc = st.session_state.wacc
                else:
                    wacc = st.number_input("WACC (%)", value=8.0, min_value=0.0, step=0.5) / 100
            else:
                wacc = st.number_input("WACC (%)", value=8.0, min_value=0.0, step=0.5) / 100
            
            i0_fcu = st.number_input("Investimento Iniziale I₀ (€)", value=100000.0, min_value=0.0, step=10000.0)
            cost = st.number_input("Costo fisso per periodo (€)", value=0.0)
        
        with col2:
            n = st.number_input("Numero di periodi", min_value=1, step=1, value=5)
        
        st.markdown("**Flussi di Cassa (FCU) per periodo**")
        fcu_list = []
        for i in range(int(n)):
            fcu_list.append(st.number_input(f"FCU periodo {i+1}", key=f"fcu_{i}", value=10000.0, step=1000.0))
        
        if st.button("Calcola NPV (FCU)"):
            try:
                npv = calc_npv_fcu(fcu_list, wacc, i0_fcu, cost)
                st.session_state.npv_fcu = npv
                
                st.markdown("---")
                st.metric("NPV", f"€{npv:,.2f}", 
                          delta="Positivo" if npv > 0 else "Negativo" if npv < 0 else "Neutro")
                
                if npv > 0:
                    st.info("Il progetto crea valore")
                elif npv < 0:
                    st.warning("Il progetto distrugge valore")
                else:
                    st.info("NPV = 0")
            except ValueError as e:
                st.error(str(e))
    
    else:
        st.markdown("### NPV con FCE (Ke come tasso di sconto)")
        
        col1, col2 = st.columns(2)
        with col1:
            ke = st.number_input("Ke (Costo dell'Equity/Required Return) (%)", value=10.0, min_value=0.0, step=0.5) / 100
            equity0 = st.number_input("Equity Iniziale (€)", value=50000.0, min_value=0.0, step=10000.0)
            cost = st.number_input("Costo fisso per periodo (€)", value=0.0)
        
        with col2:
            n = st.number_input("Numero di periodi", min_value=1, step=1, value=5)
        
        st.markdown("**Flussi di Cassa (FCE) per periodo**")
        fce_list = []
        for i in range(int(n)):
            fce_list.append(st.number_input(f"FCE periodo {i+1}", key=f"fce_{i}", value=8000.0, step=1000.0))
        
        if st.button("Calcola NPV (FCE)"):
            try:
                npv = calc_npv_fce(fce_list, ke, equity0, cost)
                st.session_state.npv_fce = npv
                
                st.markdown("---")
                st.metric("NPV (FCE)", f"€{npv:,.2f}",
                          delta="Positivo" if npv > 0 else "Negativo" if npv < 0 else "Neutro")
                
                if npv > 0:
                    st.info("Il progetto crea valore per l'azionista")
                elif npv < 0:
                    st.warning("Il progetto distrugge valore per l'azionista")
                else:
                    st.info("NPV = 0")
            except ValueError as e:
                st.error(str(e))

elif page == "Coming Soon...":
    st.write("Stay tuned for Risk Analysis and Portfolio")
