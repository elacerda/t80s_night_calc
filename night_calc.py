import sys
import warnings
import argparse as ap
import astropy.units as u
from os.path import basename
from zoneinfo import ZoneInfo
from astropy.time import Time
from astroplan import Observer
from datetime import datetime, timezone
from astropy.coordinates import EarthLocation, Angle

warnings.filterwarnings('ignore')

__script_name__ = basename(sys.argv[0])
__script_desc__ = """
    Retrieve T80-South site night duration, astronomical LSTs from both near twilights 
    (evening and morning) and Moon illumination at the sun midnight.
"""

def parse_arguments():
    parser = ap.ArgumentParser(prog=__script_name__, description=__script_desc__)
    parser.add_argument('date', metavar='YYYY-MM-DD', type=str, help='Get night information for date YYYY-MM-DD.')
    parser.add_argument('--csv', '-c', action='store_true', default=False, help='Print info with CSV format.')
    parser.add_argument('--local_midnight', '-M', action='store_true', default=False, 
                        help='Uses local midnight instead the sun midnight for the moon illumination calculation.')
    args = parser.parse_args(args=sys.argv[1:])

    # Parse arguments
    if args.date is not None:
        if len(args.date) != 10:
            parser.print_help()
            sys.exit(1)
        if '-' not in args.date:
            parser.print_help()
            sys.exit(1)
        args.date += ' 23:59:59.000+00:00'
        try:
            args.dt_obs = datetime.fromisoformat(args.date)
        except ValueError as e:
            print(f'{__script_name__}: {e}\n')
            parser.print_help()
            sys.exit()

    return args

if __name__ == '__main__':
    args = parse_arguments()

    # T80-South location information
    T80S_TZ = ZoneInfo('America/Santiago')
    UTC_TZ = timezone.utc
    T80S_LAT = '-30d10m04.31s'
    T80S_LON = '-70d48m20.48s'
    T80S_HEI = 2178
    t80s_lat = Angle(T80S_LAT, 'deg')
    t80s_lon = Angle(T80S_LON, 'deg')
    t80s_hei = T80S_HEI*u.m
    t80s_EL = EarthLocation(lat=t80s_lat, lon=t80s_lon, height=t80s_hei)

    # Date and time configuration   
    t80s_dt = args.dt_obs.astimezone(T80S_TZ)
    t80s_Time = Time(t80s_dt - t80s_dt.utcoffset(), location=t80s_EL)

    # Observer at T80-South location
    t80s_obs = Observer(location=t80s_EL, timezone=T80S_TZ)
    
    # Nearest evening and morning twilights timestamp and LST 
    twilight_evening = t80s_obs.twilight_evening_astronomical(t80s_Time, which='nearest')
    twilight_morning = t80s_obs.twilight_morning_astronomical(t80s_Time, which='nearest')
    lst_even = t80s_obs.local_sidereal_time(twilight_evening)
    lst_morn = t80s_obs.local_sidereal_time(twilight_morning)
    
    # Night duration (time between twilights)
    night_duration = (twilight_morning.datetime - twilight_evening.datetime).total_seconds()/3600

    # Moon at midnight
    if args.local_midnight:
        Time_mn = t80s_Time
    else:
        Time_mn = t80s_obs.midnight(t80s_Time)
    moon_illum = t80s_obs.moon_illumination(Time_mn)
    lst_mn = t80s_obs.local_sidereal_time(Time_mn)    

    # Make relatory
    if args.csv:
        print('#NIGHT_DUR,DT_EVEN_UTC,LST_EVEN,DT_MORN_UTC,LST_MORN,DT_MIDN,LST_MIDN,MOON_ILLUM_MIDN')
        print('{},{},{},{},{},{},{},{}'.format(
                night_duration,
                twilight_evening.datetime, 
                lst_even.to_string(), 
                twilight_morning.datetime, 
                lst_morn.to_string(), 
                Time_mn.datetime,
                lst_mn.to_string(),
                moon_illum,
            )
        )
    else:
        print(f'Night duration: {night_duration:.2f} hours')
        print(f'Evening twilight:')
        print(f'\tDATETIME (UTC):', twilight_evening.datetime)
        print(f'\tLST:', lst_even)
        print(f'Morning twilight:')
        print(f'\tDATETIME (UTC):', twilight_morning.datetime)
        print(f'\tLST:', lst_morn)
        if args.local_midnight:
            print('Using local midnight:')
        else:
            print(f'Sun midnight:')
            print(f'\tDATETIME (UTC):', Time_mn.datetime)
            print(f'\tLST:', lst_mn)
        print(f'\tMoon illumination: {moon_illum:.4f}')
