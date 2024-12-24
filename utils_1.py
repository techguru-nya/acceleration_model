#!/usr/bin/env python
# coding: utf-8

# In[35]:


import os
import pandas as pd
import numpy as np

from scipy import interpolate

import matplotlib.pyplot as plt


# # Read_DCM

# ## パラメータ検出キー

# In[36]:


PARAMETER_TYPE = ["FESTWERT", "KENNLINIE", "KENNFELD"]


# ## DCM読込み（テキストモード）

# In[37]:


def ParameterName(TEXT):
    for TYPE in PARAMETER_TYPE:
        TEXT = TEXT.replace(TYPE, "")

    TEXT = TEXT.replace("\n", "")

    P = TEXT.split(" ")

    return P[1]


def Read_DCM_w_Text(FILE):
    l_line = []

    i = 0

    try:
        f = open(FILE, 'r')

        while True:
            line = f.readline()
            l_line.append(line)

            if line == "":
                i += 1

            if i > 100:
                break

    except UnicodeDecodeError:
        try:
            f = open(FILE, 'r', encoding='shift-jis')

            while True:
                line = f.readline()
                l_line.append(line)

                if line == "":
                    i += 1

                if i > 100:
                    break

        except UnicodeEncodeError:
            f = open(FILE, 'r', encoding="utf_8")

            while True:
                line = f.readline()
                l_line.append(line)

                if line == "":
                    i += 1

                if i > 100:
                    break

    Parameter = {}
    Read = False
    P = None
    l_TEXT = []
    i = 0

    for line in l_line:
        line = str(line)
        line = line.replace("\t", "   ")

        if Read == False:
            for T in PARAMETER_TYPE:
                if T in line:
                    Read = True
                    l_TEXT.append(line)
                    P = ParameterName(line)
                    i = 0
        else:
            l_TEXT.append(line)

            A = line.replace(" ", "")
            A = A.replace("\n", "")

            if A == "END":
                if l_TEXT != []:
                    Parameter[P] = l_TEXT
                Read = False
                P = None

                l_TEXT = []
    f.close()

    return Parameter


# ## DCM読込み（パラメータ値モード）

# In[38]:


from scipy import interpolate

import pandas as pd
import numpy
import numpy as np

import os


# In[39]:


def CheckFloat(X):
    if X != None:
        try:
            Y = float(X)
            J = True
        except ValueError:
            J = False
    else:
        J = False

    return J


def ValueList(Mode, L_Data1, L_Data2):
    X1 = []
    X2 = []
    Y1 = []
    Y2 = []
    Z1 = []
    Z2 = []

    if Mode == 1:
        if L_Data1 == None:
            Z1 = None
        else:
            Z1 = L_Data1[2][0]

        if L_Data2 == None:
            Z2 = None
        else:
            Z2 = L_Data2[2][0]

    elif Mode == 2:
        if L_Data1 != None:
            X1 = L_Data1[0]

        if L_Data2 != None:
            X2 = L_Data2[0]

        if L_Data1 != None:
            Z1 = L_Data1[2]

        if L_Data2 != None:
            Z2 = L_Data2[2]

    elif Mode == 3:
        if L_Data1 != None:
            X1 = L_Data1[0]

        if L_Data2 != None:
            X2 = L_Data2[0]

        if L_Data1 != None:
            Y1 = L_Data1[1]

        if L_Data2 != None:
            Y2 = L_Data2[1]

        if L_Data1 != None:
            Z1 = L_Data1[2]

        if L_Data2 != None:
            Z2 = L_Data2[2]

    return X1, X2, Y1, Y2, Z1, Z2


def ParameterValue(Target, Text):
    OUT_temp = []

    L_Text = Text.split(" ")
    i = 0
    for T in L_Text:
        if T == Target:
            OUT_temp = L_Text[i + 1 :]
            break
        i += 1

    OUT = []
    for O in OUT_temp:
        if O != "":
            try:
                OUT.append(float(O))
            except ValueError:
                OUT.append(O)

    return OUT


