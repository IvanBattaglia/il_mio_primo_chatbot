import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
import logging

logging.basicConfig(
    level=logging.INFO,  # gerarchia: DEBUG < INFO < WARNING < ERROR < CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


load_dotenv()  # load_dotenv() cerca automaticamente un file .env nella cartella corrente (o nelle cartelle superiori), lo legge e carica ogni riga come variabile d'ambiente, os.getenv("NOME_VARIABILE") la legge da dentro Python, restituendo None se non esiste

# creo un client per interagire con l'API di Ollama in locale
client = OpenAI(
    base_url="http://localhost:11434/v1",  # Quando Ollama è in esecuzione, espone automaticamente un server web locale sulla porta 11434
    api_key="ollama",  # valore fittizio, Ollama non lo controlla (è obbligatorio inserire un API key, ma ollama che lavora in locale non lo controlla)
)
# Esempio di come leggeresti una chiave vera, quando ne avrai una:
# groq_key = os.getenv("GROQ_API_KEY")


# creo una lista a turni della conversazione: role (chi sta "parlando": system per le istruzioni di comportamento, user per l'input dell'utente) e content (il testo vero e proprio)
messaggi: list[ChatCompletionMessageParam] = [
    {"role": "system", "content": "Sei un assistente utile e conciso."},
    {"role": "user", "content": "dimmi un numero casuale tra 1 e 100."},
]
logger.info("Invio richiesta al modello...")
# invio le richieste al modello voluto
risposta1 = client.chat.completions.create(
    model="qwen3.5:9b",  # deve corrispondere a un modello che hai scaricato su ollama
    messages=messaggi,
    temperature=0,
)
logger.info("Risposta ricevuta correttamente")
# contiene la prima risposta del modello, quella in posizione [0], potrei richiedere risposte diverse alla stessa domanda
print("Turno 1:", risposta1.choices[0].message.content)

# Aggiungiamo la risposta del modello alla cronologia(cioè aggiorno il contesto del modello)
messaggi.append({"role": "assistant", "content": risposta1.choices[0].message.content})

# preparo il nuovo turno dell'utente aggiornando il messaggio contenente il contesto della conversazione
messaggi.append(
    {"role": "user", "content": "che numero casuale mi hai detto?"}
)  # commentando questa riga il modello non ricorda il numero che mi aveva detto, la memoria dei modelli devo gestirla io tramite script
logger.info("Invio richiesta al modello...")
# invio la seconda richiesta al modello contenente tutto il contesto della conversazione (ciò che ha detto l' utente + ciò che ha detto il modello)
risposta2 = client.chat.completions.create(
    model="qwen3.5:9b",
    messages=messaggi,
    temperature=0,  # 0=più preciso, 1=più creativo
)
logger.info("Risposta ricevuta correttamente")
print("Turno 2:", risposta2.choices[0].message.content)


logger.info("Token usati per la richiesta 1 e la risposta 1:")
logger.info(
    risposta1.usage
)  # sostituisco i print() con logger.info() per avere un log più leggibile e utile in caso di debug

logger.info("Token usati per la richiesta 2 e la risposta 2:")
logger.info(risposta2.usage)
