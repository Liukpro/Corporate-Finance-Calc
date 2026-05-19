import pandas as pd
import streamlit as st
import numpy as np
from formulas import (calc_fccnogc, calc_rol, calc_fcgc, calc_fcid,
                      calc_fcfr, calc_fcrf, calc_var_liq, calc_fcu,
                      calc_fce, calc_npv, calc_va_bond_zero, calc_yield_to_mat_zero, calc_ros, 
                      calc_roi, calc_roe, calc_va_ced_bond, calc_stock_price, calc_vaoc, 
                      build_italian_table, build_french_table, calc_wacc, calc_npv_fcu, calc_npv_fce)
from analisi_prospettica_area_caratteristica import (calc_mo_netto, calc_ammortamenti, calc_shield_ammortamenti,
                                                     calc_fccnogc2, calc_var_ccno, calc_fcgc2)


# Configurazione Pagina
st.set_page_config(page_title="Corporate Finance Calc", layout="wide")

st.title("Corporate Finance Calc")
st.caption("v_alpha_3.1, #added metrics for Analisi Prospettica, # english-italian mix vocabs- to be updated")

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
    "Cash Flow Analysis, Ex-Post",
    "Cash Flow Analysis, Ex-Ante",
    "WACC",
    "NPV with FCU/FCE",
    "Bond Evaluation",
    "Stock Evaluation",
    "Ratio Analysis",
    "Mortgage",
    "Coming Soon..."
])

#CASH FLOW ANALYSIS
if page == "Cash Flow Analysis, Ex-Post":
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

