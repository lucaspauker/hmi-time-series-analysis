#!/usr/bin/env python
# coding: utf-8

import drms
import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime as dt_obj
from astropy.io import fits
from sunpy.visualization.animator import ImageAnimator

def parse_tai_string(tstr, datetime=True):
    year   = int(tstr[:4])
    month  = int(tstr[5:7])
    day    = int(tstr[8:10])
    hour   = int(tstr[11:13])
    minute = int(tstr[14:16])
    if datetime: return dt_obj(year,month,day,hour,minute)
    else: return year,month,day,hour,minute

def visualize_active_region(harp_id, start_time, end_time, time_interval='4h'):
    '''Makes and returns movie based on params. Will sample the data every time interval.
    '''
    c = drms.Client()
    url_base = 'hmi.sharp_cea_720s'
    query_string = '[' + str(harp_id) + '][' + start_time + '-' + end_time + ']'
    if time_interval: query_string = query_string[:-1] + '@' + time_interval + ']'
    keys, segments = c.query(url_base + query_string,
                             key='NOAA_ARS, T_REC, USFLUX, ERRVF',
                             seg='Br, conf_disambig')
    t_rec = np.array([parse_tai_string(keys.T_REC[i], datetime=True) for i in range(keys.T_REC.size)])
    nz = (len(segments))
    ims = []
    for i in range(nz):
        url = 'http://jsoc.stanford.edu' + segments.Br[i]
        photosphere_image = fits.open(url)                  # download the data
        ims.append(photosphere_image[1].data)
    data_cube = np.stack((ims))
    animation = ImageAnimator(data_cube, cmap='seismic_r')
    ax = plt.gca()
    ax.set_title('Flux Emergence over Time for Active Region ' + str(harp_id))
    ax.set_xlabel('x position')
    ax.set_ylabel('y position')
    return animation

if __name__ == '__main__':
    animation = visualize_active_region(7117, '2017.09.03_00:00_TAI', '2017.09.06_00:00_TAI')

