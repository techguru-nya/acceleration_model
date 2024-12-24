#!/usr/bin/env python
# coding: utf-8

# # Import

# In[1]:


import os
import sys
import datetime
import time
import subprocess

import glob

import shutil

import pandas as pd
import numpy
import numpy as np

import datetime

import zipfile

import matplotlib.pyplot as plt

import utils_1 as Read_DCM_4

SAMPLING = 0.005


# # Convert ZIP(D97-->CSV)

# ## ReadComment

# In[3]:


def ReadComment(File):
    Comment = ''
    
    try:
        try:
            with zipfile.ZipFile(File) as zf:
                lst = zf.namelist()

                text = None

                for name in lst:
                    if ".par" not in name and ".TXT" in name:
                        data = zf.read(name)
                        Comment = OutputText(str(data))

        except BadZipFile:
            1
    except NameError:
         Comment = ''

    return Comment


def OutputText(A):
    B = A.split("\\r\\n")
    i = 0
    C = ""
    for b in B:
        if i < 8:
            C += b + ", "
            i += 1

    D = C.replace("b'", "")

    return D


# In[4]:


def RemoveTemp(file):
    is_file = os.path.isfile(file)
    
    if is_file:
        os.remove(file)


def MakePLT(Path0):
    Path1 = Path0 + "Temp.PLT"

    Text = ""
    for S in d_SIGNAL_PLT:
        Text += S + " key="+ d_SIGNAL_PLT[S] + "\n"

    f = open(Path1, "w")
    f.write(Text)
    f.close()

    return Path1


# ## DataTreatment

# In[5]:


def DataTreatment(File, d_Plt, Folder, Sampling):
    Csv = None
    NotConvert = False
    
    root, ext = os.path.splitext(File)
    if (ext == ".ZIP" or ext == ".zip") and "ApplContainer" not in File:
        d97 = UnPackD97(File)

        if d97 != None:
            Plt_new, d_Plt_new, NotAll = MakePLTFromD97(d97, d_Plt)
            
            if Plt_new != None:
                Csv = RunBat(d97, Plt_new, d_Plt_new, Sampling)
                
                dirname, basename = os.path.split(Csv)
                Csv_ = Folder + basename
                os.replace(Csv, Csv_)
            else:
                Csv = None
            
            if Csv == None or NotAll == True:
                NotConvert = True
                
        try:
            Remove_w_ExistFile(d97)
        except TypeError:
            print('TypeError:', File, d97)
            
    return Csv, NotConvert


def UnPackD97(file):
    file_d97 = None
    file_in_zip = ''
    
    dirname, basename = os.path.split(file)
    dirname_ = dirname + '/'
    
    try:
        try:
            with zipfile.ZipFile(file) as zf:
                lst = zf.namelist()

                for file_in_zip in lst:
                    root, ext = os.path.splitext(file_in_zip)
                    if ext == ".D97" or ext == ".d97":  
                        # shutil.unpack_archive(file, dirname_, format='zip')
                        
                        with zipfile.ZipFile(file) as existing_zip:
                            existing_zip.extract(file_in_zip, dirname_)
                            
                        file_d97 = file_in_zip
                        break
                        
        except BadZipFile:
            file_d97 = None
    except NameError:       
        if file_in_zip != '':
            Remove_w_ExistFile(Folder + file_in_zip)
            
        file_d97 = None
    
    if file_d97 != None:
        file_out = UnPackD97__Change_FileName(dirname_, file, file_d97)
    else:
        file_out = None
    
    return file_out


def UnPackD97__Change_FileName(Folder, ZIP, D97):    
    # path = Folder + D97
    root, ext = os.path.splitext(ZIP)
    path_new = root + '.D97'
    
    dirname, basename = os.path.split(ZIP)
    path_base = dirname + '/' + D97
    # path_new = Folder + file_name
    
    # print(path_base, path_new)
    if path_new != path_base:
        if os.path.exists(path_new) == True:
            os.remove(path_new)
            
        os.rename(path_base, path_new)
    
    return path_new   


