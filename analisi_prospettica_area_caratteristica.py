#analisi prospettica area caratteristica

def calc_mo_netto(ricavi_operativi, costi_operativi, tc):
    mo_netto = []
    
    for t in range(len(ricavi_operativi)):
        mo_lordo = ricavi_operativi[t] - costi_operativi[t]
        mo_netto.append(mo_lordo * (1 - tc))
        
    return mo_netto

def calc_ammortamenti(esborsi, anni_list, vita_progetto):
    risultati = []
    
    for i in range(len(esborsi)):
        esborso = float(esborsi[i])
        anni = int(anni_list[i])
        
        quota = esborso / anni
        
        serie = [0.0] * vita_progetto  # ✔ float-safe
        
        for t in range(anni):
            if t < vita_progetto:
                serie[t] = quota
        
        risultati.append(serie)
    
    return risultati

def calc_shield_ammortamenti(ammortamenti, tc):
    tax_shield_ammortamenti_list = [amm * tc for amm in ammortamenti]
    return tax_shield_ammortamenti_list

def calc_fccnogc2(mo_netto, tax_shield_ammortamenti_list):
    fccnogc = []
    for t in range(len(mo_netto)):
        fccnogc.append(mo_netto[t] + tax_shield_ammortamenti_list[t])
    return fccnogc

def calc_var_ccno(ccno):
    delta_ccno = []
    
    for t in range(len(ccno)):
        if t == 0:
            delta_ccno.append(ccno[t])
        else:
            delta_ccno.append(ccno[t] - ccno[t - 1])
    
    return delta_ccno

def calc_fcgc2(fccnogc, delta_ccno):
    fcgc = []
    
    for t in range(len(fccnogc)):
        fcgc.append(fccnogc[t] - delta_ccno[t])
        
    return fcgc
