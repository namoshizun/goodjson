import uuid

from goodjson.validators import foreach, foreach_key, is_uuid, is_string
from goodjson.decorators import validator
from goodjson.errors import ErrorMessage


"""
You can build a custom validator function that takes any arbitrary value
and return a boolean value. Decorate your function with "validator" decorator
to make it compatible with goodjson. You will also need to define a custom ErrorMessage.


Say, we want to ensure that "contacts" list must not have duplicated "user_id".
"""

duplicate_contact_user = ErrorMessage(
    name='duplicate_contact_user',
    description='Duplicated contact user'
)


@validator(duplicate_contact_user)
def are_contact_users_unique(contacts_list):
    contacts_set = set([user['id'] for user in contacts_list])
    return len(contacts_set) == len(contacts_list)


validate_fn = foreach(
    foreach_key(
        id=[is_uuid],
        name=[is_string],
        contacts=[
            foreach(foreach_key(
                id=[is_uuid],
                name=[is_string]
            )),
            are_contact_users_unique
        ]
    )
)

USER_ID = str(uuid.uuid4())

print(validate_fn([{
    'id': USER_ID,
    'name': 'Foo Bar',
    'contacts': [{
        'id': str(uuid.uuid4()),
        'name': 'John Smith'
    }, {
        'id': str(uuid.uuid4()),
        'name': 'Foo Smith'
    }]
}]))
