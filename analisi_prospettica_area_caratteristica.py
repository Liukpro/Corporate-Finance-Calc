#analisi prospettica area caratteristica

def calc_mo_netto(ricavi_operativi, costi_operativi, tc):
    mo_netto = []
    
    for t in range(len(ricavi_operativi)):
        mo_lordo = ricavi_operativi[t] - costi_operativi[t]
        mo_netto.append(mo_lordo * (1 - tc))
        
    return mo_netto

def calc_ammortamenti(esborsi, anni_list, vita_progetto):
    ammortamenti = [0] * vita_progetto
    
    for t, (esborso, anni) in enumerate(zip(esborsi, anni_list)):
        quota = esborso / anni
        for i in range(anni):
            if t + i < vita_progetto:
                ammortamenti[t + i] += quota
                
    return ammortamenti

def calc_shield_ammortamenti(ammortamenti, tc):
    tax_shield_ammortamenti_list = [amm * tc for amm in ammortamenti]
    return tax_shield_ammortamenti_list

def calc_fccnogc(mo_netto, tax_shield_ammortamenti_list):
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

def calc_fcgc(fccnogc, delta_ccno):
    fcgc = []
    
    for t in range(len(fccnogc)):
        fcgc.append(fccnogc[t] - delta_ccno[t])
        
    return fcgc
