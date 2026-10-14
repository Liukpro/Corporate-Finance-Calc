#analisi prospettica area caratteristica

#fcgc

def calc_mo_netto(ricavi_operativi, costi_operativi, tc):
    mo_netto = []
    for t in range(len(ricavi_operativi)):
        mo_lordo = ricavi_operativi[t] - costi_operativi[t]
        mo_netto.append(mo_lordo * (1 - tc))
    return mo_netto


def calc_ammortamenti(esborsi, anni_pagamento, anni_ammortamento, orizzonte):
    """Quota costante, la prima quota cade nel periodo successivo al pagamento.
    anni_ammortamento = 0 -> esborso non ammortizzabile (nessuna quota)."""
    ammortamenti = [0.0] * orizzonte
    for i in range(len(esborsi)):
        anni = int(anni_ammortamento[i])
        if anni <= 0:
            continue
        quota = float(esborsi[i]) / anni
        for k in range(anni):
            t = int(anni_pagamento[i]) + 1 + k
            if t <= orizzonte:
                ammortamenti[t - 1] += quota
    return ammortamenti


def calc_shield_ammortamenti(ammortamenti, tc):
    return [amm * tc for amm in ammortamenti]


def calc_fccnogc2(mo_netto, tax_shield_ammortamenti_list):
    return [mo_netto[t] + tax_shield_ammortamenti_list[t] for t in range(len(mo_netto))]


def aggiungi_t0(flussi):
    return [0.0] + list(flussi)


def calc_var_ccno(ccno):
    """ccno = livello di CCNO per periodo (l'ultimo valore a 0 = rilascio)."""
    delta_ccno = []
    for t in range(len(ccno)):
        prev = ccno[t - 1] if t > 0 else 0.0
        delta_ccno.append(ccno[t] - prev)
    return delta_ccno


def calc_fcgc2(fccnogc, delta_ccno):
    return [fccnogc[t] - delta_ccno[t] for t in range(len(fccnogc))]


# fcid

def calc_disinvestimento(prezzo, vc, tc):
    """Ritorna (plus/minusvalenza, imposta o scudo, netto).
    Plusvalenza: imposta > 0 (esce cassa). Minusvalenza: imposta < 0 = scudo fiscale (entra cassa)."""
    plus = prezzo - vc
    imposta = plus * tc
    netto = prezzo - imposta
    return plus, imposta, netto


def calc_netto_vendita(prezzo, vc, tc):
    return calc_disinvestimento(prezzo, vc, tc)[2]


def calc_esborsi(esborsi, anni_esborsi, orizzonte):
    """Vale sia per gli esborsi di investimento sia per i costi incrementali."""
    flussi = [0.0] * (orizzonte + 1)
    for i in range(len(esborsi)):
        anno = int(anni_esborsi[i])
        if anno < 0 or anno > orizzonte:
            raise ValueError(f"Anno {anno} fuori dall'orizzonte (0..{orizzonte})")
        flussi[anno] -= esborsi[i]
    return flussi


def calc_vc(esborso, anno_esborso, vita, t):
    """Valore contabile al tempo t di un esborso ammortizzato a quote costanti.
    vita <= 0 -> non ammortizzabile: valore contabile pieno."""
    if vita <= 0:
        return esborso
    anni_passati = t - anno_esborso
    anni_passati = max(0, min(anni_passati, vita))
    quota = esborso / vita
    return esborso - quota * anni_passati


def calc_vc_da_storico(costo_storico, perc_ammortizzata):
    """perc_ammortizzata in percentuale (es. 90 per il 90%)."""
    return costo_storico * (1 - perc_ammortizzata / 100)


def calc_flussi_disinvestimenti(prezzi, anni, vcs, tc, orizzonte, segno=1):
    """Flusso netto (prezzo - imposta/+ scudo) di ogni disinvestimento nel suo anno.
    segno = +1 per le cessioni, -1 per i mancati disinvestimenti (costo opportunita')."""
    flussi = [0.0] * (orizzonte + 1)
    for i in range(len(prezzi)):
        anno = int(anni[i])
        if anno < 0 or anno > orizzonte:
            raise ValueError(f"Anno {anno} fuori dall'orizzonte (0..{orizzonte})")
        flussi[anno] += segno * calc_netto_vendita(prezzi[i], vcs[i], tc)
    return flussi


def calc_fcid2(esb, costi, mancati, cessioni):
    return [esb[t] + costi[t] + mancati[t] + cessioni[t] for t in range(len(esb))]


#fcu

def calc_fcu2(fcgc, fcid):
    if len(fcgc) != len(fcid):
        raise ValueError("FCGC e FCID devono avere lo stesso numero di periodi")
    return [fcgc[t] + fcid[t] for t in range(len(fcid))]
