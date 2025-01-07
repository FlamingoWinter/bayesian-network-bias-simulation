import xarray as xr
from arviz import InferenceData


class PriorTrace(InferenceData):
    prior: xr.Dataset
