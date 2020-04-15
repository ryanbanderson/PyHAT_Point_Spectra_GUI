# This code is used to read individual ChemCam files
# Header data is stored as attributes of the data frame
# White space is stripped from the column names
import os
import gc

import numpy as np
import pandas as pd
import scipy.io as io

from libpyhat.data.io import lookup, file_search
from point_spectra_gui.util.spectral_data import spectral_data


def CCAM_CSV(input_data, ave=True):
    #read the beginning of the file
    header = pd.read_csv(input_data, nrows = 20, engine='c',header=None)

    #count how many rows are commented
    header_rows = header[0].str.contains('#').sum()-1
    df = pd.read_csv(input_data,header=header_rows,engine='c',delimiter=',',index_col=False)
    cols = list(df.columns.values)
    df.columns = [i.strip().replace('# ', '') for i in cols]  # strip whitespace from column names
    df.set_index(['wave'], inplace=True)  # use wavelengths as indices
    metadata = pd.read_csv(input_data, sep='=', nrows=header_rows, comment=',', engine='c', index_col=0, header=None)

    if ave:
        df = pd.DataFrame(df['mean'])
    else:
        try:
            df = df.drop(['mean'], axis=1)
            df = df.drop(['median'], axis=1)

        except:
            pass
    df.index = [['wvl'] * len(df.index),
                df.index.values.round(4)]  # create multiindex so spectra can be easily extracted with a single key
    df = df.T  # transpose so that each spectrum is a row

    # remove extraneous stuff from the metadataindices
    metadata.index = [i.strip().strip('# ').replace(' FLOAT', '').lower() for i in metadata.index.values]
    metadata = metadata.T

    # extract info from the file name
    fname = os.path.basename(input_data)
    metadata['sclock'] = fname[4:13]
    metadata['seqid'] = fname[25:34].upper()
    metadata['Pversion'] = fname[34:36]

    # duplicate the metadata for each row in the df
    if not ave:
        metadata = metadata.append([metadata] * (len(df.index) - 1), ignore_index=True)
    metadata.index = df.index  # make the indices match
    metadata.columns = [['meta'] * len(metadata.columns), metadata.columns.values]  # make the columns into multiindex
    df = pd.concat([metadata, df], axis=1)  # combine the spectra with the metadata
    return df


def CCAM_SAV(input_data, ave=True):
    # read the IDL .SAV file

    data = io.readsav(input_data, python_dict=True)

    # put the spectra into data frames and combine them
    df_UV = pd.DataFrame(data['uv'], index=data['defuv'])
    df_VIS = pd.DataFrame(data['vis'], index=data['defvis'])
    df_VNIR = pd.DataFrame(data['vnir'], index=data['defvnir'])
    df_spect = pd.concat([df_UV, df_VIS, df_VNIR])
    df_spect.columns = ['shot' + str(i + 1) for i in
                        df_spect.columns]  # add 1 to the columns so they correspond to shot number

    df_aUV = pd.DataFrame(data['auv'], index=data['defuv'], columns=['average'])
    df_aVIS = pd.DataFrame(data['avis'], index=data['defvis'], columns=['average'])
    df_aVNIR = pd.DataFrame(data['avnir'], index=data['defvnir'], columns=['average'])
    df_ave = pd.concat([df_aUV, df_aVIS, df_aVNIR])

    df_mUV = pd.DataFrame(data['muv'], index=data['defuv'], columns=['median'])
    df_mVIS = pd.DataFrame(data['mvis'], index=data['defvis'], columns=['median'])
    df_mVNIR = pd.DataFrame(data['mvnir'], index=data['defvnir'], columns=['median'])
    df_med = pd.concat([df_mUV, df_mVIS, df_mVNIR])

    df = pd.concat([df_spect, df_ave, df_med], axis=1)
    # create multiindex to access wavelength values
    # also, round the wavlength values to a more reasonable level of precision
    df.index = [['wvl'] * len(df.index), df.index.values.round(4)]
    # transpose so that spectra are rows rather than columns
    df = df.T
    df[('meta','Shot Number')] = df.index
    # extract metadata from the file name and add it to the data frame
    # use the multiindex label "meta" for all metadata

    pathname,fname = os.path.split(input_data)

    # for some reason, some ChemCam files have the 'darkname' key, others call it 'darkspect'
    # this try-except pair converts to 'darkname' when needed
    try:
        data['darkname']
    except:
        try:
            data['darkname'] = data['darkspec']
        except:
            data['darkname'] = ''


    metadata = [fname,pathname,fname[4:13],fname[25:34].upper(),fname[34:36]]
    metalist = ['continuumvismin','continuumvnirmin','continuumuvmin','continuumvnirend','distt','darkname','nshots',
                'dnoiseiter','dnoisesig','matchedfilter']
    metalist_keep = []
    for name in metalist:
        try:
            metadata.append(data[name])
            metalist_keep.append(name)
        except:
            pass

    metadata = np.tile(metadata, (len(df.index), 1))
    metadata_cols = list(zip(['meta'] * len(df.index), ['file','filepath',
                                                        'sclock',
                                                        'seqid',
                                                        'Pversion']+metalist_keep))
    try:
       metadata = pd.DataFrame(metadata, columns=pd.MultiIndex.from_tuples(metadata_cols), index=df.index)
       df = pd.concat([metadata, df], axis=1)
    except:
        pass

    if ave == True:
        df = df.loc['average']
        df = df.to_frame().T
    else:
        pass

    return df

