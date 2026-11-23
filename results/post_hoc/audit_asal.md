# Audit sample: DeepSeek QT numbers with no provenance match

## A1. qt_sel17453 u2 qtcf_ms = 409.0 (ref 417.12; correct)

FINAL: {"qt_ms": 402, "qtcb_ms": 413, "qtcf_ms": 409}

Last reply (end):
```
FINAL: {"qt_ms": 402, "qtcb_ms": 413, "qtcf_ms": 409}
```

Output seen (end):
```
    Segment an ECG signal into single heartbeats. Convenient for visualizing all the heart beats.

    Parameters
    ----------
    ecg_cleaned : Union[list, np.array, pd.Series]
        The cleaned ECG channel as returned by ``ecg_clean()``.
    rpeaks : dict
        The samples at which the R-peaks occur. Dict returned by ``ecg_peaks()``. Defaults to ``None``.
    sampling_rate : int
        The sampling frequency of ``ecg_cleaned`` (in Hz, i.e., samples/second). Defaults to 1000.
    show : bool
        If ``True``, will return a plot of heartbeats. Defaults to ``False``. If "return", returns
        the axis of the plot.
    **kwargs
        Other arguments to be passed.

    Returns
    -------
    dict
        A dict containing DataFrames for all segmented heartbeats.

    See Also
    --------
    ecg_clean, ecg_plot

    Examples
    --------
    .. ipython:: python

      import neurokit2 as nk

      ecg = nk.ecg_simulate(duration=15, sampling_rate=1000, heart_rate=80, noise = 0.05)
      @savefig p_ecg_segment.png scale=100%
      qrs_epochs = nk.ecg_segment(ecg, rpeaks=None, sampling_rate=1000, show=True)
      @suppress
      plt.close()

    """
    # Sanitize inputs
    if rpeaks is None:
        _, rpeaks = ecg_peaks(ecg_cleaned, sampling_rate=sampling_rate, correct_artifacts=True)
        rpeaks = rpeaks["ECG_R_Peaks"]

    if len(ecg_cleaned) < sampling_rate * 4:
        raise ValueError("The data length is too small to be segmented.")

    epochs_start, epochs_end, average_hr = _ecg_segment_window(
        rpeaks=rpeaks, sampling_rate=sampling_rate, desired_length=len(ecg_cleaned)
    )
    heartbeats = epochs_create(
        ecg_cleaned,
        rpeaks,
        sampling_rate=sampling_rate,
        epochs_start=epochs_start,
        epochs_end=epochs_end,
    )

    # Pad last heartbeats with nan so that segments are equal length
    last_heartbeat_key = str(np.max(np.array(list(heartbeats.keys()), dtype=int)))
    after_last_index = heartbeats[last_heartbeat_key]["Index"] >= len(ecg_cleaned)
    for col in ["Signal", "ECG_Raw", "ECG_Clean"]:
        if col in heartbeats[last_heartbeat_key].columns:
            heartbeats[last_heartbeat_key].loc[after_last_index, col] = np.nan

    # Plot or return plot axis (feature meant to be used internally in ecg_plot)
    if show is not False:
        ax = _ecg_segment_plot(heartbeats, heartrate=average_hr, ytitle="ECG", **kwargs)
    if show == "return":
        return ax

    return heartbeats


```

## A2. qt_sel38 u1 qt_ms = 495.0 (ref 362.0; wrong)

FINAL: {"qt_ms": 495, "qtcb_ms": 652, "qtcf_ms": 595}

Last reply (end):
```
FINAL: {"qt_ms": 495, "qtcb_ms": 652, "qtcf_ms": 595}
```

Output seen (end):
```
'object')
ECG_P_Peaks      0
ECG_P_Onsets     0
ECG_P_Offsets    0
ECG_Q_Peaks      0
ECG_R_Onsets     0
ECG_R_Offsets    0
ECG_S_Peaks      0
ECG_T_Peaks      0
ECG_T_Onsets     0
ECG_T_Offsets    0
Name: 0, dtype: int64
ch 1 dict_keys(['ECG_P_Peaks', 'ECG_P_Onsets', 'ECG_P_Offsets', 'ECG_Q_Peaks', 'ECG_R_Onsets', 'ECG_R_Offsets', 'ECG_S_Peaks', 'ECG_T_Peaks', 'ECG_T_Onsets', 'ECG_T_Offsets'])
<class 'pandas.core.frame.DataFrame'>
Index(['ECG_P_Peaks', 'ECG_P_Onsets', 'ECG_P_Offsets', 'ECG_Q_Peaks',
       'ECG_R_Onsets', 'ECG_R_Offsets', 'ECG_S_Peaks', 'ECG_T_Peaks',
       'ECG_T_Onsets', 'ECG_T_Offsets'],
      dtype='object')
ECG_P_Peaks      0
ECG_P_Onsets     0
ECG_P_Offsets    0
ECG_Q_Peaks      0
ECG_R_Onsets     0
ECG_R_Offsets    0
ECG_S_Peaks      0
ECG_T_Peaks      0
ECG_T_Onsets     0
ECG_T_Offsets    0
Name: 0, dtype: int64

               0       1       2       3       ...  224989  224990  224991  224992
ECG_P_Peaks         0       0       0       0  ...       0       0       0       0
ECG_P_Onsets        0       0       0       0  ...       0       0       0       0
ECG_P_Offsets       0       0       0       0  ...       0       0       0       0
ECG_Q_Peaks         0       0       0       0  ...       0       0       0       0
ECG_R_Onsets        0       0       0       0  ...       0       0       0       0
ECG_R_Offsets       0       0       0       0  ...       0       0       0       0
ECG_S_Peaks         0       0       0       0  ...       0       0       0       0
ECG_T_Peaks         0       0       0       0  ...       0       0       0       0
ECG_T_Onsets        0       0       0       0  ...       0       0       0       0
ECG_T_Offsets       0       0       0       0  ...       0       0       0       0

[10 rows x 224993 columns]
---- peak method
               0       1       2       3       ...  224989  224990  224991  224992
ECG_P_Peaks         0       0       0       0  ...       0       0       0       0
ECG_Q_Peaks         0       0       0       0  ...       0       0       0       0
ECG_S_Peaks         0       0       0       0  ...       0       0       0       0
ECG_T_Peaks         0       0       0       0  ...       0       0       0       0
ECG_P_Onsets        0       0       0       0  ...       0       0       0       0
ECG_T_Offsets       0       0       0       0  ...       0       0       0       0

[6 rows x 224993 columns]
---- local window
[1048 1049 1050 1051 1052] [150410 150556 150702 150847 150991]

```

## A3. qt_sel16786 u5 qt_ms = 394.0 (ref 422.27; wrong)

FINAL: {"qt_ms": 394, "qtcb_ms": 400, "qtcf_ms": 398}

Last reply (end):
```
FINAL: {"qt_ms": 394, "qtcb_ms": 400, "qtcf_ms": 398}
```

Output seen (end):
```
1825), np.int64(2088)]
ECG_R_Onsets [120, 447, 702, 927, 1192, 1560, 1815, 2083]
ECG_R_Offsets [175, 463, 740, 982, 1230, 1575, 1868, 2122]
ECG_S_Peaks [nan, nan, nan, nan, nan, nan, nan, nan]
ECG_T_Peaks [239, 528, 806, 1049, 1295, 1640, 1936, 2189]
ECG_T_Onsets [223, 519, 801, 1044, 1292, 1620, 1928, 2184]
ECG_T_Offsets [256, 545, 823, 1064, 1314, 1659, 1950, 2206]

err [Errno 2] No such file or directory: '/work/sel16786.atr'

R= 150369
t offsets: [-25 -20 -15 -10  -5   0   5  10  15  20  25  30  35  40  45  50  55  60  65  70  75  80  85]
ch0 [-0.23 -0.21 -0.19 -0.49  0.6   2.79 -0.09 -0.15 -0.23 -0.24 -0.23 -0.21 -0.2  -0.17 -0.11 -0.04  0.07  0.21  0.35  0.49  0.52  0.25 -0.04]
ch1 [-0.1  -0.12 -0.1   0.04 -0.52 -0.46 -0.07 -0.03 -0.01 -0.01 -0.01 -0.03 -0.03 -0.03 -0.02 -0.01 -0.01  0.01  0.01  0.04  0.06  0.02 -0.01]
R= 152063
t offsets: [-25 -20 -15 -10  -5   0   5  10  15  20  25  30  35  40  45  50  55  60  65  70  75  80  85]
ch0 [-0.18 -0.18 -0.15 -0.24  0.33  2.65  0.06 -0.11 -0.18 -0.2  -0.18 -0.17 -0.15 -0.12 -0.09 -0.03  0.07  0.19  0.34  0.49  0.55  0.38  0.07]
ch1 [-0.09 -0.1  -0.08  0.1  -0.53 -0.52 -0.06  0.04  0.03  0.01  0.03  0.03  0.03  0.05  0.05  0.06  0.07  0.09  0.12  0.14  0.14  0.12  0.04]
R= 157146
t offsets: [-25 -20 -15 -10  -5   0   5  10  15  20  25  30  35  40  45  50  55  60  65  70  75  80  85]
ch0 [-0.21 -0.18 -0.17 -0.34  0.27  2.71 -0.02 -0.12 -0.18 -0.2  -0.2  -0.18 -0.15 -0.13 -0.09 -0.01  0.07  0.18  0.34  0.47  0.54  0.33  0.04]
ch1 [-0.08 -0.07 -0.09  0.09 -0.53 -0.56 -0.02  0.04  0.03  0.04  0.04  0.03  0.04  0.03  0.04  0.07  0.06  0.09  0.1   0.12  0.14  0.1   0.01]

=== QRS onset region, index offset, ch0, ch1
-30   -0.185   -0.085
-29   -0.185   -0.085
-28   -0.185   -0.090
-27   -0.185   -0.095
-26   -0.185   -0.090
-25   -0.185   -0.085
-24   -0.180   -0.085
-23   -0.175   -0.085
-22   -0.180   -0.080
-21   -0.185   -0.085
-20   -0.185   -0.095
-19   -0.175   -0.090
-18   -0.165   -0.085
-17   -0.165   -0.085
-16   -0.165   -0.085
-15   -0.155   -0.080
-14   -0.145   -0.075
-13   -0.130   -0.080
-12   -0.120   -0.065
-11   -0.160    0.025
-10   -0.245    0.095
-9   -0.450    0.100
-8   -0.590    0.100
-7   -0.570    0.080
-6   -0.325   -0.090
-5    0.325   -0.530
-4    0.975   -0.855
-3    1.625   -1.010
-2    2.145   -0.955
-1    2.510   -0.645
0    2.645   -0.520
1    2.535   -0.590
2    1.965   -0.535
3    1.005   -0.365
4    0.410   -0.205
5    0.055   -0.055
6   -0.070    0.030
7   -0.050    0.070

```

## A4. qt_sel33 u5 qtcb_ms = 576.0 (ref 593.0; correct)

FINAL: {"qt_ms": 748, "qtcb_ms": 576, "qtcf_ms": 628}

Last reply (end):
```
FINAL: {"qt_ms": 748, "qtcb_ms": 576, "qtcf_ms": 628}
```