#Analisi Prospettica
elif page == "Cash Flow Analysis, Ex-Ante":
    st.subheader("Analisi Prospettica — Area Caratteristica")

    vita_progetto = st.number_input("Vita del progetto (periodi)", min_value=1, step=1, value=3, key="ap_vita")
    tc = st.number_input("Aliquota fiscale (tc)", min_value=0.0, max_value=1.0, value=0.35, format="%.2f", key="ap_tc")
    n = int(vita_progetto)

    st.markdown("**Ricavi e costi operativi per periodo:**")
    ricavi_operativi = []
    costi_operativi = []
    ccno = []

    for t in range(n):
        st.markdown(f"*Periodo {t+1}*")
        col1, col2, col3 = st.columns(3)
        with col1:
            ricavi_operativi.append(st.number_input(f"Ricavi operativi", key=f"ap_ric_{t}", value=0.0))
        with col2:
            costi_operativi.append(st.number_input(f"Costi operativi", key=f"ap_cost_{t}", value=0.0))
        with col3:
            ccno.append(st.number_input(f"CCNO", key=f"ap_ccno_{t}", value=0.0))

    st.markdown("**Esborsi per investimenti (ammortizzabili):**")
    n_esborsi = st.number_input("Numero di esborsi", min_value=1, step=1, value=1, key="ap_n_esborsi")
    esborsi = []
    anni_list = []

    for i in range(int(n_esborsi)):
        col1, col2 = st.columns(2)
        with col1:
            esborsi.append(st.number_input(f"Esborso {i+1}", key=f"ap_esborso_{i}", value=0.0))
        with col2:
            anni_list.append(int(st.number_input(f"Anni ammortamento esborso {i+1}", min_value=1, step=1, value=n, key=f"ap_anni_{i}")))

    if st.button("Calcola"):
        try:
          mo_netto = calc_mo_netto(ricavi_operativi, costi_operativi, tc)
          ammortamenti = calc_ammortamenti(esborsi, anni_list, n)
          shield = calc_shield_ammortamenti(ammortamenti, tc)
          fccnogc = calc_fccnogc2(mo_netto, shield)
          delta_ccno = calc_var_ccno(ccno)
          fcgc = calc_fcgc2(fccnogc, delta_ccno)

          st.markdown("---")
          st.markdown("**Risultati per periodo:**")

          header = ["Metrica"] + [f"t={t+1}" for t in range(n)]
          rows = [
              ["MO Netto"]        + [f"{v:,.2f}" for v in mo_netto],
              ["Ammortamenti"]    + [f"{v:,.2f}" for v in ammortamenti],
              ["Tax Shield Amm."] + [f"{v:,.2f}" for v in shield],
              ["FCCNOGC"]         + [f"{v:,.2f}" for v in fccnogc],
              ["Δ CCNO"]          + [f"{v:,.2f}" for v in delta_ccno],
              ["FCGC"]            + [f"{v:,.2f}" for v in fcgc],
          ]

          df = pd.DataFrame(rows, columns=header)
          st.dataframe(df, use_container_width=True)

        except Exception as e:
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
    
    approach = st.radio("Seleziona approccio", ["FCU (Cash Flow Unlevered)", "FCE (Cash Flow Equity)"])
    
    if approach == "FCU (Cash Flow Unlevered)":
        st.markdown("### NPV con FCU (WACC come tasso di sconto)")
        t_fcu_list = []
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.get('wacc') is not None:
                st.info(f"WACC calcolato in precedenza: {st.session_state.wacc:.2%}")
                use_saved_wacc = st.checkbox("Usa WACC salvato", value=True)
                if use_saved_wacc:
                    wacc = st.session_state.wacc
                else:
                    wacc = st.number_input("WACC (%)", value=8.0, min_value=0.0, step=0.001) / 100
            else:
                wacc = st.number_input("WACC (%)", value=8.0, min_value=0.0, step=0.001) / 100
            
            i0_fcu = st.number_input("Investimento Iniziale I₀ (€)", value=100000.0, min_value=0.0, step=1.0)
            cost = st.number_input("Costo fisso per periodo (€)", value=0.0)
        
        with col2:
            t_fcu = st.number_input("Numero di periodi", min_value=1, step=1, value=5)
        
        st.markdown("**Flussi di Cassa (FCU) per periodo**")
        fcu_list = []
        npv_fcu_values = []
        for i in range(t_fcu):
            fcu_list.append(st.number_input(f"FCU periodo {i+1}", key=f"fcu_{i}", value=10000.0, step=1.0))
        
        if st.button("Calcola NPV (FCU)"):
            try:
                npv = calc_npv_fcu(fcu_list, wacc, i0_fcu, cost)
                st.session_state.npv_fcu = npv
                
                st.markdown("---")
                st.metric("NPV", f"€{npv:,.2f}", 
                          delta="Positivo" if npv > 0 else "Negativo" if npv < 0 else "Neutro")

                wacc_values = np.arange(0, 1, 0.005)
                npv_fcu_values = []
                for wacc_val in wacc_values:
                  npv_at_wacc = calc_npv_fcu(fcu_list, wacc_val, i0_fcu, cost)
                  npv_fcu_values.append(npv_at_wacc)

                chart_npv_fcu = pd.DataFrame({"WACC": wacc_values, "NPV": npv_fcu_values})
                st.line_chart(chart_npv_fcu, x="WACC", y="NPV")
                zero_crossing = wacc_values[np.where(np.array(npv_fcu_values) <= 0)[0][0]] if any(np.array(npv_fcu_values) <= 0) else None
                if zero_crossing:
                  st.caption(f"NPV = 0 con WACC ≈ {zero_crossing:.2%}")
              
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
        t_fce_list = []
        col1, col2 = st.columns(2)
        with col1:
            ke = st.number_input("Ke (Costo dell'Equity/Required Return) (%)", value=10.0, min_value=0.0, step=0.5) / 100
            equity0 = st.number_input("Equity Iniziale (€)", value=50000.0, min_value=0.0, step=10000.0)
            cost = st.number_input("Costo fisso per periodo (€)", value=0.0)
        
        with col2:
            t_fce = st.number_input("Numero di periodi", min_value=1, step=1, value=5)
        
        st.markdown("**Flussi di Cassa (FCE) per periodo**")
        fce_list = []
        npv_fce_values = []
        for i in range(t_fce):
            fce_list.append(st.number_input(f"FCE periodo {i+1}", key=f"fce_{i}", value=8000.0, step=1000.0))
        
        if st.button("Calcola NPV (FCE)"):
            try:
                npv = calc_npv_fce(fce_list, ke, equity0, cost)
                st.session_state.npv_fce = npv
                
                st.markdown("---")
                st.metric("NPV (FCE)", f"€{npv:,.2f}", delta="Positivo" if npv > 0 else "Negativo" if npv < 0 else "Neutro")
                
                ke_values = np.arange(0, 1, 0.005)
                npv_fce_values = []
                for ke_val in ke_values:
                  npv_at_ke = calc_npv_fce(fce_list, ke_val, equity0, cost)
                  npv_fce_values.append(npv_at_ke)

                chart_npv_fce = pd.DataFrame({"Ke": ke_values, "NPV": npv_fce_values})
                st.line_chart(chart_npv_fce, x="Ke", y="NPV")

                zero_crossing = ke_values[np.where(np.array(npv_fce_values) <= 0)[0][0]] if any(np.array(npv_fce_values) <= 0) else None
                if zero_crossing:
                  st.caption(f"NPV = 0 con Ke ≈ {zero_crossing:.2%}")
              
                if npv > 0:
                    st.info("Il progetto crea valore per l'azionista")
                elif npv < 0:
                    st.warning("Il progetto distrugge valore per l'azionista")
                else:
                    st.info("NPV = 0, è indifferente")
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

    model = st.selectbox("Valuation Model", ["gordon", "no_growth"])

    if model == "gordon":
        st.markdown("### Gordon Growth Model")
        st.warning("Constraint: k > g")

        calc_method = st.radio(
            "Input Method",
            ["Direct (D₁, k, g)", "From Earnings (E₀, b, ROE, k)"]
        )

        if calc_method == "Direct (D₁, k, g)":
            col1, col2, col3 = st.columns(3)

            with col1:
                dividend_1 = st.number_input("Dividend D₁", value=2.0, min_value=0.0)

            with col2:
                k = st.number_input("Required Return (k)", value=0.10, format="%.4f", min_value=0.0)

            with col3:
                g = st.number_input("Growth Rate (g)", value=0.05, format="%.4f", min_value=0.0)

            earnings_t0 = None
            b = None
            retention_ratio = None
            roe = None

        else:
            col1, col2 = st.columns(2)

            with col1:
                earnings_t0 = st.number_input("Earnings (E₀)", value=5.0, min_value=0.0)
                b = st.number_input("Retention Ratio (b)", value=0.40, format="%.4f", min_value=0.0, max_value=1.0)

            with col2:
                k = st.number_input("Required Return (k)", value=0.10, format="%.4f", min_value=0.0)
                roe = st.number_input("ROE", value=0.15, format="%.4f", min_value=0.0)

            retention_ratio = None   
            g = None                
            dividend_1 = None      

            st.info(f"Payout Ratio = {1 - b:.4f}")


        if st.button("Calculate Stock Price"):
            try:
                price = calc_stock_price(
                    stock_price=None,
                    k=k,
                    g=g,
                    b=b,
                    dividend_1=dividend_1,
                    earnings_t0=earnings_t0,
                    retention_ratio=retention_ratio,
                    roe=roe,
                    model="gordon"
                )

                st.success(f"Stock Price = {price:.2f}")

                # VAOC
                no_growth_price = calc_stock_price(
                    stock_price=None,
                    k=k,
                    dividend_1=earnings_t0 if earnings_t0 is not None else dividend_1,
                    model="no_growth"
                )

            except ValueError as e:
                st.error(str(e))


    else:
        st.markdown("### No Growth Model")

        col1, col2 = st.columns(2)

        with col1:
            dividend_1 = st.number_input("Dividend (D)", value=2.0, min_value=0.0)

        with col2:
            k = st.number_input("Required Return (k)", value=0.10, format="%.4f", min_value=0.0)

        if st.button("Calculate Stock Price"):
            try:
                price = calc_stock_price(
                    stock_price=None,
                    k=k,
                    dividend_1=dividend_1,
                    model="no_growth"
                )

                st.success(f"Stock Price = {price:.2f}")

            except ValueError as e:
                st.error(str(e))


    st.markdown("---")
    st.subheader("Value of Growth Opportunities (VAOC)")

    col1, col2 = st.columns(2)

    with col1:
        price_growth = st.number_input("Growth Price", value=50.0, min_value=0.0, key="vaoc_g")

    with col2:
        price_no_growth = st.number_input("No-Growth Price", value=30.0, min_value=0.0, key="vaoc_ng")

    if st.button("Calculate VAOC"):
        try:
            vaoc = calc_vaoc(price_growth, price_no_growth)
            st.success(f"VAOC = {vaoc:.2f}")

        except ValueError as e:
            st.error(str(e))
          
