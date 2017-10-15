# Замените user, password, example.com, database на ваши данные доступа к БД.
#MONGO_URI = "mongodb://user:password@example.com:27017/database"
MONGO_URI = "mongodb://admin1:admin1@ds117935.mlab.com:17935/testtask"

# По умолчанию Eve запускает API в режиме "read-only" (т.е. поддерживаются только GET запросы),
# мы включаем поддержку методов POST, PUT, PATCH, DELETE.
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

DOMAIN = {
    # Описываем ресурс `/users`
	'users': {
        'schema': {
            'username': {
                'type': 'string',
                'minlength': 5,
                'maxlength': 32,
                'required': True,
                # уникальное поле (индекс не создаётся, просто значение должно быть уникальным)
                'unique': True,
            },
            'password':{
                'type':'string',
                'minlength': 5,
                'required':True,

            },
            'firstname': {
                'type': 'string',
                'minlength': 1,
                'maxlength': 10,
                'required': True,
            },
            'lastname': {
                'type': 'string',
                'minlength': 1,
                'maxlength': 15,
                'required': True,
            },
            'balance': {
                'type': 'integer',
                #'allowed': ["author", "contributor"], # разрешаем использовать значения: "author", "contributor"
            },
            'operations': {
                'type': 'list', # тип: список
                'default': [], #по умолчанию пустой
                # описываем "схему"
                'schema': {
                    'type':'dict',
                    'schema':{
                        'host_account': {'type': 'string'}, #счет на который зачислятся деньги
                        'transmit_account': {'type': 'string'}, #счет с которого списываются деньги
                        'amount': {'type': 'integer'} #количество
                    },
                },
            },
        }
	}
}
