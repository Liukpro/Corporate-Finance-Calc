FINANCIAL_VARIABLES = {
    # Profitability
    "mol": "Margine Operativo Lordo",
    "rol": "Reddito Operativo Lordo",
    "ros": "Return on Sales",

    # Cash flow operativo
    "fccnogc": "Flusso di Cassa del Capitale Circolante Netto Operativo della Gestione Caratteristica",
    "fcgc": "Flusso di Cassa Gestione Caratteristica",

    # Capital structure
    "cin": "Capitale Investito Netto",
    "roi": "Return on Investment",
    "roe": "Return on Equity",

    # Net result
    "utile_netto": "Net Profit",

    # Cash flows
    "fcu": "Unlevered Cash Flow",
    "fce": "Equity Cash Flow",
    "fcfr": "Financing Cash Flow",
    "fcrf": "Financial Remuneration Cash Flow",

    # Working capital
    "ccno1": "Capitale Circolante Netto Operativo Iniziale",
    "ccno2": "Capitale Circolante Netto Operativo Finale",
    "var_ccno": "Variazione CCNO",

    # Investments
    "inv": "Investimenti",
    "dis": "Disinvestimenti",
    "vnc": "Valore Netto Contabile",

    # Discounting layer
    "fc": "Cash Flow Generico",
    "fc_net": "Cash Flow Netto",
    "pv": "Present Value",
    "npv": "Net Present Value",

    #Discounting layer for bonds
    "va": "Valore Attuale",
    "vn": "Valore Nominale",
    "mont": "Montante",
    "factor": "Fattore tempo",
    "bond_zero_yield_to_maturity": "Yield to Maturity Zero Coupon",
}


RELATIONSHIPS = {

    # Profitability chain
    "mol -> rol": "ROL deriva da MOL tramite sottrazione ammortamenti",
    "rol -> ros": "ROS misura redditività su ricavi",

    # Cash flow operating
    "mol/rol -> fccnogc": "Conversione risultato economico in flussi di cassa operativi",
    "fccnogc -> fcgc": "Aggiustamento variazione CCNO",

    # Capital structure
    "rol -> roi": "ROI misura rendimento capitale investito",
    "cin = equity + debt - liquidity": "Definizione capitale investito netto",

    # Equity
    "rol -> utile_netto": "Risultato netto dopo oneri finanziari e tasse",
    "utile_netto -> roe": "Redditività capitale proprio",

    # Investments
    "investments - disinvestments -> fcid": "Flusso cassa investimenti netto",

    # Cash flow system
    "fcgc + fcid -> fcu": "Free Cash Flow Unlevered",
    "fcu + financing adjustments -> fce": "Free Cash Flow Equity",

    # Discounting
    "fc -> pv": "Attualizzazione flussi",
    "pv -> npv": "Somma valori attuali meno investimento iniziale",

    # Bonds
    "vn -> va": "Attualizzazione bond",
    "va -> ytm": "Yield implicito dal prezzo"
}


DISCOUNT_RULES = {

    "FCU": "WACC",
    "FCE": "Ke",
    "GENERIC": "k",

    "RULE": "FCU uses enterprise value logic, FCE uses equity logic"
}
