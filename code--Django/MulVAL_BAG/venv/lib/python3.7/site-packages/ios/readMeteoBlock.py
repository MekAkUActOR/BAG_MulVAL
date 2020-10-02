from ios.FortranFormat import FortranLine, FortranFormat
import numpy as np
from datetime import datetime

frmt="F7.1,F7.0,F7.1,F7.1,F7.0,F7.2,F7.0,F7.0,F7.1,F7.1,F7.1"
format=FortranFormat(frmt)

def readMeteoFile(fileobj, skiprows=5):
    """
    """
    skipr=skiprows

    P = []
    Z = []
    T = []
    DWPT = []
    RELH = []
    MIXR = []
    DRCT = []
    SKNT = []
    THTA = []
    THTE = []
    THTV = []
    
    try:
        for i in range(skipr):
            fileobj.readline()
            
        for line in fileobj:            
            [p,z,t, dwpt, relh, mixr, drct, sknt, thta, thte, thtv]=FortranLine(line,format)
            if t is None:
                t=np.nan
            
            P.append(p*100.0)
            Z.append(z)
            T.append(t+273.15)
            DWPT.append(dwpt)
            RELH.append(relh)
            MIXR.append(mixr)
            DRCT.append(drct)
            SKNT.append(sknt)
            THTA.append(thta)
            THTE.append(thte)
            THTV.append(thtv)
           
            
    except Exception, e:
        print "Error occured! ",e
    finally:
        fileobj.close()

        
    
    return {'PRES':np.array(P, dtype='float64'), 'HGHT':np.array(Z, dtype='float64'), \
        'TEMP':np.array(T, dtype='float64'), 'DWPT':np.array(DWPT, dtype='float64'), \
        'RELH':np.array(RELH, dtype='float64'), 'MIXR':np.array(MIXR, dtype='float64'), \
        'DRCT':np.array(DRCT, dtype='float64'), 'SKNT':np.array(SKNT, dtype='float64'), \
        'THTA':np.array(THTA, dtype='float64'), 'THTE':np.array(THTE, dtype='float64'), \
        'THTV':np.array(THTV, dtype='float64')}
        

def readMeteoCtx(fileobj, skipline=1):
    """
    """
    skip=skipline
    for i in range(skip):
        fileobj.readline()

    ret = {}    
    for line in fileobj:
        left, right = line.split(':')
        left=left.strip()
        left=left.replace(' ','_').replace('[','').replace(']','').lower()
        right=right.strip()

        
        if 'station_number' in left:
            ret['STID'] = int(right)
        elif 'observation' in left:
            ret['SOBS']=datetime.strptime(right,'%y%m%d/%H%M')
        elif 'latitude' in left:
            ret['SLAT']=float(right)
        elif 'longitude' in left:
            ret['SLON']=float(right)
        elif 'elevation' in left:
            ret['SELV']=float(right)
        elif 'showalter' in left:
            ret['SHOW']=float(right)
        elif 'lifted_index' in left:
            ret['LIFT']=float(right)
        elif 'lift_computed' in left:
            ret['LFTV']=float(right)
        elif 'sweat' in left:
            ret['SWET']=float(right)
        elif 'k_index' in left:
            ret['KINX']=float(right)
        elif 'cross' in left:
            ret['CTOT']=float(right)
        elif 'vertical_totals' in left:
            ret['VTOT']=float(right)
        elif 'totals_totals' in left:
            ret['TTOT']=float(right)
        elif 'convective_available' in left:
            ret['CAPE']=float(right)
        elif 'cape_using' in left:
            ret['CAPV']=float(right)
        elif 'convective_inhibition' in left:
            ret['CINS']=float(right)
        elif 'cins_using' in left:
            ret['CINV']=float(right)
        elif 'bulk_richardson_number' == left:
            ret['BRCH']=float(right)
        elif 'number_using_capv' in left:
            ret['BRCV']=float(right)
        elif 'temp_k_of_the' in left:
            ret['LCLT']=float(right)
        elif 'pres_hpa_of_the' in left:
            ret['LCLP']=float(right)
        elif 'mean_mixed_layer_potential' in left:
            ret['MLTH']=float(right)
        elif 'mean_mixed_layer_mixing' in left:
            ret['MLMR']=float(right)
        elif '1000_hpa_to_500_hpa' in left:
            ret['THTK']=float(right)
        elif 'precipitable_water' in left:
            ret['PWAT']=float(right)
            
        
            
    fileobj.close()
    return ret