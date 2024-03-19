from dataclasses import dataclass
import pandas as pd


@dataclass
class Period:
    time_min: str
    time_max: str
    freq_step: str
    unit: str

    @property
    def freq(self):
        return f"{self.freq_step}{self.unit}"

    @property
    def date_range(self):
        return pd.date_range(start=self.time_min, end=self.time_max, freq=self.freq)