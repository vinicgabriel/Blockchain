from stellar_sdk import Keypair, Network, Server, TransactionBuilder
import base64

# Defina o texto que será codificado e assinado
texto = "DEV30K"

# Gere um par de chaves (ou carregue um existente)
# Substitua pela sua chave privada (secret key) para a conta real
chave_privada = "SAYVMNCWNE2TC3TGUKVESXEQL34POVRE45ZSG3T7ATFZVYJXPN7ID5ZS"
keypair = Keypair.from_secret(chave_privada)

# Passo 1: Codifique "DEV30K" em base64
texto_codificado_base64 = base64.b64encode(texto.encode()).decode()

# Passo 2: Assine o texto codificado em base64
assinatura = keypair.sign(texto_codificado_base64.encode())

# Conectar ao servidor da Stellar testnet
server = Server("https://horizon-testnet.stellar.org")

# Carregar a conta usando a chave pública
chave_publica = keypair.public_key
conta = server.load_account(chave_publica)

# Criar a transação
transacao = (
    TransactionBuilder(
        source_account=conta,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100
    )
    .add_text_memo("DEV30K")  # Adiciona o MEMO como "DEV30K"
    .append_manage_data_op("desafio", assinatura)  # Adiciona a operação Manage Data com a assinatura sem base64 encoding extra
    .build()
)

# Assinar a transação
transacao.sign(keypair)

# Enviar a transação para o testnet da Stellar
try:
    resposta = server.submit_transaction(transacao)
    print("Hash da transação:", resposta["hash"])
    print("Link da transação:", resposta["_links"]["transaction"]["href"])
except Exception as e:
    print(f"Falha na transação: {e}")
