import streamlit as st

st.title("Corporate Finance Calc")
st.caption("Not a scientific calculator, atm")

#salvataggio dei dati
if 'fccnogc' not in st.session_state:
    st.session_state.fccnogc = []
if 'Rol' not in st.session_state:
    st.session_state.Rol = []
if 'fcgc' not in st.session_state:
    st.session_state.fcgc = []
if 'fcid' not in st.session_state:
    st.session_state.fcid = []
if 'fcfr' not in st.session_state:
    st.session_state.fcfr = []
if 'fcrf' not in st.session_state:
    st.session_state.fcrf = []
if 'pat_net_list' not in st.session_state:
    st.session_state.pat_net_list = []
if 'Of_list' not in st.session_state:
    st.session_state.Of_list = []
if 'fcu' not in st.session_state:
    st.session_state.fcu = []



#Update: trasformare la logica if in def e richiamare le def da altro file py contenente i calcoli. Questo principale deve contenere solo richiami e interfaccia utente. 


#Tendina laterale
st.sidebar.title("Tools for Corporate Finance")
page = st.sidebar.radio("Select a topic:", [
    "Cash Flows",
    "Capitalization",
    "Bonds Evaluation",
    "Stock Evaluation",
    "Ammortamenti: Francese e Italiano",
    "Comparazione tra VAN",
    "Teoria del Portafoglio"
])
#logica troppo lineare, inserire possibilità di calcolo singolari, meno sequenziali
if page == "Cash Flows":
    st.subheader("FCCNOGC, RO-L, FCGC, FCID, FCFR, FCRF in Corporate Finance Calc")
    op = st.selectbox("Quale Flusso di Cassa preferisci Calcolare?", ["FCCNOGC","RO-L", "FCGC", "FCID", "FCFR", "FCRf"])
    #input  per Flussi di cassa
    ricavi_op_mon = st.number_input("Inserisci il valore dei Ricavi operativi monetari: ", key="ricavi_op_mon")
    costi_op_mon = st.number_input("Inserisci il valore dei Costi operativi monetari: ", key="costi_op_mon")
    mol = st.number_input("Se hai già il valore del Mol, inserisci qui il valore: ", key="mol")
    rol = st.number_input("Se hai già il valore del RO-L, inserisci qui il valore: ", key="rol")
    imposte = st.number_input("Inserisci il valore delle imposte: ", key="imposte")
    ammortamenti = st.number_input("Se sono presenti Ammortamenti, inserisci qui il valore: ", key="ammortamenti")
    ccno = st.number_input("Inserire la variazione di ccno: ", key="ccno")
    if st.button("Calcola", key = "operazione di flusso cassa"):
        res = None
        
        if op == "FCCNOGC":
            if ricavi_op_mon != 0 and costi_op_mon != 0:
                res = ricavi_op_mon - costi_op_mon - imposte
            elif rol != 0 and ammortamenti != 0:
                res = rol - imposte + ammortamenti
            elif mol != 0:
                res = mol - imposte
            else:
                st.error("Dati insufficienti per FCCNOGC")
            if res is not None:
                st.session_state.fccnogc.append(res)
        
        elif op == "RO-L":
            if ricavi_op_mon != 0 and costi_op_mon != 0:
                res = ricavi_op_mon - costi_op_mon - ammortamenti
            elif mol != 0:
                res = mol - ammortamenti
            else:
                st.error("Dati insufficienti per RO-L")
            if res is not None:
                st.session_state.Rol.append(res)

        elif op == "FCGC":
            if len(st.session_state.fccnogc) == 0:
                st.error("Devi prima calcolare FCCNOGC!")
            else:
                res = st.session_state.fccnogc[-1] - ccno
                st.session_state.fcgc.append(res)

        elif op == "FCID":
            inv = st.number_input("Inserire il valore degli investimenti: ", key="inv")
            dis = st.number_input("Inserire il valore dei disinvestimenti: ", key="dis")
            res = -inv + dis
            st.session_state.fcid.append(res)
            
        elif op == "FCFR":
            pat_net0 = st.number_input("Inserire il valore del patrimonio netto: ", key="pat_net")
            deb_f0 = st.number_input("Inserire il valore del debito finanziario: ", key="deb_f")
            rimb_cap = st.number_input("Inserire il valore del rimborso di quota capitale: ", key="rimb_cap")
            res = -rimb_cap + pat_net0 + deb_f0
            st.session_state.pat_net_list.append(pat_net0)
            st.session_state.fcfr.append(res)
            
        elif op == "FCRf":
            Of0 = st.number_input("Inserire il valore degli oneri finanziari: ", key="Of")
            div = st.number_input("Inserire il valore dei dividendi: ", key="div")
            res = -Of0 - div
            st.session_state.Of_list.append(Of0)
            st.session_state.fcrf.append(res)

        if res is not None:
            st.success(f"Risultato: {res}")

    # Seconda sezione
    op2 = st.selectbox("Desideri calcolare altro?", ["Variazione Liq", "FCU", "FCE"])
    
    if st.button("Calcola", key = "operazione_base"):
        res = None
        
        # Verifica che le liste non siano vuote prima di accedere agli elementi
        if op2 == "Variazione Liq":
            if (len(st.session_state.fcgc) > 0 and len(st.session_state.fcid) > 0 and 
                len(st.session_state.fcfr) > 0 and len(st.session_state.fcrf) > 0):
                res = (st.session_state.fcgc[-1] + st.session_state.fcid[-1] + 
                      st.session_state.fcfr[-1] + st.session_state.fcrf[-1])
            else:
                st.error("Calcola prima tutti i flussi necessari (FCGC, FCID, FCFR, FCRf)")
                
        elif op2 == "FCU":
            if len(st.session_state.fcgc) > 0 and len(st.session_state.fcid) > 0:
                res = st.session_state.fcgc[-1] + st.session_state.fcid[-1]
                st.session_state.fcu.append(res)
            else:
                st.error("Calcola prima FCGC e FCID")
                
        elif op2 == "FCE":
            if len(st.session_state.fcu) > 0 and len(st.session_state.pat_net_list) > 0 and len(st.session_state.Of_list) > 0:
                res = st.session_state.fcu[-1] + st.session_state.pat_net_list[-1] + st.session_state.Of_list[-1]
            else:
                st.error("Calcola prima FCU, patrimonio netto e oneri finanziari")
        
        if res is not None:
            st.success(f"Risultato: {res}")
            
if page == "Capitalization":
        st.subheader("Interesse Semplice & Composto")
