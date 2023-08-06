import datetime


__ALL__ = ["dt2yyyymmddhhmmss", "yyyymmddhhmmss2dt"]


def dt2yyyymmddhhmmss(ymd_delimiter: str = "-", hms_delimiter: str = "-") -> str:
    return datetime.datetime.now().strftime(
        "%Y{ymd_delimiter}%m{ymd_delimiter}%d %H{hms_delimiter}%M{hms_delimiter}%S".format(
            ymd_delimiter=ymd_delimiter,
            hms_delimiter=hms_delimiter,
        )
    )


def yyyymmddhhmmss2dt(string: str, ymd_delimiter: str = "-", hms_delimiter: str = "-") -> datetime.datetime:
    return datetime.datetime.strptime(
        string, "%Y{ymd_delimiter}%m{ymd_delimiter}%d %H{hms_delimiter}%M{hms_delimiter}%S".format(
            ymd_delimiter=ymd_delimiter,
            hms_delimiter=hms_delimiter,
        )
    )

