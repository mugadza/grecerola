class CampaignStatus:
    UNFULFILLED = "unfulfilled"  # campaign with  investment goal not met
    PARTIALLY_FULFILLED = (
        "partially fulfilled"  # campaign with more than 80% of the investment fulfilled
    )
    FULFILLED = "fulfilled"  # campaign with an investment goal met
    CANCELED = "canceled"  # permanently canceled campaign

    CHOICES = [
        (UNFULFILLED, "Unfulfilled"),
        (PARTIALLY_FULFILLED, "Partially fulfilled"),
        (FULFILLED, "Fulfilled"),
        (CANCELED, "Canceled"),
    ]