def PramameterToXYZ(L_Text):
    X = []
    Y = []
    Z = []
    for T in L_Text:
        T = T.replace("\n", "")
        T = T.replace("\t", "")

        if "ST/X" in T:
            X += ParameterValue("ST/X", T)
        elif "ST/Y" in T:
            Y += ParameterValue("ST/Y", T)
        elif "WERT" in T:
            Z += ParameterValue("WERT", T)
        elif "TEXT" in T:
            Z += ParameterValue("TEXT", T)

    return [X, Y, Z]


def ParameterValueFromDCM(File):
    D_Parameter = {}
    TEXT = []
    READ = False

    TYPE = ["FESTWERT", "KENNLINIE", "KENNFELD"]

    try:
        f = open(File, "r")
        datalist = f.readlines()
    except UnicodeDecodeError:
        try:
            f = open(File, "r", encoding="shift-jis")
            datalist = f.readlines()
        except UnicodeEncodeError:
            f = open(File, "r", encoding="utf_8")
            datalist = f.readlines()

    for data in datalist:
        for T in TYPE:
            if T in data:
                READ = True

                X = data.split(" ")
                Parameter = X[1].replace("\n", "")

        if READ == True:
            TEXT.append(data)

            X = data.replace(" ", "")
            X = X.replace("\n", "")
            if X == "END":
                READ = False
                D_Parameter[Parameter] = TEXT
                TEXT = []

    f.close()

    return D_Parameter


def Read_DCM_wo_Text(File):
    d_Parameter = {}

    d_Parameter_1 = ParameterValueFromDCM(File)

    for Target in d_Parameter_1:
        d_Parameter[Target] = PramameterToXYZ(d_Parameter_1[Target])

    return d_Parameter


# ## Read_DCM

# In[40]:


def Read_DCM(File):
    d_Out = {}
    
    d_P = Read_DCM_w_Text(File)
    d_P_wo = Read_DCM_wo_Text(File)
    
    for P in d_P.keys():
        _ = d_P_wo[P]
        X = _[0]
        Y = _[1]
        Z = _[2]
        
        d_Out[P] = (X, Y, Z, d_P[P])
        
    return d_Out


# ## Read_Value_1D

# In[41]:


def Read_Value_1D(_):
    X, Y, Z, T = _
    return Z[0]


# ## Read_Value_2D

# In[42]:


def Read_Value_2D(_, x_):
    X, Y, Z, T = _
    
    if len(Z) > 1:
        if x_ > X[-1]:
            value = X[-1]
        elif x_ < X[0]:
            value = X[0]
        else:
            value = x_

        f = interpolate.interp1d(X, Z)
        Out = f(value)
    else:
        Out = Z[0]
    
    return Out


# ## Read_Value_3D

# In[70]:


def Read_Value_3D(_, value):
    X, Y, Z, T = _
    x_, y_ = value
    
    X_, Y_ = np.meshgrid(X, Y)
    Z_ = np.reshape(Z, (len(X), len(Y)))
    
    if x_ > X[-1]:
        value_x = X[-1]
    elif x_ < X[0]:
        value_x = X[0]
    else:
        value_x = x_

    if y_ > Y[-1]:
        value_y = Y[-1]
    elif y_ < Y[0]:
        value_y = Y[0]
    else:
        value_y = y_
    
    f = interpolate.interp2d(X_, Y_, Z_)
    Out = f(value_x, value_y)
    
    return Out[0]


# In[72]:


