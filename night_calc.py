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

warnings.filterwarnings("ignore")

__script_name__ = basename(sys.argv[0])
__script_desc__ = "Retrieve Night duration, astronomical LSTs from both twilights "
__script_desc__ += "(evening and morning) and Moon illumination at the T80-South site."

def parse_arguments():
    parser = ap.ArgumentParser(prog=__script_name__, description=__script_desc__)
    parser.add_argument('date', metavar='YYYY-MM-DD', type=str, help='Get night information for date YYYY-MM-DD.')
    parser.add_argument('--csv', action='store_true', default=False, help='Print info with CSV format.')
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

    T80S_TZ = ZoneInfo('America/Santiago')
    UTC_TZ = timezone.utc
    T80S_LAT = '-30.1678638889 degrees'
    T80S_LON = '-70.8056888889 degrees'
    T80S_HEI = 2187
    t80s_lat = Angle(T80S_LAT, 'deg')
    t80s_lon = Angle(T80S_LON, 'deg')
    t80s_hei = T80S_HEI*u.m
    t80s_EL = EarthLocation(lat=t80s_lat, lon=t80s_lon, height=t80s_hei)

    # DATETIME   
    t80s_dt = args.dt_obs.astimezone(T80S_TZ)
    t80s_midnight = t80s_dt - t80s_dt.utcoffset()
    t80s_Time = Time(t80s_midnight, location=t80s_EL)

    # OBSERVER
    t80s_obs = Observer(location=t80s_EL, timezone=T80S_TZ)
    t80s_Time_mn = t80s_obs.midnight(t80s_Time)
    moon_illum = t80s_obs.moon_illumination(t80s_Time_mn)
    twilight_morning = t80s_obs.twilight_morning_astronomical(t80s_Time_mn, which='nearest').datetime 
    twilight_evening = t80s_obs.twilight_evening_astronomical(t80s_Time_mn, which='nearest').datetime 
    night_duration = (twilight_morning - twilight_evening).total_seconds()/3600
    lst_even = t80s_obs.local_sidereal_time(twilight_evening)
    lst_morn = t80s_obs.local_sidereal_time(twilight_morning)

    # Final DIGEST
    if args.csv:
        print('#DT_EVEN_UTC,LST_EVEN,DT_MORN_UTC,LST_MORN,NIGHT_DUR,MOON_ILLUM')
        print('{},{},{},{},{},{}'.format(twilight_evening, lst_even.to_string(), twilight_morning, lst_morn.to_string(), night_duration, moon_illum))
    else:
        print(f'Evening twilight:')
        print(f'\tDATETIME (UTC):', twilight_evening)
        print(f'\tLST:', lst_even)
        print(f'Morning twilight:')
        print(f'\tDATETIME (UTC):', twilight_morning)
        print(f'\tLST:', lst_morn)
        print(f'Night duration: {night_duration:.2f} hours')
        print(f'Moon illumination: {moon_illum:.4f}')