# Discord Bot com Remote Quick Command Stackspot

Este projeto é um bot do Discord que permite executar comandos remotos (Remote Quick Commands) e retornar os resultados diretamente no canal do Discord. O bot utiliza a API do StackSpot para executar comandos remotos e verificar o status de execução.

## Requisitos

- Python 3.8+
- Uma conta no Discord e um bot configurado
- Token de acesso do bot do Discord
- API de Remote Quick Command configurada no StackSpot
- Bibliotecas Python:
  - `discord.py`
  - `requests`
  - `python-dotenv` (opcional, para carregar variáveis de ambiente de um arquivo `.env`)

## Instalação

1. Clone o repositório:

````
$ git clone https://github.com/GhabryelHenrique/stk-discord.git
$ cd stk-discord
````
Crie um ambiente virtual (opcional, mas recomendado):



````
$ python -m venv venv
$ source venv/bin/activate  # No Windows use: venv\Scripts\activate
````

Instale as dependências:



````
$ pip install -r requirements.txt
````
Crie um arquivo .env na raiz do projeto e adicione as seguintes variáveis de ambiente:



````
DISCORD_TOKEN=seu_token_do_discord
REMOTE_QUICK_COMMAND_URL=https://genai-code-buddy-api.stackspot.com/v1/quick-commands/create-execution
CALLBACK_URL=https://genai-code-buddy-api.stackspot.com/v1/quick-commands/callback
GET_TOKEN_URL=https://idm.stackspot.com/stackspot-freemium/oidc/oauth/token
STK_CLIENT_ID=seu_client_id
STK_CLIENT_SECRET=seu_client_secret
SLUG=slug_do_comando_remoto
````

- **DISCORD_TOKEN**: O token do seu bot do Discord.
- **REMOTE_QUICK_COMMAND_URL**: A URL da API para executar o Remote Quick Command.
- **CALLBACK_URL**: A URL da API para verificar o status do comando.
- **GET_TOKEN_URL**: A URL para obter o token de acesso.
- **STK_CLIENT_ID**: O ID do cliente para autenticação na API.
- **STK_CLIENT_SECRET**: O segredo do cliente para autenticação na API.
- **SLUG**: O slug do comando remoto que você deseja executar.


## Como Executar
1. Certifique-se de que todas as variáveis de ambiente estão configuradas corretamente no arquivo .env

2. Execute o bot:

````
$ python bot.py
````

3. No Discord, envie uma mensagem no canal onde o bot está presente com o comando:

````
!quickcommand <prompt>
````

Substitua <prompt> pelo prompt que deseja enviar para o Remote Quick Command.

4. O bot irá executar o comando remoto e retornar o resultado no canal do Discord.

Exemplo de Uso
No Discord, envie a seguinte mensagem:



````
!quickcommand Como posso programar em Ruby?
````

O bot irá processar o comando e retornar o resultado da execução.

## Estrutura do Projeto


````
.
├── main.py              # Código principal do bot
├── requirements.txt    # Dependências do projeto
└── .env                # Arquivo de variáveis de ambiente (não incluído no repositório)
````

## Dependências
- **discord.py**: Biblioteca para interagir com a API do Discord.
- **requests**: Biblioteca para fazer requisições HTTP.
- **python-dotenv**: Biblioteca para carregar variáveis de ambiente de um arquivo .env.

### Logs
O bot utiliza o módulo logging para registrar informações sobre o status das operações. Os logs são exibidos no console e incluem informações sobre a execução dos comandos e possíveis erros.

## Contribuição
Sinta-se à vontade para abrir issues ou enviar pull requests para melhorias ou correções.

## Licença
Este projeto está licenciado sob a MIT License.