# X = ([0.1201171875, 0.2001953125, 0.349609375, 0.5, 0.7998046875], [0.080078125, 0.1201171875, 0.2001953125, 0.349609375, 0.7001953125], [0.28125, 0.359375, 0.40625, 0.5, 0.5, 0.1875, 0.234375, 0.3125, 0.46875, 0.5, 0.140625, 0.1875, 0.265625, 0.421875, 0.5, 0.140625, 0.171875, 0.234375, 0.40625, 0.5, 0.140625, 0.15625, 0.203125, 0.296875, 0.296875], ['KENNFELD TCSOp_TCSStart_vTarOffset_wMu 5 5\n', '   LANGNAME "<unknown>"\n', '   EINHEIT_X ""\n', '   EINHEIT_Y ""\n', '   EINHEIT_W ""\n', '   ST/X  0.1201171875  0.2001953125  0.349609375  0.5  0.7998046875\n', '   ST/Y  0.080078125\n', '   WERT  0.28125  0.359375  0.40625  0.5  0.5\n', '   ST/Y  0.1201171875\n', '   WERT  0.1875  0.234375  0.3125  0.46875  0.5\n', '   ST/Y  0.2001953125\n', '   WERT  0.140625  0.1875  0.265625  0.421875  0.5\n', '   ST/Y  0.349609375\n', '   WERT  0.140625  0.171875  0.234375  0.40625  0.5\n', '   ST/Y  0.7001953125\n', '   WERT  0.140625  0.15625  0.203125  0.296875  0.296875\n', 'END\n'])
# # Y = (0.416992, 0.00195313)
# Y = (0.8, 0.7)

# Z = Read_Value_3D(X, Y)


# # Compare_DCM

# ## DiffCheck
# - 差分評価(分解能違いを判定)
# - 1.5%未満は差分無しと判断する。

# In[10]:


def DiffCheck(Mode, L_Data1, L_Data2):
    X1, X2, Y1, Y2, Z1, Z2 = ValueList(Mode, L_Data1, L_Data2)

    if Mode == 1:
        J = DiffCheckValue(Z1, Z2)

    elif Mode == 2:
        if DiffCheckLenValue(X1, X2) == False and DiffCheckLenValue(Z1, Z2) == False:
            J = False
        else:
            J = True

    elif Mode == 3:
        if DiffCheckLenValue(X1, X2) == False and DiffCheckLenValue(Y1, Y2) == False and DiffCheckLenValue(Z1, Z2) == False:
            J = False
        else:
            J = True

    return J


def CheckFloat(X):
    if X != None:
        try:
            Y = float(X)
            J = True
        except ValueError:
            J = False
    else:
        J = False

    return J


def DiffCheckValue(X1, X2):
    J = True

    if X1 == X2:
        J = False
    else:
        if X1 == 0 or X2 == 0:
            J = True
        else:
            if CheckFloat(X1) and CheckFloat(X2):
                if abs((X2 - X1) / X1) < 0.015 and abs((X2 - X1) / X2) < 0.015:
                    J = False

        if CheckFloat(X1) and CheckFloat(X2):
            if float(X1) == float(X2):
                J = False

    return J


def DiffCheckLenValue(X1, X2):
    J = True

    if len(X1) == len(X2):
        n = len(X1)
        for i in range(n):
            J_temp = DiffCheckValue(X1[i], X2[i])
            if J_temp == True:
                break

        if J_temp == False:
            J = False

    return J


def ValueList(Mode, L_Data1, L_Data2):
    X1 = []
    X2 = []
    Y1 = []
    Y2 = []
    Z1 = []
    Z2 = []

    if Mode == 1:
        if L_Data1 == None:
            Z1 = None
        else:
            Z1 = L_Data1[2][0]

        if L_Data2 == None:
            Z2 = None
        else:
            Z2 = L_Data2[2][0]

    elif Mode == 2:
        if L_Data1 != None:
            X1 = L_Data1[0]

        if L_Data2 != None:
            X2 = L_Data2[0]

        if L_Data1 != None:
            Z1 = L_Data1[2]

        if L_Data2 != None:
            Z2 = L_Data2[2]

    elif Mode == 3:
        if L_Data1 != None:
            X1 = L_Data1[0]

        if L_Data2 != None:
            X2 = L_Data2[0]

        if L_Data1 != None:
            Y1 = L_Data1[1]

        if L_Data2 != None:
            Y2 = L_Data2[1]

        if L_Data1 != None:
            Z1 = L_Data1[2]

        if L_Data2 != None:
            Z2 = L_Data2[2]

    return X1, X2, Y1, Y2, Z1, Z2


