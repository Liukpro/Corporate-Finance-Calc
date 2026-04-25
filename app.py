import streamlit as st
from formulas import (calc_fccnogc, calc_rol, calc_fcgc, calc_fcid,
                     calc_fcfr, calc_fcrf, calc_var_liq, calc_fcu,
                     calc_fce, calc_npv)

st.title("Corporate Finance Calc")
st.caption("v2.0")

# Inizializza session state
for key in ['fccnogc', 'rol', 'fcgc', 'fcid', 'fcfr', 'fcrf', 'fcu', 'pat_net_list', 'of_list']:
    if key not in st.session_state:
        st.session_state[key] = None

st.sidebar.title("Tools")
page = st.sidebar.radio("Select one", [
    "Cash Flow",
    "PV and NPV",
    "Bonds Evaluation",
    "Stock Evaluation",
    "Depreciation: French and Italian",
    "NPV Comparision",
    "Portfolio"
])

if page == "Cash Flow":
    st.subheader("Cash Flow")

    op = st.selectbox("Which cash flow you need to calculate?", ["FCCNOGC", "RO-L", "FCGC", "FCID",
                                                                 "FCFR", "FCRf", "Variazione Liquidità",
                                                                 "FCU", "FCE"])
    
    if op == "FCCNOGC":
        st.markdown("Insert here direct values or its components")
        use_direct = st.checkbox("Insert direct FCCNOGC value", key="use_direct_fccnogc")
        
        fccnogc_a = None
        if use_direct:
            fccnogc_a = st.number_input("FCCNOGC value:", key="fccnogc_a", value=0.0)
        
        ric = st.number_input("Ricavi operativi monetari", key="ric", value=0.0)
        cost = st.number_input("Costi operativi monetari", key="cost", value=0.0)
        imp = st.number_input("Imposte", key="imp", value=0.0)
        ammort = st.number_input("Amortisation", key="ammort", value=0.0)
        mol = st.number_input("Gross Operating Margin", key="mol", value=0.0)
        rol_a = st.number_input("EBID", key="rol_a", value=0.0)

        if st.button("Calculate FCCNOGC"):
            try:
                res = calc_fccnogc(
                    fccnogc=fccnogc_a,
                    ric_op_mon=ric, cost_op_mon=cost,
                    imp=imp, ammort=ammort, mol=mol, rol=rol_a)
                st.session_state.fccnogc = res
                st.success(f"FCCNOGC = {res}")
            except ValueError as e:
                st.error(str(e))

    elif op == "RO-L":
        st.markdown("Insert here direct values or its components: ")
        use_direct = st.checkbox("Insert direct RO-L value", key="use_direct_rol")
        
        rol_a = None
        if use_direct:
            rol_a = st.number_input("RO-L value:", key="rol_a", value=0.0)
        
        ric = st.number_input("Operating Revenue: ", key="ric_rol", value=0.0)
        cost = st.number_input("Operating Costs: ", key="cost_rol", value=0.0)
        ammort = st.number_input("Amortisation: ", key="ammort_rol", value=0.0)
        mol = st.number_input("Gross Operating Margin: ", key="mol_rol", value=0.0)

        if st.button("Calculate RO-L"):
            try:
                res = calc_rol(
                    rol=rol_a,
                    ric_op_mon=ric, cost_op_mon=cost,
                    ammort=ammort, mol=mol)
                st.session_state.rol = res
                st.success(f"EBID = {res}")
            except ValueError as e:
                st.error(str(e))

    elif op == "FCGC":
        st.markdown("Insert here direct values or its components")
        use_direct = st.checkbox("Insert direct FCGC value", key="use_direct_fcgc")
        
        fcgc_a = None
        if use_direct:
            fcgc_a = st.number_input("FCGC value:", key="fcgc_a", value=0.0)
        
        ccno = st.number_input("Variazione CCNO", key="ccno", value=0.0)
        
        # Mostra FCCNOGC se disponibile
        if st.session_state.fccnogc is not None:
            st.info(f"FCCNOGC from previous calculation: {st.session_state.fccnogc}")
        else:
            st.warning("FCCNOGC not calculated yet. Please calculate FCCNOGC first or enter FCGC directly.")

        if st.button("Calculate FCGC"):
            try:
                res = calc_fcgc(
                    fcgc=fcgc_a,
                    fccnogc=st.session_state.fccnogc if st.session_state.fccnogc is not None else 0,
                    ccno=ccno)
                st.session_state.fcgc = res
                st.success(f"FCGC = {res}")
            except ValueError as e:
                st.error(str(e))

    elif op == "FCID":
        st.markdown("Insert here direct values or its components")
        use_direct = st.checkbox("Insert direct FCID value", key="use_direct_fcid")
        
        fcid_a = None
        if use_direct:
            fcid_a = st.number_input("FCID value:", key="fcid_a", value=0.0)
        
        inv = st.number_input("Investments", key="inv", value=0.0)
        dis = st.number_input("Disinvestments", key="dis", value=0.0)

        if st.button("Calculate FCID"):
            try:
                res = calc_fcid(
                    fcid=fcid_a,
                    inv=inv, dis=dis)
                st.session_state.fcid = res
                st.success(f"FCID = {res}")
            except ValueError as e:
                st.error(str(e))
                
    elif op == "FCFR":
        st.markdown("Insert here direct values or its components")
        use_direct = st.checkbox("Insert direct FCFR value", key="use_direct_fcfr")

        fcfr_a = None
        if use_direct:
            fcfr_a = st.number_input("FCFR value:", key="fcfr_a", value=0.0)

        rimb_cap = st.number_input("Rimborso quota capitale", key="rimb_cap", value=0.0)
        pat_net  = st.number_input("Patrimonio netto", key="pat_net", value=0.0)
        deb_f    = st.number_input("Debito finanziario", key="deb_f", value=0.0)

        if st.button("Calculate FCFR"):
            res = calc_fcfr(
                fcfr=fcfr_a,
                rimb_cap=rimb_cap, pat_net=pat_net, deb_f=deb_f)
            st.session_state.fcfr = res
            st.success(f"FCFR = {res}")

    elif op == "FCRf":
        st.markdown("Insert here direct values or its components")

        use_direct = st.checkbox("Insert direct FCRf value", key="use_direct_fcrf")

        fcrf_a = None
        if use_direct:
            fcrf_a = st.number_input("FCRf value:", key="fcrf_a", value=0.0)

        of_v = st.number_input("Oneri finanziari", key="of_v", value=0.0)
        div  = st.number_input("Dividendi", key="div", value=0.0)

        if st.button("Calculate FCRf"):
            res = calc_fcrf(
                fcrf=fcrf_a,
                of=of_v, div=div)
            st.session_state.fcrf = res
            st.success(f"FCRf = {res}")

    op2 = st.selectbox("Desideri calcolare altro?", ["Variazione Liquidità", "FCU", "FCE"])

    if op2 == "Variazione Liquidità":
        st.markdown("Insert here direct values or its components")

        use_direct = st.checkbox("Insert direct Variazione Liquidità value", key="use_direct_varliq")

        var_liq_a = None
        if use_direct:
            var_liq_a = st.number_input("Variazione Liquidità value:", key="var_liq_a", value=0.0)

        fcgc_v = st.number_input("FCGC", key="fcgc_vl",
                                  value=float(st.session_state.fcgc) if st.session_state.fcgc is not None else 0.0)
        fcid_v = st.number_input("FCID", key="fcid_vl",
                                  value=float(st.session_state.fcid) if st.session_state.fcid is not None else 0.0)
        fcfr_v = st.number_input("FCFR", key="fcfr_vl",
                                  value=float(st.session_state.fcfr) if st.session_state.fcfr is not None else 0.0)
        fcrf_v = st.number_input("FCRf", key="fcrf_vl",
                                  value=float(st.session_state.fcrf) if st.session_state.fcrf is not None else 0.0)

        if st.session_state.fcgc is not None:
            st.info(f"FCGC from previous calculation: {st.session_state.fcgc}")
        if st.session_state.fcid is not None:
            st.info(f"FCID from previous calculation: {st.session_state.fcid}")
        if st.session_state.fcfr is not None:
            st.info(f"FCFR from previous calculation: {st.session_state.fcfr}")
        if st.session_state.fcrf is not None:
            st.info(f"FCRf from previous calculation: {st.session_state.fcrf}")

        if st.button("Calculate Variazione Liquidità"):
            try:
                res = calc_var_liq(
                    var_liq=var_liq_a,
                    fcgc=fcgc_v, fcid=fcid_v, fcfr=fcfr_v, fcrf=fcrf_v)
                st.success(f"Variazione Liquidità = {res}")
            except Exception as e:
                st.error(str(e))

    elif op2 == "FCU":
        st.markdown("Insert here direct values or its components")

        use_direct = st.checkbox("Insert direct FCU value", key="use_direct_fcu")

        fcu_a = None
        if use_direct:
            fcu_a = st.number_input("FCU value:", key="fcu_a", value=0.0)

        fcgc_v = st.number_input("FCGC", key="fcgc_fcu",
                                  value=float(st.session_state.fcgc) if st.session_state.fcgc is not None else 0.0)
        fcid_v = st.number_input("FCID", key="fcid_fcu",
                                  value=float(st.session_state.fcid) if st.session_state.fcid is not None else 0.0)

        if st.session_state.fcgc is not None:
            st.info(f"FCGC from previous calculation: {st.session_state.fcgc}")
        if st.session_state.fcid is not None:
            st.info(f"FCID from previous calculation: {st.session_state.fcid}")

        if st.button("Calculate FCU"):
            res = calc_fcu(
                fcu=fcu_a,
                fcgc=fcgc_v, fcid=fcid_v)
            st.session_state.fcu = res
            st.success(f"FCU = {res}")

    elif op2 == "FCE":
        st.markdown("Insert here direct values or its components")

        use_direct = st.checkbox("Insert direct FCE value", key="use_direct_fce")

        fce_a = None
        if use_direct:
            fce_a = st.number_input("FCE value:", key="fce_a", value=0.0)

        fcu_v  = st.number_input("FCU", key="fcu_fce",
                                  value=float(st.session_state.fcu) if st.session_state.fcu is not None else 0.0)
        fcfr_v = st.number_input("FCFR", key="fcfr_fce",
                                  value=float(st.session_state.fcfr) if st.session_state.fcfr is not None else 0.0)
        fcrf_v = st.number_input("FCRf", key="fcrf_fce",
                                  value=float(st.session_state.fcrf) if st.session_state.fcrf is not None else 0.0)
        rimb_cap = st.number_input("Rimborso quota capitale", key="rimb_cap_fce", value=0.0)
        div      = st.number_input("Dividendi", key="div_fce", value=0.0)

        if st.session_state.fcu is not None:
            st.info(f"FCU from previous calculation: {st.session_state.fcu}")
        if st.session_state.fcfr is not None:
            st.info(f"FCFR from previous calculation: {st.session_state.fcfr}")
        if st.session_state.fcrf is not None:
            st.info(f"FCRf from previous calculation: {st.session_state.fcrf}")

        if st.button("Calculate FCE"):
            try:
                res = calc_fce(
                    fce=fce_a,
                    fcu=fcu_v, fcfr=fcfr_v, fcrf=fcrf_v,
                    rimb_cap=rimb_cap, div=div)
                st.success(f"FCE = {res}")
            except Exception as e:
                st.error(str(e))
            
        
if page == "PV and NPV":
        st.subheader("PV and NPV")
    
