Assimilate function help:

Description:
Assimilates given data

Definition:
def assimilate(dataType, input_data, filename_boundaries, LAIDColName, filename_output):

Arguments:
dataType = type of data to assimilate (csv or dict)
input_data = filepath to csv / data object to assimilate
filename_boundaries = filepath to geojson boundaries file to assimilate into
LAIDColName = the header name for the column containing the LA area code in the csv file (if applicable - None for dict)
filename_output = filepath and name for the output file