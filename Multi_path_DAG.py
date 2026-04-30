#IN QUESTO PERCORSO IL RESOLVER-DAG AVRà LA LOGICA DEL FILE FORMULAS
#MOL
def calc_mol(ric_op_mon, cost_op_mon):
  mol = ric_op_mon - cost_op_mon
  return mol

#RO-L
def calc_rol_from_mol(mol, amortisat):
  rol = mol - amortisat
  return rol

#FCCNOGC: flusso di cassa del capitale circolante netto operativo della gestione caratteristica
def calc_fccnogc_from_revenue(ric_op_mon, cost_op_mon, tax):
  fccnogc_from_revenue = ric_op_mon - cost_op_mon - tax
  return fccnogc_from_revenue

def calc_fccnogc_from_mol(mol, tax):
  fccnogc_from_mol = mol - tax
  return fccnogc_from_mol

def calc_fccnogc_from_rol(rol, tax, amortisat):
  fccnogc_from_rol = rol - tax + amortisat
  return fccnogc_from_rol

#ROS
def calc_ros_from_rol(rol, ric_op_mon):
  ros = rol / ric_op_mon
  return ros
  
#NET FINANCIAL POSITION, CIN & ROI:
def calc_cin(patrimonio_netto, debiti_finanz, liquidity):
  cin = patrimonio_netto + debiti_finanz - liquidity
  return cin

def calc_roi_from_rol(rol, cin):
  roi = rol / cin
  return roi

#ROE
def calc_net_profit(rol, oneri_finanz, tax):
  utile_netto = rol - oneri_finanz - tax
  return utile_netto

def calc_roe(utile_netto, patrimonio_netto):
  roe = utile_netto / patrimonio_netto
  return roe

#FCGC: flusso di cassa della gestione caratteristica
def calc_var_ccno(ccno1, ccno2):
  var_ccno = ccno2 - ccno1
  return var_ccno
  
def calc_fcgc(fccnogc, var_ccno):
  fcgc = fccnogc - var_ccno
  return fcgc

#FCID: flusso di cassa area investimenti e disinvestimenti
def calc_inv(acquisition_1, acquisition_2):
  inv = acquisition_2 - acquisition_1
  return inv

def calc_vnc(valore_stor, ammo_ti, n_ammo_ti):
  vnc = valore_stor - (ammo_ti * n_ammo_ti)
  return vnc

def calc_dis_from_vnc(vnc, plus, minus):
  dis_from_vnc = vnc + plus - minus
  return dis_from_vnc

def calc_fcid_from_inv_dis(inv, dis):
  fcid_from_inv_dis = dis - inv
  return fcid_from_inv_dis

#FCFR: flusso di cassa finanziamenti e rimborsi
def calc_fcfr(patrimonio_netto, debiti_finanz, quota_rimbors_capital):
  fcfr = patrimonio_netto + debiti_finanz - quota_rimbors_capital
  return fcfr

#FCRf: flusso di cassa remunerazione finanziaria
def calc_fcrf(oneri_finanziari, dividendi):
  fcrf = - oneri_finanziari - dividendi
  return fcrf
  
#Variazione di liquidità
def calc_var_liquidity(fcgc, fcid, fcfr, fcrf):
  var_liquidity = fcgc + fcid + fcfr + fcrf
  return var_liquidity

#FCU: flussi di cassa Unlevered
def calc_fcu(fcgc, fcid):
  fcu = fcgc + fcid
  return fcu

#FCE: flussi di cassa Equity
def calc_fce(fcu, fcfr, quota_rimbors_capital, fcrf, dividendi):
  fce = fcu + fcfr - quota_rimbors_capital + fcrf - dividendi
  return fce

#NPV con flussi di cassa variabili e costi fissi sui flussi per periodo, multiperiodo.

#sarà da specificare se si tratterà con flussi di cassa unlevered o equity nel resolver
# Progettare il resolver che trasforma FCU/FCE in FC[t] coerente con WACC/Ke senza ambiguità

def calc_fc_net(fc, cost):
  fc_net = fc - cost
  return fc_net
  
#time value, discount factor  
def calc_df_constant(k, t):
  df = (1 + k) ** t
  return df

def calc_df_variable(k_t, t):
  df = (1 + k_t) ** t
  return df

def calc_pv(fc_net, df):
  pv = fc_net / df
  return pv

#pv_list è prodotto del resolver non del DAG
def calc_total_pv(pv_list):
  total_pv = sum(pv_list)
  return total_pv

def calc_npv(total_pv, i_0):
  npv = total_pv - i_0
  return npv


#BOND ZERO COUPON VA
def calc_bond_zero_discount_factor(k, t):
  df = (1 + k) ** t
  return df

def calc_bond_zero_va(vn, df):
  va = vn / df
  return va

#BOND ZERO COUPON YIELD TO MATURITY
def calc_bond_zero_mont(vn, va):
  mont = vn / va
  return mont

def calc_bond_zero_factor(t):
  factor = (1/t)
  return factor

def calc_bond_zero_yield_to_maturity(mont, factor):
  bond_zero_yield_to_maturity = mont ** factor - 1
  return bond_zero_yield_to_maturity



















