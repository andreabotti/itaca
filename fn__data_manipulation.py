from fn__import_py_libs import *



def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    # haversine formula 
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles.
    return c * r





def find_closest(df1, df2, lat_col, lon_col, name_col):
    closest_location_names = []

    for index1, row1 in df1.iterrows():
        min_distance = float('inf')
        closest_location_name = None

        for index2, row2 in df2.iterrows():
            distance = haversine(row1[lat_col], row1[lon_col], row2[lat_col], row2[lon_col])
            
            if distance < min_distance:
                min_distance = distance
                closest_location_name = row2[name_col]

        closest_location_names.append(closest_location_name)

    df1['closest_CTI_location'] = closest_location_names
    return df1





# Function to convert datetime index to month names
def convert_index_to_month_names(df):
    month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                   7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    # Assuming the index is of datetime type
    df.index = df.index.month.map(month_names)
    return df




def process_temperature_data(df, locations, prefix, statistic, percentile, convert_index_to_month):
    """
    Process the temperature data for the given locations.
    Calculate the specified statistic (mean, median, or max percentile) for each month.

    Parameters:
    df : DataFrame
        The dataframe containing temperature data.
    locations : list
        List of locations to filter in the dataframe.
    prefix : str
        Prefix to add to the column names in the resulting dataframe.
    statistic : str
        The type of statistic to calculate ('mean', 'median', or 'max').
    percentile : float, optional
        The percentile to use for the 'max' calculation. Defaults to None.
    """
    # Filter the dataframe to include only columns for the specified locations
    df_filtered = df[[col for col in df.columns if any(loc in col for loc in locations)]]
    df_filtered.index = pd.to_datetime(df_filtered.index)  # Ensure the index is in datetime format

    print(df_filtered[:5])

    # Check the statistic parameter and calculate accordingly
    if statistic == 'mean':
        df_result = df_filtered.resample('M').mean().round(1)
        df_result.columns = [f"{prefix}__{col}__mean" for col in df_result.columns]
    elif statistic == 'median':
        df_result = df_filtered.resample('M').median().round(1)
        df_result.columns = [f"{prefix}__{col}__median" for col in df_result.columns]
    elif statistic == 'max':
        if percentile is not None:
            df_result = df_filtered.resample('M').quantile(percentile).round(1)
            df_result.columns = [f"{prefix}__{col}__max" for col in df_result.columns]
        else:
            raise ValueError("Percentile value must be provided for max_percentile calculation.")
    else:
        raise ValueError("Invalid statistic type. Choose 'mean', 'median', or 'max'.")


    if convert_index_to_month==True:
        df_result = convert_index_to_month_names(df_result)
    else:
        df_result = df_result

    return df_result










'''
def process_temperature_data__CTI(df, locations, prefix, percentile):
    """
    Process the temperature data for the given locations.
    Calculate average, median, and 95th percentile for each month.
    """
    # Filter the dataframe to include only columns for the specified locations
    df_filtered = df[[col for col in df.columns if any(loc in col for loc in locations)]]
    df_filtered.index = pd.to_datetime(df_filtered.index)  # Ensure the index is in datetime format

    # Creating separate DataFrames for mean, median, and max (xth percentile)
    df_monthly_mean = df_filtered.resample('M').mean().round(1)
    df_monthly_median = df_filtered.resample('M').median().round(1)
    df_monthly_max = df_filtered.resample('M').quantile(percentile).round(1)

    # Rename columns to include prefix and statistic type
    df_monthly_mean.columns = [f"{prefix}__{col}__mean" for col in df_monthly_mean.columns]
    df_monthly_median.columns = [f"{prefix}__{col}__median" for col in df_monthly_median.columns]
    df_monthly_max.columns = [f"{prefix}__{col}__max" for col in df_monthly_max.columns]

    return df_monthly_mean, df_monthly_median, df_monthly_max




def process_temperature_data__COB(df, df_list, mapping, prefix, percentile):

    # Filter the df__DBT__COB_capo dataset
    relevant_columns = [col for col in df.columns if col.split('_')[0] in wmo_code_to_location]
    df_filtered = df[relevant_columns]

    # Rename columns according to the wmo_code_to_location mapping and append the province code
    df_filtered.rename(columns={col: wmo_code_to_location[col.split('_')[0]] for col in relevant_columns}, inplace=True)
    # df_filtered = df_filtered.rename(columns=lambda x: location_to_province.get(x, '') + '__' + x)
    df_filtered = df_filtered.rename(columns=lambda x: location_to_reg_province.get(x, '') + '__' + x)


    # Creating separate DataFrames for mean, median, and max (xth percentile)
    df_monthly_mean = df_filtered.resample('M').mean()
    df_monthly_median = df_filtered.resample('M').median()
    df_monthly_max = df_filtered.resample('M').quantile(percentile)

    # Rename columns to include prefix and statistic type
    df_monthly_mean.columns = [f"{prefix}__{col}__mean" for col in df_monthly_mean.columns]
    df_monthly_median.columns = [f"{prefix}__{col}__median" for col in df_monthly_median.columns]
    df_monthly_max.columns = [f"{prefix}__{col}__max" for col in df_monthly_max.columns]

    return df_monthly_mean, df_monthly_median, df_monthly_max

    
'''