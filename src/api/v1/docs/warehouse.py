INVENT_RESPONCE = (
    "Returns a list of all products in stock with their remaining quantities."
)
INVENT_DESCRIPTION = "This endpoint allows administrators to retrieve a list of all products in the warehouse, along with their available stock quantities. It requires administrator privileges and returns the full inventory data."
INVENT_SUMMARY = "Get all products in stock (Admin only)."

OPERATION_RESPONCE = "Returns the updated stock levels after performing the operations."
OPERATION_DESCRIPTION = "This endpoint allows administrators to perform stock operations in the warehouse. It accepts a list containing the product ID, quantity, and operation type (inbound or outbound). The outbound operation cannot reduce the stock below available levels. Administrator privileges are required."
OPERATION_SUMMARY = "Perform stock operations (Admin only)."
