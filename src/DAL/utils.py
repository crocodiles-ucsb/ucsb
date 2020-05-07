from io import StringIO

from src.database.user_roles import UserRole
from src.models import OutUser


def get_url_postfix(user: OutUser) -> str:
    res = StringIO()
    res.write('/')
    if user.type == UserRole.SECURITY.value:
        res.write(user.type[:-1])
        res.write('ies')
    else:
        res.write(user.type)
        res.write('s')
    res.write('/')
    res.write(str(user.id))
    '''
        Для текущих ролей подойдет текущая простая функция, для будущих наверно надо придумать что-то лучше
    '''
    return res.getvalue()
