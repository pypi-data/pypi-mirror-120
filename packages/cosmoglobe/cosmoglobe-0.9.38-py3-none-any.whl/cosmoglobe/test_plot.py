
from cosmoglobe.plot.plottools import standalone_colorbar
from cosmoglobe.plot import plot, gnom, trace
from cosmoglobe.h5.model import model_from_chain
from cosmoglobe.h5.chain import Chain
from astropy import constants as const
import numpy as np 
import healpy as hp 
import astropy.units as u
import matplotlib.pyplot as plt
import os

paperfigs='/Users/svalheim/work/BP/papers/09_leakage/figs/'
path='/Users/svalheim/work/cosmoglobe-workdir/'
chain='bla.h5'
dust='dust_c0001_k000200.fits'

def transform(m):
    y = m/100
    y[y > 1] = np.log10(y[y>1]) + 1
    return y

def f(nu):
    return 1/(const.c.value**2 / 2. / const.k_B.value / (nu * 1e9) **2 * 1e-26 * 1e6)

def f2(nu):
    return (nu/22)**-3

if True:
    model = model_from_chain(path+chain, components=["dust"], nside=16)
    plot(model)
    plt.show()

if True:
    plot(path+chain, comp="dust", nside=16, )
    plt.show()
    #plot(path+dust, comp="dust", nside=16, )

if True:
    plot(path+dust, comp="dust",  sig="U", interactive=True) 
    plt.show()

if True:
    plot(path+dust, sig="Q", ticks=[0, np.pi, None], norm="log", unit=u.uK, fwhm=14*u.arcmin, nside=512, cmap="chroma", left_label="Pee", right_label="Poo", title="Cool figure", width=7, graticule=True, projection_type="hammer", mask=path+"mask_common_dx12_n0512_TQU.fits", maskfill="pink", graticule_color="white", xtick_label_color="white", ytick_label_color="white",)# darkmode=True)
    plt.show()

if True:
    plot(path+dust, interactive=True, sig="Q", ticks=[0, np.pi, None], norm="log", unit=u.uK, fwhm=14*u.arcmin, nside=512, cmap="chroma", left_label="Pee", right_label="Poo", title="Cool figure", width=7, graticule=True, projection_type="hammer", mask=path+"mask_common_dx12_n0512_TQU.fits", maskfill="pink", graticule_color="white", xtick_label_color="white", ytick_label_color="white",)# darkmode=True)
    plt.show()

if True:
    plot(path+dust, comp="cmb", sig="Q", ticks=[0, np.pi, None], norm="log", unit=u.uK, fwhm=14*u.arcmin, nside=512, cmap="chroma", left_label="Pee", right_label="Poo", title="Cool figure", width=7, graticule=True, projection_type="hammer", mask=path+"mask_common_dx12_n0512_TQU.fits", maskfill="pink", graticule_color="white", xtick_label_color="white", ytick_label_color="white",)# darkmode=True)
    plt.show()

if True:
    m = hp.read_map(path+dust, field=1)
    plot(m, comp="dust",  sig="U") 
    plt.show()

if True:
    gnom(path+dust, comp="dust", subplot=(2,2,1), cbar_pad=0.0, cbar_shrink=0.7)
    gnom(path+dust, comp="dust", subplot=(2,2,2), cbar_pad=0.0, cbar_shrink=0.8)
    gnom(path+dust, comp="dust", subplot=(2,2,3), cbar_pad=0.0, cbar_shrink=0.9)
    gnom(path+dust, comp="dust", subplot=(2,2,4), cbar_pad=0.0, cbar_shrink=1)
    plt.show()


if True:
    os.system(f'cosmoglobe gnom {path}{dust} -lon 30 -lat 70 -comp freqmap -ticks auto -freq 70 -show')
    os.system(f'cosmoglobe plot {path}{dust} -comp freqmap -range 0.5 -freq 70 -show')
    os.system(f'cosmoglobe trace {path}{chain} -labels "1 2 3 4" -dataset synch/beta_pixreg_val -show')

if True:
    #c = Chain(path+chain)
    #print(c["000001/tod/023-WMAP_K/chisq"])
    trace(path+chain, figsize=(10,2), sig=0, labels=["Reg1","Reg2","Reg3","Reg4"], dataset="synch/beta_pixreg_val", subplot=(3,1,1), ylabel=r"$\beta_s^T$")
    trace(path+chain, sig=1, labels=["Reg1","Reg2","Reg3","Reg4"], dataset="synch/beta_pixreg_val", subplot=(3,1,2), ylabel=r"$\beta_s^P$")
    trace(path+chain, dataset="tod/023-WMAP_K/bp_delta", subplot=(3,1,3), ylabel=r"$\Delta_{bp}$")
    #trace(path+chain, dataset="tod/023-WMAP_K/chisq", subplot=(5,1,4), ylabel=r"$\chi^2$")
    #trace(path+chain, dataset="tod/023-WMAP_K/gain", subplot=(5,1,5), ylabel="gain", xlabel="Gibbs sample")
    plt.show()
    

if False:    
    standalone_colorbar("planck", ticks=[-0.1,0,0.1], unit=u.uK)
    plt.savefig(paperfigs+"colorbar_planck_pm0.1.pdf", bbox_inches = 'tight', pad_inches = 0)
    
    standalone_colorbar("planck", ticks=[-5,0,5], unit=u.uK)
    plt.savefig(paperfigs+"colorbar_planck_pm5.pdf", bbox_inches = 'tight', pad_inches = 0)

    standalone_colorbar("planck", ticks=[-3,0,3], unit=u.uK)
    plt.savefig(paperfigs+"colorbar_planck_pm3.pdf", bbox_inches = 'tight', pad_inches = 0)

    standalone_colorbar("planck", ticks=[-1,0,1], unit=u.uK)
    plt.savefig(paperfigs+"colorbar_planck_pm1.pdf", bbox_inches = 'tight', pad_inches = 0)

    standalone_colorbar("planck", ticks=[-10,0,10], unit=u.uK)
    plt.savefig(paperfigs+"colorbar_planck_pm10.pdf", bbox_inches = 'tight', pad_inches = 0)

"""
sky = model_from_chain(path+chain, nside=256,)
if False:
    for i, freq in enumerate([200,]): #enumerate([353,]):
        #outname = f'{str(int(freq)).zfill(4)}GHz.png'
        if freq > 180:
            s = f(freq)*1e-3
        elif freq < 20:
            s = f2(freq)
        else:
            s=1

        #s = 1/(f(freq)*1e-3) if freq > 180 else 1
        if freq < 353:
            if freq > 250:
                r = ((353-freq)/(353-250))*67
            else:
                r = 67

        else:
            r = 0
        cmb = hp.remove_dipole(sky(cmb, freq*u.GHz,)[0].value, gal_cut=30)
        fsky = hp.remove_dipole(sky(freq*u.GHz,)[0].value, gal_cut=30, copy=True)
        print(np.median(fsky))
        #fsky2 = transform(fsky[0])
        #plt.show()
        print(s,)
        plot(fsky, norm="log", remove_mono=True, cmap="planck", title=f'{freq:.0f} GHz',)
        plt.show()
        plot((fsky+1e6)*s, ticks=[-1e3, -100, 0, 100, 1e3, 1e7], norm="log", remove_mono=True, cmap="planck_log", title=f'{freq:.0f} GHz',)
        plt.show()
"""