#!/usr/bin/env python
# coding: utf-8

import drms
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as manimation

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

def create_animation(harp_id, start_time, end_time, time_interval='4h'):
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
    ax.set_title('Flux Emergence Over Time for Active Region ' + str(harp_id))
    ax.set_xlabel('x position')
    ax.set_ylabel('y position')
    return animation

def save_animation(harp_id, start_time, end_time, time_interval='4h'):
    '''Saves a movie based on params. Will sample the data every time interval.
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
    url = 'http://jsoc.stanford.edu' + segments.Br[0]
    photosphere_image = fits.open(url)
    ims = []

    my_dpi=192
    ny, nx = photosphere_image[1].data.shape
    fig = plt.figure(figsize=(nx/my_dpi, ny/my_dpi), dpi=my_dpi)
    ax = plt.gca()
    ax.set_title('Flux Emergence Over Time for Active Region ' + str(harp_id))
    ax.set_xlabel('x position')
    ax.set_ylabel('y position')
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])

    ims = []
    for i in range(keys.T_REC.size):
        url = 'http://jsoc.stanford.edu' + segments.Br[i]
        photosphere_image = fits.open(url)
        im = plt.imshow(photosphere_image[1].data, cmap='seismic_r', origin='lower',
                        vmin=-3000, vmax=3000, extent=[0, nx, 0, ny], interpolation=None, animated=True)
        ims.append([im])

    ani = manimation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)
    base_dir = './movies/'
    ani.save(base_dir + str(harp_id) + '_' + start_time + '_' + end_time +'.mp4',
             writer='ffmpeg_file', dpi=my_dpi)

if __name__ == '__main__':
    animation = create_animation(7117, '2017.09.03_00:00_TAI', '2017.09.06_00:00_TAI')
    save_animation(7117, '2017.09.03_00:00_TAI', '2017.09.06_00:00_TAI')

