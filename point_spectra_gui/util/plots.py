# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 13:09:21 2016

@author: rbanderson
"""
import numpy as np
from matplotlib import pyplot as plot

from point_spectra_gui.util import colormaps


def cmaps():
    plot.register_cmap(name='viridis', cmap=colormaps.viridis)
    plot.register_cmap(name='magma', cmap=colormaps.magma)
    plot.register_cmap(name='inferno', cmap=colormaps.inferno)
    plot.register_cmap(name='plasma', cmap=colormaps.plasma)


def make_plot(x, y, figpath, figfile=None, xrange=None, yrange=None, xtitle='Reference (wt.%)', colorvar = 'None',
              colorval = None, ytitle='Prediction (wt.%)', title=None,
              lbl='', one_to_one=False, rmse=True, dpi=1000, color=None, annot_mask=None, cmap=None, colortitle='',
              loadfig=None, masklabel='', marker='o', linestyle='None', hline=None, hlinelabel=None, hlinestyle='--',
              yzero=False, linewidth=0.2, vlines=None):
    if loadfig is not None:
        fig = loadfig
        axes = fig.gca()
    else:
        fig = plot.figure()

        axes = fig.gca()
        if title:
            fig.suptitle(title)
        if xtitle:
            axes.set_xlabel(xtitle)
        if ytitle:
            axes.set_ylabel(ytitle)
        if xrange:
            axes.set_xlim(xrange)
            xind = np.where((x > xrange[0]) & (x < xrange[1]))
        if yrange:
            axes.set_ylim(yrange)
        else:
            yrange = [np.min(np.array(y)[xind]), np.max(np.array(y)[xind])]
            axes.set_ylim(yrange)
    if hline:
        axes.axhline(hline, color='k', label=hlinelabel, linestyle=hlinestyle)
    if vlines:
        for x in vlines:
            axes.axvline(x, color='k', linestyle='--')
    if one_to_one:
        axes.plot([0, 100], [0, 100], color='k')
        if rmse:
            rmse_val = np.sqrt(np.mean((y - x) ** 2))
            lbl = lbl + ' (RMSE=' + str(round(rmse_val, 2)) + ')'

    # if cmap is not None:
    #     axes.plot(x, y, c=color, cmap=cmap, marker=marker, markeredgecolor='Black', markeredgewidth=0.25)
    #     axes.colorbar(label=colortitle)
    # else:
    #     axes.plot(x, y, color=color, label=lbl, marker=marker, ls=linestyle, linewidth=linewidth,
    #               markeredgecolor='Black', markeredgewidth=0.25)
    #
    #     if annot_mask is not None:
    #         axes.plot(x[annot_mask], y[annot_mask], facecolors='none', linewidth=linewidth, label=masklabel,
    #                   marker=marker, markeredgecolor='Black', markeredgewidth=2)

    if colorvar != 'None':
        try:
            mappable = axes.scatter(np.squeeze(x), np.squeeze(y), c=colorval, cmap=cmap, linewidth=0.2, edgecolor='Black',
                                    marker = marker)
        except:
            pass
            # try:
            #     mappable = axes.scatter(np.squeeze(x), np.squeeze(y), c=colorval, cmap=cmap, linewidth=0.2, edgecolor='Black')
            # except:
            #     pass
            # except:
            #     try:
            #         mappable = axes.scatter(np.squeeze(x), np.squeeze(y), c=data.df[('K-Means', colorvar)], cmap=cmap,
            #                            linewidth=0.2, edgecolor='Black')
            #     except:
            #         try:
            #             mappable = axes.scatter(np.squeeze(x), np.squeeze(y), c=data.df[('Spectral', colorvar)],
            #                                    cmap=cmap,
            #                                    linewidth=0.2, edgecolor='Black')
            #         except:
            # TODO: handle any top-level label for colorval and clean up these nested try/excepts
        fig.colorbar(mappable, label=colorvar, ax=axes)
    elif colorvar == 'None':
        axes.plot(x, y, markeredgecolor='Black', markeredgewidth=0.25, label=lbl, color = color, linestyle=linestyle, marker=marker,linewidth=linewidth)
        if lbl != '':
            axes.legend(loc='best', fontsize=8, scatterpoints=1, numpoints=1)

    if yzero:
        axes.set_ylim(bottom=0)


    if figpath and figfile:
        fig.savefig(figpath + '/' + figfile, dpi=dpi)
    return fig


def pca_ica_plot(data, x_component, y_component, dimred_obj, colorvar=None, cmap='viridis', method='PCA', figpath=None,
                 figfile=None):
    cmaps()
    x_label = ''
    y_label = ''
    x = [data.df[(method, x_component)]]
    y = [data.df[(method, y_component)]]
    xcomp_num = x_component.split('-')[-1]
    ycomp_num = y_component.split('-')[-1]
    pass
    if method == 'PCA':
        x_loading = dimred_obj.components_[int(xcomp_num) - 1, :]
        y_loading = dimred_obj.components_[int(ycomp_num) - 1, :]

        x_variance = dimred_obj.explained_variance_ratio_[int(xcomp_num) - 1] * 100
        y_variance = dimred_obj.explained_variance_ratio_[int(ycomp_num) - 1] * 100
        x_label = 'PC ' + str(xcomp_num) + ' (' + str(round(x_variance, 1)) + r'%)'
        y_label = 'PC ' + str(ycomp_num) + ' (' + str(round(y_variance, 1)) + r'%)'
    if method == 'FastICA':
        x_loading = dimred_obj.components_[int(xcomp_num) - 1, :]
        y_loading = dimred_obj.components_[int(ycomp_num) - 1, :]
        x_label = 'Source ' + str(xcomp_num)
        y_label = 'Source ' + str(ycomp_num)

    if method == 'JADE-ICA':
        x_loading = dimred_obj.ica_jade_loadings[int(xcomp_num) - 1, :].T
        y_loading = dimred_obj.ica_jade_loadings[int(ycomp_num) - 1, :].T
        x_label = 'Source ' + str(xcomp_num)
        y_label = 'Source ' + str(ycomp_num)

    # set up the subplots
    fig = plot.figure()
    fig.set_size_inches(10, 4)
    ax1 = fig.add_subplot(2, 2, (1, 3))
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 4, xlabel='Wavelength (nm)')

    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label)

    pass
    if colorvar:
        for label in data.df.columns.levels[0]:
            if (label,colorvar) in data.df:
                mappable = ax1.scatter(np.squeeze(x), np.squeeze(y), c=data.df[(label, colorvar)], cmap=cmap,
                                       linewidth=0.2, edgecolor='Black')
                fig.colorbar(mappable, label=colorvar, ax=ax1)
            else:
                pass

    else:
        ax1.scatter(x, y, linewidth=0.2, edgecolor='Black')

    # plot the loadings
    wvls = data.df['wvl'].columns.values
    ax2.plot(wvls, x_loading, linewidth=0.5)
    ax3.plot(wvls, y_loading, linewidth=0.5)

    ax2.set_yticklabels([])
    ax2.set_xticklabels([])
    ax2.set_ylabel(x_label)

    ax3.set_yticklabels([])
    ax3.set_ylabel(y_label)

    fig.subplots_adjust(hspace=0)

    if figpath and figfile:
        fig.savefig(figpath + '\\' + figfile, dpi=1000)

# def stratifiedfoldshist(data, datakey, colname, folds):
#     #datakey = self.chooseDataToStratifyComboBox.currentText()
#     #colname = ('comp', self.chooseVarComboBox.currentText())
#     #folds = data[datakey].df[('meta', 'Folds')]
#     folds_unique = folds.unique()[np.isfinite(folds.unique())]
#     for fold in folds_unique:
#         dat_col_folds = data[datakey].df[colname][folds == fold]
#         plot.hist(dat_col_folds, bins=20)
#         plot.xlabel(colname[1])
#         plot.ylabel('Frequency')
#         plot.title('Histogram of Fold ' + str(int(fold)))
#         #plt.axis([0, 100, 0, 100])
#         #plt.grid(True)
#         plot.show()
#         plot.savefig(outpath + '//' + colname[1] + '_fold' + str(int(fold)) + '_hist.png')
#         plot.clf()