# -*- coding: utf-8 -*-
"""
Created on Mon May 13 15:08:24 2013

@author: kshmirko
"""

from netCDF4 import Dataset, date2num, date2index
import numpy as np


class meteoFile(object):    
    def __init__(self, fname):
        self.__fname = fname
        self.datas = []
    
    def add(self, data):
        self.datas.append(data)
        
    def initfile(self):
        """
        Initialize nc file structure
        """
        f = Dataset(self.__fname,'w', format='NETCDF3_64BIT')
        time = f.createDimension('time', None)
        Len = f.createDimension('Len',300)
        
        Time = f.createVariable('Time','f4',('time',), zlib=True, complevel=9)
        Time.units = 'days since 1984-02-08 00:00:00'
        Time.calendar = 'standard'

        PRES = f.createVariable('PRES','f4',('time', 'Len',), zlib=True, complevel=9, fill_value=np.nan)
        PRES.unit = '[Pa]'
        PRES.description = 'Atmospheric Pressure'
        
        TEMP = f.createVariable('TEMP','f4',('time', 'Len',), zlib=True, complevel=9, fill_value=np.nan)
        TEMP.units = '[celsius]'
        TEMP.description = 'Temperature'
        
        HGHT = f.createVariable('HGHT','f4',('time', 'Len',), zlib=True, complevel=9, fill_value=np.nan)
        HGHT.units = '[meter]'
        HGHT.description = 'Geopotential Height'
        
        DWPT = f.createVariable('DWPT','f4',('time', 'Len',), zlib=True, complevel=9, fill_value=np.nan)
        DWPT.units = '[celsius]'
        DWPT.description = 'Dewpoint Temperature'
        
        RELH = f.createVariable('RELH','f4',('time', 'Len',), zlib=True, complevel=9, fill_value=np.nan)
        RELH.units = '[%]'
        RELH.description = 'Relative Humidity'
        
        SKNT = f.createVariable('SKNT','f4',('time', 'Len',), zlib=True, complevel=9, fill_value=np.nan)
        SKNT.units = '[knot]'
        SKNT.description = 'Wind Speed'
        
        MIXR = f.createVariable('MIXR','f4',('time', 'Len',), zlib=True, complevel=9, fill_value=np.nan)
        MIXR.units = '[gram/kilogram]'
        MIXR.description = 'Mixing Ratio'
    
        DRCT = f.createVariable('DRCT','f4',('time', 'Len',), zlib=True, complevel=9, fill_value=np.nan)
        DRCT.units = '[degrees true]'
        DRCT.description = 'Wind Direction'
        
        THTA = f.createVariable('THTA','f4',('time', 'Len',), zlib=True, complevel=9, fill_value=np.nan)
        THTA.units = '[kelvin]'
        THTA.description = 'Potential Temperature'
        
        THTE = f.createVariable('THTE','f4',('time', 'Len',), zlib=True, complevel=9, fill_value=np.nan)
        THTE.units = '[kelvin]'
        THTE.description = 'Equivalent Potential Temperature'
        
        THTV = f.createVariable('THTV','f4',('time', 'Len',), zlib=True, complevel=9, fill_value=np.nan)
        THTV.units = '[kelvin]'        
        THTV.description = 'Virtual Potential Temperature'
        
        STID = f.createVariable('STID', 'i4', ('time',), zlib=True, complevel=9)
        STID.units = '[N/A]'
        STID.description = 'Station WM id'
        
        SOBS = f.createVariable('SOBS', 'f4', ('time',), zlib=True, complevel=9)
        SOBS.units = 'days since 1984-02-08 00:00:00'
        SOBS.calendar = 'standard'
        
        SLAT = f.createVariable('SLAT', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        SLAT.units = '[degrees true]'
        SLAT.description = 'Station latitude'

        SLON = f.createVariable('SLON', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        SLON.units = '[degrees true]'
        SLON.description = 'Station longitude'

        SELV = f.createVariable('SELV', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        SELV.units = '[meter]'
        SELV.description = 'Station elevation'

        SHOW = f.createVariable('SHOW', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        SHOW.units = '[celsius]'
        SHOW.description = 'Showalter index'

        LIFT = f.createVariable('LIFT', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        LIFT.units = '[celsius]'
        LIFT.description = 'Lifted index'

        LFTV = f.createVariable('LFTV', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        LFTV.units = '[celsius]'
        LFTV.description = 'LIFT computed by using virtual temperature'

        SWET = f.createVariable('SWET', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        SWET.units = '[N/A]'
        SWET.description = 'SWEAT index'        
        
        KINX = f.createVariable('KINX', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        KINX.units = '[N/A]'
        KINX.description = 'K index'
        
        CTOT = f.createVariable('CTOT', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        CTOT.units = '[N/A]'
        CTOT.description = 'Cross Totals index'

        VTOT = f.createVariable('VTOT', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        VTOT.units = '[N/A]'
        VTOT.description = 'Vertical Totals index'

        TTOT = f.createVariable('TTOT', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        TTOT.units = '[N/A]'
        TTOT.description = 'Totals Totals index'

        CAPE = f.createVariable('CAPE', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        CAPE.units = '[J/kg]'
        CAPE.description = 'Convective Available Potential Energy'

        CAPV = f.createVariable('CAPV', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        CAPV.units = '[J/kg]'
        CAPV.description = 'CAPE computed by using the virtual temperature.'

        CINS = f.createVariable('CINS', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        CINS.units = '[J/kg]'
        CINS.description = 'Convective inhibition'

        CINV = f.createVariable('CINV', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        CINV.units = '[J/kg]'
        CINV.description = 'CINS computed by using the virtual temperature.'

        BRCH = f.createVariable('BRCH', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        BRCH.units = '[N/A]'
        BRCH.description = 'Bulk Richardson number'

        BRCV = f.createVariable('BRCV', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        BRCV.units = '[N/A]'
        BRCV.description = 'BRCH computed by using CAPV'

        LCLT = f.createVariable('LCLT', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        LCLT.units = '[kelvin]'
        LCLT.description = 'Temperature at the LCL, the lifting condensation level, from an average of the lowest 500 meters'

        LCLP = f.createVariable('LCLP', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        LCLP.units = '[hPa]'
        LCLP.description = 'Pressure at the LCL, the lifting condensation level, from an average of the lowest 500 meters'

        MLTH = f.createVariable('MLTH', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        MLTH.units = '[kelvin]'
        MLTH.description = 'Mean mixed layer THTA'

        MLMR = f.createVariable('MLMR', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        MLMR.units = '[g/kg]'
        MLMR.description = 'Mean mixed layer MIXR'

        THTK = f.createVariable('THTK', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        THTK.units = '[meter]'
        THTK.description = '1000 mb to 500 mb thickness'

        PWAT = f.createVariable('PWAT', 'f4', ('time',), zlib=True, complevel=9, fill_value=np.nan)
        PWAT.units = '[mm]'
        PWAT.description = 'Precipitable water for the entire sounding'

        f.close()
    
    def writedown(self):
        """
        Запись данных
        """
        f = Dataset(self.__fname,'r+',format='NETCDF3_64BIT')
        
        for item in self.datas:
            #unpack content
            stid, date, meteo, ctx = item
            
            #test if date already in file
            try:
                idx=date2index(date, f.variables['Time'])
                #if ok and date exist in file - replace
                
            except ValueError:
                idx = len(f.variables['Time'])
            
            self.write(f, idx, stid, date, meteo, ctx)
        
        f.close()
        self.datas = []
    
    def write(self, f, idx, stid, date, meteo, ctx):
        """
        Write single record to file
        """
        f.variables['Time'][idx] = date2num(date, units=f.variables['Time'].units, calendar='standard')
        f.variables['STID'][idx] = int(stid)
        

        for key, val in meteo.items():
            f.variables[key][idx,:len(val)] = val
        
        for key, val in ctx.items():
            if key == 'SOBS':            
                f.variables[key][idx] = date2num(val, units=f.variables[key].units, calendar=f.variables[key].calendar)
            else:
                f.variables[key][idx] = val
        
    
if __name__ == '__main__':
    m = meteoFile('tmp.nc')
    m.initfile()