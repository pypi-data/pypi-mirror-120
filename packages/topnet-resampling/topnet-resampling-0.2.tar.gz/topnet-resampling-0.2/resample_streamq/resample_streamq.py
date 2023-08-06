import argparse
import xarray as xr


all_variables_for_sum = ["aprecip", "drainge", "soilevp", "potevap", "canevap", "snowevp"]
all_variables_for_mean = ["river_flow_rate_mod", "soilh2o"]
suffix_output = {'1D': 'Daily', '1M': 'Monthly', 'W': "Weekly"}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_nc", type=str, help="Input file (TopNet streamq file)")
    parser.add_argument("--resampling_interval", choices=["1D","1M", "W"], default="1D",
                        help="Choose the resampling interval: 1D (daily), 1M (monthly) or 7D (weekly)")
    parser.add_argument("--variables", nargs="+", default=["river_flow_rate_mod", "aprecip"],
                        help="Space separated list of the variables to resample. Currently accepting "
                                 + ", ".join(all_variables_for_sum + all_variables_for_mean))
    parser.add_argument("-start_date", help="date for the plotting (dd/mm/yyyy)", default=None)
    parser.add_argument("-end_date", help="date for the plotting (dd/mm/yyyy)", default=None)
    return parser.parse_args()


def main():
    args = parse_args()
    input_nc = args.input_nc
    resampling_interval = args.resampling_interval
    variables = args.variables
    start_date = args.start_date
    end_date = args.start_date

    print("Inputs: ", input_nc, resampling_interval, variables)
    ds = xr.open_dataset(input_nc)

    if start_date is not None and end_date is not None:
        print("Resampling from {} to {}".format(start_date, end_date))
        time_slice = slice(start_date, end_date)
        ds = ds.sel(time=time_slice)
    else:
        print("Resampling for the full data range")

    variables_for_mean = []
    variables_for_sum = []
    output_file_name = input_nc.split(".")[0]+ "-" + suffix_output[resampling_interval] + ".nc"
        
    print("Will create the output file: ", output_file_name)

    for variable in variables:
        if variable in all_variables_for_sum:
            variables_for_sum.append(variable)
        elif variable in all_variables_for_mean:
            variables_for_mean.append(variable)
        else:
            print("Variable {} is not on the allowed variables for mean: {} or for sum: {}. Ignoring".format(
                        variable, all_variables_for_mean, all_variables_for_sum))

    if len(variables_for_mean) > 0:
        print("Resampling variables (mean)", variables_for_mean)
        ds_variables_mean = ds[variables_for_mean]
        ds_variables_mean_resampled = ds_variables_mean.resample(time=resampling_interval).mean()
    
    if len(variables_for_sum) > 0:
        print("Resampling variables (sum)", variables_for_sum)
        DS_variables_sum = ds[variables_for_sum]
        ds_variables_sum_resampled = DS_variables_sum.resample(time=resampling_interval).sum()

    if len(variables_for_mean) > 0 and len(variables_for_sum) > 0:
        ds_resampled = xr.merge([ds_variables_mean_resampled, ds_variables_sum_resampled])
    elif len(variables_for_mean) == 0:
        ds_resampled = ds_variables_sum_resampled
    else:
        ds_resampled = ds_variables_mean_resampled

    # Adding the reaches
    ds_resampled["rchid"] = ds["rchid"]
    ds_resampled.time.attrs["_FillValue"] = -9999
    ds_resampled.time.attrs["axis"] = "T"
    ds_resampled.time.attrs["standard_name"] = "time"

    # Editing the global attributes
    ds_resampled.attrs["source"] = "Averaged values for {} from streamq {}".format(
                                        variables_for_mean + variables_for_sum,
                                        input_nc)
    ds_resampled.attrs["institute"] = "NIWA"
    ds_resampled.attrs["title"] = "Averaged streamq values from TopNet"


    ds_resampled.to_netcdf(output_file_name)


if __name__ == "__main__":
    main()


