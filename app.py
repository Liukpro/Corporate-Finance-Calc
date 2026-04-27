import streamlit as st
from formulas import (calc_fccnogc, calc_rol, calc_fcgc, calc_fcid,
                     calc_fcfr, calc_fcrf, calc_var_liq, calc_fcu,
                     calc_fce, calc_npv)

st.title("Corporate Finance Calc")
st.caption("v2.0")
st.caption("""
**License:** Apache 2.0  
**Source code:** https://github.com/Liukpro/Corporate-Finance-Calc
""")
for key in ['fccnogc', 'rol', 'fcgc', 'fcid', 'fcfr', 'fcrf', 'fcu', 'pat_net_list', 'of_list']:
    if key not in st.session_state:
        st.session_state[key] = None
      
if st.sidebar.button("Reset Session"):
    for key in st.session_state:
        st.session_state[key] = None
    st.rerun()
  
st.sidebar.title("Tools")
page = st.sidebar.radio("Select one", [
    "Cash Flow",
    "NPV",
    "Bonds Evaluation -coming soon",
    "Stock Evaluation -coming soon",
    "Mortgage amortisation: French and Italian -coming soon",
    "NPV Comparision -coming soon",
    "Portfolio -coming soon"
])

if page == "Cash Flow":
    st.subheader("Cash Flow")

    op = st.selectbox("Which cash flow you need to calculate?", ["FCCNOGC", "RO-L", "FCGC", "FCID",
                                                                 "FCFR", "FCRf", "Variazione Liquidità",
                                                                 "FCU", "FCE"])
    
    if op == "FCCNOGC":
        st.markdown("Insert here its components")
 
        ric = st.number_input("Operating Revenue", key="ric", value=0.0)
        cost = st.number_input("Operating Costs", key="cost", value=0.0)
        imp = st.number_input("Taxes", key="imp", value=0.0)
        ammort = st.number_input("Amortisation", key="ammort", value=0.0)
        mol = st.number_input("Gross Operating Margin", key="mol", value=0.0)
        rol_a = st.number_input("RO-L", key="rol_a", value=0.0)
 
        if st.button("Calculate FCCNOGC"):
            try:
                res = calc_fccnogc(
                    fccnogc=None,
                    ric_op_mon=ric, cost_op_mon=cost,
                    imp=imp, ammort=ammort, mol=mol, rol=rol_a)
                st.session_state.fccnogc = res
                st.success(f"FCCNOGC = {res}")
            except ValueError as e:
                st.error(str(e))
 
    elif op == "RO-L":
        st.markdown("Insert here its components")
 
        ric = st.number_input("Operating Revenue", key="ric_rol", value=0.0)
        cost = st.number_input("Operating Costs", key="cost_rol", value=0.0)
        ammort = st.number_input("Amortisation", key="ammort_rol", value=0.0)
        mol = st.number_input("Gross Operating Margin", key="mol_rol", value=0.0)
 
        if st.button("Calculate RO-L"):
            try:
                res = calc_rol(
                    rol=None,
                    ric_op_mon=ric, cost_op_mon=cost,
                    ammort=ammort, mol=mol)
                st.session_state.rol = res
                st.success(f"RO-L = {res}")
            except ValueError as e:
                st.error(str(e))
 
    elif op == "FCGC":
        st.markdown("Insert here its components")
 
        # FCCNOGC: da session state oppure inserito diretto, stesso schema per le prossime dipendenze
        if st.session_state.fccnogc is not None:
            st.info(f"FCCNOGC from previous calculation: {st.session_state.fccnogc}")
            fccnogc_v = st.session_state.fccnogc
        else:
            st.warning("FCCNOGC not calculated yet.")
            use_direct_fccnogc = st.checkbox("Insert FCCNOGC directly", key="use_direct_fccnogc")
            fccnogc_v = st.number_input("FCCNOGC", key="fccnogc_direct", value=0.0) if use_direct_fccnogc else 0.0
 
        ccno = st.number_input("Variazione CCNO", key="ccno", value=0.0)
 
        if st.button("Calculate FCGC"):
            res = calc_fcgc(fcgc=None, fccnogc=fccnogc_v, ccno=ccno)
            st.session_state.fcgc = res
            st.success(f"FCGC = {res}")
 
    elif op == "FCID":
        st.markdown("Insert here its components")
        use_direct = st.checkbox("Insert FCID directly", key="use_direct_fcid_main")
        fcid_a = st.number_input("FCID value:", key="fcid_a", value=0.0) if use_direct else None
        
        st.markdown("**Method 1 — via VNC**")
        val_sto = st.number_input("Historical value (val. storico)", key="val_sto", value=0.0)
        ammo_ti = st.number_input("Annual amortisation quota", key="ammo_ti", value=0.0)
        n_ammo = st.number_input("Number of amortisation periods", key="n_ammo", value=0, step=1)
        plus = st.number_input("Capital gain (plusvalenza)", key="plus", value=0.0)
        minus = st.number_input("Capital loss (minusvalenza)", key="minus", value=0.0)
        
        st.markdown("**Method 2 — direct disinvestment value**")
        dis = st.number_input("Disinvestment (dis)", key="dis", value=0.0)
        
        st.markdown("**Investment**")
        inv = st.number_input("Direct investment value (if known)", key="inv", value=0.0)
        st.markdown("*Or insert acquisitions separately:*")
        acqui_1 = st.number_input("Acquisition 1", key="acqui_1", value=0.0)
        acqui_2 = st.number_input("Acquisition 2", key="acqui_2", value=0.0)

        if st.button("Calculate FCID"):
          res = calc_fcid(fcid = fcid_a,
                          inv = inv,
                          dis = dis,
                          vnc = None,
                          val_sto = val_sto,
                          plus = plus,
                          minus = minus,
                          ammo_ti = ammo_ti,
                          n_ammo = int(n_ammo),
                          acqui_1 = acqui_1,
                          acqui_2 = acqui_2
                         )
          st.session_state.fcid = res
          st.success(f"FCID = {res:.2f}")
 
    elif op == "FCFR":
        st.markdown("Insert here its components")
 
        rimb_cap = st.number_input("Rimborso quota capitale", key="rimb_cap", value=0.0)
        pat_net = st.number_input("Patrimonio netto", key="pat_net", value=0.0)
        deb_f = st.number_input("Debito finanziario", key="deb_f", value=0.0)
 
        if st.button("Calculate FCFR"):
            res = calc_fcfr(fcfr=None, rimb_cap=rimb_cap, pat_net=pat_net, deb_f=deb_f)
            st.session_state.fcfr = res
            st.success(f"FCFR = {res}")
 
    elif op == "FCRf":
        st.markdown("Insert here its components")
 
        of_v = st.number_input("Oneri finanziari", key="of_v", value=0.0)
        div = st.number_input("Dividendi", key="div", value=0.0)
 
        if st.button("Calculate FCRf"):
            res = calc_fcrf(fcrf=None, of=of_v, div=div)
            st.session_state.fcrf = res
            st.success(f"FCRf = {res}")
 
    elif op == "FCU":
        st.markdown("Insert here its components")
 
        # FCGC
        if st.session_state.fcgc is not None:
            st.info(f"FCGC from previous calculation: {st.session_state.fcgc}")
            fcgc_v = st.session_state.fcgc
        else:
            st.warning("FCGC not calculated yet.")
            use_direct_fcgc = st.checkbox("Insert FCGC directly", key="use_direct_fcgc")
            fcgc_v = st.number_input("FCGC", key="fcgc_direct", value=0.0) if use_direct_fcgc else 0.0
 
        
        if st.session_state.fcid is not None:
            st.info(f"FCID from previous calculation: {st.session_state.fcid}")
            fcid_v = st.session_state.fcid
        else:
            st.warning("FCID not calculated yet.")
            use_direct_fcid = st.checkbox("Insert FCID directly", key="use_direct_fcid")
            fcid_v = st.number_input("FCID", key="fcid_direct", value=0.0) if use_direct_fcid else 0.0
 
        if st.button("Calculate FCU"):
            res = calc_fcu(fcu=None, fcgc=fcgc_v, fcid=fcid_v)
            st.session_state.fcu = res
            st.success(f"FCU = {res}")
 
    elif op == "Variazione Liquidità":
        st.markdown("Insert here its components")
 
        
        if st.session_state.fcgc is not None:
            st.info(f"FCGC from previous calculation: {st.session_state.fcgc}")
            fcgc_v = st.session_state.fcgc
        else:
            st.warning("FCGC not calculated yet.")
            use_direct_fcgc = st.checkbox("Insert FCGC directly", key="use_direct_fcgc_vl")
            fcgc_v = st.number_input("FCGC", key="fcgc_direct_vl", value=0.0) if use_direct_fcgc else 0.0
 
        
        if st.session_state.fcid is not None:
            st.info(f"FCID from previous calculation: {st.session_state.fcid}")
            fcid_v = st.session_state.fcid
        else:
            st.warning("FCID not calculated yet.")
            use_direct_fcid = st.checkbox("Insert FCID directly", key="use_direct_fcid_vl")
            fcid_v = st.number_input("FCID", key="fcid_direct_vl", value=0.0) if use_direct_fcid else 0.0
 
        
        if st.session_state.fcfr is not None:
            st.info(f"FCFR from previous calculation: {st.session_state.fcfr}")
            fcfr_v = st.session_state.fcfr
        else:
            st.warning("FCFR not calculated yet.")
            use_direct_fcfr = st.checkbox("Insert FCFR directly", key="use_direct_fcfr_vl")
            fcfr_v = st.number_input("FCFR", key="fcfr_direct_vl", value=0.0) if use_direct_fcfr else 0.0
 
        
        if st.session_state.fcrf is not None:
            st.info(f"FCRf from previous calculation: {st.session_state.fcrf}")
            fcrf_v = st.session_state.fcrf
        else:
            st.warning("FCRf not calculated yet.")
            use_direct_fcrf = st.checkbox("Insert FCRf directly", key="use_direct_fcrf_vl")
            fcrf_v = st.number_input("FCRf", key="fcrf_direct_vl", value=0.0) if use_direct_fcrf else 0.0
 
        if st.button("Calculate Variazione Liquidità"):
            try:
                res = calc_var_liq(var_liq=None, fcgc=fcgc_v, fcid=fcid_v, fcfr=fcfr_v, fcrf=fcrf_v)
                st.success(f"Variazione Liquidità = {res}")
            except Exception as e:
                st.error(str(e))
 
    elif op == "FCE":
        st.markdown("Insert here its components")
 
        
        if st.session_state.fcu is not None:
            st.info(f"FCU from previous calculation: {st.session_state.fcu}")
            fcu_v = st.session_state.fcu
        else:
            st.warning("FCU not calculated yet.")
            use_direct_fcu = st.checkbox("Insert FCU directly", key="use_direct_fcu")
            fcu_v = st.number_input("FCU", key="fcu_direct", value=0.0) if use_direct_fcu else 0.0
 
        
        if st.session_state.fcfr is not None:
            st.info(f"FCFR from previous calculation: {st.session_state.fcfr}")
            fcfr_v = st.session_state.fcfr
        else:
            st.warning("FCFR not calculated yet.")
            use_direct_fcfr = st.checkbox("Insert FCFR directly", key="use_direct_fcfr_fce")
            fcfr_v = st.number_input("FCFR", key="fcfr_direct_fce", value=0.0) if use_direct_fcfr else 0.0
 
        
        if st.session_state.fcrf is not None:
            st.info(f"FCRf from previous calculation: {st.session_state.fcrf}")
            fcrf_v = st.session_state.fcrf
        else:
            st.warning("FCRf not calculated yet.")
            use_direct_fcrf = st.checkbox("Insert FCRf directly", key="use_direct_fcrf_fce")
            fcrf_v = st.number_input("FCRf", key="fcrf_direct_fce", value=0.0) if use_direct_fcrf else 0.0
 
        rimb_cap = st.number_input("Rimborso quota capitale", key="rimb_cap_fce", value=0.0)
        div = st.number_input("Dividendi", key="div_fce", value=0.0)
 
        if st.button("Calculate FCE"):
            try:
                res = calc_fce(fce=None, fcu=fcu_v, fcfr=fcfr_v, fcrf=fcrf_v, rimb_cap=rimb_cap, div=div)
                st.success(f"FCE = {res}")
            except Exception as e:
                st.error(str(e))
            
