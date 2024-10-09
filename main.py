import discord
import requests
import os
import time
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicialize o cliente do bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

SLUG = os.getenv("SLUG")

# Token do bot (substitua pelo seu token)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# URL do Remote Quick Command (substitua pela URL do seu comando)
REMOTE_QUICK_COMMAND_URL = os.getenv("REMOTE_QUICK_COMMAND_URL")
CALLBACK_URL = os.getenv("CALLBACK_URL")
GET_TOKEN_URL = os.getenv("GET_TOKEN_URL")

async def execute_remote_quick_command(selected_code):
    """
    Função para executar o Remote Quick Command.
    :param selected_code: Código selecionado pelo usuário.
    :return: ID da execução do comando remoto.
    """
    try:
        access_token = await getAccessToken()

        if not access_token:
            logger.error("Erro ao obter o token do Remote Quick Command")
            return None
        
        # Cabeçalhos para a requisição de execução do comando
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Corpo da requisição (exemplo de input_data)
        body = {
            "input_data": selected_code
        }
        
        # Faz a requisição POST para executar o comando
        response = requests.post(f'{REMOTE_QUICK_COMMAND_URL}/{SLUG}', json=body, headers=headers)
        
        # Verifica o status da resposta
        if response.status_code == 200:
            logger.info("Comando executado com sucesso")
            return response.json()
        else:
            logger.error(f"Erro ao executar o comando: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        logger.exception(f"Erro inesperado ao executar o comando: {e}")
        return None


async def execute_callback(execution_id, interval=5):
    """
    Função para verificar o status de execução de um comando remoto até que ele seja concluído.
    :param execution_id: ID da execução do comando remoto.
    :param interval: Intervalo de tempo (em segundos) entre as verificações de status.
    :return: O valor de steps[0].step_result.answer quando o status for 'COMPLETED'.
    """
    try:
        access_token = await getAccessToken()
        if not access_token:
            logger.error("Erro ao obter o token do Remote Quick Command")
            return None
        
        # URL do callback (substitua pela URL correta)
        callback_url = f"{CALLBACK_URL}/{execution_id}"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        while True:
            response = requests.get(callback_url, headers=headers)
            
            # Verifica o status da resposta
            if response.status_code == 200:
                data = response.json()
                status = data.get('progress', {}).get('status')
                
                if status == "COMPLETED":
                    # Retorna o valor de steps[0].step_result.answer
                    steps = data.get('steps', [])
                    if steps and 'step_result' in steps[0] and 'answer' in steps[0]['step_result']:
                        logger.info(f"Comando {execution_id} concluído com sucesso")
                        return steps[0]['step_result']['answer']
                    else:
                        logger.warning(f"Resposta não encontrada em steps[0].step_result.answer para {execution_id}")
                        return "Resposta não encontrada"
                else:
                    logger.info(f"[{execution_id}] - Status atual: {status}. Aguardando {interval} segundos para nova verificação...")
                    time.sleep(interval)  # Aguarda antes de verificar novamente
            else:
                logger.error(f"Erro ao executar o comando: {response.status_code}, {response.text}")
                return None
    except Exception as e:
        logger.exception(f"Erro inesperado ao verificar o status do comando: {e}")
        return None


async def getAccessToken():
    """
    Função para obter o token de acesso.
    :return: Token de acesso ou mensagem de erro.
    """
    try:        
        # Dados para a requisição (substitua pelos valores corretos)
        data = {
            'client_id': os.getenv("STK_CLIENT_ID"),
            'grant_type': 'client_credentials',
            'client_secret':  os.getenv("STK_CLIENT_SECRET")
        }
        
        # Cabeçalhos da requisição
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # Faz a requisição POST para obter o token
        response = requests.post("https://idm.stackspot.com/stackspot-freemium/oidc/oauth/token", data=data, headers=headers)

        if response.status_code == 200:
            logger.info("Token obtido com sucesso")
            return response.json().get("access_token", "Nenhum token recebido.")
        else:
            logger.error(f"Erro ao obter o token: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        logger.exception(f"Erro inesperado ao obter o token: {e}")
        return None


# Evento de inicialização do bot
@client.event
async def on_ready():
    logger.info(f'Bot conectado como {client.user}')


# Evento para responder a mensagens
@client.event
async def on_message(message):
    # Ignora mensagens do próprio bot
    if message.author == client.user:
        return

    # Comando para executar o Remote Quick Command
    if message.content.startswith('!quickcommand'):
        # Extrai o código enviado pelo usuário
        selected_code = message.content[len('!quickcommand '):].strip()

        if not selected_code:
            await message.channel.send("Por favor, forneça o código para o comando.")
            return

        # Executa o Remote Quick Command
        conversation_id = await execute_remote_quick_command(selected_code)

        if conversation_id:
            result = await execute_callback(conversation_id)
            # Envia a resposta de volta no canal do Discord
            await send_long_message(message.channel, f"Resultado do Quick Command:\n{result}")
        else:
            await message.channel.send("Erro ao executar o comando remoto.")

async def send_long_message(channel, content):
    # Limite de caracteres por mensagem no Discord
    limit = 2000

    # Se a mensagem for menor que o limite, envia diretamente
    if len(content) <= limit:
        await channel.send(content)
    else:
        # Divide a mensagem em partes sem cortar palavras
        parts = []
        while len(content) > limit:
            # Encontra o último espaço antes do limite
            split_index = content.rfind(' ', 0, limit)
            if split_index == -1:
                # Se não houver espaço, corta no limite exato
                split_index = limit
            parts.append(content[:split_index])
            content = content[split_index:].strip()

        # Adiciona a última parte
        parts.append(content)

        # Envia cada parte separadamente
        for part in parts:
            await channel.send(part)

# Inicia o bot
client.run(DISCORD_TOKEN)