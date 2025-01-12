import xarray as xr
from arviz import InferenceData


class PriorTrace(InferenceData):
    prior: xr.Dataset


class PosteriorTrace(InferenceData):
    posterior: xr.Dataset
