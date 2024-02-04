## API DE CADASTRO DE SITES PARA RESERVAS DE HOTEIS

Este documento explicita com exemplos, como utilizar os recursos disponíveis no REST API de Sites de Hotéis. Assim como, as formas de se realizar uma requisição e suas possíveis respostas.

#### 1. CONSULTAR HOTÉIS

Requisição para listar todos os hotéis do sistema, podendo opcionalmente receber filtros personalizados via path, de forma que se o cliente não definir nenhum parâmetro de consulta (nenhum filtro), os parâmetros receberão os valores padrão.

###### 1.1 Requisição

- Possíveis parâmetros de consulta
  - cidade ⇒ Filtrar hotéis pela cidade escolhida. Padrão: Nulo
  - estrela_min ⇒ Avaliações mínimas de hotéis de 0 a 5. Padrão: 0
  - estrela_max ⇒ Avaliações máximas de hotéis de 0 a 5. Padrão: 5
  - diaria_min ⇒ Valor mínimo da diária do hotel de R$ 0 a R$ 10.000,00. Padrão: 0
  - diaria_max ⇒ Valor máximo da diária do hotel de R$ 0 a R$ 10.000,00. Padrão: 10000
  - limit ⇒ Quantidade máxima de elementos exibidos por página. Padrão: 50
  - offset ⇒ Quantidade de elementos pular (geralmente múltiplo de limit). Padrão: 0

| Method | URL                                                       |
| ------ | :-------------------------------------------------------- |
| GET    | /hoteis?estrelas_min=4.5&limit=10&offset=0&diaria_max=600 |

###### 1.2 Resposta

Como resposta, obtém-se uma lista de hotéis que se enquadram nos filtros da requisição acima e código 200.</br>
![Alt text](/docs/image.png)

#### 2. CONSULTAR HOTEL

Requisição para visualizar os dados de um hotel específico.

###### 2.1 Requisição

| Method | URL          |
| ------ | :----------- |
| GET    | /hoteis/{id} |

###### 2.2 Resposta

Como resposta, obtém-se um JSON com os dados do hotel requisitado e código 200.</br>
![Alt text](/docs/image-1.png)

Quando o id não existe. Como resposta, obtém-se uma mensagem de erro, dizendo que o hotel não foi encontrado e código 404.

#### 3. CADASTRO DE USUÁRIO

###### 3.1 Requisição

Exemplo de Requisição cadastrar um novo usuário. </br>
| Method | URL |
| ------ | ----------- |
| POST | /cadastro |

---

| Header                         |
| ------------------------------ |
| Content-Type: application/json |

---

| Request Body                   |
| ------------------------------ |
| ![Alt text](/docs/image-3.png) |

###### 2.2 Resposta

Como resposta, obtém-se uma mensagem de sucesso informado que usuário foi criado, e código 201.

| Status      | Response Body                  |
| ----------- | ------------------------------ |
| 201 Created | ![Alt text](/docs/image-4.png) |

Quando o email já existe. Como resposta, obtém-se uma mensagem de erro, dizendo que o email já foi cadastrado, e código 404.

#### 4. ATIVAÇÃO DO USUÁRIO

O email cadastrado recebera um link para confirmar o cadastro. O serviço utilizado para o envio de email é a Twilio. É necessário criar um arquivo dotenv com as credenciais corretas para utilização do serviço da Twilio.

###### 4.1 Requisição

Exemplo de Requisição ativar um usuário. </br>
| Method | URL |
| ------ | ----------- |
| POST | /confirmacao/{id} |

###### 4.2 Resposta

Como resposta, obtém-se uma mensagem de sucesso informado que usuário foi ativado, e código 200.</br>
| Status | Response Body |
| ----------- | ------------------------ |
| 201 Created | ![Alt text](/docs/image-5.png) |

#### 5. LOGIN DO USUÁRIO

###### 5.1 Requisição

