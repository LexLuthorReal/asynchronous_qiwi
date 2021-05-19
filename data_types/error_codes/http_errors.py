http_request_errors = {
    400: "Wrong data format of request.",
    401: "Wrong API token or token expired.",
    403: "Not enough rights of API token for the request.",
    404: "Transaction not found or no payments with such data. Wallet not found. Active webhook not found. " +
         "Invoice not found.",
    422: "Wrong domain/subnet/host in new webhook URL, wrong webhook type or transactions type, " +
         "webhook already exists and is active",
    423: "Too many requests, service temporary unavailable. Next after 5 minutes.",
    500: "Internal service error (webhook URL too long, infrastructure maintenance, resource is unavailable and so on)",
}