# ## Compare_DCM

# In[11]:


def Check_Mode(l_):
    if len(l_[0]) != 0 and len(l_[1]) != 0:
        Mode = 3
    elif len(l_[0]) != 0:
        Mode = 2
    else:
        Mode = 1
    
    return Mode


# In[12]:


def Compare_DCM(DCM1, DCM2):
    d_Diff = {}
    
    d_DCM1 = Read_DCM(DCM1)
    d_DCM2 = Read_DCM(DCM2)
    
    Parameter = list(d_DCM1.keys()) + list(d_DCM2.keys())
    Parameter = list(set(Parameter))
    Parameter.sort()
    
    for P in Parameter:
        if '.' not in P:
            Value1 = None
            Value2 = None

            if P in d_DCM1:
                _ = d_DCM1[P]
                X, Y, Z, T = _
                Value1 = [X, Y, Z]

            if P in d_DCM2:
                _ = d_DCM2[P]
                X, Y, Z, T = _  
                Value2 = [X, Y, Z]
            
            if Value1 != Value2 and Value1 != None and Value2 != None:
                Mode1 = Check_Mode(Value1)
                Mode2 = Check_Mode(Value2)
                
                if Mode1 == Mode2:
                    if DiffCheck(Mode1, Value1, Value2) == True:
                        d_Diff[P] = (Value1, Value2)
                else:
                    d_Diff[P] = (Value1, Value2)
            
            if Value1 == None or Value2 == None:
                d_Diff[P] = (Value1, Value2)
    
    return d_Diff


# In[13]:


# DCM1 = '/Work/Traces/3T0A/20230221_Winter/DCM/Base/rev212_Complete_ESP10CB_VarCode_1.dcm'
# DCM2 = '/Work/Traces/3T0A/20230221_Winter/DCM/New/20230221_0014_SharCC_PMSe.par.txt'
# d_Out = Compare_DCM(DCM1, DCM2)


# # PLOT_3D

# In[14]:


def RangeXYZ(Range):
    x_min, x_max, y_min, y_max, z_min, z_max = Range
    
    Out = (x_min_, x_max_, y_min_, y_max_, z_min_, z_max_)
    
    return Out


# In[15]:


def PLOT_3D(F, Parameter):
    d_ = Read_DCM(F)
    
    x, y, z, _ = d_[Parameter]
    # print(d_[Parameter])
    X, Y = np.meshgrid(x, y)
    Z = np.reshape(z, (len(y), len(x)))
    
    # if Range == None:
    #     x_min = min(x)
    #     x_max = max(x)
    #     y_min = min(y)
    #     y_max = max(y)
    #     z_min = min(z)
    #     z_max = max(z)
    #     N = 10
    
    fig = plt.figure(figsize=(4, 2), dpi=100)

    # cb_min, cb_max = range_
    # cb_div = 20
    if min(z) != max(z):
        interval_of_cf = np.linspace(min(z), max(z), 10)
    else:
        interval_of_cf = [z[0]-1, z[0]+1]
    # contour_filled = plt.contourf(X, Y, Z, interval_of_cf)

    # print(interval_of_cf)
    contour_filled = plt.contourf(X, Y, Z, interval_of_cf)
    plt.xlim([min(x), max(x)])
    plt.ylim([min(y), max(y)])
    # contour_filled = plt.contourf(X, Y, Z)
    plt.colorbar(contour_filled)
    plt.title(Parameter)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()


# In[16]:


# FILE = '/Work/Traces/3T0A/20230221_Winter/DCM/New/20230221_0006_SharCC_PMSe.par.txt'
# FILE2 = '/Work/Traces/3T0A/20230221_Winter/DCM/Base/rev212_Complete_ESP10CB_VarCode_1.dcm'
# PARAMETER = 'VDC_FF_APP_CoMueRatio_NoKey'

# PLOT_3D(FILE2, PARAMETER)


# In[ ]:




