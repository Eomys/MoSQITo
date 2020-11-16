# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 11:22:22 2020

@author: wantysal
"""

import numpy as np
import matplotlib.pyplot as plt

fmod = np.arange(0,165,5)
fmod = am

fm125 = np.array([  1.0355988,  10.355987 ,  11.132686 ,  13.851132 ,  18.511328 ,
                   20.064724 ,  24.724918 ,  31.32686  ,  41.423946 ,  49.967636 ,
                   57.34628  ,  64.33657  ,  72.10356  ,  90.74434  ,  79.4822   ,
                   86.084145 ,  91.909386 , 100.45307  ])

R125 = np.array([0.        , 0.04359673, 0.09468665, 0.16416894, 0.19482289,
                 0.27656674, 0.3113079 , 0.34196186, 0.32356948, 0.26226157,
                 0.20299728, 0.15803815, 0.11512262, 0.0619891 , 0.09264305,
                 0.07016349, 0.05177112, 0.03950954])


fm250 = np.array([  0.7373272,   3.9324117,   9.585254 ,  14.2549925,  16.71275  ,
                   19.907835 ,  22.611366 ,  23.594471 ,  29.493088 ,  30.47619  ,
                   37.112137 ,  41.29032  ,  47.926266 ,  50.13825  ,  51.121353 ,
                   53.08756  ,  54.07066  ,  56.774193 ,  58.248848 ,  62.427036 ,
                   61.68971  ,  69.308754 ,  68.57143  ,  71.27496  ,  73.73272  ,
                   73.97849  ,  75.207375 ,  79.139786 ,  79.139786 ,  84.792625 ,
                   90.19969  ,  97.81874  , 104.70046  , 112.31951  , 120.92166  ,
                  129.76959  ])

R250 = np.array([0.00432277, 0.00576369, 0.06340057, 0.16138329, 0.17435159,
                 0.26945245, 0.32132566, 0.3443804 , 0.42651296, 0.44668588,
                 0.47694525, 0.4668588 , 0.42651296, 0.46253604, 0.41210374,
                 0.4020173 , 0.43948126, 0.37463978, 0.39193085, 0.3631124 ,
                 0.3429395 , 0.3040346 , 0.28242075, 0.27521613, 0.259366  ,
                 0.24207492, 0.24351585, 0.2204611 , 0.20461094, 0.17146975,
                 0.14697406, 0.11815562, 0.09942363, 0.07636888, 0.05619597,
                 0.04322766])

fm500 = np.array([  7.6375403,  15.79288  ,  20.841423 ,  26.666666 ,  30.93851  ,
                   34.43366  ,  40.2589   ,  44.919094 ,  49.190937 ,  51.521034 ,
                   57.34628  ,  64.33657  ,  69.77346  ,  74.04531  ,  81.42395  ,
                   87.63754  ,  94.23948  , 102.78317  , 116.763756 , 129.57928  ,
                  140.84143  , 149.77347  , 160.2589   ])

R500 = np.array([0.04972752, 0.1253406 , 0.23569483, 0.35013625, 0.46457765,
                 0.5258856 , 0.619891  , 0.67302454, 0.69346046, 0.69550407,
                 0.6873297 , 0.67098093, 0.6321526 , 0.57901907, 0.5074932 ,
                 0.4400545 , 0.38487738, 0.3153951 , 0.22752044, 0.16621253,
                 0.11920981, 0.08651226, 0.06811989])
                
fm1000 = np.array([  0.       ,   3.884415 ,   9.7237625,  17.147604 ,  29.302307 ,
                    37.933605 ,  48.504757 ,  55.145306 ,  55.948395 ,  57.480103 ,
                    60.618927 ,  63.314735 ,  65.28852  ,  67.201035 ,  69.55657  ,
                    76.14433  ,  77.2943   ,  82.847725 ,  83.352325 ,  88.26008  ,
                    89.019806 ,  93.92756  ,  94.4309   ,  97.78904  ,  99.06719  ,
                   104.23258  , 103.963005 , 106.03293  , 109.89504  , 111.18953  ,
                   115.05101  , 117.38172  , 119.95311  , 125.630646 , 132.60141  ,
                   137.24963  , 144.47617  , 151.19432  , 159.97737  ])

R1000 = np.array([0.        , 0.00211198, 0.03450088, 0.1382977 , 0.40437   ,
                  0.60555416, 0.80238307, 0.89103884, 0.9516347 , 0.90182984,
                  0.9753813 , 0.92339617, 0.9969634 , 0.92983717, 0.9882475 ,
                  0.9556905 , 0.92104256, 0.89138556, 0.86107534, 0.83503467,
                  0.7960629 , 0.7700222 , 0.736826  , 0.71946436, 0.6819286 ,
                  0.6529984 , 0.6284707 , 0.62555665, 0.5764418 , 0.5764243 ,
                  0.52586645, 0.52727795, 0.48683867, 0.44491437, 0.40008652,
                  0.3726063 , 0.3205599 , 0.29016566, 0.24531329])

fm2000 = np.array([  0.       ,   4.4051557,   7.5956764,  10.048887 ,  12.017292 ,
                    15.69636  ,  17.911657 ,  20.366364 ,  20.619616 ,  25.28251  ,
                    27.987852 ,  30.20053  ,  31.18548  ,  34.37525  ,  34.38161  ,
                    39.782192 ,  39.298134 ,  42.23989  ,  42.981316 ,  45.18539  ,
                    44.95683  ,  46.663754 ,  48.13538  ,  50.358532 ,  53.04068  ,
                    55.264206 ,  56.971127 ,  58.68778  ,  60.890354 ,  62.367218 ,
                    62.84529  ,  65.06246  ,  67.00842  ,  68.48715  ,  71.90736  ,
                    73.62214  ,  76.79096  ,  79.24305  ,  81.67831  ,  85.10337  ,
                    91.45038  ,  93.655945 ,  96.586105 ,  96.33435  ,  98.04801  ,
                   106.5901   , 107.57281  , 115.62524  , 118.07209  , 120.26419  ,
                   121.97673  , 129.54285  , 131.255    , 134.91576  , 135.15628  ,
                   136.87106  , 144.92911  , 159.83092  ])

R2000 = np.array([0.00271003, 0.00538277, 0.04194128, 0.06631085, 0.10694477,
                  0.1407891 , 0.18955104, 0.21934068, 0.250504  , 0.30331025,
                  0.35477808, 0.39405492, 0.41708192, 0.4509304 , 0.47396567,
                  0.54031587, 0.55929023, 0.5809457 , 0.60803974, 0.6161512 ,
                  0.674419  , 0.65407926, 0.66761696, 0.74483424, 0.71229106,
                  0.7908634 , 0.7705236 , 0.7854143 , 0.78810567, 0.8206137 ,
                  0.779959  , 0.83549607, 0.79482895, 0.83411205, 0.8164678 ,
                  0.8245834 , 0.78255093, 0.8028555 , 0.76218426, 0.76215523,
                  0.7119658 , 0.7254973 , 0.7051472 , 0.67940396, 0.6834545 ,
                  0.6088561 , 0.62375295, 0.5478037 , 0.549138  , 0.5138889 ,
                  0.5138744 , 0.4487694 , 0.44739988, 0.41484842, 0.39994115,
                  0.40805677, 0.3524327 , 0.27371538])

fm4000 = np.array([  3.1950846,  16.221199 ,  23.840246 ,  29.984638 ,  30.230415 ,
                    37.112137 ,  37.603687 ,  45.714287 ,  51.85868  ,  57.265743 ,
                    63.90169  ,  68.57143  ,  74.47005  ,  78.156685 ,  82.33487  ,
                    88.97082  ,  98.064514 , 108.14132  , 115.02304  , 123.870964 ,
                   128.78648  , 133.21045  , 143.04147  , 151.39784  , 155.08449  ,
                   157.29646  , 160.24577  ])

R4000 = np.array([0.00432277, 0.11383285, 0.23054755, 0.29538906, 0.31123918,
                  0.39337176, 0.41066283, 0.50864553, 0.5907781 , 0.62680113,
                  0.6426513 , 0.65273774, 0.64841497, 0.6440922 , 0.6152738 ,
                  0.5720461 , 0.5158501 , 0.45677233, 0.41210374, 0.3631124 ,
                  0.34149855, 0.3184438 , 0.2795389 , 0.24495678, 0.24783862,
                  0.23919308, 0.24063401])

fm8000 = np.array([  4.6498036,   7.1022663,   8.569778 ,  16.16957  ,  23.037289 ,
                    24.018497 ,  25.735521 ,  27.451048 ,  30.885843 ,  33.578465 ,
                    34.319515 ,  38.48526  ,  40.206398 ,  42.654747 ,  45.355972 ,
                    50.995964 ,  52.953144 ,  55.896774 ,  56.631092 ,  60.54957  ,
                    61.772808 ,  63.238823 ,  66.18058  ,  68.86871  ,  70.58611  ,
                    72.78196  ,  74.744    ,  78.409225 ,  80.61181  ,  82.31723  ,
                    86.23272  ,  87.20532  ,  90.384995 ,  91.11295  ,  96.73499  ,
                   100.39909  , 106.50631  , 117.26071  , 127.28154  , 137.0596   ,
                   145.37276  , 154.66376  , 159.55597  ])

R8000 = np.array ([0,           0.027040243, 0.025672795, 0.082519256, 0.14614701,
                   0.15562384,  0.17186953 , 0.18269515 , 0.21789658 , 0.22329386, 
                   0.24903294,  0.27338803 , 0.30453888 , 0.31129324 , 0.3478559, 
                   0.3952338 ,  0.39521724 , 0.42364773 , 0.42499653 , 0.43986857, 
                   0.4398582 ,  0.4330707  , 0.4547261  , 0.44386315 , 0.46146387,
                   0.43976498,  0.4573636  , 0.44107231 , 0.4437637  , 0.4180039, 
                   0.42203578,  0.40034726 , 0.39761028 , 0.3759238  , 0.35826093, 
                   0.3379046 ,  0.30533242 , 0.2686558  , 0.23334044 , 0.20480223,
                   0.18711658,  0.1667126  , 0.16396113  ])

curve1 = np.interp(fmod,fm125,R125)
curve2 = np.interp(fmod,fm250,R250) 
curve3 = np.interp(fmod,fm500,R500)
curve4 = np.interp(fmod,fm1000,R1000)
curve5 = np.interp(fmod,fm2000,R2000)
curve6 = np.interp(fmod,fm4000,R4000)
curve7 = np.interp(fmod,fm8000,R8000)

plt.figure(num = "Roughness of amplitude-modulated tones")
plt.title("Roughness of amplitude-modulated tones", fontsize = 16, fontweight = 'bold')

fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(fmod, curve1)
axs[0, 0].plot(fmod, curve3)
axs[0, 1].plot(fmod, curve5)
axs[0, 1].plot(fmod, curve7)
axs[1, 0].plot(fmod, curve4)
axs[1, 1].plot(fmod, curve2)
axs[1, 1].plot(fmod, curve6)


    
    
    
    
    
    
    
    
    
    
