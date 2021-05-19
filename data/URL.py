class HeadTailString(str):

    __head__: str = ""
    __tail__: str = ""

    def __new__(cls, tail: str = None, head: str = None):
        if tail is None:
            tail = cls.__tail__

        if head is None:
            head = cls.__head__

        return str.__new__(cls, head + tail)


class QIWIURL(HeadTailString):
    __head__ = "https://qiwi.com/"


class QIWIOplata(HeadTailString):
    __head__ = "https://oplata.qiwi.com/"


class QIWIEdgeURL(HeadTailString):
    __head__ = "https://edge.qiwi.com/"


class QIWIAPIURL(HeadTailString):
    __head__ = "https://api.qiwi.com/"


class QIWIWalletURLS:
    me = QIWIEdgeURL("person-profile/v1/profile/current")
    identification = QIWIEdgeURL("identification/v1/persons/{}/identification")
    limits = QIWIEdgeURL("qw-limits/v1/persons/{}/actual-limits")
    restrictions = QIWIEdgeURL("person-profile/v1/persons/{}/status/restrictions")
    history = QIWIEdgeURL("payment-history/v2/persons/{}/payments")
    statistic = QIWIEdgeURL("payment-history/v2/persons/{}/payments/total")
    transaction_info = QIWIEdgeURL("payment-history/v2/transactions/{}")
    receipt_file = QIWIEdgeURL("payment-history/v1/transactions/{}/cheque/file")
    receipt_email = QIWIEdgeURL("payment-history/v1/transactions/{}/cheque/send")

    class Balance:
        base = QIWIEdgeURL("funding-sources/v2/persons/")
        balance = QIWIEdgeURL("{}/accounts", head=base)
        available_aliases = QIWIEdgeURL("/offer", head=balance)
        set_new_balance = QIWIEdgeURL("/{}", head=balance)

    class QIWIMaster:
        QIWI_Master_package = QIWIEdgeURL("sinap/api/v2/terms/28004/payments")
        create_virtual_card_order = QIWIEdgeURL("/cards/v2/persons/{}/orders")
        confirmation_order = QIWIEdgeURL("cards/v2/persons/{}/orders/{}/submit")
        buy_virtual_card = QIWIEdgeURL("sinap/api/v2/terms/32064/payments")
        list_card = QIWIEdgeURL("cards/v1/cards/?vas-alias={}")
        card_statement = QIWIEdgeURL("payment-history/v1/persons/{}/cards/{}/statement?from={}&till={}")
        block_card = QIWIEdgeURL("cards/v2/persons/{}/cards/{}/block")
        unblock_card = QIWIEdgeURL("cards/v2/persons/{}/cards/{}/unblock")
        card_details = QIWIEdgeURL("cards/v1/cards/{}/details")
        rename_card = QIWIEdgeURL("cards/v1/cards/{}/alias")

    class Payments:
        commission = QIWIEdgeURL("sinap/providers/{}/onlineCommission")
        autofill_form = QIWIURL("payment/form/{}")
        send_to_qiwi = QIWIEdgeURL("sinap/api/v2/terms/99/payments")
        convert = QIWIEdgeURL("sinap/api/v2/terms/1099/payments")
        currency_rates = QIWIEdgeURL("sinap/crossRates")
        payments = QIWIEdgeURL("sinap/api/v2/terms/{}/payments")
        detect_card = QIWIURL("card/detect.action")
        detect_mobile = QIWIURL("mobile/detect.action")
        detect_phrase = QIWIURL("search/results/json.action?searchPhrase={}")

    class Bills:
        list_bills = QIWIEdgeURL("checkout-api/api/bill/search")
        pay_bill = QIWIEdgeURL("checkout-api/invoice/pay/wallet")
        reject_bill = QIWIEdgeURL("checkout-api/api/bill/reject")

    class Invoice:
        p2p_issue = QIWIEdgeURL("widgets-api/api/p2p/protected/keys/create")
        invoice_statements = QIWIEdgeURL("widgets-api/api/p2p/protected/invoices/")
        check_invoice_uid = QIWIEdgeURL("qw-p2p-checkout-api/v1/invoice/{}")

    class WebHooks:
        register = QIWIEdgeURL("payment-notifier/v1/hooks")
        remove = QIWIEdgeURL("payment-notifier/v1/hooks/{}")
        get_sign_key = QIWIEdgeURL("payment-notifier/v1/hooks/{}/key")
        new_sign_key = QIWIEdgeURL("payment-notifier/v1/hooks/{}/newkey")
        active = QIWIEdgeURL("payment-notifier/v1/hooks/active")
        test = QIWIEdgeURL("payment-notifier/v1/hooks/test")


class QIWIP2PURLS:
    generate_form = QIWIOplata("create")
    invoice = QIWIAPIURL("partner/bill/v1/bills/{}")
    reject_invoice = QIWIAPIURL("partner/bill/v1/bills/{}/reject")
    refund = QIWIAPIURL("partner/bill/v1/bills/{}/refunds/{}")


class QIWITerminals:
    ttp_groups = QIWIEdgeURL("locator/v3/ttp-groups")
    search_coordinates = QIWIEdgeURL("locator/v3/nearest/clusters")