Output seen (end):
```
 0.    0.   -0.01  0.01  0.   -0.   -0.   -0.    0.    0.01  0.01 -0.01  0.    0.    0.    0.01  0.    0.    0.    0.   -0.01 -0.01  0.    0.    0.    0.    0.    0.    0.
  0.01]
ch 1
[ 0.    0.    0.    0.    0.   -0.01  0.   -0.    0.01  0.01  0.01  0.   -0.01 -0.    0.    0.    0.   -0.   -0.   -0.   -0.    0.   -0.    0.02  0.04  0.03  0.   -0.   -0.01 -0.01  0.56  0.46 -0.06
 -0.03  0.   -0.01  0.    0.    0.01  0.    0.    0.    0.    0.    0.   -0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.01  0.01  0.    0.    0.    0.    0.    0.    0.    0.
  0.    0.    0.    0.    0.   -0.01  0.    0.    0.   -0.01 -0.01 -0.01  0.    0.    0.    0.   -0.    0.01  0.   -0.01  0.    0.01  0.01  0.   -0.01 -0.01  0.    0.01  0.    0.    0.    0.    0.
  0.  ]

ch 0
[-0.07 -0.07 -0.06 -0.06 -0.06 -0.05 -0.05 -0.05 -0.05 -0.05 -0.06 -0.05 -0.04 -0.03  0.05  0.06 -0.02 -0.07 -0.09  0.05  0.66  0.01 -0.1  -0.06 -0.06 -0.05 -0.04 -0.02 -0.01 -0.    0.01  0.03  0.03  0.03  0.03  0.03  0.02  0.04  0.08  0.14  0.19
  0.22  0.23  0.22  0.18  0.15  0.11  0.06  0.02 -0.01 -0.04 -0.05 -0.06 -0.06 -0.07 -0.08 -0.08 -0.08 -0.08 -0.08 -0.07 -0.07 -0.06 -0.07 -0.07 -0.07 -0.06 -0.06 -0.06 -0.07 -0.08 -0.08 -0.08 -0.08 -0.07]
ch 1
[-0.04 -0.04 -0.03 -0.03 -0.03 -0.03 -0.03 -0.04 -0.03 -0.04 -0.04 -0.04 -0.05 -0.01  0.02  0.06  0.03 -0.05 -0.06 -0.1   0.56  0.31 -0.15 -0.05 -0.07 -0.06 -0.05 -0.05 -0.04 -0.02 -0.01 -0.   -0.    0.01  0.01  0.01  0.01  0.02  0.05  0.09  0.15
  0.18  0.2   0.2   0.17  0.14  0.1   0.05  0.01 -0.02 -0.04 -0.05 -0.07 -0.07 -0.08 -0.07 -0.07 -0.08 -0.08 -0.08 -0.07 -0.07 -0.07 -0.06 -0.06 -0.06 -0.06 -0.06 -0.06 -0.06 -0.08 -0.08 -0.06 -0.06 -0.06]

ch 0
[-0.06 -0.06 -0.03  0.05  0.05 -0.06 -0.09  0.33  0.23 -0.1  -0.06 -0.05 -0.04 -0.02 -0.01  0.01  0.03  0.04  0.03  0.03  0.04  0.08  0.16  0.22  0.23  0.21  0.16  0.11  0.05 -0.   -0.04 -0.05 -0.06 -0.07 -0.08 -0.08 -0.08 -0.08 -0.07 -0.06 -0.06
 -0.07 -0.06 -0.06 -0.06 -0.08 -0.08 -0.08 -0.07 -0.07 -0.07 -0.06 -0.06 -0.03  0.04  0.05 -0.06 -0.1   0.41  0.3  -0.06 -0.06 -0.06 -0.06 -0.04]
ch 1
[-0.04 -0.04 -0.02  0.02  0.06 -0.03 -0.06 -0.01  0.59 -0.15 -0.06 -0.06 -0.05 -0.04 -0.02 -0.01 -0.    0.01  0.01  0.02  0.02  0.05  0.11  0.17  0.2   0.19  0.15  0.1   0.04 -0.01 -0.04 -0.05 -0.07 -0.08 -0.07 -0.08 -0.08 -0.08 -0.07 -0.07 -0.06
 -0.06 -0.06 -0.06 -0.06 -0.08 -0.07 -0.06 -0.06 -0.05 -0.04 -0.03 -0.03 -0.02  0.02  0.07 -0.02 -0.04  0.02  0.66 -0.08 -0.04 -0.05 -0.05 -0.05]

```

## A5. qt_sele0604 u2 qtcb_ms = 440.0 (ref 440.35; correct)

FINAL: {"qt_ms": 388, "qtcb_ms": 440, "qtcf_ms": 422}

Last reply (end):
```
FINAL: {"qt_ms": 388, "qtcb_ms": 440, "qtcf_ms": 422}
```

Output seen (end):
```
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
ECG_S_Peaks [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
ECG_T_Peaks [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
ECG_T_Onsets [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
ECG_T_Offsets [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]

ch 0 min -5.52 max -3.865 mean -4.7317004888888885 std 0.2152949586646832
[-4.785 -4.88  -4.73  -4.85  -4.745 -4.49  -4.635 -4.705 -4.795 -4.855
 -4.795 -4.905 -5.09  -4.86  -4.72  -4.515 -4.655 -4.72  -4.8   -4.85
 -4.78  -4.875 -5.31  -4.825 -4.67  -4.485 -4.63  -4.635 -4.76  -4.78 ]
ch 1 min -4.78 max -3.22 mean -4.1221376888888885 std 0.12157600209833486
[-4.13  -4.22  -3.88  -4.29  -4.295 -4.19  -4.08  -4.175 -4.195 -4.175
 -4.03  -4.205 -3.63  -4.225 -4.225 -4.115 -4.07  -4.145 -4.145 -4.14
 -4.02  -4.155 -3.605 -4.23  -4.235 -4.1   -4.08  -4.15  -4.105 -4.105]

ch 0 [ 0.257  0.253  0.114  0.041  0.048  0.02  -0.038 -0.082 -0.095 -0.048
 -0.032 -0.066 -0.141  0.029 -0.326 -0.132 -0.098 -0.054  0.04   0.163
  0.242  0.251  0.1    0.049  0.034  0.013 -0.047 -0.078 -0.099 -0.02
 -0.032 -0.104 -0.131  0.247 -0.571 -0.129 -0.092 -0.056  0.056  0.197]
ch 1 [-0.019  0.059  0.087  0.04  -0.012 -0.014 -0.036 -0.014 -0.021 -0.018
  0.12   0.087 -0.06  -0.071  0.512 -0.055 -0.086 -0.093 -0.09  -0.066
  0.017  0.071  0.059 -0.032 -0.019 -0.02  -0.021 -0.003 -0.019  0.02
  0.099  0.088 -0.038 -0.058  0.511 -0.075 -0.116 -0.137 -0.123 -0.065]

ch 0 hp min -0.7586691497500673 max 0.8495408434138906 std 0.21087452277452892
[-4.8  -4.78 -4.8  -4.81 -4.8  -4.8  -4.8  -4.82 -4.82 -4.83 -4.83 -4.86
 -4.88 -4.88 -4.88 -4.89 -4.89 -4.9  -4.9  -4.9  -4.9  -4.9  -4.9  -4.91
 -4.91 -4.89 -4.88 -4.88 -4.86 -4.82 -4.74 -4.62 -4.46 -4.31 -4.36 -4.46
 -4.58 -4.73 -4.82 -4.93 -5.09 -5.22 -5.32 -5.32 -5.21 -5.07 -4.99 -4.94
 -4.92 -4.9  -4.89 -4.89 -4.89 -4.89 -4.88 -4.87 -4.87 -4.86 -4.86 -4.86
 -4.86 -4.86 -4.85 -4.84 -4.84 -4.84 -4.84 -4.84 -4.84 -4.82 -4.82 -4.81
 -4.8  -4.8  -4.78 -4.78 -4.78 -4.77 -4.76 -4.74]
ch 1 hp min -0.5078172247556412 max 0.8348466881657005 std 0.11211540154499382
[-4.03 -4.04 -4.06 -4.06 -4.06 -4.04 -4.04 -4.03 -4.03 -4.04 -4.06 -4.07
 -4.08 -4.1  -4.12 -4.14 -4.16 -4.18 -4.18 -4.2  -4.2  -4.22 -4.2  -4.2
 -4.2  -4.19 -4.2  -4.2  -4.2  -4.22 -4.22 -4.2  -4.2  -4.22 -4.21 -4.18
 -4.09 -4.   -3.88 -3.74 -3.63 -3.56 -3.62 -3.76 -3.88 -3.99 -4.08 -4.12
 -4.14 -4.16 -4.2  -4.2  -4.2  -4.22 -4.22 -4.23 -4.24 -4.24 -4.24 -4.23
 -4.22 -4.23 -4.24 -4.24 -4.24 -4.24 -4.24 -4.24 -4.24 -4.24 -4.23 -4.24
 -4.24 -4.23 -4.23 -4.24 -4.24 -4.24 -4.24 -4.23]

```

## A6. qt_sele0303 u4 qt_ms = 440.0 (ref 493.73; wrong)

FINAL: {"qt_ms": 440, "qtcb_ms": 470, "qtcf_ms": 460}

Last reply (end):
```
FINAL: {"qt_ms": 440, "qtcb_ms": 470, "qtcf_ms": 460}
```

Output seen (end):
```
d=220186
ch0 R=220311 bl=-0.845 onset=220302 tpk=220389 slope_center=220391 m=-0.0112 tend=220408
ch0 R=220534 bl=-0.845 onset=220525 tpk=220612 slope_center=220655 m=0.0009 tend=220628
ch0 R=220755 bl=-0.840 onset=220746 tpk=220833 slope_center=220840 m=-0.0109 tend=220852
ch0 R=220977 bl=-0.845 onset=220968 tpk=221055 slope_center=221062 m=-0.0115 tend=221074
ch0 R=221199 bl=-0.837 onset=221190 tpk=221278 slope_center=221281 m=-0.0119 tend=221296
ch0 R=221421 bl=-0.830 onset=221412 tpk=221499 slope_center=221553 m=0.0106 tend=221547
ch0 R=221643 bl=-0.835 onset=221634 tpk=221721 slope_center=221728 m=-0.0106 tend=221741
ch0 R=221865 bl=-0.840 onset=221856 tpk=221943 slope_center=221950 m=-0.0105 tend=221963
ch0 R=222087 bl=-0.835 onset=222078 tpk=222166 slope_center=222174 m=-0.0102 tend=222185
ch0 R=222308 bl=-0.835 onset=222299 tpk=222386 slope_center=222396 m=-0.0105 tend=222406
ch0 R=222532 bl=-0.830 onset=222523 tpk=222610 slope_center=222614 m=-0.0098 tend=222630
ch0 R=222756 bl=-0.835 onset=222747 tpk=222834 slope_center=222842 m=-0.0110 tend=222853
ch0 R=222976 bl=-0.840 onset=222967 tpk=223056 slope_center=223063 m=-0.0107 tend=223074
ch0 R=223196 bl=-0.840 onset=223187 tpk=223275 slope_center=223279 m=-0.0105 tend=223294
ch0 R=223416 bl=-0.840 onset=223407 tpk=223495 slope_center=223497 m=-0.0106 tend=223514
ch0 R=223635 bl=-0.845 onset=223626 tpk=223714 slope_center=223725 m=-0.0094 tend=223736
ch0 R=223852 bl=-0.840 onset=223843 tpk=223930 slope_center=223956 m=-0.0019 tend=223984
ch0 R=224070 bl=-0.830 onset=224062 tpk=224149 slope_center=224159 m=-0.0095 tend=224168
ch0 R=224289 bl=-0.840 onset=224280 tpk=224367 slope_center=224376 m=-0.0102 tend=224387
ch0 R=224506 bl=-0.835 onset=224497 tpk=224585 slope_center=224596 m=-0.0074 tend=224608
ch0 R=224723 bl=-0.825 onset=224714 tpk=224800 slope_center=224854 m=-0.0037 tend=224847

[stderr]
Traceback (most recent call last):
  File "/work/_agen.py", line 64, in <module>
    o0,t0=delineate(R,0,verbose=True)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/work/_agen.py", line 46, in delineate
    slope=np.gradient(y[a2:b2])
          ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/numpy/lib/_function_base_impl.py", line 1289, in gradient
    raise ValueError(
ValueError: Shape of array too small to calculate a numerical gradient, at least (edge_order + 1) elements are required.

1045 1045 [ 50 253 457 660 865] [224070 224289 224506 224723 224944]
median abs diff 0.0 max 10

```

## A7. qt_sel872 u5 qt_ms = 398.0 (ref 393.6; correct)

FINAL: {"qt_ms": 398, "qtcb_ms": 415.4, "qtcf_ms": 409.4}

Last reply (end):
```
FINAL: {"qt_ms": 398, "qtcb_ms": 415.4, "qtcf_ms": 409.4}
```

Output seen (end):
```
h larger
    amplitude than the P-wave. The T wave represents the ventricular repolarization of the
    ventricles.On rare occasions, a U wave can be seen following the T wave. The U wave is believed
    to be related to the last remnants of ventricular repolarization.

    Parameters
    ----------
    ecg_cleaned : Union[list, np.array, pd.Series]
        The cleaned ECG channel as returned by ``ecg_clean()``.
    rpeaks : Union[list, np.array, pd.Series]
        The samples at which R-peaks occur. Accessible with the key "ECG_R_Peaks" in the info
        dictionary returned by ``ecg_findpeaks()``.
    sampling_rate : int
        The sampling frequency of ``ecg_signal`` (in Hz, i.e., samples/second). Defaults to 1000.
    method : str
        Can be one of ``"peak"`` for a peak-based method, ``"prominence"`` for a peak-prominence-based
        method (Emrich et al., 2024), ``"cwt"`` for continuous wavelet transform or ``"dwt"`` (default)
        for discrete wavelet transform.
        The ``"prominence"`` method might be useful to detect the waves, allowing to set individual physiological
        limits (see kwargs), while the ``"dwt"`` method might be more precise for detecting the onsets and offsets
        of the waves (but might exhibit lower accuracy when there is significant variation in wave morphology).
        The ``"peak"`` method, which uses the zero-crossings of the signal derivatives, works best with very clean signals.
    show : bool
        If ``True``, will return a plot to visualizing the delineated waves information.
    show_type: str
        The type of delineated waves information showed in the plot.
        Can be ``"peaks"``, ``"bounds_R"``, ``"bounds_T"``, ``"bounds_P"`` or ``"all"``.
    check : bool
        Defaults to ``False``. If ``True``, replaces the delineated features with ``np.nan`` if its
        standardized distance from R-peaks is more than 3.
    **kwargs
        Other optional arguments:
        If using the ``"prominence"`` method, additional parameters (in milliseconds) can be passed to set
        individual physiological limits for the search boundaries:
        - ``max_qrs_interval``: The maximum allowable QRS complex interval. Defaults to 180 ms.
        - ``max_pr_interval``: The maximum PR interval duration. Defaults to 300 ms.
        - ``max_r_rise_time``: Maximum duration for the R-wave rise. Defaults to 120 ms.
        - ``typical_st_segment``: Typical duration of the ST segment. Defaults to 150 ms.
 

```

## A8. qt_sel17453 u1 qt_ms = 375.0 (ref 400.53; wrong)

