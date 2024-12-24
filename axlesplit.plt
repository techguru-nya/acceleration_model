~ Co_FA._20ms.PT_Model  nobit 1 unit=- scmin=0 scmax=1
Co_FA  nobit 1 unit=- scmin=0 scmax=1
MotPedalPosDriver  nobit 17 key=ThrottlePos unit=- scmin=-899.879 scmax=100.121
~ ThrottlePos  nobit 17 unit=- scmin=-899.879 scmax=100.121
ax  nobit 1 key=Ax_Sensor unit=m/s^2 scmin=-30 scmax=30
dvxVeh.F_KalmanFilter.F_LongitudinalDynamics.VSE_VDC20ms.VDC_VSE  nobit 1 key=Ax_vWheel unit=m/s^2 scmin=-30 scmax=30
dvxVeh.F_KalmanFilter.F_LongitudinalDynamics.VSE_VDC20ms.VSE_20ms  nobit 1 key=Ax_vWheel unit=m/s^2 scmin=-30 scmax=30
~ axVeh_model.F_AccelerationComputation_Model.F_LongAccelerationModel.F_PreProcessing.F_ModelErrorHandling.VSE_VDC20ms.VDC_VSE  nobit 1 key=Ax_Model unit=m/s^2 scmin=-30 scmax=30
axVeh_model.F_AccelModelRaw.F_LongAccelerationModel.F_PreProcessing.F_ModelErrorHandling.VSE_Common.VSE_20ms  nobit 1 key=Ax_Model unit=m/s^2 scmin=-30 scmax=30
~ airResistance.F_AirResistance.VSE_VDC20ms.VDC_VSE  nobit 31 key=airResistance unit=N scmin=-12000 scmax=12000
airResistance.F_AirResistance.VSE_Common.VSE_20ms  nobit 1 key=airResistance unit=N scmin=-12000 scmax=12000
~ airResistance.F_AirResistance._VSE_LeanTCS20ms._TCS_VehicleModel._LeanTCSCalc.LeanTCS20ms_VSE  nobit 31 key=airResistance unit=N scmin=-12000 scmax=12000
~ Mass._MF_AxeEquiv._ForceModel._TCS_VehicleModel._LeanTCSCalc.LeanTCS20ms_VSE  nobit 11 key=Mass unit=kg scmin=0 scmax=10000
~ mass.MergeMassEstimation._MassEstimation.LACest_Fn_mass.VDC_LAC_MassEstimation  nobit 1 key=mass.MergeMassEstimation._MassEstimation unit=- scmin=100 scmax=16000
~ CoEtaProp._CoEtaCalc._PT_BaseModel20ms_Axle_FA.PTModel_20ms_AxleSplit  nobit 8 key=CoEtaProp.FA unit=- scmin=-0.257218 scmax=4.74278
~ CoEtaProp._CoEtaCalc._PT_BaseModel20ms_Axle_RA.PTModel_20ms_AxleSplit  nobit 8 key=CoEtaProp.RA unit=- scmin=-0.257218 scmax=4.74278
~ CoEtaProp._CoEtaCalc._PT_BaseModel20ms.PTModel_20ms_Extended  nobit 8 key=CoEtaProp unit=- scmin=-0.257218 scmax=4.74278
~ CoEta._TorqueRatio._Gearbox._TransmissionModel._DriveSystem._xWD._20ms.PT_Model  nobit 1 unit=- scmin=0.100586 scmax=1.5
~ CoEta_Gearbox._TorqueRatio._Gearbox._TransmissionModel._DriveSystem._xWD._20ms.PT_Model  nobit 1 unit=- scmin=0.100586 scmax=1.5
CoEta._TorqueRatio._Gearbox._TransmissionModel._DriveSystem._FA_1Mot._20ms.PT_Model  nobit 1 key=CoEtaProp.FA unit=- scmin=0.100586 scmax=1.5
CoEta._TorqueRatio._Gearbox._TransmissionModel._DriveSystem._RA_1Mot._20ms.PT_Model  nobit 1 key=CoEtaProp.RA unit=- scmin=0.100586 scmax=1.5
~ i_over_iDiff._CoEtaCalc._PT_BaseModel20ms_Axle_FA.PTModel_20ms_AxleSplit  nobit 1 key=i_over_iDiff.FA unit=- scmin=0.1 scmax=15
~ i_over_iDiff._CoEtaCalc._PT_BaseModel20ms_Axle_RA.PTModel_20ms_AxleSplit  nobit 1 key=i_over_iDiff.RA unit=- scmin=0.1 scmax=15
~ iDiff._Gearbox._TransmissionModel._DriveSystem._xWD._20ms.PT_Model  nobit 1 key=i_over_iDiff.FA unit=- scmin=1 scmax=30
~ iDiff._iKin._Gearbox._TransmissionModel._DriveSystem._xWD._20ms.PT_Model  nobit 1 key=i_over_iDiff.FA unit=- scmin=1 scmax=30
iDiff._Gearbox._TransmissionModel._DriveSystem._FA_1Mot._20ms.PT_Model  nobit 1 key=i_over_iDiff.FA unit=- scmin=1 scmax=30
iDiff._Gearbox._TransmissionModel._DriveSystem._RA_1Mot._20ms.PT_Model  nobit 1 key=i_over_iDiff.RA unit=- scmin=1 scmax=30
~ i_over_iDiff._CoEtaCalc._PT_BaseModel20ms.PTModel_20ms_Extended  nobit 12 key=i_over_iDiff unit=- scmin=0.36 scmax=15.4
~ CM_PT_MDrvUnitNET_FA  nobit 1 key=MDrvUnitNET.FA unit=Nm scmin=-30000 scmax=10000
CM_PT_MDrvUnitNET_RA  nobit 1 key=MDrvUnitNET.RA unit=Nm scmin=-30000 scmax=10000
MMotActWhl_FA  nobit 1 key=MDrvUnitNET.FA unit=Nm scmin=-30000 scmax=30000
MMotActWhl_RA  nobit 1 key=MDrvUnitNET.RA unit=Nm scmin=-30000 scmax=30000
~ MMotAct_FA  nobit 1 key=MDrvUnitNET.FA unit=Nm scmin=-30000 scmax=30000
~ MMotAct_RA  nobit 1 key=MDrvUnitNET.RA unit=Nm scmin=-30000 scmax=30000
v_FL  nobit 7 unit=m/s scmin=-2.5 scmax=47.5
v_FR  nobit 3 unit=m/s scmin=-2.5 scmax=47.5
v_RL  nobit 6 unit=m/s scmin=-2.5 scmax=47.5
v_RR  nobit 5 unit=m/s scmin=-2.5 scmax=47.5
