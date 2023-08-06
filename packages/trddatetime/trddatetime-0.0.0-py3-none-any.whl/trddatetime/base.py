# -*- coding: utf-8 -*-
import inspect
from datetime import datetime, date, time, tzinfo, timedelta, timezone
import os
import math
import re

import pandas as pd
from idebug import *
from ipylib.idatetime import *



from trddatetime.data import get_KrxHolidayPath


class TrdDatetime:
    def __init__(self, tz):
        self.clsloc = f"{__name__}.{__class__.__name__}"
        # ------------------------------------------------------------
        self._set_tz(tz)
        self.HOLIDAYS = self.get_holidays()
        # ------------------------------------------------------------
    def _set_tz(self, tz):
        print(f"tz가 문자열, 숫자이냐에 따라 자동으로 셋업해라.")
        if isinstance(tz, str):
            if tz.isnumeric():
                self.tz=timezone(timedelta(hours=int(tz)))
            else:
                raise
        elif isinstance(tz, int):
            self.tz=timezone(timedelta(hours=tz))
        else:
            raise
        return self

    # ------------------------------------------------------------ Util-Functions.
    def parse(self, dt):
        """
        krx 전용 parser. --> 보다 범용적인 함수는 idatetime.py 에서 다룰 것.
        반환값은 datetime.datetime 객체.
        초 단위까지만 제공한다.
        [ WorkList ]
        [1] Parse dt.
        [2] Convert as Korea TimeZone.
        """
        p_tz = re.compile('(\+\d+:\d+)')

        def _normalize_timezonestr_(s):
            m = p_tz.search(s)
            if m is None:
                pass
            else:
                tz = m.group(1).replace(":", "")
                s = p_tz.sub(repl=tz, string=s)
            return s
        def _build_fmts_():
            fmt_sectz = ['%Y-%m-%dT%H:%M:%S%z']
            fmt_sectz.append(fmt_sectz[0].replace("T", " "))

            fmt_sec = ['%Y-%m-%dT%H:%M:%S']
            fmt_sec.append(fmt_sec[0].replace("T", " "))

            fmt_day = ['%Y-%m-%d']
            fmt_month = ['%Y-%m']
            for symbol in ["", "/"]:
                fmt_day.append(fmt_day[0].replace("-", symbol))
                fmt_month.append(fmt_month[0].replace("-", symbol))
            fmt_year = ['%Y']
            return fmt_sectz + fmt_sec + fmt_day + fmt_month + fmt_year

        if isinstance(dt, str):
            dt = _normalize_timezonestr_(dt)
            fmts = _build_fmts_()
            for fmt in fmts:
                try:
                    _dt = datetime.strptime(dt, fmt)
                except Exception as e:
                    pass
                else:
                    return _dt.astimezone(self.tz)
        elif isinstance(dt, datetime):
            return dt.astimezone(self.tz)
        else:
            raise

    # ------------------------------------------------------------ HolidayHandler.
    # def _set_HolidayHandler(self):
    #     self.HolidayHandler = HolidayHandler()
    def omit_holidays(self, dts):
        """dts의 dt 는 datetime or pd.Timestamp
        """
        s = pd.Series(dts)
        if s.dt.tz is None:
            s = s.dt.tz_localize(tz=self.TZ_STRING)
        else:
            s = s.dt.tz_convert(tz=self.TZ_STRING)

        dts = s[~s.isin(self.HOLIDAYS)].dt.to_pydatetime()
        return list(dts)
    def to_last(self, dt):
        """마지막 거래일/일시로 조정."""
        td = timedelta(days=-1)
        while (dt.weekday() in [5,6] or dt in self.HOLIDAYS):
            dt += td
        return dt
    def now(self):
        dt = datetime.now()
        dt = dt.replace(microsecond=0)
        return dt.astimezone(self.tz)
    def today(self):
        """python datetime.py 와 달리 date 부분만 다룬다."""
        dt = datetime.today()
        dt = datetime(dt.year, dt.month, dt.day)
        return dt.astimezone(self.tz)
    def get_holidays(self, fpath=get_KrxHolidayPath()):
        funcloc = f"{__name__}.{inspect.stack()[0][3]}"
        try:
            df = pd.read_csv(fpath)
        except Exception as e:
            print(f"{'#'*50} {funcloc} | e: {e}")
            raise
        else:
            if re.search('csv$', fpath) is None:
                print(f"{'#'*50} {funcloc} | CSV파일이 아니다.")
                raise
            else:
                df.dt = df.dt.apply(self.parse)
                return sorted(df.dt)

    # ------------------------------------------------------------ Specific-TrdDatetime.
    def lastdate(self):
        """당일에 시장이 열렀다면, 당일이 마지막거래일."""
        return to_last(today())
    def lastdt(self):
        return lastdate().replace(hour=15, minute=30)
    def _shifting_by_delta_(self, dt, **delta):
        def _shift_days_(dt, v):
            def _get_periods_(v):
                def _get_bufferDays_(days):
                    avg_holidays = 10
                    f, i = math.modf(days/365)
                    return avg_holidays * (i+1)

                v = abs(v)
                return v + _get_bufferDays_(v)
            """bdatetime pool 준비."""
            if v > 0:
                dti = pd.bdate_range(start=dt, periods=_get_periods_(v))
            else:
                dti = pd.bdate_range(end=dt, periods=_get_periods_(v))
            """주말을 제외한 추가 공휴일을 pool에서 제거."""
            # pp.pprint(dti)
            dts = omit_holidays(dti)
            # pp.pprint(dts)
            """delta에 해당하는 타겟일 찾기."""
            if v < 0:
                d = dts[-(abs(v)+1)]
            elif v == 0:
                d = dts[-1]
            else:
                d = dts[v]

            # print(f"shifted date: {d}")
            return dt.replace(year=d.year, month=d.month, day=d.day)

        def _shift_times_(dt, k, v):
            # print(dt)
            dt = dt + timedelta(**{k:v})
            # print(f"shifted dt: {dt}")
            return dt

        for k, v in delta.items():
            if k == 'days':
                dt = _shift_days_(dt, v)
            elif k in ['hours','minutes','seconds']:
                dt = _shift_times_(dt, k, v)
            else:
                raise

        return dt
    def trddate(self, dt=None, **delta):
        """특정 거래일."""
        if dt is None:
            dt = lastdate()
        else:
            dt = to_last(parse(dt))
        # print(f"기준일: {dt}")

        return _shifting_by_delta_(dt, **delta)
    def trddt(self, dt=None, **delta):
        """특정 거래일시.
        dt: 기준 거래일. None일 경우, 마지막 거래일.
        """
        if dt is None:
            dt = lastdt()
        else:
            dt = to_last(parse(dt))
        # print(f"기준일시: {dt}")

        return _shifting_by_delta_(dt, **delta)
    def thisyear(self):
        return now().year
    def diff_bdays(self, dt1, dt2=None):
        """
        dt1(start)부터 dt2(end)까지 KRX-Market Open Days를 반환.
        """
        dt1 = parse(dt1)
        if dt2 is None: dt2 = today()
        else: dt2 = parse(dt2)
        print(f"{__name__}.{inspect.stack()[0][3]} | start: {dt1} | end: {dt2}")
        days = pd.bdate_range(start=dt1, end=dt2)
        # pp.pprint(days)
        return omit_holidays(days)

    # ------------------------------------------------------------ Market Timing.
    def mkt_buyable_opening(self):
        """정규장 매매가능 시작."""
        return today().replace(hour=8, minute=20)
    def preMkt_opening(self):
        """장전 동시호가 시작."""
        return today().replace(hour=8, minute=30)
    def mkt_opening(self):
        """장 시작."""
        return today().replace(hour=9)
    def mkt_closing_callprc(self):
        """장 마감 동시호가."""
        return today().replace(hour=15, minute=20)
    def mkt_closing(self):
        """장 종료."""
        return today().replace(hour=15, minute=30)
    def todayClosePrc_mkt(self):
        """장후 당일종가 거래."""
        return today().replace(hour=15, minute=40)
    def postMkt_opening(self):
        """시간외 단일가 시작."""
        return today().replace(hour=16)
    def postMkt_closing(self):
        """시간외 단일가 종료."""
        return today().replace(hour=18)
    """왜 필요한지 모르겠다."""
    def is_mkt_open(self):
        funcnm = f"{__name__}.{inspect.stack()[0][3]}"
        t = now()
        if t.weekday() in [5,6]:
            print(f"{t} | {funcnm} | 주말({t.weekday()})에는 시장을 닫는다.")
            return False
        else:
            if (t >= mkt_buyable_opening()) and (t < mkt_opening()):
                print(f"""{t} | {funcnm}
                    정규장 매수/매도 주문가능시간: 08:20 ~
                    장 시작 동시호가:           08:30 ~ 09:00
                    장전 시간외 종가 거래:       08:30 ~ 08:40 (전일 종가로 거래)
                """)
            elif (t >= mkt_opening()) and (t < mkt_closing()):
                print(f"""{t} | {funcnm}
                    한국거래소 정규시간. | 09:00 ~ 15:30
                """)
                return False
            elif (t.hour >= 9) and (t.hour < 16):
                print(f"""{t} | {funcnm}

                    KR_NOW : {t}
                """)
                if (t.hour >= 15) and (t.hour < 16):
                    if (t.minute >= 0) and (t.minute <= 30):
                        print(f"""{t} | {funcnm}
                            장 마감 동시호가.   | 15:20 ~ 15:30
                        """)
                    else:
                        print(f"""{t} | {funcnm}
                            장후 시간외 종가. | 15:40 ~ 16:00 (당일 종가로 거래)
                        """)
                return True
            elif (t.hour >= 16) and (t.hour < 18):
                print(f"""{t} | {funcnm}
                    시간외 단일가. | 16:00 ~ 18:00 (10분단위로 체결, 당일 종가대비 ±10% 가격으로 거래)
                """)
                return False
            else:
                print(f"""{t} | {funcnm}
                    한국거래소 장 종료.
                    KR_NOW : {t}
                    Market Open Time : 09시 ~ 16시
                """)
                return False
    def market_allyears(self):
        return  list(range(INIT_YEAR, thisyear()+1))





