# Vehicle Acceleration Model Tuning
This project tunes parameters to match a vehicle acceleration model. The process is conducted using JupyterLab, specifically in `main.ipynb`.

## Features
- Reads and processes measurement data, PLT signals, and parameter files.
- Converts measurement data into CSV format and loads it as a DataFrame.
- Removes outliers and corrects data biases.
- Uses Linear Regression for parameter tuning.
- Compares the effects of parameter changes before and after tuning.

## Requirements
- Python
- JupyterLab

## How to Use
1. Open `main.ipynb`.
2. Set the paths for the following files in the notebook:
   - Measurement data
   - PLT signal
   - Parameter file
3. Run all cells in the notebook.

## Workflow
1. **Load Parameter File**:  
   The parameter file is loaded for tuning.
2. **Process Measurement Data**:  
   Measurement data is converted to CSV format and loaded into a DataFrame.
3. **Data Cleaning**:  
   Outliers are removed, and data bias is corrected.
4. **Parameter Tuning**:  
   Linear Regression is applied to adjust the parameters.
5. **Comparison**:  
   The effects of parameter changes are compared before and after tuning.

## Results
The project generates a comparison plot and reports improvements in model accuracy after parameter tuning.
