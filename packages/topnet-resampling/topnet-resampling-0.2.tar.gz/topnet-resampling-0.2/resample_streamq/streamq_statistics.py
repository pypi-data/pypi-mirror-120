import argparse
import xarray as xr
import matplotlib.pyplot as plt

vars_for_statistics = ["aprecip", "drainge", "soilh2o", "river_flow_rate_mod", "mod_streamq"]
vars_for_grouping = ["day", "month", "season"]
internal_vars = ["time.dayofyear", "time.month", 'time.season']
grouping_variables = dict(zip(vars_for_grouping, internal_vars))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_nc", type=str, help="Input file (TopNet streamq file)")
    parser.add_argument("-variable", type=str, choices=vars_for_statistics)
    parser.add_argument("-grouping", type=str, choices=vars_for_grouping)
    parser.add_argument("-output_file_name", type=str, default="out.nc")
    return parser.parse_args()


def main():
    args = parse_args()
    input_nc = args.input_nc
    grouping = args.grouping
    grouping_var = grouping_variables[grouping]
    variable = args.variable
    output_file_name = args.output_file_name

    DS = xr.open_dataset(input_nc)
    DS_grouped = DS.get(variable).groupby(grouping_var)

    print(DS_grouped)

    mean_values = DS_grouped.mean()
    median_values = DS_grouped.median()
    ninety_five_quantile = DS_grouped.quantile(0.95)
    five_quantile = DS_grouped.quantile(0.05)

    stats_dict = {
        grouping: {'dims': ('month',), 'data': list(DS_grouped.groups.keys()),
                   'attrs': {"description": "Grouping by {}".format(grouping)}},
        'mean': mean_values.to_dict(), "median": median_values.to_dict(), "pct95": ninety_five_quantile.to_dict(),
        'pct5': five_quantile.to_dict(), "rchid": DS.rchid.to_dict()
    }

    ds = xr.Dataset.from_dict(stats_dict)
    ds.to_netcdf(output_file_name)


if __name__ == "__main__":
    main()