def RunBat(file_, Plt, d_Plt, Sampling):
    dirname, basename = os.path.split(file_)
    file = basename
    
    if ".D97" in file:
        CSV = file.replace(".D97", ".CSV")
    elif ".d97" in file:
        CSV = file.replace(".d97", ".CSV")

    Bat = dirname + "ChangeFormat.bat"
    File0 = dirname + '/' + file
    File1 = dirname + '/' + "1__" + file
    File2 = dirname + '/' + "2__" + file
    File3 = dirname + '/' + "3__" + CSV

    # Text = "MDFDSET3c ifn=" + File0 + ";pltfn=" + Plt + " ofn=" + File1 + "\n"
    Text = "MDFDSET6c ifn=" + File0 + ";pltfn=" + Plt + " ofn=" + File1 + "\n"
    # Text = "MDFMDL6c ifn=" + File0 + " ofn=" + File1 + " INCLUDE_SG=" + Plt + "\n" 
    Text += "MDFMDL6c ifn=" + File1 + " ofn=" + File2 + " tc=" + str(Sampling) + "\n"
    Text += "SDTM3c ifn=" + File2 + " ofn=" + File3
    
    f = open(Bat, "w")
    f.write(Text)
    f.close()

    res = subprocess.run([Bat], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    Remove_w_ExistFile(File0)
    Remove_w_ExistFile(File1)
    Remove_w_ExistFile(Bat)

    try:        
        FileOut = ModifyCSV(File3, d_Plt)
        Remove_w_ExistFile(File2)
        Remove_w_ExistFile(File3)
        Remove_w_ExistFile(Plt)
        
    except FileNotFoundError:
        # dirname, basename = os.path.split(file)
        root, ext = os.path.splitext(file_)
        Plt_ = root + '.PLT'
        Bat_ = root + '.bat'
        
        os.rename(Plt, Plt_)
        
        root, ext = os.path.splitext(File0)
        File0_ = root + '_.D97'
        File3_ = root + '.csv'
        
        # DFMDL6c ifn=c:/TSDE_Workarea/ktt2yk/Work/CarSim/SIM_ABS_Ice/ABS_Ice_N_Spike_base_.D97 t0=1 t1=23 ofn=c:/TSDE_Workarea/ktt2yk/Work/CarSim/SIM_ABS_Ice/1__ABS_Ice_N_Spike_base.D97
        Text_ = "MDFMDL6c ifn=" + File0 + " t0=0 t1=30" + " ofn=" + File0_ + "\n"
        Text_ += "MDFDSET3c ifn=" + File0_ + ";pltfn=" + Plt_ + " ofn=" + File1 + "\n"
        Text_ += "MDFMDL6c ifn=" + File1 + " ofn=" + File2 + " tc=" + str(Sampling) + "\n"
        Text_ += "SDTM3c ifn=" + File2 + " ofn=" + File3_
        
        f = open(Bat_, "w")
        f.write(Text_)
        f.close()
        
        print("FileNotFoundError", Bat_, Plt_)
        FileOut = None

    return FileOut


def ChangePath(Folder0, File0):
    FILE1 = File0.split("/")
    File = Folder0 + FILE1[-1]
    Folder = Folder0 + FILE1[-2]
    
    return File, Folder, FILE1[-1]


def ModifyCSV(File, d_Plt):
    for i, S in enumerate(d_Plt):
        if i == 0:
            Text_PLT = "TIME" + "," + d_Plt[S]
        else:
            Text_PLT += "," + d_Plt[S]

    with open(File) as f:
        Text_CSV = f.read()

    Text = Text_PLT + "\n" + Text_CSV
    Text = Text.replace(",", "\t")

    f = open(File, "w")
    f.write(Text)
    f.close()
    
    df = pd.read_table(File, sep="\t", index_col=0, skiprows=[1])
    
    dirname, basename = os.path.split(File)
    File2 = dirname + '/' + basename.replace("3__", "")
    # File2 = File2.replace(".CSV", ".csv")
    
    basename_without_ext = os.path.splitext(os.path.basename(File2))[0]
    dirname, basename = os.path.split(File2)
    # now = datetime.datetime.now()
    # FileOut = dirname + '\\' + basename_without_ext + '_' + now.strftime('%Y%m%d_%H%M%S') + '.csv'
    FileOut = dirname + '/' + basename_without_ext + '.csv'
    df.to_csv(FileOut)

    # ExistFile(FileOut)

    return FileOut


def Remove_w_ExistFile(PathFile):
    if os.path.exists(PathFile) == True:
        os.remove(PathFile)


# ##  MakePLTFromD97

# In[6]:


def MakePLTFromD97(File_D97, d_Plt):
    l_Signals_new = []
    d_Plt_new = {}
    
    dirname, basename = os.path.split(File_D97)
    dirname_ = dirname + '/'
    
    D97 = File_D97

    if os.path.exists(D97) == True:
        l_Signals_D97 = ReadD97(D97)
        l_Signals_PLT = list(d_Plt.keys())
        
        for T in l_Signals_PLT:
            if T in l_Signals_D97:
                l_Signals_new.append(T)
            else:
                Error = "Error: " + T + " is nothing."
                # print(Error)

        d_Plt2 = {}
        for S in d_Plt:
            if d_Plt[S] in d_Plt2:
                d_Plt2[d_Plt[S]] = d_Plt2[d_Plt[S]] + [S]
            else:
                d_Plt2[d_Plt[S]] = [S]

        # print(1, d_Plt2)
        NotAll = False
        for S in d_Plt2:
            Found = False
            
            for S1 in d_Plt2[S]:
                if S1 in l_Signals_new:
                    d_Plt_new[S1] = S
                    Found = True
                    break
            
            if Found == False:
                NotAll = True
                    
        # print(2, d_Plt_new)

        Text = ""
        for T in d_Plt_new:
            Text += T + "\n"
        
        # print(3, Text)
                
        Plt_new = dirname_ + 'Temp.PLT'
        
        if Text != "":
            f = open(Plt_new, 'w')
            f.write(Text)
            f.close()
        else:
            Plt_new = None
            d_Plt_new = None
            NotAll = False
    else:
        Plt_new = None    
        d_Plt_new = None
        NotAll = False

    return Plt_new, d_Plt_new, NotAll


def ReadD97(Path):
    Out = []

    #f=open(Path, 'r', encoding="utf_8")
    f = open(Path, 'rb')

    i = 2
    while True:
        line_b = f.readline()
        line = str(line_b)

        # if "[SIGNAL0]" not in line and "[SIGNAL" in line:
        if "[SIGNAL" in line:
            i = 0

        if i == 1 and "NAME=" in line:
            T = line.replace("NAME=", "")
            T = T.replace("\n", "")
            T = T.replace("b'", "")
            T = T.replace("'", "")
            T = T.replace("\\", "*")
            T = T.replace("*r*n", "")

            Out.append(T)

        if "[DATA]" in line:
            break

        i += 1

    f.close()

    return Out


# ## MakeTraceList

# In[3]:


def MakeTraceList(l_Folder, l_Ext, l_Ext_wo):
    print(l_Folder)
    
    l_Traces = []
    
    for Folder in l_Folder:
        for current, subfolders, subfiles in os.walk(Folder):
            for file in subfiles:
                if "ApplContainer" not in file:
                    for Ext_ in l_Ext:
                        if Ext_ in file: 
                            Trace = current + '/'+ file
                            l_Traces.append(Trace)
                            break
    
    l_Traces_ = []
    for T in l_Traces:
        Delete = False
        for Ext in l_Ext_wo:
            if Ext in T:
                Delete = True
                break
                
        if Delete == False:
            l_Traces_.append(T)

    return l_Traces_


def CopyMeasurement(df, Folder):
    df1 = df.dropna(subset=["File"])
    L_Measurement = list(df1["File"])

    L_Measurement_New = []

    i = 0
    for Path in L_Measurement:
        FileName = os.path.basename(Path)

        Path1 = Folder + FileName
        if Path1 not in L_Measurement_New:
            L_Measurement_New.append(Path1)
        else:
            FileName1 = FileName.replace(".zip", "")
            FileName1 = FileName1.replace(".ZIP", "")
            Folder_new = Folder + FileName1 + "_" + str(i)
            os.mkdir(Folder_new)
            Path1 = Folder_new + "/" + FileName
            L_Measurement_New.append(Path1)
        i += 1

    i = 0
    for M in L_Measurement:
        try:
            shutil.copy(M, L_Measurement_New[i])
        except FileNotFoundError:
            0
        i += 1


# ## Select_Signal
# - D97ファイルをCSV変換するためのPLT作成で使用する信号
# - PLTから計測信号を設定する。

# In[4]:


def Select_Signal(File):
    d_Signal = {}
    
    f = open(File, 'r', encoding="ascii")
    l_line_plt = f.readlines()

    for line in l_line_plt:
        line = line.replace("\n", "")
        l_line = line.split(" ")

        if l_line[0] != "" and "~" not in l_line[0] and "//" not in l_line[0] and "+" not in l_line[0] and "*" not in l_line[0]:
            d_Signal[l_line[0]] = GetKey(l_line)

    f.close()

    return d_Signal


def GetKey(l_in):
    Out = l_in[0]
    
    for Text in l_in:
        l_Text = Text.split("=")
        
        if l_Text[0] == "key":
            Out = l_Text[1]
            
    return Out


# ## SaveData, ReadData

# In[9]:


def SaveData(Data1, Data2, File):
    # basename_without_ext = os.path.splitext(os.path.basename(File))[0]
    # dirname, basename = os.path.split(File)
    root, ext = os.path.splitext(File)
    now = datetime.datetime.now()
    File_new = root + '___' + now.strftime('%Y%m%d_%H%M%S') + ext
    
    print('Save:', File_new)
    pd.to_pickle((Data1, Data2), File_new)
    
    return File_new


def ReadData(File):
    # basename_without_ext = os.path.splitext(os.path.basename(File))[0]
    dirname, basename = os.path.split(File)
    root, ext = os.path.splitext(File)
    # now = datetime.datetime.now()
    
    l_Files = os.listdir(dirname)
    l_date = []
    
    for F in l_Files:
        root1, ext1 = os.path.splitext(dirname + '/' + F)
        dirname1, basename1 = os.path.split(dirname + '/' + F)
        
        if ext == ext1:
            if '___' in basename1:
                l_basename1 = basename1.split('___')
                basename0, ext0 = os.path.splitext(basename)

                if basename0 == l_basename1[0]:                
                    date = l_basename1[-1]
                    date1, date1_ext = os.path.splitext(date)
                    l_date.append(date1)
                    # print(2, date)
                
    l_date.sort()
    print(l_date)
    
    File_new = root + '___' + l_date[-1] + ext
    
    print('Read:', File_new)
    Data1, Data2 = pd.read_pickle(File_new)
    
    return Data1, Data2


# ## SAVE_ZIP_to_CSV

# In[16]:


def SAVE_ZIP_to_CSV(d_Plt, Folder_In, Folder_Out, Sampling):
    d_Csvs = {}
    l_None = []
    
    l_Traces = MakeTraceList(Folder_In, ['.ZIP', '.zip'], [])
    
    # for Zip in l_Traces:
    for i, Zip in enumerate(l_Traces):
        Size = os.path.getsize(Zip)
        print(i + 1, '/', len(l_Traces), ';', Zip, Size)
        
        Csv, NotConvert = DataTreatment(Zip, d_Plt, Folder_Out, Sampling)
        Text = ReadComment(Zip)
        
        if Csv != None:
            d_Csvs[Zip] = (Text, Csv, Size)
        
        if NotConvert == True:
            l_None.append(Zip)
    
    return d_Csvs, l_None


# ## Run 

# In[17]:


# SEARCH_PATH = ['c:/TSDE_Workarea/ktt2yk/Work/Traces/Honda-e/Winter_Fix/2023_0216__PT_OffsetLogic_v3/', 'c:/TSDE_Workarea/ktt2yk/Work/Traces/Honda-e/Winter_Fix/2023_0223__PT_OffsetLogic_V4/', 'c:/TSDE_Workarea/ktt2yk/Work/Traces/Honda-e/Winter_Fix/2023_0309_4Katosan/']
# OUT_PATH = 'c:/TSDE_Workarea/ktt2yk/Work/Traces/XT1E/SIM/Winter_Fix/SIM_Vehicle/'
# PLT_SIMOUT_CONVERT = 'c:/TSDE_Workarea/ktt2yk/Work/PLT/MTCS_MEDC_SIMOUT_1CH_w_MM6.PLT'

# d_SIGNAL_PLT = Select_Signal(PLT_SIMOUT_CONVERT)
# d_CSVs, l_Not_Convert = SAVE_ZIP_to_CSV(d_SIGNAL_PLT, SEARCH_PATH, OUT_PATH, SAMPLING)


# # Modify Signal

# ## Modify_Signal_CSSIM_INPUT

# In[79]:


def Modify_Signal_CSSIM_INPUT(l_Traces, File):
    l_Out = []
    
    d_Parameter = Read_DCM_4.Read_DCM(File)
    Abrollumfang_VA = d_Parameter['Abrollumfang_VA'][2][0]
    Abrollumfang_HA = d_Parameter['Abrollumfang_HA'][2][0]
    
    for Csv in l_Traces:
        print(Csv)
        df = pd.read_table(Csv, sep=",", index_col=None)
        
        # df['nMotNET_TRC'] = df['nMotNET_TRC'] / (2 * 3.14 / 60)        
        df['Ays'] = df['Ays'] * (-1)
        df['Yrs'] = df['Yrs'] * (-1)
        df['v_FL'] = df['v_FL'] * 3.6 * ((1000 / 3600) / Abrollumfang_VA * 60)
        df['v_FR'] = df['v_FR'] * 3.6 * ((1000 / 3600) / Abrollumfang_VA * 60)
        df['v_RL'] = df['v_RL'] * 3.6 * ((1000 / 3600) / Abrollumfang_HA * 60)
        df['v_RR'] = df['v_RR'] * 3.6 * ((1000 / 3600) / Abrollumfang_HA * 60)
        # df['SasInCor'] = df['SasInCor'] * (-1) * 180 / 3.14
        # df['p_MC_Model'] = df['p_MC_Model'] * 10
        
        # if 'nMotNET_SMU' in df.columns:
        #     df['nMotNET_SMU'] = df['nMotNET_SMU'] / (2 * 3.14 / 60)
        
        root, ext = os.path.splitext(Csv)
        Csv_ = root + '_mod' + ext
        df.to_csv(Csv_, header=False, index=False)
        
        l_Out.append(Csv_)
        
    return l_Out


# In[79]:


def Modify_Signal_CSSIM_INPUT_pMC_10(l_Traces, File):
    l_Out = []
    
    d_Parameter = Read_DCM_4.Read_DCM(File)
    Abrollumfang_VA = d_Parameter['Abrollumfang_VA'][2][0]
    Abrollumfang_HA = d_Parameter['Abrollumfang_HA'][2][0]
    
    for Csv in l_Traces:
        print(Csv)
        df = pd.read_table(Csv, sep=",", index_col=None)
        
        # df['nMotNET_TRC'] = df['nMotNET_TRC'] / (2 * 3.14 / 60)        
        df['Ays'] = df['Ays'] * (-1)
        df['Yrs'] = df['Yrs'] * (-1)
        df['v_FL'] = df['v_FL'] * 3.6 * ((1000 / 3600) / Abrollumfang_VA * 60)
        df['v_FR'] = df['v_FR'] * 3.6 * ((1000 / 3600) / Abrollumfang_VA * 60)
        df['v_RL'] = df['v_RL'] * 3.6 * ((1000 / 3600) / Abrollumfang_HA * 60)
        df['v_RR'] = df['v_RR'] * 3.6 * ((1000 / 3600) / Abrollumfang_HA * 60)
        # df['SasInCor'] = df['SasInCor'] * (-1) * 180 / 3.14
        df['p_MC_Model'] = df['p_MC_Model'] / 10
        
        # if 'nMotNET_SMU' in df.columns:
        #     df['nMotNET_SMU'] = df['nMotNET_SMU'] / (2 * 3.14 / 60)
        
        root, ext = os.path.splitext(Csv)
        Csv_ = root + '_mod' + ext
        df.to_csv(Csv_, header=False, index=False)
        
        l_Out.append(Csv_)
        
    return l_Out


# ## Modify_Signal_Simout

# In[80]:


def Modify_Signal_Simout(l_Traces, File):
    l_Out = []
    
    d_Parameter = Read_DCM_4.Read_DCM(File)
    Cp_FA = d_Parameter['Abrollumfang_VA'][2][0]
    Cp_RA = d_Parameter['Abrollumfang_HA'][2][0]
    
    for Csv in l_Traces:
        print(Csv)
        df = pd.read_table(Csv, sep=",", index_col=None)
        
        # df['nMotNET_TRC'] = df['nMotNET_TRC'] / (2 * 3.14 / 60)        
        df['BRK_TRQ_FL'] = df['BRK_TRQ_FL'] * Cp_FA
        df['BRK_TRQ_FR'] = df['BRK_TRQ_FR'] * Cp_FA
        df['BRK_TRQ_RL'] = df['BRK_TRQ_RL'] * Cp_RA
        df['BRK_TRQ_RR'] = df['BRK_TRQ_RR'] * Cp_RA
        
        root, ext = os.path.splitext(Csv)
        Csv_ = root + '_mod' + ext
        df.to_csv(Csv_, header=True, index=False)
        
        l_Out.append(Csv_)
        
    return l_Out


# ## Run

# In[81]:


# OUT_PATH = 'c:/TSDE_Workarea/ktt2yk/Work/Traces/Honda-e/Winter_Fix/SIM_Vehicle/'
# DCM = 'c:/TSDE_Workarea/ktt2yk/Work/DCM/Honda-e_20230228/Honda-e/Complete_ESP10CB_VarCode_1_Honda_e.dcm'

# l_TRACE = MakeTraceList([OUT_PATH], ['.CSV', '.csv'], ['_mod.csv'])

# l_TRACE = Modify_Signal_CSSIM_INPUT(l_TRACE, DCM)
# l_TRACE = Modify_Signal_Simout(l_TRACE, DCM)


# # CSSIM(Matlab) Run File

# ## MATLAB_RUN_FILE_ZIP

# In[14]:


def MATLAB_RUN_FILE_ZIP(l_Trace, Mdl, Path):
    Text = ''
    Out = Path + 'Matlab_Run_w_ZIP.m'
    
    for T in l_Trace:
        dirname, basename = os.path.split(T)
        root_, ext = os.path.splitext(basename)
        root = root_.replace('_mod', '')
        File_ = root + '_simout.zip'
        File_Sim = root + '_simout.xls'
        
        Text += 'delete INPUT.csv\n'
        Text += 'delete simout.xls\n'
        Text += 'copyfile ' + basename + ' INPUT.csv\n'
        Text += "sim('" + Mdl + "')\n"
        Text += 'movefile oml_bbxxxxx.zip ' + File_ + '\n'
        Text += 'delete INPUT.csv\n'
        Text += 'copyfile simout.xls ' + File_Sim + '\n'
        Text += '\n'
        
    f = open(Out, "w")
    f.write(Text)
    f.close()
    
    return Out


# ## MATLAB_RUN_FILE_D97

# In[15]:


def MATLAB_RUN_FILE_D97(l_Trace, Mdl, Path):
    Text = ''
    Out = Path + 'Matlab_Run_w_D97.m'
    
    for T in l_Trace:
        dirname, basename = os.path.split(T)
        root_, ext = os.path.splitext(basename)
        root = root_.replace('_mod', '')
        File_d97 = root + '.d97'
        File_zip = root + '_simout.zip'
        File_Sim = root + '_simout.xls'
        
        Text += 'delete INPUT.csv\n'
        Text += 'delete simout.xls\n'
        Text += 'copyfile ' + basename + ' INPUT.csv\n'
        Text += "sim('" + Mdl + "')\n"
        Text += 'movefile oml_bbxxxxx.d97 ' + File_d97 + '\n'
        Text += "zip('" + File_zip + "' , '" + File_d97 + "')\n"
        Text += 'delete INPUT.csv\n'
        Text += 'delete ' + File_d97 + '\n'
        Text += 'copyfile simout.xls ' + File_Sim + '\n'
        Text += '\n'
        
    f = open(Out, "w")
    f.write(Text)
    f.close()
    
    return Out


# ## MATLAB_RUN_FILE_wo_D97

# In[16]:


def MATLAB_RUN_FILE_wo_D97(l_Trace, Mdl, Path):
    Text = ''
    Out = Path + 'Matlab_Run_wo_D97.m'
    
    for T in l_Trace:
        dirname, basename = os.path.split(T)
        root_, ext = os.path.splitext(basename)
        root = root_.replace('_mod', '')
        # File_d97 = root + '_OOL.d97'
        # File_zip = root + '_OOL.zip'
        File_Sim = root + '_simout.xls'
        
        Text += 'delete INPUT.csv\n'
        Text += 'delete simout.xls\n'
        Text += 'copyfile ' + basename + ' INPUT.csv\n'
        Text += "sim('" + Mdl + "')\n"
        # Text += 'movefile oml_bbxxxxx.d97 ' + File_d97 + '\n'
        # Text += "zip('" + File_zip + "' , '" + File_d97 + "')\n"
        Text += 'delete INPUT.csv\n'
        # Text += 'delete ' + File_d97 + '\n'
        Text += 'copyfile simout.xls ' + File_Sim + '\n'
        Text += '\n'
        
    f = open(Out, "w")
    f.write(Text)
    f.close()
    
    return Out


# ## Run

# In[18]:


# SEARCH_PATH = ['c:/TSDE_Workarea/ktt2yk/Work/Traces/XT1E/SIM/Winter_Fix/2023_0222__Jenkins_N245_2ChTrqLatest_wBugFix/', 'c:/TSDE_Workarea/ktt2yk/Work/Traces/XT1E/SIM/Winter_Fix/2023_0302_XT1E_Bigslip/']
# OUT_PATH = 'c:/TSDE_Workarea/ktt2yk/Work/Traces/Honda-e/Winter_Fix/SIM_Vehicle/'

# MDL = 'HM_BB86152_Var01_M_TCS_HondaE_RWD_20230315.mdl'
# MDL = 'HM_BB86153_Var01_M_TCS_XT1E_4WD_20230317_OOL.mdl'
# MDL = 'HM_BB86153_Var01_M_TCS_XT1E_4WD_20230317.mdl'

# l_TRACE = MakeTraceList(SEARCH_PATH, ['_mod.CSV', '_mod.csv'], [])

# MATLAB_RUN_FILE_ZIP(l_TRACE, MDL, OUT_PATH)
# MATLAB_RUN_FILE_D97(l_TRACE, MDL, OUT_PATH)
# MATLAB_RUN_FILE_wo_D97(l_TRACE, MDL, OUT_PATH)


# # CSSIM SIMOUT to CSV

# ## SIMOUT_to_CSV

# In[89]:


def SIMOUT_to_CSV(l_Trace, Plt):
    l_Out = []
    
    d_Signal = Select_Signal(Plt)
    
    for T in l_Trace:
        df = pd.read_excel(T, header=None)
        df_ = pd.read_excel(T, header=None)
        
        for e, Col in enumerate(df.columns):
            if e == 0:
                df_ = df_.rename(columns={e: "TIME"})
            else:
                S = list(d_Signal.keys())[e - 1]
                df_ = df_.rename(columns={e: S})
        
        root, ext = os.path.splitext(T)
        T_ = root + '.csv'
        df_.to_csv(T_, index=False)
        
        l_Out.append(T_)
    
    return l_Out


# ## Run

# In[90]:


# SEARCH_PATH_SIMOUT = ['c:/TSDE_Workarea/ktt2yk/Work/Traces/Honda-e/Winter_Fix/SIM_OOL_w_D97/', 'c:/TSDE_Workarea/ktt2yk/Work/Traces/Honda-e/Winter_Fix/SIM_OOL_wo_D97/']
# PLT_SIMOUT = 'c:/TSDE_Workarea/ktt2yk/Work/PLT/MTCS_MEDC_SIMOUT_1CH.PLT'

# l_TRACE = MakeTraceList(SEARCH_PATH_SIMOUT, ['_simout.xls'], [])
# SIMOUT_to_CSV(l_TRACE, PLT_SIMOUT)


# # PATH

# In[ ]:


def CHANGE_PATH(Path):
    Path = Path.replace('c:/TSDE_Workarea/ktt2yk', '')
    Path = Path.replace('c:\\TSDE_Workarea\\ktt2yk', '')
    
    return Path