FINAL: {"qt_ms": 375, "qtcb_ms": 392, "qtcf_ms": 386}

Last reply (end):
```
FINAL: {"qt_ms": 375, "qtcb_ms": 392, "qtcf_ms": 386}
```

Output seen (end):
```
 -0.96
 -0.8  ]
153999 [0.19  0.2   0.21  0.215 0.22  0.225 0.225 0.22  0.205 0.185 0.165] [0.22  0.215 0.21  0.2   0.19  0.18  0.185 0.145 0.125 0.095 0.065]

1047
[0.728 0.728 0.732 0.74  0.748 0.748 0.748 0.756 0.764 0.764 0.764 0.768
 0.768 0.768 0.772]
(array([  8,  76, 257, 272, 211, 118,  46,  36,   9,   6,   2,   2,   2,
         0,   1]), array([0.728 , 0.7616, 0.7952, 0.8288, 0.8624, 0.896 , 0.9296, 0.9632,
       0.9968, 1.0304, 1.064 , 1.0976, 1.1312, 1.1648, 1.1984, 1.232 ]))
[150274 150482 150720 150992 151231 151469 151711 151947 152168 152389
 152619 152836 153051 153275 153506 153719 153926 154135 154351 154550
 154742 154949 155168 155397 155596 155789 155996 156232 156459 156691] [0.832 0.952 1.088 0.956 0.952 0.968 0.944 0.884 0.884 0.92  0.868 0.86
 0.896 0.924 0.852 0.828 0.836 0.864 0.796 0.768 0.828 0.876 0.916 0.796
 0.772 0.828 0.944 0.908 0.928]

ok

152108  -0.055  -0.135
152112  -0.060  -0.145
152116  -0.065  -0.125
152120  -0.055  -0.135
152124  -0.020  -0.095
152128   0.005  -0.080
152132   0.080  -0.055
152136   0.110  -0.060
152140   0.055  -0.110
152144  -0.010  -0.150
152148  -0.040  -0.150
152152  -0.065  -0.160
152156  -0.030  -0.120
152160  -0.070   0.070
152164   1.040   0.815
152168   2.655  -0.190
152172  -0.320  -0.970
152176  -0.540  -0.440
152180  -0.245  -0.150
152184  -0.115  -0.055
152188  -0.085  -0.035
152192  -0.080  -0.035
152196  -0.070  -0.015
152200  -0.065  -0.015
152204  -0.045   0.015
152208  -0.035   0.030
152212  -0.010   0.060
152216   0.015   0.090
152220   0.040   0.130
152224   0.070   0.175
152228   0.125   0.195
152232   0.195   0.210
152236   0.215   0.210
152240   0.220   0.180
152244   0.170   0.080
152248   0.100   0.000
152252  -0.005  -0.065
152256  -0.045  -0.075
152260  -0.045  -0.095
152264  -0.035  -0.085
152268  -0.045  -0.095
152272  -0.045  -0.075
152276  -0.035  -0.075
152280  -0.015  -0.055
152284  -0.015  -0.075
152288  -0.025  -0.065
152292  -0.015  -0.090
152296  -0.015  -0.090
152300  -0.025  -0.105
152304  -0.035  -0.105
152308  -0.035  -0.125
152312  -0.030  -0.110
152316  -0.040  -0.130
152320  -0.045  -0.115
152324  -0.035  -0.125
152328  -0.030  -0.115
152332  -0.030  -0.120
152336  -0.035  -0.115
152340  -0.045  -0.115
152344  -0.045  -0.105
152348   0.015  -0.075
152352   0.035  -0.045
152356   0.125  -0.040
152360   0.080  -0.070
152364   0.040  -0.095
152368  -0.030  -0.125
152372  -0.050  -0.135
152376  -0.060  -0.120
152380  -0.075  -0.050
152384   0.380   0.285

```

## A9. qt_sel16265 u1 qt_ms = 368.0 (ref 406.0; wrong)

FINAL: {"qt_ms": 368, "qtcb_ms": 429, "qtcf_ms": 408}

Last reply (end):
```
FINAL: {"qt_ms": 368, "qtcb_ms": 429, "qtcf_ms": 408}
```

Output seen (end):
```
-0.42 -0.33 -0.23
 150630 +0.01 +0.23 +0.38 +0.51 +0.57 +0.50 -0.04 -0.45 -0.49 -0.47
 150640 -0.32 -0.18 -0.10 -0.04 -0.04 -0.04 -0.06 -0.07 -0.07 -0.06
 150650 -0.05 -0.05 -0.06 -0.07 -0.07 -0.07 -0.07 -0.07 -0.07 -0.07
 150660 -0.08 -0.09 -0.09 -0.10 -0.10 -0.10 -0.10 -0.11 -0.12 -0.12
 150670 -0.14 -0.14 -0.14 -0.14 -0.14 -0.15 -0.17 -0.17 -0.18 -0.18
 150680 -0.17 -0.18 -0.19 -0.20 -0.22 -0.23 -0.24 -0.24 -0.24 -0.24
 150690 -0.24 -0.25 -0.26 -0.27 -0.27 -0.26 -0.26 -0.25 -0.24 -0.24
 150700 -0.23 -0.21 -0.18 -0.16 -0.14 -0.12 -0.11 -0.10 -0.09 -0.07
 150710 -0.05 -0.04 -0.02 -0.01 +0.00 +0.01 +0.01 +0.01 +0.01 +0.01
 150720 +0.01 +0.03 +0.02 +0.01 +0.01 +0.01 +0.01 +0.01 +0.01 +0.01
 150730 +0.01 +0.01 +0.00 -0.01 +0.00 +0.01 +0.01 +0.01 +0.01 +0.01
 150740 +0.01 +0.01 +0.01 +0.01 +0.01 +0.01 +0.01 +0.01 +0.00 -0.01
 150750 -0.01 +0.01 +0.01 +0.01 +0.01 +0.00 -0.01 -0.01 -0.01 +0.00
 150760 +0.01 +0.00 -0.01 -0.01 +0.00 +0.01 +0.03 +0.03 +0.02 +0.01
 150770 -0.01 -0.04 -0.04 -0.03 -0.02 -0.01 -0.01 -0.02 -0.03 -0.03
 150780 -0.04 -0.03 -0.01 +0.00 +0.01 +0.00 -0.01 -0.01 -0.01 -0.01
 150790 -0.01 -0.01 -0.01 -0.01 -0.01 -0.01 -0.01 -0.01 +0.00 +0.01
 150800 +0.05 +0.10 +0.14 +0.15 +0.03 -0.12 -0.28 -0.35 -0.26 -0.12
 150810 +0.09 +0.28 +0.45 +0.50 +0.42 +0.10 -0.42 -0.58 -0.49 -0.35
 150820 -0.20 -0.10 -0.04 -0.03 -0.03 -0.04 -0.04 -0.04 -0.04 -0.04
 150830 -0.04 -0.05 -0.06 -0.07 -0.06 -0.06 -0.06 -0.06 -0.06 -0.07

(224999, 2)
R 150434
  ch0 onset=150424 tpk=150504 tend=-inf amp=0.30 base=-0.54
  ch1 onset=150429 tpk=150500 tend=inf amp=-0.23 base=0.06
R 150632
  ch0 onset=150631 tpk=150698 tend=-inf amp=0.32 base=-0.71
  ch1 onset=150627 tpk=150693 tend=inf amp=-0.20 base=0.12
R 150812
  ch0 onset=150811 tpk=150877 tend=151078.0 amp=0.32 base=-0.39
  ch1 onset=150807 tpk=150874 tend=inf amp=-0.21 base=0.07
R 150983
  ch0 onset=150982 tpk=151049 tend=-inf amp=0.29 base=-0.40
  ch1 onset=150983 tpk=151043 tend=151096.0 amp=-0.22 base=0.06
R 151154
  ch0 onset=151153 tpk=151221 tend=-inf amp=0.29 base=-0.36
  ch1 onset=151149 tpk=151211 tend=151269.0 amp=-0.22 base=0.08
R 151326
  ch0 onset=151317 tpk=151391 tend=151545.0 amp=0.25 base=-0.54
  ch1 onset=151297 tpk=151385 tend=151412.0 amp=-0.17 base=0.06

[stderr]
/work/_agen.py:49: RuntimeWarning: divide by zero encountered in scalar divide
  tend=t0+ipk+j+(base-segt[ipk+j])/slope
/work/_agen.py:53: RuntimeWarning: divide by zero encountered in scalar divide
  tend=t0+ipk+j+(base-segt[ipk+j])/slope

```

## A10. qt_sel46 u5 qtcf_ms = 372.13 (ref 525.42; wrong)

FINAL: {"qt_ms": 376.0, "qtcb_ms": 370.21, "qtcf_ms": 372.13}

Last reply (end):
```
FINAL: {"qt_ms": 376.0, "qtcb_ms": 370.21, "qtcf_ms": 372.13}
```

Output seen (end):
```
<wfdb.io.record.Record object at 0x747027e0f860>
(224993, 2) 250
['ECG1', 'ECG2']
['Produced by xform from record 46, beginning at 9:50.000', 'Produced by xform from record 46, beginning at 3:10:00.000', '------------------------------------------', 'Produced by "/files2/scheherazade/plaguna/database/delay" from record sel46', 'The signal 0 was delayed with a delay=7 samples']

['sel46.dat', 'sel46.hea', '_agen.py']
--- header sel46.hea ---
sel46 2 250 224993
sel46.dat 212 200 12 0 -9 -11702 0 ECG1
sel46.dat 212 200 12 0 17 -31879 0 ECG2
#Produced by xform from record 46, beginning at 9:50.000
#Produced by xform from record 46, beginning at 3:10:00.000
#------------------------------------------
#Produced by "/files2/scheherazade/plaguna/database/delay" from record sel46
#The signal 0 was delayed with a delay=7 samples


 rdrecord
<wfdb.io.record.Record object at 0x747b31f693a0>
shape (224993, 2) fs 250 n_sig 2 sig_name ['ECG1', 'ECG2'] units ['mV', 'mV']
comments ['Produced by xform from record 46, beginning at 9:50.000', 'Produced by xform from record 46, beginning at 3:10:00.000', '------------------------------------------', 'Produced by "/files2/scheherazade/plaguna/database/delay" from record sel46', 'The signal 0 was delayed with a delay=7 samples']
rd_record ERR module 'wfdb' has no attribute 'rd_record'

NONCE_ABC123
files ['sel46.dat', 'sel46.hea', '_agen.py']
size 674979
header:
sel46 2 250 224993
sel46.dat 212 200 12 0 -9 -11702 0 ECG1
sel46.dat 212 200 12 0 17 -31879 0 ECG2
#Produced by xform from record 46, beginning at 9:50.000
#Produced by xform from record 46, beginning at 3:10:00.000
#------------------------------------------
#Produced by "/files2/scheherazade/plaguna/database/delay" from record sel46
#The signal 0 was delayed with a delay=7 samples


[stderr]
Traceback (most recent call last):
  File "/work/_agen.py", line 8, in <module>
    print('hdr', h.fs, h.sig_len, h.n_sig, h.fmt, h.gain, h.baseline, h.sig_name)
                                                  ^^^^^^
AttributeError: 'Record' object has no attribute 'gain'

```

## A11. qt_sel33 u5 qt_ms = 748.0 (ref 770.4; wrong)

FINAL: {"qt_ms": 748, "qtcb_ms": 576, "qtcf_ms": 628}

Last reply (end):
```
FINAL: {"qt_ms": 748, "qtcb_ms": 576, "qtcf_ms": 628}
```

