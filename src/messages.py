from enum import Enum


class Message(Enum):
    LINK_INVALID_OR_OUTDATED = (
        'Ссылкой кто-то уже воспользовался или она не действительная'
    )
    USER_ALREADY_EXISTS = (
        'Пользователь с таким именем уже есть, выберите другое имя пользователя'
    )
    USER_DOES_NOT_EXISTS = 'User does not exists'
    COULD_NOT_VALIDATE_CREDENTIALS = 'Could not validate credentials'
    NOT_EXPECTING_PAYLOAD = 'Not expecting payload'
    ACCESS_TOKEN_OUTDATED = 'Access token outdated'
    INCORRECT_USERNAME_OR_PASSWORD = 'Incorrect username or password'
    INVALID_REFRESH_TOKEN = 'Invalid refresh token'
    INVALID_IMAGE = 'Invalid image'
    INCORRECTLY_MARKED_USERS = 'Nonexistent user is marked or one user repeated \
        multiple times or marked himself'
    POST_ACCEPTED_FOR_PROCESSING = 'Post accepted for processing'
    POST_READY = 'Post ready'
    POST_TASK_FALLEN = 'Post task fallen'
    ACCESS_FORBIDDEN = 'access_forbidden'
    BYTES_ARE_NOT_A_IMAGE = 'Bytes are not a image'
    INVALID_BASE64_PADDING = 'Invalid base64 padding'
    TASK_NOT_EXISTS = 'Task not exists'
    POST_NOT_EXISTS = 'Post not exists'
    POSTS_DO_NOT_EXIST = 'Posts do not exist'
    IMAGE_DOES_NOT_EXISTS_ON_STORAGE = 'Image does not exists on storage'
    USER_DOES_NOT_HAVE_IMAGES = 'User does not have images'
    USER_HAS_ALREADY_LIKE_THIS_POST = 'user has already like this post'
    USER_DID_NOT_LIKE_THIS_POST = 'User did not like this post'
    USER_CANNOT_SUBSCRIBE_ON_HIMSELF = 'User cannot subscribe on himself'
    USER_CANNOT_UNSUBSCRIBE_FROM_HIMSELF = 'User cannot unsubscribe from himself'
    USER_ALREADY_SUBSCRIBED_ON_THIS_USER = 'User already subscribed on this user'
    USER_NOT_SUBSCRIBED_ON_THIS_USER = 'User not subscribed on this user'
    INVALID_PAGINATION_PARAMS = 'Invalid page or size params'
    INVALID_PARAMS_FOR_GETTING_TOKEN = 'Endpoint needs login/password or refresh token'
    INVALID_CATALOG_VALUE = 'Неверное значение поля'
    ELEMENT_OF_CATALOG_ALREADY_EXISTS = 'Такой элемиент справочника уже существует'
    CATALOG_DOES_NOT_EXISTS = 'Такого каталога не существует, обновите страницу'
    PROFESSION_DOES_NOT_EXITS = 'Указанная профессия была удалена'
