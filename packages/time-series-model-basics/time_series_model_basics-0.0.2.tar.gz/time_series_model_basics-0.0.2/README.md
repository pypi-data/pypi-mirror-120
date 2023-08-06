# Forecasting Basics
> <a href='https://github.com/kikejimenez/time_series_model_basics'>Documentation and Code is hosted on Github</a>  


> Generate and Plot Forecasts for Time Series Data 

> Includes:SMA, WMA and Single and Double Exponential Smoothing 

## Install

```bash
pip install time-series-model-basics
```

## Simple Moving Average

Plot a Simulated Time Series with two or  any number of Simple Moving Averages as follows:

```python
from time_series_model_basics.moving_average import SMA

df, fig = SMA(1, 4)

fig.write_image("images/sma.png")
```

<img src="nbs/images/sma.png" width="700" height="400" style="max-width: 700px">

When running on a notebook you may alternatively use
```python
fig.show()
```

## Weighted Moving Average

For the case of  Weighted Moving Averages, pass the weights as lists:

```python
from time_series_model_basics.moving_average import WMA

df,fig = WMA([1,1,2],[3,2])

fig.write_image("images/wma.png")
```

<img src="nbs/images/wma.png" width="700" height="400" style="max-width: 700px">

## Simple Smoothing 

Plot a Simulated Time Series with two or  any number of simple exponential smoothing as follows:

```python
from time_series_model_basics.smoothing import SIMPLE

df, fig = SIMPLE(.15, .5)
fig.write_image("images/simple.png",)
```

<img src="nbs/images/simple.png" width="700" height="400" style="max-width: 700px">

## Double Smoothing 

```python
from time_series_model_basics.smoothing import DOUBLE

df, fig = DOUBLE(
    [.25, .3],
    [.5, .6],
)
fig.write_image("images/double.png")
```

<img src="nbs/images/double.png" width="700" height="400" style="max-width: 700px">
