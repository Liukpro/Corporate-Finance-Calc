import streamlit as st
from formulas import (calc_fccnogc, calc_rol, calc_fcgc, calc_fcid,
                      calc_fcfr, calc_fcrf, calc_var_liq, calc_fcu,
                      calc_fce, calc_npv, calc_va_bond_zero, calc_yield_to_mat_zero, calc_ros, 
                      calc_roi, calc_roe, calc_va_ced_bond, calc_stock_price, calc_vaoc)


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
        st.caption("Inserisci i dati per UNO dei seguenti metodi (gli altri lasciali a 0)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Metodo 1: Revenue - Costs - Taxes**")
            ric = st.number_input("Operating Revenue", value=0.0, key="fccnogc_ric")
            cost = st.number_input("Operating Costs", value=0.0, key="fccnogc_cost")
            imp = st.number_input("Taxes (Income)", value=0.0, key="fccnogc_imp")
        with col2:
            st.markdown("**Metodo 2: MOL - Taxes**")
            mol = st.number_input("MOL (EBITDA)", value=0.0, key="fccnogc_mol")
            st.markdown("**Metodo 3: ROL - Taxes + Ammort**")
            rol_input = st.number_input("RO-L (EBIT)", value=0.0, key="fccnogc_rol")
            ammort = st.number_input("Amortisation", value=0.0, key="fccnogc_amm")

        if st.button("Calculate FCCNOGC"):
            try:
                # Determina quale metodo usare in base a valori non-zero
                if ric != 0 and cost != 0 and imp != 0:
                    res = ric - cost - imp
                    st.info("Usato metodo: Revenue - Costs - Taxes")
                elif mol != 0 and imp != 0:
                    res = mol - imp
                    st.info("Usato metodo: MOL - Taxes")
                elif rol_input != 0 and ammort != 0 and imp != 0:
                    res = rol_input - imp + ammort
                    st.info("Usato metodo: ROL - Taxes + Ammort")
                else:
                    raise ValueError("Inserisci dati validi per almeno un metodo di calcolo")
                    
                st.session_state.fccnogc = res
                st.success(f"FCCNOGC = {res:.2f}")
            except ValueError as e:
                st.error(f"Error: {e}")

    elif op == "RO-L":
        st.write("Formula: Revenue - Costs - Ammort  OR  MOL - Ammort")
        
        col1, col2 = st.columns(2)
        with col1:
            ric = st.number_input("Operating Revenue", value=0.0, key="rol_ric")
            cost = st.number_input("Operating Costs", value=0.0, key="rol_cost")
        with col2:
            ammort = st.number_input("Amortisation", value=0.0, key="rol_amm")
            mol = st.number_input("MOL (EBITDA)", value=0.0, key="rol_mol")

        if st.button("Calculate RO-L"):
            try:
                if ric != 0 and cost != 0 and ammort != 0:
                    res = ric - cost - ammort
                    st.info("Usato metodo: Revenue - Costs - Ammort")
                elif mol != 0 and ammort != 0:
                    res = mol - ammort
                    st.info("Usato metodo: MOL - Ammort")
                else:
                    raise ValueError("Inserisci dati validi per almeno un metodo")
                    
                st.session_state.rol = res
                st.success(f"RO-L = {res:.2f}")
            except ValueError as e:
                st.error(f"Error: {e}")

    elif op == "FCGC":
        st.caption("Formula: FCGC = FCCNOGC - ΔCCNO")
        
        fccnogc_v = show_dependency('fccnogc', 'FCCNOGC')
        ccno = st.number_input("Delta CCNO (Working Capital Variation)", value=0.0)
        
        if st.button("Calculate FCGC"):
            res = fccnogc_v - ccno
            st.session_state.fcgc = res
            st.success(f"FCGC = {res:.2f}")
            st.caption(f"Calcolo: {fccnogc_v:.2f} - {ccno:.2f} = {res:.2f}")

    elif op == "FCID":
        st.write("Cash Flow from Investing Activities")
        st.warning("⚠️ Scegli UNO dei seguenti metodi (gli altri lasciali vuoti)")
        
        metodo = st.radio("Seleziona metodo:", 
                          ["Direct Input", "Divestments - Investments", "Only Investments (negative)"])
        
        if metodo == "Direct Input":
            direct_val = st.number_input("Direct FCID value", value=0.0)
            if st.button("Calculate FCID"):
                st.session_state.fcid = direct_val
                st.success(f"FCID = {direct_val:.2f}")
        
        elif metodo == "Divestments - Investments":
            col1, col2 = st.columns(2)
            with col1:
                divestments = st.number_input("Divestments (sale of assets)", value=0.0)
            with col2:
                investments = st.number_input("Investments (purchase of assets)", value=0.0)
            
            if st.button("Calculate FCID"):
                res = divestments - investments
                st.session_state.fcid = res
                st.success(f"FCID = {res:.2f}")
                st.caption(f"Calcolo: {divestments:.2f} - {investments:.2f} = {res:.2f}")
        
        else:  # Only Investments
            investments = st.number_input("Investment Amount", value=0.0)
            if st.button("Calculate FCID"):
                res = -abs(investments)
                st.session_state.fcid = res
                st.success(f"FCID = {res:.2f}")
                st.caption(f"Calcolo: -{abs(investments):.2f} (nessun disinvestimento)")

    elif op == "FCFR":
        st.caption("Formula: FCFR = Equity + Debt - Capital Repayment")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            pat_net = st.number_input("Equity (Patrimonio Netto)", value=0.0)
        with col2:
            deb_f = st.number_input("Financial Debt", value=0.0)
        with col3:
            rimb_cap = st.number_input("Capital Repayment", value=0.0)
        
        if st.button("Calculate FCFR"):
            res = pat_net + deb_f - rimb_cap
            st.session_state.fcfr = res
            st.success(f"FCFR = {res:.2f}")

    elif op == "FCRf":
        st.caption("Formula: FCRf = - Interest Expense - Dividends")
        
        col1, col2 = st.columns(2)
        with col1:
            of = st.number_input("Interest Expense (Oneri Finanziari)", value=0.0)
        with col2:
            div = st.number_input("Dividends", value=0.0)
        
        if st.button("Calculate FCRf"):
            res = -of - div
            st.session_state.fcrf = res
            st.success(f"FCRf = {res:.2f}")

    elif op == "FCU":
        st.caption("Formula: FCU = FCGC + FCID")
        
        fcgc_val = show_dependency('fcgc', 'FCGC')
        fcid_val = show_dependency('fcid', 'FCID')
        
        if st.button("Calculate FCU"):
            res = fcgc_val + fcid_val
            st.session_state.fcu = res
            st.success(f"FCU = {res:.2f}")

    elif op == "FCE":
        st.caption("Formula: FCE = FCU + FCFR - RimborsoCapitale + FCRf - Dividends")
        
        fcu_val = show_dependency('fcu', 'FCU')
        fcfr_val = show_dependency('fcfr', 'FCFR')
        fcrf_val = show_dependency('fcrf', 'FCRf')
        
        col1, col2 = st.columns(2)
        with col1:
            rimb_cap = st.number_input("Capital Repayment", value=0.0)
        with col2:
            div = st.number_input("Dividends Paid", value=0.0)
        
        if st.button("Calculate FCE"):
            res = fcu_val + fcfr_val - rimb_cap + fcrf_val - div
            st.session_state.fce = res
            st.success(f"FCE = {res:.2f}")

    elif op == "Variazione Liquidità":
        st.caption("Formula: ΔCash = FCGC + FCID + FCFR + FCRf")
        
        fcgc_val = show_dependency('fcgc', 'FCGC')
        fcid_val = show_dependency('fcid', 'FCID')
        fcfr_val = show_dependency('fcfr', 'FCFR')
        fcrf_val = show_dependency('fcrf', 'FCRf')
        
        if st.button("Calculate Delta Cash"):
            res = fcgc_val + fcid_val + fcfr_val + fcrf_val
            st.success(f"Total Liquidity Variation = {res:.2f}")
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
        st.warning("⚠️ Richiede k > g (required return > growth rate)")
        
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
            g = retention_ratio * roe
            dividend_1 = None
            
            st.info(f"Retention Ratio = {retention_ratio:.4f} | Growth Rate = {g:.4%}")
        
        if st.button("Calculate Stock Price"):
            try:
                # Verifica condizione Gordon
                if g >= k:
                    st.error(f"Gordon model requires k > g. Got k={k:.2%}, g={g:.2%}")
                else:
                    # Calcola D1 se necessario
                    if dividend_1 is None and earnings_t0 is not None:
                        earnings_t1 = earnings_t0 * (1 + g)
                        dividend_1 = earnings_t1 * payout_ratio
                    
                    if dividend_1 is None:
                        raise ValueError("Dividend cannot be calculated from given inputs")
                    
                    price = dividend_1 / (k - g)
                    st.success(f"Stock Price = {price:.2f}")
                    
                    # VAOC
                    if earnings_t0 is not None and k is not None:
                        no_growth_price = earnings_t0 / k
                        vaoc = price - no_growth_price
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
                if k <= 0:
                    raise ValueError("Required return must be positive")
                price = dividend / k
                st.success(f"Stock Price = {price:.2f}")
            except ValueError as e:
                st.error(str(e))
    
    # VAOC diretto
    st.markdown("---")
    st.subheader("Value of Growth Opportunities (VAOC)")
    
    col1, col2 = st.columns(2)
    with col1:
        price_growth = st.number_input("Stock Price (with growth)", value=50.0, min_value=0.0, key="vaoc_growth")
    with col2:
        price_no_growth = st.number_input("Stock Price (no growth)", value=30.0, min_value=0.0, key="vaoc_no_growth")
    
    if st.button("Calculate VAOC"):
        vaoc = price_growth - price_no_growth
        st.success(f"VAOC = {vaoc:.2f}")
        if vaoc > 0:
            st.info("Positive VAOC = growth creates value")
        elif vaoc < 0:
            st.warning("Negative VAOC = growth destroys value")
        else:
            st.info("VAOC = 0 = growth adds no value")
