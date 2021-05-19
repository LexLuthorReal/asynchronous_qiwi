from uuid import UUID
from typing import Optional, Union, Set, List
from ..utils.tools.phone_module import parse_phone
from ..data_types.QIWIWallet import (
    LimitsTypes,
    PaymentTypes, PaymentSources,
    DateRange,
    ReceiptFormat,
    CardAlias,
    LockedFields, AccountTypes,
    InvoicesTypes,
    HookType, NotifyType
)
from .API.QIWIWallet import (
    UserInfoAPI,
    IdentificationAPI,
    LimitsInfoAPI,
    UserRestrictionsAPI,
    HistoryPaymentsAPI, StatisticPaymentsAPI, TransactionInfoAPI, ReceiptAPI,
    ListBalancesAPI, CreateBalanceAPI, AvailableBalancesAPI, DefaultBalanceAPI,
    BuyQIWIMasterAPI, IssueQVC, ListQVCAPI, QVCStatementAPI, BlockQVCAPI, UnblockQVCAPI, QVCDetailsAPI, RenameQVCAPI,
    CommissionAPI, SendQIWIAPI, ConvertCurrencyAPI, CurrencyRatesAPI, CellularPaymentAPI, TransferCardAPI,
    OtherPaymentsAPI, FreePaymentsAPI, DetectCardAPI, DetectMobileAPI, DetectProviderAPI,
    IssueP2PTokenAPI, BillsListAPI, BillPayAPI, BillRejectAPI,
    RegistrationHookAPI, RemoveHookAPI, GetHookSignKeyAPI, NewHookSignKeyAPI, ActiveHookHandlersAPI,
    SendTestHookNotificationAPI,
    InvoiceStatementsAPI, InvoiceInfoAPI, CheckoutInvoiceAPI
)
from .ADDONS.QIWIWallet import (
    AutofillFormGenerator
)
from ..models.QIWIWallet import (
    AuthUser,
    Identification, SendIdentification,
    Limits,
    Restrictions,
    History, NextPayment, Statistic, PaymentData,
    ListBalances, AvailableBalances,
    PaymentInfo,
    VirtualCard, ListCardMaster, UnblockCardMaster, QVCDetails, RenameQVC,
    ResultCommission,
    CurrencyRates,
    ProviderData,
    BillsData, BillPayment,
    HookData, HookResponse, HookSignKey,
    TokenResult, InvoicesResult, CheckoutInvoiceInfo
)


