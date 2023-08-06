# Outlier Detection
> Detect and filter outliers.


> [Documentation and Code can be found on Github]()

## Install

`pip install sensor_dataset`

## Z-SCORE Normalization

> Normalize data with Z-SCORE

```python
from sensor_dataset.outlier_detection import ZSCORE
```

Get a normalized Koalas dataframe for the sensor dataset and fig objects by calling:

```python
kdf, figs = ZSCORE()

figs['NORMAL'].write_image("images/zscore_normal.png")
figs['RECOVERING'].write_image("images/zscore_recovering.png")
figs['BROKEN'].write_image("images/zscore_broken.png")
```

<img src="nbs/images/zscore_normal.png" width="400" height="300" style="max-width: 400px">
<img src="nbs/images/zscore_recovering.png" width="400" height="300" style="max-width: 400px">
<img src="nbs/images/zscore_broken.png" width="400" height="300" style="max-width: 400px">

When running on a notebook you may show an interactive plot by using:
```python
fig.show()
```

## IQR

> Filter data using IQR

```python
from sensor_dataset.outlier_detection import IQR

kdf, figs = IQR()

figs['NORMAL'].write_image("images/iqr_normal.png")
figs['RECOVERING'].write_image("images/iqr_recovering.png")
figs['BROKEN'].write_image("images/iqr_broken.png")
```

<img src="nbs/images/iqr_normal.png" width="400" height="300" style="max-width: 400px">
<img src="nbs/images/iqr_recovering.png" width="400" height="300" style="max-width: 400px">
<img src="nbs/images/iqr_broken.png" width="400" height="300" style="max-width: 400px">
