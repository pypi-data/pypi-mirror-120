Post-processing utils for TopNet
-------------------------------------

- Python Requirements: xarray netcdf4
- Other Requirements: ncatted needs to be avialable (part of NCO)

Resampling of streamq files
-------------------------------------

resample_streamq.py resamples a streamq file to daily, monthly or weekly time step.

- prerequisite: run the fix_streamq.sh script on the streamq file. This will remove the time:bounds attribute on the target netcdf file.
- It can also have an start and end date.

Example:

``resample_streamq streamq.nc {1D,1M,W} [-start_date "mm/dd/yyyy hh:mm:ss" -end_date "mm/dd/yyyy hh:mm:ss"  --variables [list of variables to resample]``

Currently we have the following available variables to resample:

- Resample by sum: aprecip, drainge, soilevp, potevap, canevap, snowevp
- Resample by averaging: river_flow_rate_mod

Resampling of tseries files
-------------------------------------

resample_tseries.py in the same way as the streamq files. Usage is the same.

Currently we have the following available variables to resample:

- Resample by sum: aprecip, drainge, soilevp, potevap, canevap, snowevp, lakeprec, lakevap
- Resample by averaging: mod_streamq, lakeqin, lakeqout, lakevol, lakarea, lakedepth.

Streamq statistics
-------------------------------------

Use the script ``streamq_statistics`` to this. Groupings available: month, season and day.