Output seen (end):
```
 0.    0.   -0.01  0.01  0.   -0.   -0.   -0.    0.    0.01  0.01 -0.01  0.    0.    0.    0.01  0.    0.    0.    0.   -0.01 -0.01  0.    0.    0.    0.    0.    0.    0.
  0.01]
ch 1
[ 0.    0.    0.    0.    0.   -0.01  0.   -0.    0.01  0.01  0.01  0.   -0.01 -0.    0.    0.    0.   -0.   -0.   -0.   -0.    0.   -0.    0.02  0.04  0.03  0.   -0.   -0.01 -0.01  0.56  0.46 -0.06
 -0.03  0.   -0.01  0.    0.    0.01  0.    0.    0.    0.    0.    0.   -0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.01  0.01  0.    0.    0.    0.    0.    0.    0.    0.
  0.    0.    0.    0.    0.   -0.01  0.    0.    0.   -0.01 -0.01 -0.01  0.    0.    0.    0.   -0.    0.01  0.   -0.01  0.    0.01  0.01  0.   -0.01 -0.01  0.    0.01  0.    0.    0.    0.    0.
  0.  ]

ch 0
[-0.07 -0.07 -0.06 -0.06 -0.06 -0.05 -0.05 -0.05 -0.05 -0.05 -0.06 -0.05 -0.04 -0.03  0.05  0.06 -0.02 -0.07 -0.09  0.05  0.66  0.01 -0.1  -0.06 -0.06 -0.05 -0.04 -0.02 -0.01 -0.    0.01  0.03  0.03  0.03  0.03  0.03  0.02  0.04  0.08  0.14  0.19
  0.22  0.23  0.22  0.18  0.15  0.11  0.06  0.02 -0.01 -0.04 -0.05 -0.06 -0.06 -0.07 -0.08 -0.08 -0.08 -0.08 -0.08 -0.07 -0.07 -0.06 -0.07 -0.07 -0.07 -0.06 -0.06 -0.06 -0.07 -0.08 -0.08 -0.08 -0.08 -0.07]
ch 1
[-0.04 -0.04 -0.03 -0.03 -0.03 -0.03 -0.03 -0.04 -0.03 -0.04 -0.04 -0.04 -0.05 -0.01  0.02  0.06  0.03 -0.05 -0.06 -0.1   0.56  0.31 -0.15 -0.05 -0.07 -0.06 -0.05 -0.05 -0.04 -0.02 -0.01 -0.   -0.    0.01  0.01  0.01  0.01  0.02  0.05  0.09  0.15
  0.18  0.2   0.2   0.17  0.14  0.1   0.05  0.01 -0.02 -0.04 -0.05 -0.07 -0.07 -0.08 -0.07 -0.07 -0.08 -0.08 -0.08 -0.07 -0.07 -0.07 -0.06 -0.06 -0.06 -0.06 -0.06 -0.06 -0.06 -0.08 -0.08 -0.06 -0.06 -0.06]

ch 0
[-0.06 -0.06 -0.03  0.05  0.05 -0.06 -0.09  0.33  0.23 -0.1  -0.06 -0.05 -0.04 -0.02 -0.01  0.01  0.03  0.04  0.03  0.03  0.04  0.08  0.16  0.22  0.23  0.21  0.16  0.11  0.05 -0.   -0.04 -0.05 -0.06 -0.07 -0.08 -0.08 -0.08 -0.08 -0.07 -0.06 -0.06
 -0.07 -0.06 -0.06 -0.06 -0.08 -0.08 -0.08 -0.07 -0.07 -0.07 -0.06 -0.06 -0.03  0.04  0.05 -0.06 -0.1   0.41  0.3  -0.06 -0.06 -0.06 -0.06 -0.04]
ch 1
[-0.04 -0.04 -0.02  0.02  0.06 -0.03 -0.06 -0.01  0.59 -0.15 -0.06 -0.06 -0.05 -0.04 -0.02 -0.01 -0.    0.01  0.01  0.02  0.02  0.05  0.11  0.17  0.2   0.19  0.15  0.1   0.04 -0.01 -0.04 -0.05 -0.07 -0.08 -0.07 -0.08 -0.08 -0.08 -0.07 -0.07 -0.06
 -0.06 -0.06 -0.06 -0.06 -0.08 -0.07 -0.06 -0.06 -0.05 -0.04 -0.03 -0.03 -0.02  0.02  0.07 -0.02 -0.04  0.02  0.66 -0.08 -0.04 -0.05 -0.05 -0.05]

```

## A12. qt_sel232 u1 qtcb_ms = 552.4 (ref 487.45; wrong)

FINAL: {"qt_ms": 470.2, "qtcb_ms": 552.4, "qtcf_ms": 526.3}

Last reply (end):
```
FINAL: {"qt_ms": 470.2, "qtcb_ms": 552.4, "qtcf_ms": 526.3}
```

Output seen (end):
```
.075 0.07
155932  -0.115 0.06
155942  -0.095 0.045
155952  -0.09 0.035

155800 -0.045 0.02
155803 -0.05 0.08
155806 0.02 0.085
155809 0.24 0.115
155812 0.815 -0.12
155815 0.14 -0.285
155818 -0.435 0.095
155821 -0.275 0.29
155824 -0.29 0.315
155827 -0.175 0.415
155830 -0.18 0.48
155833 -0.18 0.26
155836 -0.065 0.03
155839 -0.035 0.035
155842 -0.06 -0.03
155845 -0.04 -0.015
155848 -0.045 0.015
155851 -0.04 -0.025
155854 -0.015 -0.01
155857 -0.035 -0.02
155860 -0.015 -0.02
155863 0.03 -0.01
155866 0.03 -0.045
155869 0.055 -0.05
155872 0.105 -0.075
155875 0.14 -0.105
155878 0.195 -0.12
155881 0.25 -0.125
155884 0.265 -0.15
155887 0.25 -0.095
155890 0.225 -0.09
155893 0.1 -0.045
155896 0.075 0.025
155899 0.02 0.005
155902 -0.03 0.05
155905 -0.055 0.07

dwt
(np.int64(155441), np.float64(155430.0), np.float64(155530.0), np.float64(400.0))
(np.int64(155626), np.float64(155589.0), np.float64(155720.0), np.float64(524.0))
(np.int64(155812), np.float64(155764.0), np.float64(155912.0), np.float64(592.0))
(np.int64(155999), np.float64(155981.0), np.float64(156094.0), np.float64(452.0))
(np.int64(156185), np.float64(156156.0), np.float64(156277.0), np.float64(484.0))
(np.int64(156373), np.float64(156338.0), np.float64(156465.0), np.float64(508.0))
(np.int64(156559), np.float64(156532.0), np.float64(156634.0), np.float64(408.0))
(np.int64(156742), np.float64(156717.0), np.float64(156836.0), np.float64(476.0))
(np.int64(156930), np.float64(156906.0), np.float64(157019.0), np.float64(452.0))
(np.int64(157121), np.float64(157105.0), np.float64(157203.0), np.float64(392.0))
(np.int64(157308), np.float64(157281.0), np.float64(157402.0), np.float64(484.0))
mean qt 470.1818181818182
peak
(np.int64(155441), nan, np.float64(155533.0), np.float64(nan))
(np.int64(155626), nan, np.float64(155719.0), np.float64(nan))
(np.int64(155812), nan, np.float64(155897.0), np.float64(nan))
(np.int64(155999), nan, np.float64(156143.0), np.float64(nan))
(np.int64(156185), nan, np.float64(156276.0), np.float64(nan))
(np.int64(156373), nan, np.float64(156464.0), np.float64(nan))
(np.int64(156559), nan, np.float64(156701.0), np.float64(nan))
(np.int64(156742), nan, np.float64(156828.0), np.float64(nan))
(np.int64(156930), nan, np.float64(157056.0), np.float64(nan))
(np.int64(157121), nan, np.float64(157266.0), np.float64(nan))
(np.int64(157308), nan, np.float64(157400.0), np.float64(nan))
mean qt nan

[stderr]
/work/_agen.py:40: RuntimeWarning: Mean of empty slice
  print('mean qt',np.nanmean(qts))

```

## A13. qt_sele0114 u4 qtcb_ms = 412.0 (ref 354.62; wrong)

FINAL: {"qt_ms": 470, "qtcb_ms": 412, "qtcf_ms": 430}

Last reply (end):
```
FINAL: {"qt_ms": 470, "qtcb_ms": 412, "qtcf_ms": 430}
```

Output seen (end):
```
 159635 159934 160154 160344 160734 161006 161234 161650]
diffs [419 398 392 291 226 235 187 386 319 404 403 384 394 398 301 245 423 385
 303 262 224 205 389 280 255 423 386 396 359 389 299 220 190 390 272 228
 416]

151280 9.03 6.905
151284 9.125 6.93
151288 8.94 7.405
151292 8.24 7.97
151296 8.635 6.97
151300 9.085 6.72
151304 8.915 6.885
151308 8.975 6.945
151312 9.015 6.945
151316 9.02 6.965
151320 9.03 6.965
151324 9.015 6.965
151328 9.015 6.955
151332 8.985 6.98
151336 9.0 6.99
151340 9.015 7.025
151344 8.985 7.055
151348 8.985 7.04
151352 8.985 7.08
151356 8.975 7.105
151360 8.975 7.16
151364 8.985 7.135
151368 9.015 7.135
151372 9.055 7.09
151376 9.115 7.03
151380 9.135 6.945
151384 9.14 6.87
151388 9.125 6.855
151392 9.085 6.86
151396 9.05 6.905
151400 9.015 6.905
151404 9.015 6.93
151408 8.985 6.915
151412 9.0 6.915
151416 9.015 6.915
151420 9.015 6.915
151424 9.015 6.905
151428 9.0 6.905
151432 9.03 6.885
151436 9.03 6.88
151440 9.03 6.88
151444 9.03 6.86
151448 9.03 6.855
151452 9.03 6.855
151456 9.0 6.845
151460 9.02 6.855
151464 9.02 6.845
151468 9.02 6.835
151472 9.015 6.855
151476 9.055 6.845
151480 9.02 6.855
151484 9.015 6.855
151488 9.03 6.845
151492 9.05 6.835
151496 9.015 6.845
151500 9.015 6.835
151504 9.03 6.845
151508 9.03 6.835
151512 9.015 6.845
151516 9.02 6.82
151520 9.015 6.835
151524 9.03 6.82
151528 9.015 6.835
151532 9.015 6.83
151536 9.015 6.835
151540 9.015 6.845
151544 8.995 6.835
151548 9.015 6.8
151552 9.0 6.835
151556 9.0 6.845
151560 9.0 6.845
151564 8.985 6.81
151568 8.995 6.855
151572 8.985 6.835
151576 8.985 6.855
151580 8.985 6.835
151584 8.985 6.855
151588 9.015 6.86
151592 9.0 6.855
151596 8.985 6.855
151600 8.985 6.86
151604 9.0 6.88
151608 8.995 6.88
151612 8.985 6.88
151616 8.985 6.88
151620 8.985 6.885
151624 8.995 6.895
151628 8.985 6.905
151632 8.985 6.915
151636 8.985 6.93
151640 8.985 6.92
151644 8.985 6.93
151648 8.985 6.905
151652 9.015 6.92
151656 8.985 6.905
151660 8.985 6.93
151664 8.985 6.945
151668 9.015 6.955
151672 9.015 6.955
151676 9.045 6.97
151680 9.05 6.99
151684 9.015 6.965
151688 8.985 6.92
151692 8.985 6.92
151696 8.96 6.945
151700 8.985 6.955
151704 8.995 6.97
151708 9.03 7.135
151712 8.425 7.965
151716 8.12 7.725
151720 9.055 6.7
151724 8.91 6.895
151728 8.89 6.955
151732 8.975 6.995
151736 8.975 6.99
151740 8.985 6.995
151744 8.985 6.995
151748 9.015 7.015
151752 9.015 7.03
151756 8.985 7.03
151760 8.985 7.065
151764 8.995 7.075
151768 8.995 7.125
151772 8.985 7.125
151776 8.965 7.16

```

## A14. qt_sele0609 u2 qt_ms = 405.0 (ref 456.0; wrong)

FINAL: {"qt_ms": 405, "qtcb_ms": 448, "qtcf_ms": 434}

Last reply (end):
```
FINAL: {"qt_ms": 405, "qtcb_ms": 448, "qtcf_ms": 434}
```

Output seen (end):
```
 0.]
ECG_Q_Peaks (225000,) 0 0.0 1.0 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
ECG_R_Onsets (225000,) 0 0.0 1.0 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
ECG_R_Offsets (225000,) 0 0.0 1.0 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
ECG_S_Peaks (225000,) 0 0.0 1.0 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
ECG_T_Peaks (225000,) 0 0.0 1.0 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
ECG_T_Onsets (225000,) 0 0.0 1.0 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
ECG_T_Offsets (225000,) 0 0.0 1.0 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
ECG_R_Onsets in win []
ECG_R_Offsets in win []
ECG_T_Onsets in win []
ECG_T_Offsets in win []

lead 0
ECG_R_Onsets 1126 [ 220  415  607  801  996 1193 1390 1587 1788 1989 2189 2389 2594 2796
 2999 3206 3409 3610 3808 4010] [223421 223585 223752 223918 224084 224252 224422 224591 224762 224934]
ECG_R_Offsets 1125 [ 253  450  645  834 1030 1228 1429 1620 1826 2025 2219 2424 2620 2829
 3031 3236 3444 3640 3843 4039] [223287 223452 223620 223783 223954 224116 224285 224455 224622 224793]
ECG_T_Onsets 1125 [ 291  483  673  871 1068 1263 1459 1656 1852 2057 2259 2458 2665 2864
 3068 3277 3482 3678 3873 4083] [223321 223486 223652 223825 223978 224147 224299 224488 224659 224827]
ECG_T_Offsets 1125 [ 317  513  709  909 1094 1288 1489 1683 1879 2089 2288 2494 2692 2898
 3103 3302 3515 3708 3910 4111] [223355 223520 223680 223851 224013 224177 224308 224522 224685 224859]
ECG_T_Peaks 1125 [ 304  499  692  886 1080 1277 1475 1671 1873 2074 2273 2476 2679 2880
 3083 3292 3496 3694 3894 4095] [223341 223502 223668 223835 224001 224165 224304 224505 224673 224844]
lead 1
ECG_R_Onsets 1126 [ 225  419  613  808  999 1198 1393 1594 1794 1992 2191 2394 2595 2800
 3003 3212 3416 3616 3814 4012] [223424 223589 223756 223921 224087 224255 224425 224595 224765 224937]
ECG_R_Offsets 1098 [ 258  437  629  823 1032 1214 1412 1608 1827 2026 2229 2424 2632 2818
 3021 3228 3449 3643 3848 4051] [223295 223459 223626 223789 223953 224124 224298 224461 224628 224800]
ECG_T_Onsets 1098 [ 303  499  695  887 1083 1282 1481 1670 1882 2079 2276 2479 2673 2881
 3084 3301 3505 3699 3897 4101] [223338 223496 223668 223824 223994 224170 224338 224491 224685 224831]
ECG_T_Offsets 1098 [ 318  510  707  900 1097 1287 1491 1680 1892 2088 2288 2487 2689 2893
 3095 3309 3513 3714 3908 4109] [223355 223521 223683 223849 224011 224181 224348 224520 224695 224884]
ECG_T_Peaks 1098 [ 314  507  702  895 1090 1285 1487 1678 1886 2085 2284 2485 2686 2890
 3090 3302 3509 3705 3902 4104] [223350 223513 223676 223844 224009 224177 224344 224515 224687 224854]

```

