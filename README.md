T80S Night Calculator
=====================

Retrieve T80-South site night duration, astronomical LSTs from both near twilights (evening and morning) and Moon illumination at the sun midnight.

Usage
-----

**night_calc.py** usage:

    usage: night_calc.py [-h] [--csv] [--local_midnight] YYYY-MM-DD

    Retrieve T80-South site night duration, astronomical LSTs from both near twilights (evening and morning) and Moon illumination at the sun midnight.

    positional arguments:
      YYYY-MM-DD            Get night information for date YYYY-MM-DD.

    options:
      -h, --help            show this help message and exit
      --csv, -c             Print info with CSV format.
      --local_midnight, -M  Uses local midnight instead the sun midnight for the moon illumination calculation.

**get_date_interval.sh** usage:

    usage: bash get_date_interval.sh INIDATE FINDATE

*INIDATE* and *FINDATE* must be at *YYYY-MM-DD* format. Last date will be *FINDATE* - 1 day.

Examples
--------

```bash
    $ python3 night_calc.py 2023-01-01
    Night duration: 6.75 hours
    Evening twilight:
        DATETIME (UTC): 2023-01-02 01:24:23.207661
        LST: 3h26m53.51370588s
    Morning twilight:
        DATETIME (UTC): 2023-01-02 08:09:41.051338
        LST: 10h13m17.93840088s
    Sun midnight:
        DATETIME (UTC): 2023-01-02 04:47:02.012401
        LST: 6h50m05.60860765s
        Moon illumination: 0.8032

    $ python3 night_calc.py 2023-01-01 --csv
    #NIGHT_DUR,DT_EVEN_UTC,LST_EVEN,DT_MORN_UTC,LST_MORN,DT_MIDN,LST_MIDN,MOON_ILLUM_MIDN
    6.754956576944445,2023-01-02 01:24:23.207661,3h26m53.51370588s,2023-01-02 08:09:41.051338,10h13m17.93840088s,2023-01-02 04:47:02.012401,6h50m05.60860765s,0.8032165343009382

    $ bash get_date_interval.sh 2023-01-01 2023-01-05
    #NIGHT_DUR,DT_EVEN_UTC,LST_EVEN,DT_MORN_UTC,LST_MORN,DT_MIDN,LST_MIDN,MOON_ILLUM_MIDN
    6.754956576944445,2023-01-02 01:24:23.207661,3h26m53.51370588s,2023-01-02 08:09:41.051338,10h13m17.93840088s,2023-01-02 04:47:02.012401,6h50m05.60860765s,0.8032165343009382
    6.768178928888889,2023-01-03 01:24:27.277443,3h30m54.15437295s,2023-01-03 08:10:32.721587,10h18m06.31061791s,2023-01-03 04:47:30.126149,6h54m30.35945389s,0.8750535541745281
    6.782489072500001,2023-01-04 01:24:29.045851,3h34m52.48983602s,2023-01-04 08:11:26.006512,10h22m56.30421445s,2023-01-04 04:47:57.856998,6h58m54.72873387s,0.9314920905532926
    6.797870289722222,2023-01-05 01:24:28.522739,3h38m48.52918417s,2023-01-05 08:12:20.855782,10h27m47.86783566s,2023-01-05 04:48:25.179159,7h03m18.68974587s,0.9712297317299345
```

Contact
-------
	
Contact us: [dhubax@gmail.com](mailto:dhubax@gmail.com).