def formdatestyle(dt):
    return dt.isoformat()[:10].replace('-','')

def annual_fromtodates(fromyear, toyear):
    # 예외처리.
    for e in [fromyear, toyear]:
        if isinstance(e, str):
            e = int(e)
    if fromyear > toyear:
        print(f"\n Error ! fromyear is greater than toyear.\n")
    else:
        years = list(range(fromyear, toyear+1, 1))
        start_datetimes = [datetime(y,1,1) for y in years]
        end_datetimes = [datetime(y,12,31) for y in years]
        df = pd.DataFrame({'fromdate':start_datetimes, 'todate':end_datetimes})
        return df.to_dict('records')

def annual_fromtodate(fromyear, toyear):
    return datetime(fromyear,1,1), datetime(toyear,12,31)

def handle_iso_fromtodate(fromdate, todate):
    if (isinstance(fromdate, str)) and (isinstance(todate, str)):
        fromdate = datetime.strptime(fromdate,'%Y-%m-%d')
        todate = datetime.strptime(todate,'%Y-%m-%d')
    return fromdate, todate

def convert_datestr(isodate):
    if isinstance(isodate, str):
        isodate = datetime.strptime(isodate,'%Y-%m-%d').astimezone()
    return isodate

def clean_trddate(tbl):
    cursor = tbl.find(projection={'trddate':1})
    df = pd.DataFrame(list(cursor)).sort_values('trddate')
    df.trddate = df.trddate.apply(lambda x:datetime(x.year, x.month, x.day) )
    for d in df.to_dict('records'):
        UpdateResult = tbl.update_one(
                            filter={'_id':d['_id']},
                            update={'$set':{'trddate':d['trddate']}},
                            upsert=False)
        pp.pprint(UpdateResult.raw_result)