class Wallet:

    def __init__(self, wallet_api_key: str, phone_number: Optional[Union[str, int]]) -> None:
        """
        :param wallet_api_key: QIWI unique token given for an account
        :param phone_number: Bind phone number integer or string
        """
        self.wallet_api_key = wallet_api_key

        if phone_number:
            self._phone_number = parse_phone(phone_number)
        else:
            self._phone_number = None

    @property
    def phone_number(self) -> str:
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value: Optional[Union[str, int]]) -> None:
        self._phone_number = parse_phone(value)

    @staticmethod
    async def _raise_for_phone(_has_invalid_format: bool = False) -> None:
        raise RuntimeWarning(
            "Phone number could not be recognised. Please enter set it correctly."
            if _has_invalid_format
            else "Some methods require setting phone number, instance.phone_number = '+...'"
        )

    async def get_me(self, auth_info_enabled: bool = True, contract_info_enabled: bool = True,
                     user_info_enabled: bool = True) -> AuthUser:
        """
        View params in documentation or ->
        Get authorization info
        :param user_info_enabled:
        :param contract_info_enabled:
        :param auth_info_enabled:
        :return:
        """

        response_data = await UserInfoAPI.get_me(wallet_api_key=self.wallet_api_key,
                                                 auth_info_enabled=auth_info_enabled,
                                                 contract_info_enabled=contract_info_enabled,
                                                 user_info_enabled=user_info_enabled)
        return AuthUser(**response_data)

    async def identification(self,
                             identification_class: Optional[SendIdentification] = None) -> Union[Identification, bool]:
        """
        Get your current identification status, or verify your account.
        :param identification_class: convenient class for params storing.
        :return: current identification status and request status.
        """
        if not self.phone_number:
            await self._raise_for_phone()

        response_data = await IdentificationAPI.identification(wallet_api_key=self.wallet_api_key,
                                                               phone_number=self.phone_number,
                                                               identification_class=identification_class)
        if isinstance(response_data, dict):
            # Return model if success
            return Identification(**response_data)
        # Return False if some problem
        return response_data

    async def account_limits(self, type_limits: Optional[List[Set[LimitsTypes]]] = None) -> Limits:
        """
        Get your current account limits.
        :param type_limits: (see data_types.QIWIWallet.limits).
        :return: current Limit model.
        """
        if not self.phone_number:
            await self._raise_for_phone()

        response_data = await LimitsInfoAPI.get_limits(wallet_api_key=self.wallet_api_key,
                                                       phone_number=self.phone_number,
                                                       type_limits=type_limits)

        return Limits(**response_data)

    async def account_restrictions(self) -> Restrictions:
        """
        The next request checks if there is a limit on outgoing payments from the QIWI Wallet.
        if restrictions not exist restrictions length = 0
        else restriction.restrictionCode is restriction code
        :return: current restriction on account
        """
        if not self.phone_number:
            await self._raise_for_phone()

        response_data = await UserRestrictionsAPI.get_restrictions(wallet_api_key=self.wallet_api_key,
                                                                   phone_number=self.phone_number)
        return Restrictions(restrictions=response_data)

    async def get_history_payments(self, rows: int = 50, operation_type: Optional[PaymentTypes] = None,
                                   sources_type: Optional[List[Set[PaymentSources]]] = None,
                                   date_range: Optional[DateRange] = None, next_txn: Optional[NextPayment] = None,
                                   all_transactions: bool = False) -> History:
        """
        :param rows: quantity of operations
        :param operation_type: see data_types.QIWIWallet.payments.PaymentTypes, default = <ALL>
        :param sources_type: payment source see data_types.QIWIWallet.payments.PaymentSources
        :param date_range: models.QIWIWallet.history.DateRange you can manually set (see utils.tools.datetime_str)
        :param next_txn: models.QIWIWallet.history.next_transactions, need if you want get transaction manually
        :param all_transactions: get all transactions (the number of requests direct dependence on "rows", "date_range")
        :return: History object
        """
        if not self.phone_number:
            await self._raise_for_phone()

        response_data = await HistoryPaymentsAPI.get_history(wallet_api_key=self.wallet_api_key,
                                                             phone_number=self.phone_number,
                                                             rows=rows,
                                                             operation_type=operation_type,
                                                             sources_type=sources_type,
                                                             date_range=date_range,
                                                             next_txn=next_txn,
                                                             all_transactions=all_transactions)
        return History(**response_data)

    async def get_statistic_payments(self, date_range: DateRange, operation_type: Optional[PaymentTypes] = None,
                                     sources_type: Optional[List[Set[PaymentSources]]] = None) -> Statistic:
        """
        :param date_range: models.QIWIWallet.history.DateRange. You can manually convert (see utils.tools.datetime_str)
        :param operation_type: see data_types.QIWIWallet.payments.PaymentTypes, default = <ALL>
        :param sources_type: payment source see data_types.QIWIWallet.payments.PaymentSources
        """
        if not self.phone_number:
            await self._raise_for_phone()

        response_data = await StatisticPaymentsAPI.get_statistic_payments(wallet_api_key=self.wallet_api_key,
                                                                          phone_number=self.phone_number,
                                                                          operation_type=operation_type,
                                                                          sources_type=sources_type,
                                                                          date_range=date_range)
        return Statistic(**response_data)

    async def get_transaction_info(self, txn_id: int, type_operation: Optional[PaymentTypes] = None) -> PaymentData:
        """
        :param txn_id: transaction_id in history payments.
        :param type_operation: see data_types.QIWIWallet.payments.PaymentTypes. In this request can be None.
        """
        response_data = await TransactionInfoAPI.get_transaction_info(wallet_api_key=self.wallet_api_key,
                                                                      txn_id=txn_id,
                                                                      type_operation=type_operation)
        return PaymentData(**response_data)

    async def get_payment_receipt_file(self, txn_id: int, type_operation: PaymentTypes,
                                       file_format: ReceiptFormat) -> Union[bool, bytes]:
        """
        :param txn_id: transaction_id
        :param type_operation: see data_types.QIWIWallet.payments.PaymentTypes
        :param file_format: can be PDF or JPEG, see data_types.QIWIWallet.receipt.ReceiptFormat
        :return binary data for write to the file (PDF, JPEG) or bool if some error.
        """
        response_data = await ReceiptAPI.get_payment_receipt_file(wallet_api_key=self.wallet_api_key,
                                                                  txn_id=txn_id,
                                                                  type_operation=type_operation,
                                                                  file_format=file_format)
        return response_data

    async def send_payment_receipt_email(self, txn_id: int, type_operation: PaymentTypes, email: str) -> bool:
        """
        :param txn_id: transaction_id
        :param type_operation: see data_types.QIWIWallet.payments.PaymentTypes
        :param email: send to email, if None need set file_format & save_path
        :return bool status. True - email sent. False - some error.
        """
        status = await ReceiptAPI.send_payment_receipt_email(wallet_api_key=self.wallet_api_key,
                                                             txn_id=txn_id,
                                                             type_operation=type_operation,
                                                             email=email)
        return status

    async def get_list_balances(self) -> ListBalances:
        """
        The request dumps the current account balances of your QIWI Wallet.
        """
        if not self.phone_number:
            await self._raise_for_phone()

        response_data = await ListBalancesAPI.get_list_balances(wallet_api_key=self.wallet_api_key,
                                                                phone_number=self.phone_number)
        return ListBalances(**response_data)

    async def create_balance(self, alias: str) -> bool:
        """
        The request creates a new "account" and balance in your QIWI Wallet.
        The list of balances available for creating can be obtained by another request. (get_available_balances())
        :param alias: New balance alias
        :return: status
        """
        if not self.phone_number:
            await self._raise_for_phone()

        status = await CreateBalanceAPI.create_balance(wallet_api_key=self.wallet_api_key,
                                                       phone_number=self.phone_number,
                                                       alias=alias)
        return status

    async def get_available_balances(self) -> AvailableBalances:
        """
        The request displays the aliases of the balances available for creation in your QIWI Wallet.
        :return: model
        """
        if not self.phone_number:
            await self._raise_for_phone()

        response_data = await AvailableBalancesAPI.get_available_balances(wallet_api_key=self.wallet_api_key,
                                                                          phone_number=self.phone_number)
        return AvailableBalances(available_balances=response_data)

    async def set_default_balance(self, balance_alias: str) -> bool:
        """
        The request sets up an balance for your QIWI Wallet.
        The balance of which will be used to fund all payments by default. The balance must be in the list of balances.
        :return: status
        """
        if not self.phone_number:
            await self._raise_for_phone()

        status = await DefaultBalanceAPI.set_default_balance(wallet_api_key=self.wallet_api_key,
                                                             phone_number=self.phone_number,
                                                             balance_alias=balance_alias)
        return status

    # NOT TESTED NEED CHECK
    async def buy_qiwi_master(self, comment: str, master_price: int = 2999, payment_currency: int = 643,
                              method_type: str = "Account", account_currency: int = 643) -> Union[PaymentInfo, bool]:
        """
        Buying a QIWI Master package.
        :param comment: random comment.
        :param master_price: price QIWI Master package.
        :param payment_currency: package currency in the QIWI System.
        :param method_type: payment method.
        :param account_currency: Account currency for payment, only 643.
        :return: PaymentInfo if success
        """
        if not self.phone_number:
            await self._raise_for_phone()

        response_data = await BuyQIWIMasterAPI.buy_qiwi_master(wallet_api_key=self.wallet_api_key,
                                                               phone_number=self.phone_number,
                                                               comment=comment,
                                                               master_price=master_price,
                                                               payment_currency=payment_currency,
                                                               method_type=method_type,
                                                               account_currency=account_currency)
        if isinstance(response_data, dict):
            return PaymentInfo(**response_data)
        else:
            return response_data

    # NOT TESTED NEED CHECK
    async def issue_qvc(self, card_alias: CardAlias, method_type: str = "Account",
                        account_currency: int = 643) -> Union[VirtualCard, PaymentInfo, bool]:
        """
        QIWI Master Virtual Card Issue
        :param card_alias: QVC_CPA/QVC_CPA_DEBIT (QIWI Master Prepaid/QIWI Master Debit).
        :param method_type: payment method.
        :param account_currency: Account currency for payment, only 643.
        :return: return VirtualCard if card is free. PaymentInfo if paid. bool if error.
        """
        if not self.phone_number:
            await self._raise_for_phone()

        response_data = await IssueQVC.issue_qvc(wallet_api_key=self.wallet_api_key,
                                                 phone_number=self.phone_number,
                                                 card_alias=card_alias,
                                                 method_type=method_type,
                                                 account_currency=account_currency)
        if isinstance(response_data, VirtualCard):
            # Return if card free
            return response_data
        elif isinstance(response_data, dict):
            # Return if success pay
            return PaymentInfo(**response_data)
        # Return False if some error
        return response_data

    # NOT TESTED NEED CHECK
    async def get_list_qvc_master(self) -> ListCardMaster:
        """
        Lets you get a list of QIWI Master cards.
        :return qiwi master cards list.
        """

        response_data = await ListQVCAPI.get_list_qvc_master(wallet_api_key=self.wallet_api_key)
        return ListCardMaster(data=response_data)

    # NOT TESTED NEED CHECK
    async def get_qvc_statement(self, card_id: int, date_range: DateRange) -> Union[bool, bytes]:
        """
        The request is intended for unloading transactions a specific card for a specified period in the QIWI Master.
        :param card_id - id your card. You can get id from method get_list_qvc_master().
        :param date_range - data range with start_date, end_date for get statements of this period.
        :return binary data for write to the file (only "PDF") or bool if some error.
        """
        if not self.phone_number:
            await self._raise_for_phone()

        response_data = await QVCStatementAPI.get_qvc_statement(wallet_api_key=self.wallet_api_key,
                                                                phone_number=self.phone_number,
                                                                card_id=card_id,
                                                                date_range=date_range)
        return response_data

    # NOT TESTED NEED CHECK
    async def block_qvc(self, card_id: int) -> bool:
        """
        Blocking the QIWI Master Card.
        :param card_id: you can get from get_list_qvc_master().
        :return: True - card blocked. False - some error, maybe wrong card_id.
        """
        if not self.phone_number:
            await self._raise_for_phone()

        status = await BlockQVCAPI.block_qvc(wallet_api_key=self.wallet_api_key,
                                             phone_number=self.phone_number,
                                             card_id=card_id)
        return status

    # NOT TESTED NEED CHECK
    async def unblock_qvc(self, card_id: int) -> Union[UnblockCardMaster, bool]:
        """
        Unlocking is available within 90 days from the moment the card was blocked according to API v2.
        :return model with status code.
        """
        if not self.phone_number:
            await self._raise_for_phone()

        response_data = await UnblockQVCAPI.unblock_qvc(wallet_api_key=self.wallet_api_key,
                                                        phone_number=self.phone_number,
                                                        card_id=card_id)
        if isinstance(response_data, dict):
            # Return model if success
            return UnblockCardMaster(**response_data)
        # Return model if some error
        return response_data

    # NOT TESTED NEED CHECK
    async def get_qvc_details(self, card_id: int, operation_id: UUID) -> Union[QVCDetails, bool]:
        """
        Receiving QIWI Virtual Card details.
        :param card_id: you can get from get_list_qvc_master().
        :param operation_id: any UUID
        :return model with status, cvv, pan, error_code.
        """
        response_data = await QVCDetailsAPI.get_qvc_details(wallet_api_key=self.wallet_api_key,
                                                            card_id=card_id,
                                                            operation_id=operation_id)
        if isinstance(response_data, dict):
            # Return model if success
            return QVCDetails(**response_data)
        # Return model if some error
        return response_data

    # NOT TESTED NEED CHECK
    async def rename_qvc(self, card_id: int, alias: str) -> Union[RenameQVC, bool]:
        """
        Changing the name QIWI Virtual Card.
        :param card_id: you can get from get_list_qvc_master().
        :param alias: new name of the card.
        :return: model with status, error, errorCode.
        """
        response_data = await RenameQVCAPI.rename_qvc(wallet_api_key=self.wallet_api_key,
                                                      card_id=card_id,
                                                      alias=alias)
        if isinstance(response_data, dict):
            # Return model if success
            return RenameQVC(**response_data)
        # Return model if some error
        return response_data

    async def get_commission(self, provider_id: int, target_account: str, amount: float, target_currency: int,
                             account_currency: int, method_type: str = "Account") -> ResultCommission:
        """
        The full commission of the QIWI Wallet is returned for the payment in favor of the specified provider.
        :param provider_id: id in QIWI System.
        :param target_account: for calculating commission.
        :param amount: sum payment/transfer.
        :param target_currency: currency payment.
        :param account_currency: Account currency for payment.
        :param method_type: payment method.
        :return: model with commission.
        """
        response_data = await CommissionAPI.get_commission(wallet_api_key=self.wallet_api_key,
                                                           provider_id=provider_id,
                                                           target_account=target_account,
                                                           amount=amount,
                                                           method_type=method_type,
                                                           account_currency=account_currency,
                                                           target_currency=target_currency)
        return ResultCommission(**response_data)

    @staticmethod
    async def autofill_form(provider_id: int, currency: Optional[int] = None, comment: Optional[str] = None,
                            target_account: Optional[str] = None, amount_integer: Optional[int] = None,
                            amount_fraction: Optional[int] = None, account_type: Optional[AccountTypes] = None,
                            locked_fields: Optional[List[Set[LockedFields]]] = None) -> str:
        """
        Autocomplete payment forms.
        :param provider_id: provider identifier.
        :param currency: payment currency code. Required parameter if you pass the payment amount in the link.
        :param comment: Comment. The parameter is used only for ID = (99, 99999).
        :param target_account: Wallet number, phone/account/card number/recipient's user ID.
        :param amount_integer: The whole part of the payment amount.
        :param amount_fraction: Fractional part of the payment amount.
        :param locked_fields: Sign of an inactive form field. The user will not be able to change the value of this.
        :param account_type: The value determines the transfer to the QIWI wallet by nickname or number (ID = 99, 99999)
        :return: generated url for send to customer.
        """
        url = await AutofillFormGenerator.autofill_form(provider_id=provider_id,
                                                        currency=currency,
                                                        target_account=target_account,
                                                        amount_integer=amount_integer,
                                                        amount_fraction=amount_fraction,
                                                        comment=comment,
                                                        locked_fields=locked_fields,
                                                        account_type=account_type)
        return url

    async def send_to_qiwi(self, comment: str, target_account: str, amount: float, target_currency: int,
                           account_currency: int, method_type: str = "Account") -> PaymentInfo:
        """
        Target currency must be same account currency.
        :param comment: comment.
        :param target_account: target account for payment.
        :param amount: payment amount.
        :param target_currency: currency payment.
        :param account_currency: Account currency for payment.
        :param method_type: payment method.
        :return: model with payment info.
        """
        response_data = await SendQIWIAPI.send_to_qiwi(wallet_api_key=self.wallet_api_key,
                                                       target_account=target_account,
                                                       comment=comment,
                                                       amount=amount,
                                                       method_type=method_type,
                                                       account_currency=account_currency,
                                                       target_currency=target_currency)
        return PaymentInfo(**response_data)

    async def convert_currency(self, comment: str, amount: float, target_currency: int, account_currency: int,
                               method_type: str = "Account", target_account: Optional[str] = None) -> PaymentInfo:
        """
        :param comment: comment.
        :param amount: amount in currency code.
        :param target_currency: currency code to convert or target currency.
        :param account_currency: Account currency for exchange.
        :param method_type: payment method.
        :param target_account: target account for detailed requisites.
        :return: model with payment info.
        """
        if target_account is None:
            if not self.phone_number:
                await self._raise_for_phone()
            target_account = self.phone_number
        response_data = await ConvertCurrencyAPI.convert_currency(wallet_api_key=self.wallet_api_key,
                                                                  comment=comment,
                                                                  amount=amount,
                                                                  target_currency=target_currency,
                                                                  target_account=target_account,
                                                                  method_type=method_type,
                                                                  account_currency=account_currency)
        return PaymentInfo(**response_data)

    async def get_currency_rates(self) -> CurrencyRates:
        """
        The method returns the current exchange rates and cross-rates of the QIWI Bank currencies.
        :return: model with currencies and cross-rates.
        """
        response_data = await CurrencyRatesAPI.get_currency_rates(wallet_api_key=self.wallet_api_key)
        return CurrencyRates(**response_data)

    async def send_cellular_payment(self, provider_id: int, target_number: str, amount: float, target_currency: int,
                                    account_currency: int, method_type: str = "Account") -> PaymentInfo:
        """
        Payment for cellular communication.
        :param provider_id: provider identifier. Determined by checking the mobile operator.
        :param target_number: mobile phone number for top-up (without prefix 8, +7).
        :param amount: amount of payment.
        :param target_currency: target currency must be same account currency.
        :param account_currency: Account currency for payment.
        :param method_type: payment method.
        :return: model with payment info.
        """
        response_data = await CellularPaymentAPI.send_cellular_payment(wallet_api_key=self.wallet_api_key,
                                                                       provider_id=provider_id,
                                                                       target_number=target_number,
                                                                       amount=amount,
                                                                       target_currency=target_currency,
                                                                       account_currency=account_currency,
                                                                       method_type=method_type)
        return PaymentInfo(**response_data)

    async def transfer_to_card(self, provider_id: int, target_card: str, amount: float,
                               target_currency: int, account_currency: int, method_type: str = "Account",
                               sender_address: Optional[str] = None, sender_city: Optional[str] = None,
                               sender_country: Optional[str] = None, receiver_name: Optional[str] = None,
                               receiver_surname: Optional[str] = None, sender_name: Optional[str] = None,
                               sender_surname: Optional[str] = None) -> PaymentInfo:
        """
        The request makes a money transfer to cards of Visa, MasterCard or MIR payment systems.
        First, you need to find out the provider code for transferring to the card by the card number.
        :param provider_id: provider identifier.
        :param target_card: card number for transfer.
        :param amount: amount of transfer.
        :param target_currency: target currency must be same account currency.
        :param account_currency: account currency for payment.
        :param method_type: payment method.
        :param sender_address: sender address.
        :param sender_city: sender city.
        :param sender_country: sender country.
        :param receiver_name: receiver name.
        :param receiver_surname: receiver surname.
        :param sender_name: sender name.
        :param sender_surname: sender surname.
        :return: model with payment info.
        """
        response_data = await TransferCardAPI.transfer_to_card(wallet_api_key=self.wallet_api_key,
                                                               provider_id=provider_id,
                                                               target_card=target_card,
                                                               amount=amount,
                                                               target_currency=target_currency,
                                                               account_currency=account_currency,
                                                               method_type=method_type,
                                                               sender_address=sender_address,
                                                               sender_city=sender_city,
                                                               sender_country=sender_country,
                                                               receiver_name=receiver_name,
                                                               receiver_surname=receiver_surname,
                                                               sender_name=sender_name,
                                                               sender_surname=sender_surname)
        return PaymentInfo(**response_data)

    async def other_payment(self, provider_id: int, target_account: str, amount: float,
                            target_currency: int, account_currency: int, method_type: str = "Account") -> PaymentInfo:
        """
        Payment for services by user ID.
        This request is used for providers using a single user identifier in their details.
        Without checking the account number.
        :param provider_id: provider identifier.
        :param target_account: target account for transfer.
        :param amount: amount of transfer.
        :param target_currency: target currency must be same account currency.
        :param account_currency: account currency for payment.
        :param method_type: payment method.
        :return: model with payment info.
        """
        response_data = await OtherPaymentsAPI.other_payment(wallet_api_key=self.wallet_api_key,
                                                             provider_id=provider_id,
                                                             target_account=target_account,
                                                             amount=amount,
                                                             target_currency=target_currency,
                                                             account_currency=account_currency,
                                                             method_type=method_type)
        return PaymentInfo(**response_data)

    async def payment_free_details(self, target_account: str, amount: float, target_currency: int,
                                   account_currency: int, name_bank: str, bik_recipient: int, city_recipient: str,
                                   name_organization: str, inn_organization: int, kpp_organization: int, nds: str,
                                   goal_payment: str, payer_name: str, payer_surname: str, payer_patronymic: str,
                                   request_protocol: str = "qw1", service_id: int = 1717, urgent_payment: int = 0,
                                   is_commercial: int = 1, info: str = "Коммерческие организации",
                                   method_type: str = "Account") -> PaymentInfo:
        """
        Payment for the services of commercial organizations according to their bank details.
        :param target_account: beneficiary account number.
        :param amount: amount of transfer.
        :param target_currency: target currency must be same account currency.
        :param account_currency: account currency for payment.
        :param name_bank: beneficiary bank name (quotes are escaped with '\').
        :param bik_recipient: beneficiary bank BIC.
        :param city_recipient: city of location of the recipient.
        :param name_organization: organization name (quotes are escaped with '\').
        :param inn_organization: INN of the organization
        :param kpp_organization: KPP of the organization
        :param nds: if the receipt does not include (VAT/НДС) then = "НДС не облагается". Otherwise "В т.ч. НДС".
        :param goal_payment: purpose of payment.
        :param payer_name: payer name.
        :param payer_surname: payer surname.
        :param payer_patronymic: payer patronymic.
        :param request_protocol: service information, constant "qw1" (not exactly).
        :param service_id: Service information, constant "1717" (not exactly).
        :param urgent_payment: Can be 0, 1. Urgent payment takes from 10 minutes.
        Possible on weekdays from 9:00 to 20:30 Moscow time. The cost of the service is 25 rubles.
        :param is_commercial: Service information, constant "1" (not exactly).
        :param info: constant, "Коммерческие организации" (not exactly).
        :param method_type: payment method.
        :return: model with payment info.
        """
        response_data = await FreePaymentsAPI.payment_free_details(wallet_api_key=self.wallet_api_key,
                                                                   target_account=target_account,
                                                                   amount=amount,
                                                                   target_currency=target_currency,
                                                                   account_currency=account_currency,
                                                                   name_bank=name_bank,
                                                                   bik_recipient=bik_recipient,
                                                                   city_recipient=city_recipient,
                                                                   name_organization=name_organization,
                                                                   inn_organization=inn_organization,
                                                                   kpp_organization=kpp_organization,
                                                                   nds=nds,
                                                                   goal_payment=goal_payment,
                                                                   payer_name=payer_name,
                                                                   payer_surname=payer_surname,
                                                                   payer_patronymic=payer_patronymic,
                                                                   request_protocol=request_protocol,
                                                                   service_id=service_id,
                                                                   urgent_payment=urgent_payment,
                                                                   is_commercial=is_commercial,
                                                                   info=info,
                                                                   method_type=method_type)
        return PaymentInfo(**response_data)

    @staticmethod
    async def get_card_provider(card_number: str) -> ProviderData:
        """
        The definition of the provider of the transfer to the card is performed by this request.
        The response returns the provider identifier for transferring the request to the card.
        :param card_number: Unmasked card number (no spaces).
        :return: ProviderData model.
        """
        response_data = await DetectCardAPI.get_card_provider(card_number=card_number)
        return ProviderData(**response_data)

    @staticmethod
    async def get_mobile_provider(phone_number: str) -> ProviderData:
        """
        The definition of the provider of the transfer to the card is performed by this request.
        The response returns the provider identifier for transferring the request to the card.
        :param phone_number: phone number (no +).
        :return: ProviderData model.
        """
        response_data = await DetectMobileAPI.get_mobile_provider(phone_number=phone_number)
        return ProviderData(**response_data)

    @staticmethod
    async def get_provider_phrase(search_phrase: str) -> ProviderData:
        """
        :param search_phrase: string of keywords to search for a provider.
        :return: ProviderData model.
        """
        response_data = await DetectProviderAPI.get_provider_phrase(search_phrase=search_phrase)
        return ProviderData(**response_data)

    async def issue_p2p_token(self, keys_pair_name: str,
                              server_notifications_url: Optional[str] = None) -> TokenResult:
        """
        You can get a P2P token at p2p.qiwi.com in your personal account, or use the request below.
        You can also configure the invoice notification address with this request.
        This request returns a pair of P2P tokens (for invoicing when calling a payment form and via API, respectively)
        in the PublicKey and SecretKey response fields. The QIWI Wallet API token is used for authorization.
        :param keys_pair_name: P2P token pair name (arbitrary string).
        :param server_notifications_url: URL for invoice payment notifications (optional).
        :return:
        """
        response_data = await IssueP2PTokenAPI.issue_p2p_token(wallet_api_key=self.wallet_api_key,
                                                               keys_pair_name=keys_pair_name,
                                                               server_notifications_url=server_notifications_url)
        return TokenResult(**response_data)

    async def get_list_of_bills(self, status: InvoicesTypes, rows: Optional[int] = None,
                                next_id: Optional[int] = None, all_bills: bool = False) -> BillsData:
        """
        Function for getting a list of bills in a wallet.
        :param status: bill status (see data_types.QIWIWallet.invoices).
        :param rows: quantity of bills (max: 50).
        :param next_id: the starting bill identifier for the search.
        :param all_bills: get all bills (the number of requests direct dependence on "rows")
        :return:
        """
        response_data = await BillsListAPI.get_list_of_bills(wallet_api_key=self.wallet_api_key,
                                                             status=status,
                                                             rows=rows,
                                                             next_id=next_id,
                                                             all_bills=all_bills)
        return BillsData(**response_data)

    async def pay_bill(self, bill_id: int, account_currency: int) -> BillPayment:
        """
        Execution of unconditional payment of the invoice without SMS confirmation.
        :param bill_id: you can get id from get_list_of_bills().
        :param account_currency: account currency for payment.
        :return: BillPayment model.
        """
        response_data = await BillPayAPI.pay_bill(wallet_api_key=self.wallet_api_key,
                                                  bill_id=bill_id,
                                                  account_currency=account_currency)
        return BillPayment(**response_data)

    async def reject_unpaid_bill(self, bill_id: int) -> bool:
        """
        The method rejects the unpaid invoice. In this case, the account becomes unavailable for payment.
        :param bill_id: you can get id from get_list_of_bills().
        :return: True if rejected.
        """
        response_data = await BillRejectAPI.reject_unpaid_bill(wallet_api_key=self.wallet_api_key,
                                                               bill_id=bill_id)
        return response_data

    async def register_hook(self, hook_type: HookType, url_hook: str, notify_type: NotifyType) -> HookData:
        """
        Hook registration.
        :param hook_type: (see data_types.QIWIWallet.hook_types.HookType)
        :param url_hook: webhook processing server address.
        :param notify_type: the type of transactions for which notifications will be enabled.
        :return: HookData model with details.
        """
        response_data = await RegistrationHookAPI.register_hook(wallet_api_key=self.wallet_api_key,
                                                                hook_type=hook_type,
                                                                url_hook=url_hook,
                                                                notify_type=notify_type)
        return HookData(**response_data)

    async def remove_hook(self, hook_id: str) -> HookResponse:
        """
        Removing a webhook.
        :param hook_id: webhook UUID.
        :return: HookResponse model with details.
        """
        response_data = await RemoveHookAPI.remove_hook(wallet_api_key=self.wallet_api_key,
                                                        hook_id=hook_id)
        return HookResponse(**response_data)

    async def get_hook_sign_key(self, hook_id: str) -> HookSignKey:
        """
        Each notification contains a digital signature of the message, encrypted with a key.
        To obtain a signature verification key, use this request.
        :param hook_id: webhook UUID.
        :return: HookSignKey model with key.
        """
        response_data = await GetHookSignKeyAPI.get_hook_sign_key(wallet_api_key=self.wallet_api_key,
                                                                  hook_id=hook_id)
        return HookSignKey(**response_data)

    async def new_hook_sign_key(self, hook_id: str) -> HookSignKey:
        """
        Use this request to change the encryption key for notifications.
        :param hook_id: webhook UUID.
        :return: HookSignKey model with new key.
        """
        response_data = await NewHookSignKeyAPI.new_hook_sign_key(wallet_api_key=self.wallet_api_key,
                                                                  hook_id=hook_id)
        return HookSignKey(**response_data)

    async def get_active_hook_handlers(self) -> HookData:
        """
        :return: HookData model with details.
        """
        response_data = await ActiveHookHandlersAPI.get_active_hook_handlers(wallet_api_key=self.wallet_api_key)
        return HookData(**response_data)

    async def send_test_hook_notification(self) -> HookResponse:
        """
        :return: HookResponse model with details.
        """
        response_data = await SendTestHookNotificationAPI.send_hook_notification(wallet_api_key=self.wallet_api_key)
        return HookResponse(**response_data)

    async def get_invoice_statements(self, rows: Optional[int] = None, data_type: str = "CREATED",
                                     date_range: Optional[DateRange] = None, status: Optional[InvoicesTypes] = None,
                                     all_invoices: bool = False) -> InvoicesResult:
        """
        Get invoice statements history.
        :param rows: quantity of operations (max: 50).
        :param data_type: constant value (not exactly).
        :param date_range: models.QIWIWallet.history.DateRange you can manually set (see utils.tools.datetime_str)
        :param status: invoice status (see data_types.QIWIWallet.invoices)
        :param all_invoices: get all invoices (the number of requests direct dependence on "rows", "date_range")
        :return: InvoicesResult model.
        """
        response_data = await InvoiceStatementsAPI.get_invoice_statements(wallet_api_key=self.wallet_api_key,
                                                                          rows=rows,
                                                                          data_type=data_type,
                                                                          date_range=date_range,
                                                                          status=status,
                                                                          all_invoices=all_invoices)
        return InvoicesResult(**response_data)

    async def get_invoice_info(self, external_invoice_uid: str) -> InvoicesResult:
        """
        Get invoice info.
        :param external_invoice_uid: you can get from get_invoice_statements().
        :return: InvoicesResult model.
        """
        response_data = await InvoiceInfoAPI.get_invoice_info(wallet_api_key=self.wallet_api_key,
                                                              external_invoice_uid=external_invoice_uid)
        return InvoicesResult(**response_data)

    async def checkout_invoice(self, invoice_uid: str) -> CheckoutInvoiceInfo:
        """
        Get info about invoice.
        :param invoice_uid: you can get from pay_url.
        :return: CheckoutInvoiceInfo model with details this invoice data and status.
        """
        response_data = await CheckoutInvoiceAPI.checkout_invoice(wallet_api_key=self.wallet_api_key,
                                                                  invoice_uid=invoice_uid)
        return CheckoutInvoiceInfo(**response_data)
