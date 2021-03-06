#!/usr/bin/env python
"""
Displays projection matrix
"""

import os
import copy
import lo
import csh

# define data set
datadir = os.getenv('CSH_DATA')
filenames = [datadir + '/1342185454_blue_PreparedFrames.fits[10000:10032]',
             datadir + '/1342185455_blue_PreparedFrames.fits[10000:10032]']
# no compression
output_path = os.path.join(os.getenv('HOME'), 'data', 'csh', 'output',)
# compression modes
#compressions = ["", "ca", "cs"]
compressions = ["ca"]
#compressions = [""]
factor=8
# median filter length
deglitch=True
covariance=False
filtering = False
filter_length = 10000
#hypers = (1e9, 1e9)
hypers = (1e0, 1e0)
#hypers = (0., 0.)
ext = ".fits"
pre = "matrix"
# to store results
M = []
# define same header for all maps
tod, projection, header, obs = csh.load_data(filenames)
# get the weight map
weights = projection.transpose(tod.ones(tod.shape))
#weights.writefits(os.path.join(output_path, pre + 'weights' + ext))
del tod, projection, obs
# choose a small portion of the map (in the center)
# center the new map
n = 64
header['CRPIX1'] -= header['NAXIS1'] / 2 - n / 2
header['CRPIX2'] -= header['NAXIS2'] / 2 - n / 2
# correct for wrong centering
#header['CRPIX1'] += 7
#header['CRPIX2'] += 7
# 
header['NAXIS1'] = n
header['NAXIS2'] = n
# reload data with new header
tod, projection, header, obs = csh.load_data(filenames, header=header)
# get weighted backprojection
bpj = projection.transpose(tod)
weights = projection.transpose(tod.ones(tod.shape))
pipe = bpj / weights

# get the model dense matrix
P = lo.aslinearoperator(projection.aslinearoperator())
PtPd = (P.T * P).todense()