if page == "NPV":
    st.subheader("Net Present Value (NPV)")

    k = st.number_input("Discount rate k", key="k", value=0.0, format="%.4f")
    i_0 = st.number_input("Initial investment I₀", key="i_0", value=0.0)
    cost = st.number_input("Fixed cost per period", key="cost", value=0.0)
    n = st.number_input("Number of periods", key="n", min_value=1, step=1, value=1)

    st.markdown("**Cash flows and time for each period:**")

    fc_list = []
    t_list = []

    for i in range(int(n)):
        col1, col2 = st.columns(2)
        with col1:
            fc_list.append(st.number_input(f"Cash flow period {i+1}", key=f"fc_{i}", value=0.0))
        with col2:
            t_list.append(st.number_input(f"Time period {i+1}", key=f"t_{i}", min_value=0, step=1, value=i+1))

    use_direct = st.checkbox("Insert NPV directly", key="use_direct_npv")
    npv_a = st.number_input("NPV value:", key="npv_a", value=0.0) if use_direct else None

    if st.button("Calculate NPV"):
        res = calc_npv(npv=npv_a, fc=fc_list, k=k, i_0=i_0, t=t_list, cost=cost)
        st.metric(label="NPV", value=f"{res:.2f}")
        if res > 0:
            st.info("NPV > 0: the project creates value.")
        elif res < 0:
            st.info("NPV < 0: the project destroys value.")
        else:
            st.info("NPV = 0: the project is neutral.")
