"""Class for identifying an individual security within the portfolio."""

from dataclasses import dataclass, fields

@dataclass
class Stock:
    """
    A security tracked in the portfolio: ticker, display name, sector, and 
    listing exchange.
    """
    ticker: str
    name: str
    sector: str
    exchange: str

    def __post_init__(self) -> None:
        """Normalize fields and raise on empty."""
        for f in fields(self):
            value = getattr(self, f.name)     # current value, a str
            value = value.strip()             # normalize: trim whitespace
            if not value:                     # validate: reject empty
                raise ValueError(f"a value is required, got {f.name!r}")
            if f.name == "ticker":            # field-specific normalization
                value = value.upper()
            setattr(self, f.name, value)      # write the normalized value back

        