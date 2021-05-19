import datetime


class DatetimeModule:

    @classmethod
    async def datetime_str(cls, dt: datetime.datetime, fmt: str) -> str:
        return dt.strftime(fmt).replace("UTC", "")

    @classmethod
    async def parse_datetime(cls, dt: datetime.datetime) -> str:
        if dt.tzinfo is not None:
            """
            If tz is set, we know current timezone.
            Sample 1: datetime.datetime.now(tz=datetime.timezone.utc)
            Sample 2: datetime.datetime.now().astimezone()
            In Sample 1 we get time with UTC timezone
            In Sample 2 we get current time with our local timezone
            Recommended use 1 or 2 sample with date_range or next_txn for datetime 
            Because of this we just convert this timezone
            """
            # Replace microseconds
            dt = dt.replace(microsecond=0)
            # Convert user timezone to +03:00
            dt = dt.astimezone(tz=datetime.timezone(datetime.timedelta(seconds=10800)))
            # Format
            dt = await cls.datetime_str(dt=dt, fmt="%Y-%m-%dT%H:%M:%S%Z")
            return dt
        else:
            """
            If tz not set, we do not know current timezone.
            Sample 1: datetime.datetime.utcnow()
            WARNING Sample 1: Can return bad time if our local time is bad
            WARNING Sample 1: Return BAD local timezone (not UTC) if use datetime.datetime.utcnow().astimezone()
            Because of this we just replace/set QIWI timezone
            """
            dt = dt.replace(microsecond=0, tzinfo=datetime.timezone(datetime.timedelta(seconds=10800)))
            dt = await cls.datetime_str(dt=dt, fmt="%Y-%m-%dT%H:%M:%S%Z")
            return dt

    @classmethod
    async def parse_datetime_p2p(cls, dt: datetime.datetime) -> str:
        if dt.tzinfo is not None:
            # Convert user timezone to +03:00
            dt = dt.astimezone(tz=datetime.timezone(datetime.timedelta(seconds=10800)))
            # Remove tzinfo
            dt = dt.replace(tzinfo=None)
        # Format
        dt = await cls.datetime_str(dt=dt, fmt="%Y-%m-%dT%H:%M:%S.%fZ")
        # Append
        dt = dt[0:-4] + "Z"
        return dt