def ccam_batch(directory, searchstring='*.csv', to_csv=None, lookupfile=None, ave=True, left_on = 'sclock', right_on='Spacecraft Clock',versioncheck=True):
    # Determine if the file is a .csv or .SAV
    if 'sav' in searchstring.lower():
        is_sav = True
    else:
        is_sav = False
    filelist = file_search(directory, searchstring)
    if len(filelist)==0:
        print('No files found in '+directory+' using search string '+searchstring)
        return
    basenames = np.zeros_like(filelist)
    sclocks = np.zeros_like(filelist)
    P_version = np.zeros_like(filelist, dtype='int')

    if versioncheck==True:
        # Extract the sclock and version for each file and ensure that only one
        # file per sclock is being read, and that it is the one with the highest version number
        for i, name in enumerate(filelist):
            basenames[i] = os.path.basename(name)
            sclocks[i] = basenames[i][4:13]  # extract the sclock
            P_version[i] = basenames[i][-5:-4]  # extract the version

        sclocks_unique = np.unique(sclocks)  # find unique sclocks
        filelist_new = np.array([], dtype='str')
        for i in sclocks_unique:
            match = (sclocks == i)  # find all instances with matching sclocks
            maxP = P_version[match] == max(P_version[match])  # find the highest version among these files
            filelist_new = np.append(filelist_new, filelist[match][maxP])  # keep only the file with thei highest version

        filelist = filelist_new

    filecount = 0
    workinglist = []
    subcount = 0


    for i, file in enumerate(filelist):
        filecount = filecount + 1
        print('File #'+str(filecount)+' of '+str(len(filelist)))
        print(file)
        if is_sav:
            tmp = CCAM_SAV(file, ave=ave)
        else:
            tmp = CCAM_CSV(file, ave=ave)
        try:
            # This ensures that rounding errors are not causing mismatches in columns
            cols1 = list(combined['wvl'].columns)
            cols2 = list(tmp['wvl'].columns)
            if set(cols1) == set(cols2):
                combined = pd.concat([combined, tmp])
            else:
                print("Wavelengths don't match!")
        except:
            combined = tmp
        # if doing single shots, save out the data every 50 files so that the program doesn't run out of memory
        if filecount % 50 == 0 and ave == False:
            workingfilename = 'temporary_data_files_'+str(subcount)+'-'+str(filecount)+'.csv'
            workinglist.append(workingfilename)
            combined.to_csv(workingfilename)
            subcount = filecount
            del combined
            gc.collect()

        pass
    if ave == False:
        for f in workinglist:
            pass
        

    try:
        combined.loc[:, ('meta', 'sclock')] = pd.to_numeric(combined.loc[:, ('meta', 'sclock')])
    except:
        pass

    if lookupfile is not None:
        try:
            combined = lookup(combined, lookupfile=lookupfile, left_on=left_on, right_on=right_on, skiprows=1)
        except:
            combined = lookup(combined, lookupfile=lookupfile, left_on=left_on, right_on=right_on, skiprows=0)
    if to_csv is not None:
        combined.to_csv(to_csv)
    return spectral_data(combined)
