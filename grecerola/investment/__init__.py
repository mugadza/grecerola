class InvestmentStatus:
    UNFULFILLED = "unfulfilled"  # Investment payment not received
    PARTIALLY_FULFILLED = (
        "partially fulfilled"  # part of the investment promised is received
    )
    FULFILLED = "fulfilled"  # total investment received
    CANCELED = "canceled"  # investment cancelled

    CHOICES = [
        (UNFULFILLED, "Unfulfilled"),
        (PARTIALLY_FULFILLED, "Partially fulfilled"),
        (FULFILLED, "Fulfilled"),
        (CANCELED, "Canceled"),
    ]