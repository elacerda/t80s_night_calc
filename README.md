T80S Night Calculator
=====================

Retrieve Night duration, astronomical LSTs from both twilights (evening and morning) and Moon illumination at the T80-South site.

Usage
-----

**night_calc.py** usage:

    usage: night_calc.py [-h] [--csv] YYYY-MM-DD

    Retrieve Night duration, astronomical LSTs from both twilights (evening and morning) and Moon illumination at the T80-South site.

    positional arguments:
        YYYY-MM-DD  Get night information for date YYYY-MM-DD.

    options:
        -h, --help  show this help message and exit
        --csv       Print CSV info.

**get_date_interval.sh** usage:

    bash get_date_interval.sh INIDATE FINDATE
    
    INIDATE and FINDATE must be at YYYY-MM-DD format. 
    
    Last date will be FINDATE - 1 day.

Examples
--------

    $ python3 night_calc.py 2023-01-01
    Evening twilight:
        DATETIME (UTC): 2023-01-02 01:24:22.700924
        LST: 3h26m53.00558825s
    Morning twilight:
        DATETIME (UTC): 2023-01-02 08:09:41.137598
        LST: 10h13m18.02489793s
    Night duration: 6.76 hours
    Moon illumination: 0.8032

    $ python3 night_calc.py 2023-01-01 --csv
    #DT_EVEN_UTC,LST_EVEN,DT_MORN_UTC,LST_MORN,NIGHT_DUR,MOON_ILLUM
    2023-01-02 01:24:22.700924,3h26m53.00558825s,2023-01-02 08:09:41.137598,10h13m18.02489793s,6.755121298333333,0.8032165343009382

    $ bash get_date_interval.sh 2023-01-01 2023-01-05
    #DT_EVEN_UTC,LST_EVEN,DT_MORN_UTC,LST_MORN,NIGHT_DUR,MOON_ILLUM
    2023-01-02 01:24:22.700924,3h26m53.00558825s,2023-01-02 08:09:41.137598,10h13m18.02489793s,6.755121298333333,0.8032165343009382
    2023-01-03 01:24:26.585152,3h30m53.46017355s,2023-01-03 08:10:33.493137,10h18m07.08427088s,6.768585551388889,0.8750535542046118
    2023-01-04 01:24:28.638892,3h34m52.08175925s,2023-01-04 08:11:26.905119,10h22m57.20527928s,6.782851729722222,0.9314920905532926
    2023-01-05 01:24:28.411776,3h38m48.41791728s,2023-01-05 08:12:21.776034,10h27m48.79061102s,6.798156738333334,0.9712297317299345

Contact
-------
	
Contact us: [dhubax@gmail.com](mailto:dhubax@gmail.com).