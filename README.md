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

Contact
-------
	
Contact us: [dhubax@gmail.com](mailto:dhubax@gmail.com).