elif page == "Mortgage":
    st.subheader("Mutuo - Ammortamento")
    st.caption("Confronto tra ammortamento italiano (quota capitale costante) e francese (rata costante)")
    st.info("**Nota:** Per ora i calcoli per l'ammortamento italiano sono disponibili solo con resa annuale")
    
    mortgage_type = st.radio("Tipo di ammortamento", ["Italiano (Quota Capitale Costante)", "Francese (Rata Costante)"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        mortgage_debt = st.number_input("Debito iniziale (€)", value=100000.0, min_value=0.0, step=10000.0, key="mortgage_debt")
    with col2:
        annual_rate = st.number_input("Tasso di interesse annuo (%)", value=3.0, min_value=0.0, step=0.5, key="annual_rate") / 100
        monthly_rate = annual_rate / 12
        st.caption(f"Tasso mensile equivalente: {monthly_rate:.4%}")
    with col3:
        years = st.number_input("Anni", value=20, min_value=1, max_value= 10000, step=1, key="years")
        months = years * 12
        st.caption(f"Durata in mesi: {months}")
    
    st.markdown("---")
    
    # Display mode fuori dal bottone (con key per mantenere lo stato)
    display_mode = st.radio(
        "Visualizzazione", 
        ["Resa annuale (sintesi)", "Mensile (primi 12 mesi)", "Completa (tutti i mesi)"], #aggiungere bimestrale, trimestrale, quzadrimestrale e semestrale
        key="mortgage_display_mode"
    )
  #modificare in base ai display mode disponibili
    if mortgage_type == "Italiano (Quota Capitale Costante)":
        st.markdown("### Piano di Ammortamento Italiano (Annuale)")

        current_params = (mortgage_debt, annual_rate, years)

        if "italian_params" not in st.session_state or st.session_state["italian_params"] != current_params:
            st.session_state.pop("italian_table", None)
            st.session_state["italian_params"] = current_params

        if st.button("Calcola Ammortamento Italiano", key="btn_italian"):
            n = years
          #aggiungere if not annual select st.button periodizzazione ammortamento
            k = annual_rate

            capital_annual = mortgage_debt / n

            annual_table = []

            for y in range(1, n + 1):

                residual_prev = mortgage_debt - (y - 1) * capital_annual

                interest_year = residual_prev * k

                payment_year = capital_annual + interest_year

                residual = mortgage_debt - y * capital_annual

                annual_table.append({
                    "Anno": y,
                    "Capitale Pagato": capital_annual,
                    "Interessi Pagati": interest_year,
                    "Rata Annua Totale": payment_year,
                    "Debito Residuo": residual
                })

            st.session_state["italian_table"] = annual_table

        if "italian_table" in st.session_state:
            table = st.session_state["italian_table"]

            total_interest = sum(r["Interessi Pagati"] for r in table)

            col_a, col_b, col_c, col_d = st.columns(4)
            col_a.metric("Quota Capitale Annuo", f"€{table[0]['Capitale Pagato']:,.2f}")
            col_b.metric("Interessi Anno 1", f"€{table[0]['Interessi Pagati']:,.2f}")
            col_c.metric("Interessi Anno Ultimo", f"€{table[-1]['Interessi Pagati']:,.2f}")
            col_d.metric("Totale Interessi", f"€{total_interest:,.2f}")

            st.info(f"**Totale pagato:** €{mortgage_debt + total_interest:,.2f}")

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




elif page == "Coming Soon...":
    st.write("Stay tuned for Risk Analysis and Portfolio")
