import sys
import pytz
import warnings
import argparse as ap
import astropy.units as u
from os.path import basename
from datetime import datetime
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
        args.isoformatdt = args.date + ' 23:59:59'
        try:
            args.dt_obs = datetime.fromisoformat(args.isoformatdt)
        except ValueError as e:
            print(f'{__script_name__}: {e}\n')
            parser.print_help()
            sys.exit()

    return args

def create_T80S_Observer():
    from astroplan import Observer
    
    # T80-South location information
    return Observer(
        location=EarthLocation(
            lat=Angle('-30d10m04.31s', 'deg'), 
            lon=Angle('-70d48m20.48s', 'deg'), 
            height=2178*u.m,
        ), 
        timezone=pytz.timezone('America/Santiago'), 
        name='T80-South',
    )

if __name__ == '__main__':
    args = parse_arguments()

    t80s_obs = create_T80S_Observer()
    local_Time = t80s_obs.datetime_to_astropy_time(args.dt_obs)

    # Nearest evening and morning twilights timestamp and LST 
    twilight_evening = t80s_obs.twilight_evening_astronomical(local_Time, which='nearest')
    twilight_morning = t80s_obs.twilight_morning_astronomical(local_Time, which='nearest')
    lst_even = t80s_obs.local_sidereal_time(twilight_evening)
    lst_morn = t80s_obs.local_sidereal_time(twilight_morning)
    
    # Night duration (time between twilights)
    night_duration = (twilight_morning - twilight_evening).to_value('hr')

    # Moon at midnight
    if args.local_midnight:
        local_Time_mn = local_Time
    else:
        local_Time_mn = t80s_obs.midnight(local_Time)
    moon_illum = t80s_obs.moon_illumination(local_Time_mn)
    lst_mn = t80s_obs.local_sidereal_time(local_Time_mn)    

    # Make relatory
    if args.csv:
        print('#NIGHT_DUR,DT_EVEN_UTC,LST_EVEN,DT_MORN_UTC,LST_MORN,DT_MIDN,LST_MIDN,MOON_ILLUM_MIDN')
        print('{},{},{},{},{},{},{},{}'.format(
                night_duration,
                twilight_evening.datetime, 
                lst_even.to_string(), 
                twilight_morning.datetime, 
                lst_morn.to_string(), 
                local_Time_mn.datetime,
                lst_mn.to_string(),
                moon_illum,
            )
        )
    else:
        print(f'Night duration: {night_duration:.2f} hours')
        print(f'Evening twilight:')
        print(f'\tDATETIME (UTC):', twilight_evening.datetime)
        print(f'\tDATETIME (LOCAL):', t80s_obs.astropy_time_to_datetime(twilight_evening))
        print(f'\tLST:', lst_even)
        print(f'Morning twilight:')
        print(f'\tDATETIME (UTC):', twilight_morning.datetime)
        print(f'\tDATETIME (LOCAL):', t80s_obs.astropy_time_to_datetime(twilight_morning))
        print(f'\tLST:', lst_morn)
        if args.local_midnight:
            print('Using local midnight:')
        else:
            print(f'Sun midnight:')
            print(f'\tDATETIME (UTC):', local_Time_mn.datetime)
            print(f'\tDATETIME (LOCAL):', t80s_obs.astropy_time_to_datetime(local_Time_mn))
            print(f'\tLST:', lst_mn)
        print(f'\tMoon illumination: {moon_illum:.4f}')
