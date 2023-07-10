d=$1
DF=$2
echo "#DT_EVEN_UTC,LST_EVEN,DT_MORN_UTC,LST_MORN,NIGHT_DUR,MOON_ILLUM"
while [ "$d" != "$DF" ]
do
    python3 night_calc.py $d --csv | grep -v '^#'
    d=$(TZ=UTC date "+%Y-%m-%d" -d "$d + 1 day")
done
