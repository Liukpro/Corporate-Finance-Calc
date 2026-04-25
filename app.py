import streamlit as st
from formulas import (calc_fccnogc, calc_rol, calc_fcgc, calc_fcid,
                     calc_fcfr, calc_fcrf, calc_var_liq, calc_fcu,
                     calc_fce, calc_npv)

st.title("Corporate Finance Calc")
st.caption("v2.0")

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
    "PV and NPV",
    "Bonds Evaluation",
    "Stock Evaluation",
    "Mortgage amortization: French and Italian",
    "NPV Comparision",
    "Portfolio"
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
        rol_a = st.number_input("EBIT", key="rol_a", value=0.0)
 
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
 
        inv = st.number_input("Investments", key="inv", value=0.0)
        dis = st.number_input("Disinvestments", key="dis", value=0.0)
 
        if st.button("Calculate FCID"):
            res = calc_fcid(fcid=None, inv=inv, dis=dis)
            st.session_state.fcid = res
            st.success(f"FCID = {res}")
 
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
        div      = st.number_input("Dividendi", key="div_fce", value=0.0)
 
        if st.button("Calculate FCE"):
            try:
                res = calc_fce(fce=None, fcu=fcu_v, fcfr=fcfr_v, fcrf=fcrf_v, rimb_cap=rimb_cap, div=div)
                st.success(f"FCE = {res}")
            except Exception as e:
                st.error(str(e))
            
if page == "PV and NPV":
    st.subheader("PV and NPV")
    
