"""Module containing the Binance Exchange class."""

from __future__ import annotations

import datetime as dtlib
import itertools

import ccxt

from trading.datasets import dataset_info
from trading.datasets import exchange
from trading.datasets.utils import datetime_utils
from trading.datasets.utils import generic_utils


__all__ = [
    # Class exports
    'BinanceExchange',
]


class BinanceExchange(exchange.Exchange, ccxt.binance):
    """Improved class implementation of the CCXT Binance Exchange."""

    FETCH_OHLCV_LIMIT = 999

    def _generate_fetch_ohlcv_params(
        self,
        timeframe: dataset_info.Timeframe,
        start: dtlib.datetime,
        end: dtlib.datetime,
        limit: int,
    ) -> dict:

        # Binance accepts the ending timestamp in milliseconds
        end_ms = datetime_utils.get_milliseconds(end)

        return {
            'endTime': int(end_ms),
            'limit': limit,
        }

    def get_funding_rates(
        self,
        symbol: str,
        start: dtlib.datetime | str | int | None = None,
        end: dtlib.datetime | str | int | None = None,
        pbar: generic_utils.Progbar | None = None,
    ) -> list[list[int | float]]:

        """Fetches the funding rates from an exchange.

        Arguments:
            symbol: Ticker symbol of the crypto asset.
            start: Starting datetime of the data to be fetched.
                The input argument can be a string indicating a
                valid datetime-like string or a number indicating the
                timestamp in milliseconds.
            end: Ending timestamp of the data to be fetched.
                The input argument can be a string indicating a
                valid datetime-like string or a number indicating the
                timestamp in milliseconds.
            pbar: Optional `ProgBar` instance input. Used for combining
                multiple calls of `get_ohlcv()`.

        Raises:
            FundingRatesFetchError: Raised for any errors that causes
                the fetching of funding rates to fail.

        Returns:
            A list of list representing the funding rates data fetched
            from the exchange. Each row/inner list contains two
            datapoints: the timestamp in milliseconds and the
            funding rate for that time.

            Example:

            ```
            [
                [1546128000000, 0.00123],
                [1546214400000, 0.00102],
                [1546300800000, -0.00105],
            ]
            ```
        """

        # Validate and standardize the symbol before using it
        symbol = self.get_valid_symbol(symbol)

        # Make sure that the start and end times are valid
        timeframe = dataset_info.Timeframe("8h")
        tf_duration = timeframe.get_duration()
        start, end = self.get_valid_start_end(
            start, end, timeframe, include_latest=True)

        # Create millisecond versions of the start and end times
        start_ms = datetime_utils.get_milliseconds(start)
        end_ms = datetime_utils.get_milliseconds(end)

        # Keep the original starting point since start_ms is modified
        # every iteration in the main loop of the downloading process
        orig_start_ms = start_ms
        orig_end_ms = end_ms

        # Inform user of funding rates download but don't create a new
        # progress bar if one is passed through the input parameters
        pbar_target = end_ms - start_ms
        if not(pbar and isinstance(pbar, generic_utils.Progbar)):
            print(f'Downloading {self.name} {symbol} funding rates '
                  f'from {start} to {end}...')
            pbar = generic_utils.Progbar(pbar_target)
            orig_pbar_progress = 0
        else:
            orig_pbar_progress = pbar.progress

        funding_rates = []
        error_counter = 0
        while True:
            try:
                limit = (orig_end_ms - start_ms) / tf_duration + 1
                limit = self._get_valid_limit(limit)

                # Run CCXT's internal funding rates fetch function
                # force an empty list if the limit passed is zero
                if limit > 0:

                    current_raw_frates = self.fapiPublic_get_fundingrate({
                        "symbol": self.market(symbol)["id"],
                        "startTime": int(start_ms),
                        "limit": limit,
                    })

                    # Pre-process
                    current_raw_frates = [
                        [
                            int(frate["fundingTime"]),
                            float(frate["fundingRate"]),
                        ]
                        for frate in current_raw_frates[:]
                    ]

                    # We want the oldest candle at the first index
                    current_raw_frates.sort(key=lambda e: e[0])

                else:
                    current_raw_frates = []

                if len(current_raw_frates) > 0:
                    # Update the starting and ending timestamps (ms)
                    start_ms = current_raw_frates[-1][0] - 1
                    end_ms = start_ms + (
                        tf_duration * self.FETCH_OHLCV_LIMIT)

                    # Adjust the starting time to the original one if it
                    # passes below it but the end time is still over it
                    if end_ms > orig_end_ms > start_ms:
                        end_ms = orig_end_ms
                    if start_ms > orig_end_ms:
                        start_ms = end_ms

                    # Add the current raw funding rates to the
                    # total funding rates list
                    funding_rates += current_raw_frates
                    pbar.add(abs(
                        current_raw_frates[0][0] -
                        current_raw_frates[-1][0]))

                # No funding rates was downloaded, we're done
                else:
                    break

                # Special check for funding rates because they
                # don't return an exact millisecond conversion
                # of the start or end time in the current raw frates
                raw_end = current_raw_frates[-1][0]
                raw_start = current_raw_frates[0][0]
                if ((raw_end // tf_duration == orig_end_ms // tf_duration) and
                    (raw_start // tf_duration == orig_start_ms // tf_duration)
                ):
                    break

            except (
                ccxt.ExchangeError,
                ccxt.AuthenticationError,
                ccxt.ExchangeNotAvailable,
                ccxt.RequestTimeout
            ) as err:

                # Exit the while loop if we had a lot of errors
                error_counter += 1
                if error_counter > 5:
                    raise errors.FundingRatesFetchError(
                        'Unable to load the dataset.') from err

                # Retry after 30 seconds
                time.sleep(30)

        # Make sure the total target is added to the progress bar
        pbar.update(orig_pbar_progress + pbar_target)

        # Sort final OHLCV list just to be sure
        funding_rates.sort(key=lambda e: e[0])
        funding_rates = list(
            funding_rates for funding_rates, _ in itertools.groupby(
                funding_rates))

        # Remove over elements because funding rates are over some dates
        return [e for e in funding_rates if e[0] <= orig_end_ms]
