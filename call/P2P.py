from typing import Optional, Dict, Set, List, Any
from ..data_types.QIWIP2P import (
    PaySourcesTypes
)
from .API.QIWIP2P import (
    CreateInvoiceAPI, CheckInvoiceAPI, RejectInvoiceAPI, RefundInvoiceAPI, RefundStatusAPI
)
from .ADDONS.QIWIP2P import (
    PublicFormGenerator
)
from ..models.QIWIP2P import (
    Invoice, RefundData
)


class P2P:

    def __init__(self, public_key: str, secret_key: str) -> None:
        """
        :param public_key: The public key (PUBLIC_KEY) is used for invoicing through the form.
        :param secret_key: Your requests are authorized with the API secret key (SECRET_KEY).
        """
        self.public_key = public_key
        self.secret_key = secret_key

    async def generate_form(self, bill_id: Optional[str] = None, amount: Optional[float] = None,
                            phone_customer: Optional[str] = None, email_customer: Optional[str] = None,
                            account_customer: Optional[str] = None, comment: Optional[str] = None,
                            custom_fields: Optional[Dict[str, Any]] = None, theme_code: Optional[str] = None,
                            pay_sources_filter: Optional[List[Set[PaySourcesTypes]]] = None,
                            lifetime: Optional[int] = None, success_url: Optional[str] = None) -> str:
        """
        Upon opening the form, the customer is automatically billed.
        Account parameters are passed in clear text in the link.
        :param bill_id: unique id.
        :param amount: billed amount, round down to 2 decimal places
        :param phone_customer: customer phone number (in international format).
        :param email_customer: customer email.
        :param account_customer: customer ID on your system.
        :param comment: invoice comment.
        :param custom_fields: if use custom_fields (pay_sources_filter, theme_code) will be ignored.
        :param theme_code: customize your form personalization in (p2p.qiwi.com).
        :param pay_sources_filter: when you open the form, only the specified translation methods will be displayed.
        :param lifetime: the period until which the invoice will be available for payment (days).
        :param success_url: URL to redirect to your site in case of successful translation.
        :return: generated url for send to customer.
        """
        url = await PublicFormGenerator.generate_form(public_key=self.public_key,
                                                      bill_id=bill_id,
                                                      amount=amount,
                                                      phone_customer=phone_customer,
                                                      email_customer=email_customer,
                                                      account_customer=account_customer,
                                                      comment=comment,
                                                      custom_fields=custom_fields,
                                                      theme_code=theme_code,
                                                      pay_sources_filter=pay_sources_filter,
                                                      lifetime=lifetime,
                                                      success_url=success_url)
        return url

    async def new_invoice(self, bill_id: str, amount: float, invoice_currency: str, lifetime: int = 1,
                          comment: Optional[str] = None, phone_customer: Optional[str] = None,
                          email_customer: Optional[str] = None, account_customer: Optional[str] = None,
                          custom_fields: Optional[Dict[str, Any]] = None, theme_code: Optional[str] = None,
                          pay_sources_filter: Optional[List[Set[PaySourcesTypes]]] = None) -> Invoice:
        """

        :param bill_id: unique id.
        :param amount: data on the amount of the bill.
        :param invoice_currency: the currency of the invoice amount (RUB, KZT...).
        :param lifetime: the period until which the invoice will be available for payment (days).
        :param comment: invoice comment.
        :param phone_customer: customer phone number (in international format).
        :param email_customer: customer email.
        :param account_customer: customer ID on your system.
        :param custom_fields: if use custom_fields (pay_sources_filter, theme_code) will be ignored.
        :param theme_code: customize your form personalization in (p2p.qiwi.com).
        :param pay_sources_filter: when you open the form, only the specified translation methods will be displayed.
        :return: Invoice model with details new invoice.
        """
        response_data = await CreateInvoiceAPI.new_invoice(secret_key=self.secret_key,
                                                           bill_id=bill_id,
                                                           amount=amount,
                                                           invoice_currency=invoice_currency,
                                                           lifetime=lifetime,
                                                           comment=comment,
                                                           phone_customer=phone_customer,
                                                           email_customer=email_customer,
                                                           account_customer=account_customer,
                                                           theme_code=theme_code,
                                                           pay_sources_filter=pay_sources_filter,
                                                           custom_fields=custom_fields)
        return Invoice(**response_data)

    async def check_invoice(self, bill_id: str) -> Invoice:
        """
        The method allows you to check the status of the transfer on the account.
        :param bill_id: unique invoice identifier, specified when issuing.
        :return: Invoice model with details invoice.
        """
        response_data = await CheckInvoiceAPI.check_invoice(secret_key=self.secret_key,
                                                            bill_id=bill_id)
        return Invoice(**response_data)

    async def reject_invoice(self, bill_id: str) -> Invoice:
        """
        The method allows you to cancel an account that has not been transferred.
        :param bill_id: unique invoice identifier, specified when issuing.
        :return: Invoice model with details invoice.
        """
        response_data = await RejectInvoiceAPI.reject_invoice(secret_key=self.secret_key,
                                                              bill_id=bill_id)
        return Invoice(**response_data)

    async def refund_invoice(self, bill_id: str, refund_id: str, amount: float, return_currency: str) -> RefundData:
        """
        The method allows you to return funds.
        :param bill_id: unique invoice identifier, specified when issuing.
        :param refund_id: unique identifier of the refund in the merchant's system.
        :param amount: refund amount.
        :param return_currency: return currency (RUB, KZT...).
        :return: RefundData model with details.
        """
        response_data = await RefundInvoiceAPI.refund_invoice(secret_key=self.secret_key,
                                                              bill_id=bill_id,
                                                              refund_id=refund_id,
                                                              amount=amount,
                                                              return_currency=return_currency)
        return RefundData(**response_data)

    async def refund_status(self, bill_id: str, refund_id: str) -> RefundData:
        """
        The method allows you to check return status.
        :param bill_id: unique invoice identifier, specified when issuing.
        :param refund_id: unique identifier of the refund in the merchant's system.
        :return: RefundData model with details.
        """
        response_data = await RefundStatusAPI.refund_status(secret_key=self.secret_key,
                                                            bill_id=bill_id,
                                                            refund_id=refund_id)
        return RefundData(**response_data)