#MORTGAGE
elif page == "Mortgage":
    st.subheader("Mutuo - Ammortamento")
    st.caption("Confronto tra ammortamento italiano (quota capitale costante) e francese (rata costante)")
    st.info("📌 **Nota:** I calcoli sono basati su rate MENSILI. Inserisci la durata in anni, il sistema convertirà automaticamente in mesi.")
    
    mortgage_type = st.radio("Tipo di ammortamento", ["Italiano (Quota Capitale Costante)", "Francese (Rata Costante)"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        mortgage_debt = st.number_input("Debito iniziale (€)", value=100000.0, min_value=0.0, step=10000.0)
    with col2:
        annual_rate = st.number_input("Tasso di interesse annuo (%)", value=3.0, min_value=0.0, step=0.5) / 100
        monthly_rate = annual_rate / 12  # Tasso mensile
        st.caption(f"Tasso mensile equivalente: {monthly_rate:.4%}")
    with col3:
        years = st.number_input("Durata (anni)", value=20, min_value=1, max_value=50, step=1)
        months = years * 12
        st.caption(f"Durata in mesi: {months}")
    
    st.markdown("---")
    
    if mortgage_type == "Italiano (Quota Capitale Costante)":
        st.markdown("### Piano di Ammortamento Italiano (Quota Capitale Costante)")
        st.caption(f"**Formula:** Quota capitale costante = Debito / {months} mesi")
        st.caption("Ogni mese paghi la stessa quota di capitale + interessi sul residuo")
        
        if st.button("Calcola Ammortamento Italiano"):
            # Quota capitale costante (mensile)
            capital_share_monthly = mortgage_debt / months
            st.session_state.mortgage_capital_share = capital_share_monthly
            
            # Opzione: mostrare solo alcuni anni o tutti i mesi?
            display_mode = st.radio("Visualizzazione", ["Resa annuale (sintesi)", "Mensile (primi 12 mesi)", "Completa (tutti i mesi)"])
            
            # Creazione tabella mensile
            monthly_table = []
            residual_debt = mortgage_debt
            
            for t in range(1, months + 1):
                # Interessi del mese sul debito residuo
                interest_t = residual_debt * monthly_rate
                # Quota capitale (costante, ultimo mese aggiusta arrotondamenti)
                capital_t = capital_share_monthly if t < months else residual_debt
                # Rata totale del mese
                payment_t = capital_t + interest_t
                # Nuovo debito residuo
                residual_debt -= capital_t
                
                monthly_table.append({
                    "Mese": t,
                    "Anno": (t - 1) // 12 + 1,
                    "Residuo Iniziale": round(residual_debt + capital_t, 2),
                    "Quota Capitale": round(capital_t, 2),
                    "Quota Interessi": round(interest_t, 2),
                    "Rata": round(payment_t, 2),
                    "Residuo Finale": round(max(residual_debt, 0), 2)
                })
            
            # RIEPILOGO ANNUALE (sintesi per anno)
            annual_summary = []
            for year in range(1, years + 1):
                year_months = [m for m in monthly_table if m["Anno"] == year]
                annual_summary.append({
                    "Anno": year,
                    "Capitale Pagato": sum(m["Quota Capitale"] for m in year_months),
                    "Interessi Pagati": sum(m["Quota Interessi"] for m in year_months),
                    "Totale Rata Annua": sum(m["Rata"] for m in year_months),
                    "Debito Residuo Fine Anno": year_months[-1]["Residuo Finale"] if year_months else 0
                })
            
            st.session_state.mortgage_amortization_table = monthly_table
            
            # RIEOLOGO GENERALE
            total_interest = sum(m["Quota Interessi"] for m in monthly_table)
            total_paid = mortgage_debt + total_interest
            first_payment = monthly_table[0]["Rata"]
            last_payment = monthly_table[-1]["Rata"]
            
            st.markdown("### 📊 Riepilogo Generale")
            col_a, col_b, col_c, col_d = st.columns(4)
            col_a.metric("Quota Capitale Mensile", f"€{capital_share_monthly:,.2f}")
            col_b.metric("Prima Rata (max interessi)", f"€{first_payment:,.2f}")
            col_c.metric("Ultima Rata (solo capitale)", f"€{last_payment:,.2f}")
            col_d.metric("Totale Interessi", f"€{total_interest:,.2f}")
            st.info(f"💰 **Totale pagato:** €{total_paid:,.2f} (Capitale €{mortgage_debt:,.2f} + Interessi €{total_interest:,.2f})")
            
            # VISUALIZZAZIONE IN BASE ALLA SCELTA
            if display_mode == "Resa annuale (sintesi)":
                st.markdown("### 📅 Riepilogo Annuale")
                st.dataframe(annual_summary, use_container_width=True)
                
                # Grafico dell'andamento annuale
                chart_data = {
                    "Anno": [a["Anno"] for a in annual_summary],
                    "Interessi Pagati": [a["Interessi Pagati"] for a in annual_summary],
                    "Debito Residuo": [a["Debito Residuo Fine Anno"] for a in annual_summary]
                }
                st.line_chart(chart_data, x="Anno", y=["Interessi Pagati", "Debito Residuo"])
                
            elif display_mode == "Mensile (primi 12 mesi)":
                st.markdown("### 📆 Primi 12 mesi (dettaglio mensile)")
                st.dataframe(monthly_table[:12], use_container_width=True)
                
            else:  # Completa
                st.markdown(f"### 📆 Piano completo ({months} mesi)")
                st.warning(f"Mostrando tutti i {months} mesi. Puoi usare la ricerca nella tabella.")
                st.dataframe(monthly_table, use_container_width=True)
            
            # Grafico dell'andamento della rata nel tempo (campione ogni 12 mesi)
            st.markdown("### 📉 Andamento della Rata nel tempo")
            sample_months = monthly_table[::12]  # Una rata ogni 12 mesi
            sample_data = {
                "Mese": [m["Mese"] for m in sample_months],
                "Rata": [m["Rata"] for m in sample_months],
                "Quota Interessi": [m["Quota Interessi"] for m in sample_months],
                "Quota Capitale": [m["Quota Capitale"] for m in sample_months]
            }
            st.line_chart(sample_data, x="Mese", y=["Rata", "Quota Interessi", "Quota Capitale"])
    
    else:  # FRANCESE - RATA COSTANTE MENSILE
        st.markdown("### Piano di Ammortamento Francese (Rata Costante)")
        st.caption(f"**Formula:** Rata mensile costante = Debito × [k(1+k)^{months}] / [(1+k)^{months} - 1]")
        st.caption("Ogni mese paghi la stessa rata, ma cambia la composizione tra interessi e capitale")
        
        if st.button("Calcola Ammortamento Francese"):
            k = monthly_rate
            n = months
            
            # Calcolo rata mensile costante
            if k == 0:
                constant_payment = mortgage_debt / n
            else:
                constant_payment = mortgage_debt * (k * (1 + k) ** n) / ((1 + k) ** n - 1)
            
            st.session_state.mortgage_payment = constant_payment
            
            # Opzione visualizzazione
            display_mode = st.radio("Visualizzazione", ["Resa annuale (sintesi)", "Mensile (primi 12 mesi)", "Completa (tutti i mesi)"])
            
            # Creazione tabella mensile
            monthly_table = []
            residual_debt = mortgage_debt
            
            for t in range(1, months + 1):
                # Interessi sul debito residuo del mese precedente
                interest_t = residual_debt * k
                # Quota capitale = rata costante - interessi
                capital_t = constant_payment - interest_t
                # Gestione ultimo mese (arrotondamenti)
                if t == months:
                    capital_t = residual_debt  # Chiudi esattamente il debito
                    constant_payment = capital_t + interest_t
                
                residual_debt -= capital_t
                
                monthly_table.append({
                    "Mese": t,
                    "Anno": (t - 1) // 12 + 1,
                    "Residuo Iniziale": round(residual_debt + capital_t, 2),
                    "Quota Capitale": round(capital_t, 2),
                    "Quota Interessi": round(interest_t, 2),
                    "Rata": round(constant_payment, 2),
                    "Residuo Finale": round(max(residual_debt, 0), 2)
                })
            
            # RIEPILOGO ANNUALE
            annual_summary = []
            for year in range(1, years + 1):
                year_months = [m for m in monthly_table if m["Anno"] == year]
                annual_summary.append({
                    "Anno": year,
                    "Capitale Pagato": sum(m["Quota Capitale"] for m in year_months),
                    "Interessi Pagati": sum(m["Quota Interessi"] for m in year_months),
                    "Totale Rata Annua": sum(m["Rata"] for m in year_months),
                    "Debito Residuo Fine Anno": year_months[-1]["Residuo Finale"] if year_months else 0
                })
            
            st.session_state.mortgage_amortization_table = monthly_table
            
            # RIEPILOGO GENERALE
            total_interest = sum(m["Quota Interessi"] for m in monthly_table)
            total_paid = mortgage_debt + total_interest
            
            st.markdown("### 📊 Riepilogo Generale")
            col_a, col_b, col_c, col_d = st.columns(4)
            col_a.metric("Rata Mensile Costante", f"€{constant_payment:,.2f}")
            col_b.metric("Prima Rata (max interessi)", f"€{constant_payment:,.2f}")
            col_c.metric("Ultima Rata (min interessi)", f"€{constant_payment:,.2f}")
            col_d.metric("Totale Interessi", f"€{total_interest:,.2f}")
            st.info(f"💰 **Totale pagato:** €{total_paid:,.2f} (Capitale €{mortgage_debt:,.2f} + Interessi €{total_interest:,.2f})")
            
            # VISUALIZZAZIONE
            if display_mode == "Resa annuale (sintesi)":
                st.markdown("### 📅 Riepilogo Annuale")
                st.dataframe(annual_summary, use_container_width=True)
                
                chart_data = {
                    "Anno": [a["Anno"] for a in annual_summary],
                    "Interessi Pagati": [a["Interessi Pagati"] for a in annual_summary],
                    "Debito Residuo": [a["Debito Residuo Fine Anno"] for a in annual_summary]
                }
                st.line_chart(chart_data, x="Anno", y=["Interessi Pagati", "Debito Residuo"])
                
            elif display_mode == "Mensile (primi 12 mesi)":
                st.markdown("### 📆 Primi 12 mesi (dettaglio mensile)")
                st.dataframe(monthly_table[:12], use_container_width=True)
                
                # Grafico della composizione della rata nel primo anno
                import pandas as pd
                df_first_year = pd.DataFrame(monthly_table[:12])
                st.markdown("### Composizione rata - Primo anno")
                st.bar_chart(df_first_year.set_index("Mese")[["Quota Capitale", "Quota Interessi"]])
                
            else:  # Completa
                st.markdown(f"### 📆 Piano completo ({months} mesi)")
                st.warning(f"Mostrando tutti i {months} mesi. Puoi usare la ricerca nella tabella.")
                st.dataframe(monthly_table, use_container_width=True)
            
            # Grafico dell'evoluzione della composizione rata (campione annuale)
            st.markdown("### 📉 Evoluzione della composizione della rata")
            sample_months = monthly_table[::12]  # Una rata ogni 12 mesi
            if sample_months:
                sample_data = {
                    "Anno": [(m["Mese"] - 1) // 12 + 1 for m in sample_months],
                    "Quota Capitale": [m["Quota Capitale"] for m in sample_months],
                    "Quota Interessi": [m["Quota Interessi"] for m in sample_months]
                }
                st.bar_chart(sample_data, x="Anno", y=["Quota Capitale", "Quota Interessi"])
#WACC
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
            # Validazione base
            if equity + debt == 0:
                st.error("La somma di Equity e Debito non può essere zero")
            else:
                wacc = (cost_of_equity * (equity / (equity + debt))) + (cost_of_debt * (1 - tax_rate) * (debt / (equity + debt)))
                st.session_state.wacc = wacc
                st.session_state.cost_of_equity = cost_of_equity
                st.session_state.cost_of_debt = cost_of_debt
                st.session_state.tax_rate = tax_rate
                
                st.markdown("---")
                st.metric("WACC", f"{wacc:.2%}")
                
                # Spiegazione dettagliata
                with st.expander("Vedi calcolo dettagliato"):
                    st.write(f"E/V = {equity:,.0f} / {equity + debt:,.0f} = {equity/(equity+debt):.2%}")
                    st.write(f"D/V = {debt:,.0f} / {equity + debt:,.0f} = {debt/(equity+debt):.2%}")
                    st.write(f"r_e × (E/V) = {cost_of_equity:.2%} × {equity/(equity+debt):.2%} = {cost_of_equity * equity/(equity+debt):.2%}")
                    st.write(f"r_d × (1-t_c) × (D/V) = {cost_of_debt:.2%} × {1-tax_rate:.2%} × {debt/(equity+debt):.2%} = {cost_of_debt * (1-tax_rate) * debt/(equity+debt):.2%}")
        except Exception as e:
            st.error(f"Errore nel calcolo: {e}")

# NPV con FCU/FCE
elif page == "NPV with FCU/FCE":
    st.subheader("NPV - Due Approcci")
    st.caption("NPV con logica del capitale investito (FCU) vs logica dell'azionista (FCE)")
    
    approach = st.radio("Seleziona approccio", ["FCU (Free Cash Flow to Firm)", "FCE (Free Cash Flow to Equity)"])
    
    if approach == "FCU (Free Cash Flow to Firm)":
        st.markdown("### NPV con FCU (WACC come tasso di sconto)")
        
        col1, col2 = st.columns(2)
        with col1:
            # WACC automatico o manuale
            if st.session_state.wacc is not None:
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
                total_pv = 0
                pv_list = []
                
                for t, fcu in enumerate(fcu_list, start=1):
                    fc_net = fcu - cost
                    df = (1 + wacc) ** t
                    pv = fc_net / df
                    pv_list.append(pv)
                    total_pv += pv
                
                npv_fcu = total_pv - i0_fcu
                
                st.session_state.total_pv_fcu = total_pv
                st.session_state.npv_fcu = npv_fcu
                
                st.markdown("---")
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Valore Attuale Totale", f"€{total_pv:,.2f}")
                col_b.metric("Investimento Iniziale", f"€{i0_fcu:,.2f}")
                col_c.metric("NPV", f"€{npv_fcu:,.2f}", 
                             delta="Positivo" if npv_fcu > 0 else "Negativo" if npv_fcu < 0 else "Neutro")
                
                # Tabella dettagliata
                with st.expander("Vedi calcolo dettagliato"):
                    detail_data = []
                    for t, (fcu, pv) in enumerate(zip(fcu_list, pv_list), start=1):
                        detail_data.append({
                            "Periodo": t,
                            "FCU": f"€{fcu:,.2f}",
                            "Costo Fisso": f"€{cost:,.2f}",
                            "FC Netto": f"€{fcu - cost:,.2f}",
                            "DF (1+WACC)^t": f"{(1+wacc)**t:.4f}",
                            "PV": f"€{pv:,.2f}"
                        })
                    st.dataframe(detail_data, use_container_width=True)
                    
            except Exception as e:
                st.error(f"Errore nel calcolo: {e}")
    
    else:  # FCE
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
                total_pv = 0
                pv_list = []
                
                for t, fce in enumerate(fce_list, start=1):
                    fc_net = fce - cost
                    df = (1 + ke) ** t
                    pv = fc_net / df
                    pv_list.append(pv)
                    total_pv += pv
                
                npv_fce = total_pv - equity0
                
                st.session_state.total_pv_fce = total_pv
                st.session_state.npv_fce = npv_fce
                
                st.markdown("---")
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Valore Attuale Totale", f"€{total_pv:,.2f}")
                col_b.metric("Equity Iniziale", f"€{equity0:,.2f}")
                col_c.metric("NPV (FCE)", f"€{npv_fce:,.2f}",
                             delta="Positivo" if npv_fce > 0 else "Negativo" if npv_fce < 0 else "Neutro")
                
                with st.expander("Vedi calcolo dettagliato"):
                    detail_data = []
                    for t, (fce, pv) in enumerate(zip(fce_list, pv_list), start=1):
                        detail_data.append({
                            "Periodo": t,
                            "FCE": f"€{fce:,.2f}",
                            "Costo Fisso": f"€{cost:,.2f}",
                            "FC Netto": f"€{fce - cost:,.2f}",
                            "DF (1+Ke)^t": f"{(1+ke)**t:.4f}",
                            "PV": f"€{pv:,.2f}"
                        })
                    st.dataframe(detail_data, use_container_width=True)
                    
            except Exception as e:
                st.error(f"Errore nel calcolo: {e}")

elif page == "Coming Soon...":
    st.write("Stay tuned for Risk Analysis and Portfolio")