Exemplo de Requisição logar com um usuário. </br>
| Method | URL |
| ------ | ----------- |
| POST | /login |

---

| Header                         |
| ------------------------------ |
| Content-Type: application/json |

---

| Request Body                   |
| ------------------------------ |
| ![Alt text](/docs/image-6.png) |

###### 5.2 Resposta

Como resposta, obtém-se o token de acesso que será necessário para fazer as requisições que só podem ser feitas com login, e código 200.</br>

Ao informar um email ou senha inválidos, como resposta, obtém-se uma mensagem de erro de código 401 não autorizado, informando que usuário ou senha estão incorretos.

#### 6. CONSULTAR USUÁRIOS

###### 6.1 Requisição

Exemplo de Requisição para consultar usuários. </br>
| Method | URL |
| ------ | ----------- |
| GET | /usuarios |

---

| Header                          |
| ------------------------------- |
| Authorization: Bearer seu-token |

###### 6.2 Resposta

Como resposta, obtém-se uma lista de usuários, e código 200.</br>
| Status | Response Body |
| ----------- | ------------------------ |
| 200 | ![Alt text](/docs/image-7.png) |

#### 7. CONSULTAR USUÁRIO ESPECIFÍCO

###### 7.1 Requisição

Exemplo de Requisição para consultar um usuário. </br>
| Method | URL |
| ------ | ----------- |
| GET | /usuarios/{id} |

---

| Header                          |
| ------------------------------- |
| Authorization: Bearer seu-token |

---

###### 6.2 Resposta

Como resposta, obtém-se um usuário, e código 200.</br>
| Status | Response Body |
| ----------- | ------------------------ |
| 200 | ![Alt text](/docs/image-8.png) |

Quando o id não existe. Como resposta, obtém-se uma mensagem de erro, dizendo que o usuário não foi encontrado e código 404.

#### 8. EDITAR USUÁRIO

###### 8.1 Requisição

Exemplo de Requisição para editar um usuário. </br>
| Method | URL |
| ------ | ----------- |
| PUT | /usuarios/{id} |

---

| Header                          |
| ------------------------------- |
| Authorization: Bearer seu-token |

---

| Request Body                   |
| ------------------------------ |
| ![Alt text](/docs/image-9.png) |

###### 8.2 Resposta

Como resposta, obtém-se o usuário editado, e código 200.</br>
| Status | Response Body |
| ----------- | ------------------------ |
| 200 | ![Alt text](/docs/image-10.png) |

Quando o id não existe. Como resposta, obtém-se uma mensagem de erro, dizendo que o usuário não foi encontrado e código 404.

#### 9. DELETAR USUÁRIO

###### 9.1 Requisição

Exemplo de requisição para deletar um usuário. </br>
| Method | URL |
| ------ | ----------- |
| DELETE | /usuarios/{id} |

---

| Header                          |
| ------------------------------- |
| Authorization: Bearer seu-token |

###### 9.2 Resposta

Como resposta, obtém-se uma mensagem confirmando a exclusão do usuário, e código 200.</br>

| Status | Response Body                   |
| ------ | ------------------------------- |
| 200    | ![Alt text](/docs/image-11.png) |

Quando o id não existe. Como resposta, obtém-se uma mensagem de erro, dizendo que o usuário não foi encontrado e código 404.

#### 10. CONSULTAR SITES

###### 10.1 Requisição

Exemplo de Requisição para consultar sites. </br>
| Method | URL |
| ------ | ----------- |
| GET | /sites |

###### 10.2 Resposta

Como resposta, obtém-se uma lista de usuários, e código 200.</br>
| Status | Response Body |
| ----------- | ------------------------ |
| 200 | ![Alt text](/docs/image-12.png) |

#### 10. CADASTRAR UM SITE

###### 10.1 Requisição

Exemplo de Requisição para consultar um site. </br>
| Method | URL |
| ------ | ----------- |
| POST | /adicionar |

