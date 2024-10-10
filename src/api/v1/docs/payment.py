CREATE_RESPONCE = "Returns a payment link for the transaction."
CREATE_DESCRIPTION = "This endpoint creates a transaction to fund an account by accepting the account ID and the deposit amount. It returns a payment link from the payment system for the user to complete the transaction."
CREATE_SUMMARY = "Create a funding transaction."

WEBHOOK_RESPONCE = "Returns the payment status upon confirmation."
WEBHOOK_DESCRIPTION = "This endpoint allows the payment system to confirm a transaction by providing the payment signature and other required data. It validates the transaction and returns the payment status upon success."
WEBHOOK_SUMMARY = "Confirm a payment transaction (Payment system only)."

TRANSACTION_RESPONCE = (
    "Returns a list of all user's funding transactions with their payment statuses."
)
TRANSACTION_DESCRIPTION = "This endpoint retrieves all transactions related to funding the user's account, including their payment statuses. It returns a comprehensive list of these transactions upon successful request."
TRANSACTION_SUMMARY = "Get all funding transactions."

BUY_RESPONCE = "Returns the account balance after the purchase."
BUY_DESCRIPTION = "This endpoint allows a user to purchase a product by providing the wallet ID, product ID, and quantity of the product. Upon successful completion of the transaction, it returns the updated account balance."
BUY_SUMMARY = "Purchase a product."
