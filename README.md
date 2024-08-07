## Генерация jwt ключей
`openssl genrsa -out certs/jwt_private.pem 2048`

`openssl rsa -in certs/jwt_private.pem -outform PEM -pubout -out certs/jwt_public.pem`