## A15. qt_sele0114 u5 qt_ms = 490.4 (ref 416.27; wrong)

FINAL: {"qt_ms": 490.4, "qtcb_ms": 417.6, "qtcf_ms": 440.0}

Last reply (end):
```
FINAL: {"qt_ms": 490.4, "qtcb_ms": 417.6, "qtcf_ms": 440.0}
```

Output seen (end):
```
9941 T_On=159969 T_Of=160020 T_Pe=159997

beat 27 R 160335
 lead 0 R_On=160298 R_Of=160344 T_On=160350 T_Of=160377 T_Pe=160367
 lead 1 R_On=160302 R_Of=160351 T_On=160384 T_Of=160430 T_Pe=160406

beat 28 R 160726
 lead 0 R_On=160689 R_Of=160734 T_On=160801 T_Of=160836 T_Pe=160820
 lead 1 R_On=160691 R_Of=160742 T_On=160774 T_Of=160821 T_Pe=160797

beat 29 R 160998
 lead 0 R_On=160959 R_Of=161006 T_On=161071 T_Of=161112 T_Pe=161090
 lead 1 R_On=160962 R_Of=161013 T_On=161043 T_Of=161092 T_Pe=161070


LEAD 0 median aligned
 -80   0.000
 -76   0.000
 -72   0.000
 -68   0.000
 -64   0.000
 -60   0.000
 -56   0.000
 -52   0.000
 -48   0.000
 -44   0.000
 -40   0.025
 -36   0.005
 -32   0.000
 -28   0.000
 -24   0.000
 -20   0.000
 -16  -0.005
 -12   0.000
  -8   0.055
  -4  -0.030
   0  -0.700
   4  -0.570
   8   0.065
  12  -0.095
  16  -0.080
  20  -0.020
  24   0.000
  28   0.000
  32   0.000
  36   0.000
  40  -0.005
  44  -0.010
  48  -0.010
  52  -0.015
  56  -0.015
  60  -0.035
  64  -0.035
  68  -0.035
  72  -0.030
  76  -0.005
  80   0.030
  84   0.075
  88   0.130
  92   0.155
  96   0.155
 100   0.120
 104   0.085
 108   0.050
 112   0.025
 116   0.005
 120   0.005
 124   0.000
 128   0.010
 132   0.010
 136   0.015
 140   0.020
 144   0.025
 148   0.025
 152   0.025
 156   0.025
 160   0.025
 164   0.025
 168   0.020
 172   0.020
 176   0.025
 180   0.015
 184   0.015
 188   0.015
 192   0.015
 196   0.020
 200   0.020
 204   0.020
 208   0.015
 212   0.015
 216   0.015

LEAD 1 median aligned
 -80  -0.005
 -76  -0.005
 -72   0.000
 -68   0.000
 -64   0.000
 -60   0.000
 -56   0.000
 -52   0.010
 -48   0.025
 -44   0.045
 -40   0.070
 -36   0.050
 -32   0.050
 -28   0.015
 -24   0.005
 -20   0.010
 -16   0.020
 -12   0.045
  -8   0.070
  -4   0.425
   0   1.085
   4   0.455
   8  -0.155
  12   0.015
  16   0.070
  20   0.085
  24   0.090
  28   0.095
  32   0.105
  36   0.110
  40   0.125
  44   0.135
  48   0.155
  52   0.170
  56   0.200
  60   0.230
  64   0.265
  68   0.295
  72   0.305
  76   0.305
  80   0.260
  84   0.195
  88   0.095
  92   0.000
  96  -0.045
 100  -0.050
 104  -0.005
 108   0.035
 112   0.055
 116   0.075
 120   0.080
 124   0.080
 128   0.080
 132   0.075
 136   0.070
 140   0.060
 144   0.050
 148   0.035
 152   0.025
 156   0.015
 160   0.005
 164  -0.005
 168  -0.010
 172  -0.015
 176  -0.025
 180  -0.015
 184  -0.025
 188  -0.027
 192  -0.030
 196  -0.030
 200  -0.035
 204  -0.025
 208  -0.035
 212  -0.035
 216  -0.035

```

## A16. qt_sele0607 u1 qt_ms = 396.0 (ref 400.8; correct)

FINAL: {"qt_ms": 396, "qtcb_ms": 472, "qtcf_ms": 445}

Last reply (end):
```
FINAL: {"qt_ms": 396, "qtcb_ms": 472, "qtcf_ms": 445}
```

Output seen (end):
```
Peaks': 1183, 'ECG_P_Onsets': 1183, 'ECG_P_Offsets': 1183, 'ECG_Q_Peaks': 1183, 'ECG_R_Onsets': 1183, 'ECG_R_Offsets': 1172, 'ECG_S_Peaks': 1182, 'ECG_T_Peaks': 1172, 'ECG_T_Onsets': 1172, 'ECG_T_Offsets': 1172}
     ECG_P_Peaks  ECG_P_Onsets  ECG_P_Offsets  ECG_Q_Peaks  ECG_R_Onsets  ECG_R_Offsets  ECG_S_Peaks  ECG_T_Peaks  ECG_T_Onsets  ECG_T_Offsets
770            0             0              0            0             0              0            0            0             0              0
771            0             0              0            0             0              0            0            0             0              0
772            0             0              0            0             0              0            0            0             0              0
773            0             0              0            0             0              0            0            0             0              0
774            0             0              0            0             0              0            0            0             0              0
775            0             0              0            0             0              0            0            0             0              0
776            0             0              0            0             0              0            0            0             0              0
777            0             0              0            0             0              0            0            0             0              0
778            0             0              0            0             0              0            1            0             0              0
779            0             0              0            0             0              0            0            0             0              0
780            0             0              0            0             0              0            0            0             0              0
781            0             0              0            0             0              0            0            0             0              0
782            0             0              0            0             0              0            0            0             0              0
783            0             0              0            0             0              0            0            0             0              0
784            0             0              0            0             0              0            0            0             0              0

```

## A17. qt_sel872 u3 qt_ms = 435.0 (ref 393.6; wrong)

FINAL: {"qt_ms": 435, "qtcb_ms": 454, "qtcf_ms": 447}

Last reply (end):
```
FINAL: {"qt_ms": 435, "qtcb_ms": 454, "qtcf_ms": 447}
```

Output seen (end):
```
-0.097 -0.098 -0.097 -0.097 -0.097] | [ 0.078  0.059  0.042  0.027  0.014  0.002 -0.008 -0.017 -0.026 -0.034 -0.04  -0.044 -0.046 -0.046 -0.047 -0.048 -0.05  -0.051 -0.053 -0.054]
100 [-0.096 -0.094 -0.094 -0.093 -0.094 -0.094 -0.092 -0.09  -0.088 -0.086 -0.084 -0.082 -0.081 -0.08  -0.079 -0.077 -0.074 -0.072 -0.071 -0.071] | [-0.054 -0.053 -0.051 -0.05  -0.049 -0.05  -0.05  -0.049 -0.048 -0.046 -0.044 -0.043 -0.043 -0.043 -0.043 -0.043 -0.041 -0.04  -0.039 -0.037]
120 [-0.071 -0.071 -0.069 -0.067 -0.065 -0.064 -0.063 -0.064 -0.065 -0.066 -0.067 -0.066 -0.066 -0.066 -0.068 -0.07  -0.072 -0.073 -0.073 -0.073] | [-0.037 -0.036 -0.036 -0.036 -0.035 -0.033 -0.032 -0.031 -0.03  -0.031 -0.033 -0.035 -0.036 -0.035 -0.033 -0.033 -0.033 -0.034 -0.035 -0.036]
140 [-0.074 -0.076 -0.078 -0.079 -0.08  -0.079 -0.079 -0.079 -0.079 -0.079 -0.08  -0.082 -0.083 -0.084 -0.084 -0.084 -0.083 -0.083 -0.084 -0.085] | [-0.036 -0.037 -0.037 -0.037 -0.037 -0.038 -0.04  -0.04  -0.04  -0.04  -0.04  -0.041 -0.042 -0.043 -0.043 -0.044 -0.044 -0.043 -0.043 -0.044]
160 [-0.085 -0.083 -0.078 -0.072 -0.065 -0.06  -0.056 -0.052 -0.048 -0.043 -0.037 -0.031 -0.024 -0.017 -0.008  0.     0.007  0.011  0.013  0.015] | [-0.044 -0.044 -0.042 -0.041 -0.04  -0.038 -0.035 -0.032 -0.029 -0.027 -0.024 -0.02  -0.014 -0.009 -0.005 -0.003 -0.001  0.001  0.003  0.004]
180 [ 0.017  0.017  0.015  0.01   0.001 -0.009 -0.02  -0.031 -0.042 -0.053 -0.063 -0.071 -0.076 -0.08  -0.083 -0.086 -0.088 -0.09  -0.092 -0.095] | [ 0.003  0.    -0.002 -0.005 -0.007 -0.008 -0.009 -0.011 -0.015 -0.02  -0.026 -0.032 -0.037 -0.04  -0.042 -0.043 -0.045 -0.047 -0.049 -0.05 ]
200 [-0.097 -0.097 -0.096 -0.096 -0.096 -0.098 -0.099 -0.099 -0.097 -0.094 -0.092 -0.089 -0.087 -0.085 -0.084 -0.085 -0.086 -0.089 -0.09  -0.085] | [-0.05  -0.05  -0.049 -0.048 -0.047 -0.047 -0.047 -0.048 -0.049 -0.049 -0.048 -0.046 -0.045 -0.045 -0.045 -0.045 -0.045 -0.044 -0.042 -0.041]
220 [-0.065 -0.022  0.052  0.157  0.289  0.431  0.562  0.66   0.703  0.68   0.591  0.454  0.306  0.18   0.095  0.046  0.018 -0.001 -0.021 -0.046] | [-0.041 -0.039 -0.036 -0.028 -0.017 -0.003  0.009  0.016  0.012 -0.004 -0.033 -0.075 -0.124 -0.17  -0.203 -0.216 -0.209 -0.187 -0.158 -0.128]
240 [-0.072 -0.091 -0.096 -0.088 -0.075 -0.064 -0.056 -0.052 -0.05  -0.049 -0.049 -0.049 -0.048 -0.046 -0.042 -0.038 -0.035 -0.032 -0.029 -0.026] | [-0.102 -0.081 -0.065 -0.051 -0.035 -0.016  0.001  0.015  0.024  0.029  0.031  0.032  0.032  0.032  0.032  0.032  0.034  0.036  0.04   0.043]

```

## A18. qt_sel42 u4 qt_ms = 444.0 (ref 447.87; correct)

FINAL: {"qt_ms": 444.0, "qtcb_ms": 520.0, "qtcf_ms": 494.0}

Last reply (end):
```
FINAL: {"qt_ms": 444.0, "qtcb_ms": 520.0, "qtcf_ms": 494.0}
```

Output seen (end):
```
   -1.49    0.94
154069   -1.54    1.12
154074   -1.54    1.13

--- QRS around 150523 (indices, lead0, lead1) ---
150493   -0.38   -0.07
150494   -0.39   -0.07
150495   -0.36   -0.07
150496   -0.35   -0.06
150497   -0.35   -0.05
150498   -0.38   -0.04
150499   -0.39   -0.03
150500   -0.38   -0.03
150501   -0.39   -0.03
150502   -0.37   -0.03
150503   -0.33   -0.01
150504   -0.28    0.01
150505   -0.24    0.02
150506   -0.17    0.03
150507   -0.07    0.02
150508    0.04   -0.01
150509    0.18   -0.09
150510    0.39   -0.17
150511    0.62   -0.27
150512    0.86   -0.36
150513    1.06   -0.45
150514    1.23   -0.53
150515    1.36   -0.59
150516    1.44   -0.66
150517    1.55   -0.74
150518    1.75   -0.80
150519    2.08   -0.84
150520    2.36   -0.81
150521    2.56   -0.69
150522    2.56   -0.49
150523    2.56   -0.33
150524    2.56   -0.37
150525    2.56   -0.63
150526    2.56   -0.94
150527    2.56   -1.13
150528    2.56   -1.29
150529    2.56   -1.34
150530    2.56   -1.39
150531    2.56   -1.39
150532    2.56   -1.36
150533    2.56   -1.29
150534    2.56   -1.17
150535    2.56   -1.08
150536    2.56   -0.99
150537    2.56   -0.94
150538    2.56   -0.84
150539    2.56   -0.73
150540    2.56   -0.59
150541    1.97   -0.46
150542    1.08   -0.36
150543    0.40   -0.30
150544    0.06   -0.27
150545   -0.11   -0.24
150546   -0.20   -0.23
150547   -0.28   -0.21
150548   -0.34   -0.20
150549   -0.39   -0.20
150550   -0.42   -0.18
150551   -0.46   -0.18
150552   -0.49   -0.17
150553   -0.54   -0.17
150554   -0.56   -0.15
150555   -0.59   -0.15
150556   -0.62   -0.14
150557   -0.67   -0.13
150558   -0.70   -0.12
150559   -0.73   -0.12
150560   -0.78   -0.11
150561   -0.81   -0.10
150562   -0.85   -0.09

QT=693.6 QTcB=813.2 QTcF=771.1 n=30
QTlist [696.0, 700.0, 704.0, 696.0, 688.0, 692.0, 692.0, 696.0, 700.0, 700.0, 696.0, 688.0, 692.0, 696.0, 692.0, 688.0, 696.0, 696.0, 688.0, 696.0, 704.0, 692.0, 692.0, 700.0, 696.0, 648.0, 700.0, 696.0, 692.0, 696.0]
RRmean 0.7276

0.05 QT 688.7 QTcB 807.1 QTcF 765.1
0.1 QT 666.0 QTcB 780.5 QTcF 739.8
0.15 QT 650.1 QTcB 761.7 QTcF 721.8
0.2 QT 638.3 QTcB 747.4 QTcF 708.3

0.1 438.3 509.8 483.5
0.15 420.5 493.3 467.8
0.2 416.5 488.5 463.3
0.25 412.4 483.7 458.7
0.3 409.2 479.9 455.1

QT=606.8 QTcB=718.1 QTcF=679.7 n=30
QTlist [540.0, 724.0, 596.0, 532.0, 0.0, 568.0, 2468.0, 2424.0, 508.0, 540.0, 528.0, 528.0, 520.0, 532.0, 372.0, 464.0, 0.0, 524.0, 520.0, 524.0, 536.0, 0.0, 548.0, 516.0, 524.0, 532.0, 532.0, 532.0, 528.0, 544.0]

```

