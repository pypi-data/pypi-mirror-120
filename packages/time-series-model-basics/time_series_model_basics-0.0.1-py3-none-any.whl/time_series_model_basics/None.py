

# Cell
from .moving_average import SMA

df,fig = SMA(1,4)
fig.show()

# Cell
from .moving_average import WMA

df,fig = WMA([1,1,2],[3,2])
fig.show()

# Cell
from .smoothing import SIMPLE

df, fig = SIMPLE(.15, .5)
fig.show()

# Cell
from .smoothing import DOUBLE

df, fig = DOUBLE(
    [.25, .3],
    [.5, .6],
)
fig.show()