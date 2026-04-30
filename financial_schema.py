FINANCIAL_VARIABLES = {
    # Profitability
    "mol": "Margine Operativo Lordo",
    "rol": "Risultato Operativo Lordo",
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
    "vn": "Valore nominale",
    "mont": "Montante",
    "factor": "Fattore",
    "bond_zero_yield_to_maturity": "Yield to maturity of the Zero Coupon",
    
}

RELATIONSHIPS = {
    "mol -> rol": "rol = mol - amortisation",
    "rol -> fcgc": "operating cash flow derived from RO-L adjustments",
    "fcu -> fce": "equity adjustments from financing structure",
    "fc -> pv": "discounted cash flow transformation",
}

DISCOUNT_RULES = {
    "FCU": "WACC",
    "FCE": "Ke",
    "GENERIC": "custom rate k",
}