## A19. qt_sel14157 u2 qt_ms = 393.0 (ref 419.2; wrong)

FINAL: {"qt_ms": 393, "qtcb_ms": 432, "qtcf_ms": 419}

Last reply (end):
```
FINAL: {"qt_ms": 393, "qtcb_ms": 432, "qtcf_ms": 419}
```

Output seen (end):
```
0  -2.355
151102   2.605  -3.010
151103   2.350  -3.360


FULL BEAT 150686 to 150893
150686   2.665  -2.480
150688   2.375  -3.375
150690   1.560  -3.540
150692   0.845  -2.830
150694   0.425  -2.055
150696  -0.215  -1.555
150698  -0.565  -1.065
150700  -0.585  -0.705
150702  -0.500  -0.480
150704  -0.365  -0.250
150706  -0.260   0.020
150708  -0.240   0.195
150710  -0.225   0.225
150712  -0.220   0.220
150714  -0.235   0.255
150716  -0.240   0.285
150718  -0.250   0.290
150720  -0.285   0.300
150722  -0.310   0.315
150724  -0.345   0.330
150726  -0.380   0.345
150728  -0.395   0.385
150730  -0.405   0.430
150732  -0.425   0.455
150734  -0.450   0.490
150736  -0.490   0.540
150738  -0.540   0.580
150740  -0.620   0.615
150742  -0.645   0.670
150744  -0.740   0.725
150746  -0.750   0.765
150748  -0.785   0.805
150750  -0.790   0.810
150752  -0.820   0.840
150754  -0.810   0.840
150756  -0.765   0.810
150758  -0.630   0.750
150760  -0.505   0.695
150762  -0.335   0.605
150764  -0.155   0.495
150766  -0.015   0.405
150768   0.075   0.305
150770   0.130   0.225
150772   0.110   0.145
150774   0.085   0.100
150776   0.100   0.090
150778   0.100   0.080
150780   0.085   0.060
150782   0.100   0.065
150784   0.085   0.080
150786   0.070   0.065
150788   0.050   0.050
150790   0.010   0.050
150792   0.000   0.070
150794   0.005   0.075
150796  -0.005   0.065
150798   0.000   0.070
150800   0.015   0.085
150802   0.010   0.075
150804   0.010   0.055
150806   0.000   0.060
150808  -0.010   0.065
150810   0.015   0.050
150812   0.030   0.035
150814   0.025   0.035
150816   0.050   0.045
150818   0.060   0.045
150820   0.060   0.040
150822   0.030   0.080
150824   0.005   0.175
150826   0.000   0.165
150828   0.025   0.185
150830   0.085   0.165
150832   0.125   0.075
150834   0.140   0.040
150836   0.160   0.000
150838   0.130   0.000
150840   0.140  -0.020
150842   0.140   0.000
150844   0.110  -0.010
150846   0.120   0.010
150848   0.105   0.020
150850   0.070   0.000
150852   0.070  -0.010
150854   0.080  -0.010
150856   0.085  -0.005
150858   0.060  -0.025
150860   0.055   0.000
150862   0.080  -0.010
150864   0.090   0.000
150866   0.095   0.020
150868   0.085   0.010
150870   0.110   0.010
150872   0.085   0.015
150874   0.050   0.025
150876   0.100   0.015
150878   0.110   0.010
150880   0.100  -0.005
150882   0.120   0.000
150884   0.180   0.025
150886   0.410   0.090
150888   0.700   0.095
150890   1.455  -0.530
150892   2.380  -2.115
150894   2.490  -3.225

```

## A20. qt_sel15814 u2 qt_ms = 488.0 (ref 466.5; wrong)

FINAL: {"qt_ms": 488.0, "qtcb_ms": 521.4, "qtcf_ms": 510.6}

Last reply (end):
```
FINAL: {"qt_ms": 488.0, "qtcb_ms": 521.4, "qtcf_ms": 510.6}
```

Output seen (end):
```
 *
151304 -0.160                      *
151308 -0.565          *
151312 -0.795    *
151316 -0.555           *
151320 -0.530           *
151324 -0.445              *
151328 -0.310                 *
151332 -0.125                       *
151336 -0.015                          *
151340 +0.085                            *
151344 +0.200                                *
151348 +0.215                                *
151352 +0.235                                 *
151356 +0.245                                 *
151360 +0.265                                 *
151364 +0.290                                  *
151368 +0.300                                  *
151372 +0.340                                   *
151376 +0.340                                   *
151380 +0.335                                   *
151384 +0.335                                   *
151388 +0.310                                   *
151392 +0.250                                 *
151396 +0.205                                *
151400 +0.150                              *
151404 +0.100                             *
151408 +0.055                            *
151412 +0.055                            *
151416 +0.035                           *
151420 +0.050                           *
151424 +0.025                           *
151428 +0.025                           *
151432 +0.030                           *
151436 +0.025                           *
151440 +0.030                           *
151444 +0.030                           *
151448 +0.040                           *
151452 +0.030                           *
151456 +0.030                           *
151460 +0.025                           *
151464 +0.050                           *
151468 +0.060                            *
151472 +0.080                            *
151476 +0.105                             *
151480 +0.085                            *
151484 +0.040                           *
151488 +0.035                           *
151492 +0.030                           *
151496 +0.005                          *
151500 -0.020                         *
151504 -0.020                         *
151508 -0.020                         *
151512 -0.015                          *
151516 -0.015                          *
151520 +0.155                              *
151524 -0.155                      *
151528 -0.615         *
151532 -0.795    *
151536 -0.620         *
151540 -0.535           *
151544 -0.445              *
151548 -0.285                  *

```

## A21. qt_sel50 u4 qtcf_ms = 549.94 (ref 434.74; wrong)

FINAL: {"qt_ms": 544.93, "qtcb_ms": 550.63, "qtcf_ms": 549.94}

Last reply (end):
```
FINAL: {"qt_ms": 544.93, "qtcb_ms": 550.63, "qtcf_ms": 549.94}
```

Output seen (end):
```
['sel50.dat', 'sel50.hea', '_agen.py']
250 224993 2 ['ECG1', 'ECG2'] ['mV', 'mV']
(224993, 2) [[-0.015  0.045]
 [-0.015  0.05 ]
 [-0.01   0.06 ]
 [ 0.     0.07 ]
 [ 0.     0.065]]
[200.0, 200.0] [0, 0]

fs 250 len 224993 corr 0.955241733173785
range [-1.395 -1.365] [1.795 2.36 ]
ch 0 n 628 win [150611, 150954, 151297, 151536, 151860, 152178, 152524, 152780, 153144, 153613, 154037, 154521, 154992, 155483, 155874, 156099, 156391, 156624, 157044, 157440, 157800, 158262, 158572, 159059, 159509, 159890, 160184, 160505, 160819, 161016]
first last [123, 470, 710, 1075, 1391] [223470, 223904, 224183, 224559, 224852]
ch 1 n 614 win [150610, 150953, 151296, 151535, 151859, 152177, 152523, 152778, 153143, 153612, 154035, 154520, 154990, 155481, 155872, 156098, 156390, 156623, 157043, 157438, 157799, 158261, 158570, 159058, 159508, 159889, 160183, 160504, 160818, 161015]
first last [121, 468, 708, 1073, 1389] [223469, 223903, 224182, 224558, 224851]

fs 250 nwin 30 prev 150198
rw [150611, 150954, 151297, 151535, 151860, 152178, 152524, 152780, 153144, 153614, 154036, 154521, 154991, 155482, 155873, 156099, 156391, 156624, 157043, 157439, 157800, 158262, 158571, 159058, 159509, 159890, 160183, 160505, 160819, 161015]
rr_ms [1372.0, 1372.0, 952.0, 1300.0, 1272.0, 1384.0, 1024.0, 1456.0, 1880.0, 1688.0, 1940.0, 1880.0, 1964.0, 1564.0, 904.0, 1168.0, 932.0, 1676.0, 1584.0, 1444.0, 1848.0, 1236.0, 1948.0, 1804.0, 1524.0, 1172.0, 1288.0, 1256.0, 784.0]
q 150611 lead0 range -1.395 1.795 lead1 range -1.365 2.36
offs [-30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
ch0 [0.065, 0.03, 0.065, 1.2, -0.455, -0.125, -0.155, -0.18, -0.185, -0.225, -0.28, -0.365, -0.365, -0.295, -0.105, 0.02, 0.12, 0.14, 0.11]
ch1 [0.155, 0.13, 0.19, 1.57, -0.33, -0.085, -0.105, -0.15, -0.17, -0.21, -0.29, -0.36, -0.32, -0.24, -0.025, 0.11, 0.21, 0.19, 0.16]

offs [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260]
ch0 [-0.295, -0.105, 0.02, 0.12, 0.14, 0.11, 0.065, 0.065, 0.015, 0.01, 0.01, -0.005, 0.015, 0.02, 0.025, 0.0, 0.0]
ch1 [-0.24, -0.025, 0.11, 0.21, 0.19, 0.16, 0.105, 0.08, 0.035, 0.02, 0.025, 0.01, 0.03, 0.035, 0.06, 0.025, 0.03]

```

## A22. qt_sel232 u5 qt_ms = 406.5 (ref 422.91; correct)

FINAL: {"qt_ms": 406.5, "qtcb_ms": 469.4, "qtcf_ms": 447.1}

Last reply (end):
```
FINAL: {"qt_ms": 406.5, "qtcb_ms": 469.4, "qtcf_ms": 447.1}
```

Output seen (end):
```
  0.185  -0.150
155512   0.190  -0.160
155513   0.200  -0.145
155514   0.210  -0.130
155515   0.205  -0.125
155516   0.215  -0.130
155517   0.210  -0.140
155518   0.215  -0.135
155519   0.210  -0.135
155520   0.210  -0.115
155521   0.205  -0.115
155522   0.195  -0.100
155523   0.165  -0.085
155524   0.135  -0.070
155525   0.125  -0.070
155526   0.075  -0.015
155527   0.045   0.005
155528   0.020   0.030
155529  -0.005   0.050
155530  -0.015   0.055
155531  -0.015   0.050
155532  -0.035   0.045
155533  -0.055   0.040
155534  -0.065   0.045
155535  -0.080   0.035
155536  -0.075   0.050
155537  -0.065   0.055
155538  -0.065   0.055
155539  -0.065   0.045
155540  -0.080   0.035
155541  -0.100   0.020
155542  -0.110   0.025
155543  -0.105   0.035
155544  -0.090   0.045
155545  -0.090   0.070
155546  -0.100   0.070
155547  -0.100   0.050
155548  -0.095   0.035
155549  -0.110   0.030
155550  -0.115   0.030
155551  -0.125   0.040
155552  -0.130   0.060
155553  -0.110   0.070
155554  -0.085   0.075
155555  -0.080   0.070
155556  -0.080   0.065
155557  -0.090   0.065
155558  -0.100   0.060
155559  -0.110   0.050
155560  -0.125   0.035
155561  -0.125   0.045
155562  -0.115   0.045
155563  -0.115   0.030
155564  -0.110   0.005
155565  -0.120   0.010
155566  -0.130   0.015
155567  -0.125   0.010
155568  -0.115   0.005
155569  -0.080   0.005
155570  -0.090  -0.005
155571  -0.090   0.000
155572  -0.090  -0.005
155573  -0.075   0.010
155574  -0.060   0.010
155575  -0.055   0.015
155576  -0.080   0.010
155577  -0.090   0.025
155578  -0.085   0.050
155579  -0.075   0.045
155580  -0.075   0.025
155581  -0.080   0.000
155582  -0.085  -0.005
155583  -0.105  -0.015
155584  -0.110  -0.005
155585  -0.110   0.015
155586  -0.100   0.030
155587  -0.080   0.055
155588  -0.070   0.070
155589  -0.060   0.060
155590  -0.070   0.040
155591  -0.095   0.045
155592  -0.100   0.055
155593  -0.100   0.070
155594  -0.085   0.055
155595  -0.075   0.040
155596  -0.060   0.045
155597  -0.075   0.055
155598  -0.090   0.075
155599  -0.090   0.065
155600  -0.095   0.055
155601  -0.090   0.055
155602  -0.085   0.065
155603  -0.080   0.085
155604  -0.070   0.075
155605  -0.085   0.075
155606  -0.080   0.075
155607  -0.080   0.080
155608  -0.085   0.070
155609  -0.090   0.065
155610  -0.085   0.065
155611  -0.070   0.060
155612  -0.050   0.060
155613  -0.040   0.080
155614  -0.050   0.085
155615  -0.060   0.065
155616  -0.075   0.070
155617  -0.075   0.040
155618  -0.065   0.050
155619  -0.035   0.085

```

