#analisi prospettica area caratteristica

def calc_mo_netto(ricavi_operativi, costi_operativi, tc):
    mo_netto = []
    
    for t in range(len(ricavi_operativi)):
        mo_lordo = ricavi_operativi[t] - costi_operativi[t]
        mo_netto.append(mo_lordo * (1 - tc))
        
    return mo_netto

def calc_ammortamenti(esborsi, anni_list, vita_progetto):
    ammortamenti = [0.0] * vita_progetto

    for i in range(len(esborsi)):
        esborso = float(esborsi[i])
        anni = int(anni_list[i])

        quota = esborso / anni

        for t in range(anni):
            if t < vita_progetto:
                ammortamenti[t] += quota

    return ammortamenti

def calc_shield_ammortamenti(ammortamenti, tc):
    tax_shield_ammortamenti_list = [amm * tc for amm in ammortamenti]
    return tax_shield_ammortamenti_list

def calc_fccnogc2(mo_netto, tax_shield_ammortamenti_list):
    fccnogc = []
    for t in range(len(mo_netto)):
        fccnogc.append(mo_netto[t] + tax_shield_ammortamenti_list[t])
    return fccnogc

def aggiungi_t0(flussi):
    return [0.0] + list(flussi)

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

#FCID
def calc_netto_vendita(prezzo, vc, tc):
    return prezzo - tc * (prezzo - vc)

#sia per esborsi che per i costi incrementali
def calc_esborsi(esborsi, anni_esborsi, vita_progetto):
    flussi = [0.0] * (vita_progetto + 1)

    for i in range(len(esborsi)):
        flussi[anni_esborsi[i]] -= esborsi[i]

    return flussi

#valore contabile futuro disinvestimento
def calc_vc(esborso, anno_esborso, vita, t):
    anni_passati = t - anno_esborso

    if anni_passati < 0:
        anni_passati = 0
    if anni_passati > vita:
        anni_passati = vita

    quota = esborso / vita
    return esborso - quota * anni_passati

#mancato disinvestimento
def calc_costo_opportunita(prezzo, vc, tc, vita_progetto):
    flussi = [0.0] * (vita_progetto + 1)
    flussi[0] = - calc_netto_vendita(prezzo, vc, tc)
    return flussi

#valore contabile del nuovo impianto
def calc_cessione(prezzo, anno_cessione, esborsi, anni_esborsi, vite, tc, vita_progetto):
    vc_totale = 0.0

    for i in range(len(esborsi)):
        vc_totale += calc_vc(esborsi[i], anni_esborsi[i], vite[i], anno_cessione)

    flussi = [0.0] * (vita_progetto +1)
    flussi[anno_cessione] = calc_netto_vendita(prezzo, vc_totale, tc)
    return flussi

#FCID totale
def calc_fcid2(esb, costi, opp, ces):
    fcid = []

    for t in range(len(esb)):
        fcid.append(esb[t] + costi[t] + opp[t] + ces[t])

    return fcid

#FCU
def calc_fcu2(fcgc, fcid):
    if len(fcgc) != len(fcid):
        raise ValueError("FCGC e FCID devono avere lo stesso numero di periodi")
    return [fcgc[t] + fcid[t] for t in range(len(fcid))]