---

| Request Body                    |
| ------------------------------- |
| ![Alt text](/docs/image-13.png) |

###### 10.2 Resposta

Como resposta, obtém-se uma mensagem de sucesso informado que o site foi criado, e código 201.</br>

| Status | Response Body                   |
| ------ | ------------------------------- |
| 200    | ![Alt text](/docs/image-14.png) |

#### 11. EDITAR UM SITE

###### 11.1 Requisição

Exemplo de Requisição para consultar um site. </br>
| Method | URL |
| ------ | ----------- |
| PUT | /site/{nome} |

---

| Request Body                    |
| ------------------------------- |
| ![Alt text](/docs/image-13.png) |

###### 11.2 Resposta

Como resposta, obtém-se uma mensagem de sucesso informado que o site foi editado, e código 200.</br>

| Status | Response Body                   |
| ------ | ------------------------------- |
| 200    | ![Alt text](/docs/image-15.png) |

Quando o nome não existe. Como resposta, obtém-se uma mensagem de erro, dizendo que o site não foi encontrado e código 404.

#### 12. DELETAR UM SITE

###### 12.1 Requisição

Exemplo de requisição para deletar um site. </br>
| Method | URL |
| ------ | ----------- |
| DELETE | /site/{nome} |

###### 12.2 Resposta

Como resposta, obtém-se uma mensagem confirmando a exclusão do site, e código 200.</br>

| Status | Response Body                   |
| ------ | ------------------------------- |
| 200    | ![Alt text](/docs/image-16.png) |

Quando o nome não existe. Como resposta, obtém-se uma mensagem de erro, dizendo que o site não foi encontrado e código 404.

#### 13. CADASTRAR UM HOTEL

Para cadastrar um hotel é necessário ter cadastrado antes o site ao qual
ele pertence.

###### 13.1 Requisição

Exemplo de requisição para cirar um hotel. </br>

| Method | URL          |
| ------ | ------------ |
| POST   | /hoteis/{id} |

---

| Header                          |
| ------------------------------- |
| Authorization: Bearer seu-token |

---

| Request Body                    |
| ------------------------------- |
| ![Alt text](/docs/image-17.png) |

###### 13.2 Resposta

Como resposta, obtém-se uma mensagem de sucesso informado que o hotel foi criado, e código 201.</br>

| Status | Response Body                   |
| ------ | ------------------------------- |
| 200    | ![Alt text](/docs/image-18.png) |

#### 13. EDITAR UM HOTEL

###### 13.1 Requisição

Exemplo de requisição para editar um hotel. </br>

| Method | URL          |
| ------ | ------------ |
| PUT    | /hoteis/{id} |

---

| Header                          |
| ------------------------------- |
| Authorization: Bearer seu-token |

---

| Request Body                    |
| ------------------------------- |
| ![Alt text](/docs/image-19.png) |

###### 13.2 Resposta

Como resposta, obtém-se uma mensagem de sucesso informado que o hotel foi criado, e código 201.</br>

| Status | Response Body |
| ------ | ------------- |
| 200    | ---           |

Quando o id não existe. Como resposta, obtém-se uma mensagem de erro, dizendo que o hotel não foi encontrado e código 404.

#### 12. DELETAR UM HOTEL

###### 12.1 Requisição

Exemplo de requisição para deletar um hotel. </br>
| Method | URL |
| ------ | ----------- |
| DELETE | /hoteis/{id} |

---

| Header                          |
| ------------------------------- |
| Authorization: Bearer seu-token |

###### 12.2 Resposta

Como resposta, obtém-se uma mensagem confirmando a exclusão do hotel, e código 200.</br>

| Status | Response Body                   |
| ------ | ------------------------------- |
| 200    | ![Alt text](/docs/image-20.png) |

Quando o id não existe. Como resposta, obtém-se uma mensagem de erro, dizendo que o hotel não foi encontrado e código 404.