## A23. qt_sel891 u5 qtcf_ms = 407.2 (ref 462.09; wrong)

FINAL: {"qt_ms": 360.0, "qtcb_ms": 433.2, "qtcf_ms": 407.2}

Last reply (end):
```
FINAL: {"qt_ms": 360.0, "qtcb_ms": 433.2, "qtcf_ms": 407.2}
```

Output seen (end):
```
['sel891.dat', 'sel891.hea', '_agen.py']
<wfdb.io.record.Record object at 0x77e0410753d0>
250 224999 ['ECG1', 'ECG2'] ['mV', 'mV']
(224999, 2)
[[ 0.14   0.13 ]
 [ 0.055  0.03 ]
 [ 0.02   0.   ]
 [-0.005 -0.025]
 [-0.03  -0.05 ]]

(224999, 2) 250
0 224999 0    0
1    0
2    0
3    0
4    0
5    0
6    0
7    0
8    0
9    0
Name: ECG_R_Peaks, dtype: int64 224989    0
224990    0
224991    0
224992    0
224993    0
224994    0
224995    0
224996    0
224997    0
224998    0
Name: ECG_R_Peaks, dtype: int64
1 224999 0    0
1    0
2    0
3    0
4    0
5    0
6    0
7    0
8    0
9    0
Name: ECG_R_Peaks, dtype: int64 224989    0
224990    0
224991    0
224992    0
224993    0
224994    0
224995    0
224996    0
224997    0
224998    0
Name: ECG_R_Peaks, dtype: int64

0 []
last nonzero 224998
dtype int64 max 655

XYZ123

NOW1

[timeout after 120 s]
n 0
on []
to []

[stderr]
/usr/local/lib/python3.12/site-packages/neurokit2/ecg/ecg_delineate.py:169: NeuroKitWarning: No R-peaks were detected. Returning empty results for ECG delineation.
  warn(

224999 [0, 0, 0, 0, 0] [0, 0, 0, 0, 0]
0 0

1266 [257, 375, 604, 779, 951] [224297, 224465, 224635, 224768, 224973]
21

```

## A24. qt_sel873 u2 qtcb_ms = 384.0 (ref 401.08; correct)

FINAL: {"qt_ms": 400, "qtcb_ms": 384, "qtcf_ms": 389}

Last reply (end):
```
FINAL: {"qt_ms": 400, "qtcb_ms": 384, "qtcf_ms": 389}
```

Output seen (end):
```
.3.0
<class 'tuple'> 2
<class 'pandas.core.frame.DataFrame'>
Index(['ECG_P_Peaks', 'ECG_P_Onsets', 'ECG_P_Offsets', 'ECG_Q_Peaks',
       'ECG_R_Onsets', 'ECG_R_Offsets', 'ECG_S_Peaks', 'ECG_T_Peaks',
       'ECG_T_Onsets', 'ECG_T_Offsets'],
      dtype='object')
   ECG_P_Peaks  ECG_P_Onsets  ...  ECG_T_Onsets  ECG_T_Offsets
0            0             0  ...             0              0
1            0             0  ...             0              0
2            0             0  ...             0              0
3            0             0  ...             0              0
4            0             0  ...             0              0

[5 rows x 10 columns]

ch 0
     ECG_P_Peaks  ECG_P_Onsets  ...  ECG_T_Onsets  ECG_T_Offsets
498            0             0  ...             0              0
499            0             0  ...             0              0
500            0             0  ...             0              0
501            0             0  ...             0              0
502            1             0  ...             0              0
503            0             0  ...             0              0
504            0             0  ...             0              0
505            0             0  ...             0              0
506            0             0  ...             0              0
507            0             0  ...             0              0
508            0             0  ...             0              0
509            0             0  ...             0              0

[12 rows x 10 columns]
ch 1
     ECG_P_Peaks  ECG_P_Onsets  ...  ECG_T_Onsets  ECG_T_Offsets
498            0             0  ...             0              0
499            0             0  ...             0              0
500            0             0  ...             0              0
501            0             0  ...             0              0
502            0             0  ...             0              0
503            0             0  ...             0              0
504            0             0  ...             0              0
505            0             0  ...             0              0
506            1             0  ...             0              0
507            0             0  ...             0              0
508            0             0  ...             0              0
509            0             0  ...             0              0

[12 rows x 10 columns]

a type <class 'pandas.core.frame.DataFrame'> (224999, 10)
b type <class 'dict'> None

```

## A25. qt_sel306 u2 qt_ms = 380.0 (ref 381.33; correct)

FINAL: {"qt_ms": 380.0, "qtcb_ms": 410.9, "qtcf_ms": 400.1}

Last reply (end):
```
FINAL: {"qt_ms": 380.0, "qtcb_ms": 410.9, "qtcf_ms": 400.1}
```

Output seen (end):
```
51195:-0.06 151196:-0.07
151197 151197:-0.05 151198:-0.04 151199:-0.05 151200:-0.06 151201:-0.09
151202 151202:-0.07 151203:-0.06 151204:-0.05 151205:-0.07 151206:-0.07
151207 151207:-0.06 151208:-0.07 151209:-0.07 151210:-0.07 151211:-0.06
151212 151212:-0.06 151213:-0.07 151214:-0.07 151215:-0.07 151216:-0.07
151217 151217:-0.07 151218:-0.09 151219:-0.07 151220:-0.07 151221:-0.07
151222 151222:-0.07 151223:-0.07 151224:-0.07 151225:-0.07 151226:-0.09
151227 151227:-0.07 151228:-0.07 151229:-0.07 151230:-0.07 151231:-0.07
151232 151232:-0.07 151233:-0.08 151234:-0.09 151235:-0.07 151236:-0.07
151237 151237:-0.07 151238:-0.08 151239:-0.08 151240:-0.07 151241:-0.07
151242 151242:-0.06 151243:-0.04 151244:-0.02 151245:-0.01 151246:-0.03
151247 151247:-0.03 151248:-0.03 151249:-0.04 151250:-0.04 151251:-0.08
151252 151252:-0.09 151253:-0.09
151257 

rr samples 199 sec 0.796

ch 0
150287: 2.030  
150291: 1.070  150295:-0.200  150299:-0.190  150303:-0.215  150307:-0.215  150311:-0.210  150315:-0.215  150319:-0.215  150323:-0.225  150327:-0.215  
150331:-0.250  150335:-0.285  150339:-0.350  150343:-0.425  150347:-0.500  150351:-0.530  150355:-0.475  150359:-0.345  150363:-0.210  150367:-0.145  
150371:-0.125  150375:-0.105  150379:-0.115  150383:-0.125  150387:-0.090  150391:-0.110  150395:-0.115  150399:-0.110  150403:-0.105  150407:-0.095  
150411:-0.080  150415:-0.080  150419:-0.075  150423:-0.080  150427:-0.075  150431:-0.060  150435:-0.015  150439:-0.005  150443: 0.010  150447: 0.005  
150451: 0.005  150455:-0.070  150459:-0.140  150463:-0.150  150467:-0.145  150471:-0.145  150475:-0.140  150479: 0.295  150483: 1.070  150487: 1.685  
150491: 0.625  150495:-0.160  

ch 1
150287:-1.835  
150291:-1.990  150295:-0.420  150299: 0.000  150303: 0.035  150307: 0.055  150311: 0.085  150315: 0.075  150319: 0.095  150323: 0.115  150327: 0.130  
150331: 0.165  150335: 0.220  150339: 0.295  150343: 0.375  150347: 0.445  150351: 0.425  150355: 0.275  150359: 0.110  150363: 0.000  150367:-0.030  
150371:-0.065  150375:-0.065  150379:-0.050  150383:-0.070  150387:-0.050  150391:-0.060  150395:-0.040  150399:-0.050  150403:-0.040  150407:-0.040  
150411:-0.055  150415:-0.065  150419:-0.070  150423:-0.060  150427:-0.075  150431:-0.050  150435:-0.030  150439:-0.060  150443:-0.100  150447:-0.145  
150451:-0.145  150455:-0.100  150459:-0.100  150463:-0.090  150467:-0.090  150471:-0.090  150475: 0.000  150479:-0.085  150483:-0.735  150487:-2.070  
150491:-1.710  150495:-0.260  

```

## A26. qt_sel873 u2 qt_ms = 400.0 (ref 417.04; correct)

FINAL: {"qt_ms": 400, "qtcb_ms": 384, "qtcf_ms": 389}

Last reply (end):
```
FINAL: {"qt_ms": 400, "qtcb_ms": 384, "qtcf_ms": 389}
```

Output seen (end):
```
.3.0
<class 'tuple'> 2
<class 'pandas.core.frame.DataFrame'>
Index(['ECG_P_Peaks', 'ECG_P_Onsets', 'ECG_P_Offsets', 'ECG_Q_Peaks',
       'ECG_R_Onsets', 'ECG_R_Offsets', 'ECG_S_Peaks', 'ECG_T_Peaks',
       'ECG_T_Onsets', 'ECG_T_Offsets'],
      dtype='object')
   ECG_P_Peaks  ECG_P_Onsets  ...  ECG_T_Onsets  ECG_T_Offsets
0            0             0  ...             0              0
1            0             0  ...             0              0
2            0             0  ...             0              0
3            0             0  ...             0              0
4            0             0  ...             0              0

[5 rows x 10 columns]

ch 0
     ECG_P_Peaks  ECG_P_Onsets  ...  ECG_T_Onsets  ECG_T_Offsets
498            0             0  ...             0              0
499            0             0  ...             0              0
500            0             0  ...             0              0
501            0             0  ...             0              0
502            1             0  ...             0              0
503            0             0  ...             0              0
504            0             0  ...             0              0
505            0             0  ...             0              0
506            0             0  ...             0              0
507            0             0  ...             0              0
508            0             0  ...             0              0
509            0             0  ...             0              0

[12 rows x 10 columns]
ch 1
     ECG_P_Peaks  ECG_P_Onsets  ...  ECG_T_Onsets  ECG_T_Offsets
498            0             0  ...             0              0
499            0             0  ...             0              0
500            0             0  ...             0              0
501            0             0  ...             0              0
502            0             0  ...             0              0
503            0             0  ...             0              0
504            0             0  ...             0              0
505            0             0  ...             0              0
506            1             0  ...             0              0
507            0             0  ...             0              0
508            0             0  ...             0              0
509            0             0  ...             0              0

[12 rows x 10 columns]

a type <class 'pandas.core.frame.DataFrame'> (224999, 10)
b type <class 'dict'> None

```

## A27. qt_sel38 u4 qt_ms = 490.0 (ref 362.0; wrong)

FINAL: {"qt_ms": 490, "qtcb_ms": 642, "qtcf_ms": 586}

Last reply (end):
```
FINAL: {"qt_ms": 490, "qtcb_ms": 642, "qtcf_ms": 586}
```

