# Static Pages Client

API Repository for Static Pages Client

## 📝 Installation

Install using your favourite package manager

```bash
pip install static_pages_client
```

## 📦️ Methods

| Name                              | Type      | Description                                       |
| --------------------------------- | --------- | --------------------------------------------------|
| set_host                          | function  | Set client host                                   |
| set_silent                        | function  | Silence errors                                    |
| set_api_key                       | function  | Set client api key                                |
| set_authorization                 | function  | Set client authorization token                    |
| make_application                  | function  | Create a static pages application                 |
| make_application_user             | function  | Create a static pages application user or users   |
| make_application_user_token       | function  | Create an application user authorization token    |
| requester                         | function  | Static api caller                                 |
| v1                                | function  | Exposes v1 caller api methods                     |
| v2                                | function  | Exposes v2 caller api method                      |

## 🔧 Usage

##### Init Static Client

```
static = StaticAPI(host='domain/api/')
```

##### Create Application

```
static.make_application()
```

``hash`` equals to `X-API-Key` header

##### Set Application Key

```
static.set_api_key(key='hash')
```

##### Create Application Users

```
static.make_application_user(users=[{
    'email': 'someone@ebs-integrator.com',
}])
```

##### Create Application User

```
static.make_application_user(user={
    'email': 'someone.else@ebs-integrator.com',
})
```

##### Create Application User Token

```
token = static.make_application_user_token(email='someone.else@ebs-integrator.com', secret='super')
```

Or use the `settings` property in application to setup `secret` and use tokens from your own `main service`

##### Set Authorization

```
static.set_authorization(token=token)
```

##### Make V1 Requests

```
static.v1(method='get', endpoint='article/')
```

##### Make V2 Requests

```
static.v2(method='post', endpoint='job/', data={'i18n': {'ro': {'title': 'Static'}}})
```