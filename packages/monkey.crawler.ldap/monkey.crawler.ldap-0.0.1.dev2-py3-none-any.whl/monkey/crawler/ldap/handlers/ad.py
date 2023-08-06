from enum import Enum
from collections import namedtuple

from monkey.crawler.op_codes import OpCode
from monkey.crawler.processor import Handler


class UACFlagTuple(namedtuple('UACFlag', ['name', 'value'])):

    def __str__(self):
        return f'{self.name}: {self.value}'


class UACFlag(Enum):
    # TODO: Voir IntEnum ou IntFlag -> https://docs.python.org/3/library/enum.html
    SCRIPT = UACFlagTuple('SCRIPT', 1)
    ACCOUNT_DISABLE = UACFlagTuple('ACCOUNTDISABLE', 2)
    HOMEDIR_REQUIRED = UACFlagTuple('HOMEDIR_REQUIRED', 8)
    LOCKOUT = UACFlagTuple('LOCKOUT', 16)
    PASSWORD_NOT_REQUIRED = UACFlagTuple('PASSWD_NOTREQD', 32)
    PASSWORD_CANT_CHANGE = UACFlagTuple('PASSWD_CANT_CHANGE', 64)
    ENCRYPTED_TEXT_PWD_ALLOWED = UACFlagTuple('ENCRYPTED_TEXT_PWD_ALLOWED', 128)
    TEMP_DUPLICATE_ACCOUNT = UACFlagTuple('TEMP_DUPLICATE_ACCOUNT', 256)
    NORMAL_ACCOUNT = UACFlagTuple('NORMAL_ACCOUNT', 512)
    INTER_DOMAIN_TRUST_ACCOUNT = UACFlagTuple('INTERDOMAIN_TRUST_ACCOUNT', 2048)
    WORKSTATION_TRUST_ACCOUNT = UACFlagTuple('WORKSTATION_TRUST_ACCOUNT', 4096)
    SERVER_TRUST_ACCOUNT = UACFlagTuple('SERVER_TRUST_ACCOUNT', 8192)
    DONT_EXPIRE_PASSWORD = UACFlagTuple('DONT_EXPIRE_PASSWORD', 65536)
    MNS_LOGON_ACCOUNT = UACFlagTuple('MNS_LOGON_ACCOUNT', 131072)
    SMART_CARD_REQUIRED = UACFlagTuple('SMARTCARD_REQUIRED', 262144)
    TRUSTED_FOR_DELEGATION = UACFlagTuple('TRUSTED_FOR_DELEGATION', 524288)
    NOT_DELEGATED = UACFlagTuple('NOT_DELEGATED', 1048576)
    USE_DES_KEY_ONLY = UACFlagTuple('USE_DES_KEY_ONLY', 2097152)
    DONT_REQ_PRE_AUTH = UACFlagTuple('DONT_REQ_PREAUTH', 4194304)
    PASSWORD_EXPIRED = UACFlagTuple('PASSWORD_EXPIRED', 8388608)
    TRUSTED_TO_AUTH_FOR_DELEGATION = UACFlagTuple('TRUSTED_TO_AUTH_FOR_DELEGATION', 16777216)
    PARTIAL_SECRETS_ACCOUNT = UACFlagTuple('PARTIAL_SECRETS_ACCOUNT', 67108864)

    def get_value(self):
        return self.value.value

    def __str__(self):
        return str(self.value)


class UserAccountControlHandler(Handler):
    USER_ACCOUNT_CONTROL = 'userAccountControl'

    def __init__(self, attr_name: str = USER_ACCOUNT_CONTROL):
        """Initializes the handler.
        :param attr_name: the name of the attribute that contains user account control flags
        """
        super().__init__()
        self.attr_name = attr_name


class UACFilter(UserAccountControlHandler):
    def __init__(self, attr_name: str = UserAccountControlHandler.USER_ACCOUNT_CONTROL, flag_filter: int = 0,
                 match_op_code=None, no_match_op_code=OpCode.IGNORE):
        """Initializes the handler.
        :param attr_name: the name of the attribute that contains user account control flags
        :param flag_filter: the value used to filter the UAC flags
        :param match_op_code: the operation code to return if the UAC matches the filter
        :param no_match_op_code: the operation code to return if the UAC does not match the filter
        """
        super().__init__(attr_name)
        self.flag_filter = flag_filter
        self.match_op_code = OpCode[match_op_code] if isinstance(match_op_code, str) else match_op_code
        self.no_match_op_code = OpCode[no_match_op_code] if isinstance(no_match_op_code, str) else no_match_op_code

    def handle(self, record: dict, op_code: OpCode = None) -> (dict, OpCode):
        """Performs the filtering operation.
        :param record: the record to validate
        :param op_code: the operation code computed by any previous operation
        :return: a copy of the provided record
        :return: the provided operation code if the UAC flags match teh filter value or IGNORE if not.
        """
        user_account_control: int = record.get(self.attr_name, 0)
        if (user_account_control & self.flag_filter) == self.flag_filter:
            op_code = op_code if self.match_op_code is None else self.match_op_code
        else:
            op_code = op_code if self.no_match_op_code is None else self.no_match_op_code
        return record, op_code


class UACFlagHandler(UserAccountControlHandler):
    """Converts the Active Directory UserAccountControl flags into a dict of boolean named values.
    See: 'Use the UserAccountControl flags to manipulate user account properties <https://docs.microsoft.com/en-us/troubleshoot/windows-server/identity/useraccountcontrol-manipulate-account-properties>'_
    """

    def __init__(self, attr_name: str = UserAccountControlHandler.USER_ACCOUNT_CONTROL, keep_original_attr: bool = True,
                 true_flag_only: bool = True, wrapper_field: str = None):
        """Initializes the handler.
        :param attr_name: the name of the attribute that contains user account control flags
        :param keep_original_attr: indicates if the original UserAccountControl attributes within the record after conversion
        :param true_flag_only: indicates if new record includes only true flags or not.
        :param wrapper_field: the name of the field that wraps the UAC flags in the handled record. If None, flag fields won't be wrapped.
        """
        super().__init__(attr_name)
        self.keep_original_attr = keep_original_attr
        self.true_flag_only = true_flag_only
        self.wrapper_field = wrapper_field

    def handle(self, record: dict, op_code: OpCode = None) -> (dict, OpCode):
        """Performs the conversion operation and store the value in a copy of the provided record.
        :param record: the record to validate
        :param op_code: the operation code computed by any previous operation
        :return: a copy of the provided record that contains the UAC flags as separate field
        :return: the provided operation code
        """
        uac_flags = {}
        user_account_control: int = record.get(self.attr_name, 0)
        for flag in UACFlag:
            val = flag.get_value()
            uac_flags[flag.name] = (val & user_account_control) == val
        if self.true_flag_only:
            uac_flags = dict(filter(lambda elem: elem[1] is True, uac_flags.items()))
        rec = record.copy()
        if self.wrapper_field is None:
            rec.update(uac_flags)
        else:
            rec[self.wrapper_field] = uac_flags
        if not self.keep_original_attr:
            del rec[self.attr_name]
        return rec, op_code