Output seen (end):
```
0.4  -0.48 -0.55 -0.6  -0.64 -0.66 -0.67 -0.68 -0.68 -0.69 -0.68
 -0.68 -0.65 -0.61 -0.56 -0.5  -0.44 -0.36 -0.28 -0.22 -0.16 -0.1  -0.06 -0.02  0.    0.02  0.04  0.06  0.07  0.08  0.1   0.1   0.12  0.12  0.14  0.14  0.16  0.16  0.17  0.18  0.19  0.2   0.2   0.22
  0.22  0.24  0.25  0.26  0.28  0.28  0.3   0.32  0.34  0.34  0.36  0.37  0.38  0.39  0.39  0.4   0.4   0.4   0.4   0.39  0.38  0.37  0.37  0.36  0.36  0.35  0.34  0.34  0.33  0.32  0.32  0.32  0.31
  0.31  0.3   0.3   0.29  0.28  0.28  0.26  0.26  0.26  0.26  0.24  0.24  0.26  0.24  0.24  0.23  0.23  0.22  0.22  0.2   0.19  0.18  0.16  0.14  0.12  0.1   0.1   0.08  0.08  0.08  0.07  0.06  0.06
  0.06  0.06  0.06]
--- 155400
[ 0.13  0.14  0.15  0.16  0.18  0.19  0.2   0.22  0.24  0.25  0.27  0.28  0.3   0.3   0.3   0.31  0.31  0.32  0.31  0.31  0.3   0.3   0.29  0.28  0.28  0.27  0.27  0.26  0.26  0.24  0.24  0.24  0.24
  0.24  0.22  0.22  0.2   0.2   0.2   0.18  0.18  0.18  0.18  0.18  0.18  0.18  0.16  0.16  0.14  0.14  0.12  0.1   0.08  0.06  0.04  0.02  0.01  0.    0.   -0.   -0.01 -0.02 -0.02 -0.02 -0.03 -0.04
 -0.04 -0.04 -0.04 -0.05 -0.05 -0.06 -0.06 -0.06 -0.07 -0.07 -0.08 -0.08 -0.08 -0.07 -0.07 -0.06 -0.06 -0.04 -0.02  0.    0.04  0.08  0.12  0.12  0.12  0.1   0.08  0.   -0.1  -0.24 -0.36 -0.46 -0.55
 -0.63 -0.69 -0.74 -0.77 -0.8  -0.79 -0.8  -0.8  -0.8  -0.81 -0.78 -0.76 -0.72 -0.68 -0.62 -0.56 -0.49 -0.42 -0.37 -0.32 -0.28 -0.24 -0.2  -0.18 -0.16 -0.14 -0.12 -0.12 -0.12 -0.1  -0.08 -0.08 -0.06
 -0.06 -0.05 -0.04 -0.03 -0.02 -0.01  0.    0.    0.01  0.02  0.02  0.04  0.04  0.06  0.07  0.08  0.09  0.1   0.11  0.13  0.14  0.16  0.16  0.18  0.18  0.19  0.2   0.2   0.22  0.22  0.22  0.22  0.2
  0.2   0.18  0.18  0.18  0.17  0.16  0.16  0.16  0.14  0.14  0.13  0.13  0.12  0.12  0.12  0.11  0.1   0.09  0.08  0.08  0.08  0.07  0.07  0.06  0.06  0.06  0.06  0.04  0.04  0.04  0.02  0.   -0.
 -0.03 -0.05 -0.08 -0.09 -0.1  -0.1  -0.11 -0.11 -0.12 -0.12 -0.12 -0.12 -0.14 -0.14 -0.14 -0.14 -0.16 -0.16 -0.16 -0.16 -0.16 -0.18 -0.16 -0.18 -0.18 -0.18 -0.18 -0.17 -0.16 -0.16 -0.16 -0.14 -0.12
 -0.1  -0.06 -0.01  0.01  0.02  0.02  0.   -0.03 -0.1  -0.22 -0.36 -0.48 -0.58 -0.68 -0.74 -0.8  -0.85 -0.87 -0.88 -0.88 -0.9  -0.9  -0.9  -0.88 -0.85 -0.82 -0.77 -0.72 -0.65 -0.58 -0.51 -0.44 -0.4
 -0.36 -0.32 -0.28 -0.26 -0.24 -0.22 -0.2  -0.18 -0.17 -0.16 -0.16 -0.14 -0.14 -0.12 -0.12 -0.1  -0.1  -0.1  -0.09 -0.08 -0.07 -0.06 -0.05 -0.04 -0.02 -0.01  0.    0.    0.02  0.03  0.04  0.06  0.07
  0.08  0.1   0.1 ]

```

## A28. qt_sel16265 u2 qt_ms = 385.0 (ref 406.0; wrong)

FINAL: {"qt_ms": 385, "qtcb_ms": 450, "qtcf_ms": 427}

Last reply (end):
```
FINAL: {"qt_ms": 385, "qtcb_ms": 450, "qtcf_ms": 427}
```

Output seen (end):
```
12 -0.112 -0.112 -0.111 -0.106 -0.098 -0.087 -0.077 -0.07  -0.066 -0.06  -0.044 -0.023 -0.004]
-40 [ 0.011  0.018  0.014 -0.002 -0.022 -0.039 -0.053 -0.062 -0.065 -0.066 -0.072 -0.081 -0.088 -0.094 -0.1   -0.109 -0.117 -0.125 -0.132 -0.135]
-20 [-0.135 -0.134 -0.131 -0.129 -0.127 -0.119 -0.107 -0.103 -0.12  -0.225 -0.434 -0.733 -0.932 -0.876 -0.575  0.108  1.003  1.926  2.589  2.909]
0 [ 3.044  2.939  2.706  2.227  1.473  0.574  0.031 -0.251 -0.285 -0.239 -0.21  -0.207 -0.229 -0.253 -0.271 -0.284 -0.29  -0.292 -0.29  -0.286]
20 [-0.282 -0.277 -0.272 -0.269 -0.265 -0.261 -0.255 -0.248 -0.239 -0.233 -0.226 -0.221 -0.215 -0.209 -0.202 -0.195 -0.19  -0.184 -0.178 -0.172]
40 [-0.166 -0.16  -0.152 -0.143 -0.134 -0.125 -0.118 -0.109 -0.1   -0.091 -0.081 -0.07  -0.06  -0.049 -0.038 -0.026 -0.014 -0.002  0.007  0.017]
60 [ 0.027  0.036  0.043  0.052  0.059  0.065  0.072  0.077  0.081  0.083  0.082  0.075  0.066  0.055  0.042  0.027  0.012 -0.004 -0.021 -0.035]
80 [-0.049 -0.059 -0.069 -0.079 -0.087 -0.093 -0.097 -0.101 -0.104 -0.106 -0.107 -0.107 -0.107 -0.109 -0.109 -0.108 -0.109 -0.111 -0.111 -0.112]
100 [-0.113 -0.115 -0.117 -0.118 -0.119 -0.12  -0.12  -0.121 -0.121 -0.122 -0.122 -0.122 -0.123 -0.122 -0.122 -0.122 -0.122 -0.122 -0.122 -0.124]
=== avg chan 1
-60 [0.057 0.058 0.057 0.056 0.055 0.054 0.053 0.053 0.053 0.054 0.056 0.057 0.06  0.064 0.071 0.077 0.081 0.083 0.081 0.074]
-40 [0.059 0.045 0.038 0.037 0.037 0.034 0.029 0.028 0.028 0.031 0.037 0.044 0.049 0.049 0.044 0.04  0.039 0.038 0.037 0.039]
-20 [ 0.042  0.042  0.044  0.045  0.045  0.045  0.046  0.047  0.05   0.075  0.126  0.185  0.186  0.095 -0.031 -0.19  -0.298 -0.279 -0.122  0.082]
0 [ 0.274  0.431  0.541  0.514  0.258 -0.137 -0.396 -0.467 -0.348 -0.207 -0.09  -0.02   0.005  0.013  0.01   0.005  0.    -0.002 -0.003 -0.002]
20 [-0.001 -0.001 -0.003 -0.006 -0.008 -0.01  -0.013 -0.015 -0.018 -0.02  -0.023 -0.028 -0.032 -0.036 -0.04  -0.044 -0.048 -0.051 -0.057 -0.063]
40 [-0.071 -0.078 -0.084 -0.09  -0.097 -0.103 -0.11  -0.117 -0.123 -0.131 -0.139 -0.145 -0.153 -0.159 -0.166 -0.172 -0.177 -0.181 -0.186 -0.189]
60 [-0.19  -0.19  -0.189 -0.188 -0.185 -0.179 -0.171 -0.161 -0.148 -0.134 -0.12  -0.102 -0.084 -0.066 -0.051 -0.03  -0.013  0.002  0.013  0.022]
80 [0.03  0.038 0.045 0.05  0.053 0.056 0.059 0.061 0.062 0.063 0.065 0.066 0.067 0.067 0.066 0.066 0.065 0.064 0.066 0.067]
100 [0.067 0.067 0.067 0.066 0.065 0.064 0.063 0.063 0.064 0.064 0.064 0.063 0.063 0.063 0.063 0.063 0.063 0.062 0.061 0.059]

```

## A29. qt_sel308 u3 qt_ms = 393.6 (ref 406.75; correct)

FINAL: {"qt_ms": 393.6, "qtcb_ms": 472.7, "qtcf_ms": 467.6}

Last reply (end):
```
FINAL: {"qt_ms": 393.6, "qtcb_ms": 472.7, "qtcf_ms": 467.6}
```

Output seen (end):
```
['sel308.dat', 'sel308.hea', '_agen.py']
<wfdb.io.record.Record object at 0x7a629c740110>
250 225000 2 ['ECG1', 'ECG2']
(225000, 2)
[[-0.105 -0.02 ]
 [-0.19  -0.015]
 [-0.22  -0.025]
 [-0.23  -0.03 ]
 [-0.165 -0.03 ]]
['mV', 'mV']

(225000, 2) 0
0 [-1.605 -0.79 ] [1.14 1.06] [0.51341657 0.30775242]
20000 [-1.675 -0.815] [1.365 1.195] [0.54795727 0.31950956]
40000 [-1.725 -0.945] [1.375 1.395] [0.52584665 0.32973414]
60000 [-1.21 -0.89] [1.335 1.32 ] [0.37347213 0.33990793]
80000 [-1.925 -0.745] [1.41  1.315] [0.40107204 0.31246368]
100000 [-1.005 -0.74 ] [0.725 1.285] [0.30629608 0.31139216]
120000 [-0.96  -0.755] [0.725 1.28 ] [0.28288283 0.29544521]
140000 [-0.945 -0.795] [0.71  1.255] [0.26861441 0.28655384]
160000 [-0.905 -0.745] [0.7   1.195] [0.25924598 0.28023344]
180000 [-0.92 -0.72] [0.69 1.2 ] [0.25672313 0.27932341]
200000 [-0.895 -0.72 ] [0.735 1.17 ] [0.25134481 0.26735313]
220000 [-0.87  -0.695] [0.715 1.195] [0.25543295 0.27115164]

```

## A30. qt_sel42 u2 qt_ms = 495.0 (ref 447.87; wrong)

FINAL: {"qt_ms": 495, "qtcb_ms": 572, "qtcf_ms": 545}

Last reply (end):
```
FINAL: {"qt_ms": 495, "qtcb_ms": 572, "qtcf_ms": 545}
```

Output seen (end):
```
54546), np.int64(154366), np.float64(0.72), ('RO', None), ('RO', None), ('TO', None), ('TP', None), ('TO', None), ('RO', 154527), ('RO', 154562), ('TO', None), ('TP', np.int64(154610)), ('TO', np.int64(154634))]
[np.int64(864), np.int64(154726), np.int64(154546), np.float64(0.72), ('RO', None), ('RO', None), ('TO', None), ('TP', None), ('TO', None), ('RO', 154708), ('RO', 154742), ('TO', None), ('TP', np.int64(154792)), ('TO', np.int64(154816))]
[np.int64(865), np.int64(154907), np.int64(154726), np.float64(0.724), ('RO', None), ('RO', None), ('TO', None), ('TP', None), ('TO', None), ('RO', 154888), ('RO', 154923), ('TO', None), ('TP', np.int64(154972)), ('TO', np.int64(154996))]
[np.int64(866), np.int64(155088), np.int64(154907), np.float64(0.724), ('RO', None), ('RO', None), ('TO', None), ('TP', None), ('TO', None), ('RO', 155069), ('RO', 155104), ('TO', None), ('TP', np.int64(155154)), ('TO', np.int64(155178))]
[np.int64(867), np.int64(155271), np.int64(155088), np.float64(0.732), ('RO', None), ('RO', None), ('TO', None), ('TP', None), ('TO', None), ('RO', 155254), ('RO', 155287), ('TO', None), ('TP', np.int64(155337)), ('TO', np.int64(155361))]
[np.int64(868), np.int64(155455), np.int64(155271), np.float64(0.736), ('RO', None), ('RO', None), ('TO', None), ('TP', None), ('TO', None), ('RO', 155437), ('RO', 155471), ('TO', None), ('TP', np.int64(155520)), ('TO', np.int64(155544))]

1246 839 868 30
dwt lead 0 RO nan frac 0.6404494382022472 within window nan 0.9333333333333333 TO nan 1.0
  beat 842 150693 RO 150668.0 TO nan Tpeak nan
  beat 843 150864 RO nan TO nan Tpeak nan
  beat 844 151035 RO 151009.0 TO nan Tpeak nan
dwt lead 1 RO nan frac 0.0 within window nan 0.0 TO nan 0.0
  beat 842 150693 RO 150678.0 TO 150776.0 Tpeak 150757
  beat 843 150864 RO 150850.0 TO 150946.0 Tpeak 150927
  beat 844 151035 RO 151020.0 TO 151118.0 Tpeak 151099

[stderr]
Traceback (most recent call last):
  File "/work/_agen.py", line 13, in <module>
    ro=np.array(w['ECG_R_Onsets'],dtype=float)
                ~^^^^^^^^^^^^^^^^
KeyError: 'ECG_R_Onsets'

sel42 2 250 224993
sel42.dat 212 200 12 0 268 -28495 0 ECG1
sel42.dat 212 200 12 0 -38 -2300 0 ECG2
#Produced by xform from record 42, beginning at 18:10.000
#Produced by xform from record 42, beginning at 10:03:00.000
#------------------------------------------
#Produced by "/files2/scheherazade/plaguna/database/delay" from record sel42
#The signal 0 was delayed with a delay=7 samples

best lag -127 corr 0.4225332484291314

```
