from enum import Enum


class UserRole(Enum):
    ADMIN = 'admin'
    OPERATOR = 'operator'
    SECURITY = 'security'
    CONTRACTOR_REPRESENTATIVE = 'contractor_representative'
