from dataclasses import dataclass


@dataclass
class Result:
    rub: float
    btc: float


def configure(rub: float, btc: float):
    return Result(rub=rub,
                  btc=btc)
