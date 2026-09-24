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

# creo un client per interagire con l'API di google
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

# decido quale modello usare
modello = (
    "gemini-3-flash-preview"  # controlla su google ai studio i nomi modello disponibili
)
# creo una lista a turni della conversazione: role (chi sta "parlando": system per le istruzioni di comportamento, user per l'input dell'utente) e content (il testo vero e proprio)
messaggi: list[ChatCompletionMessageParam] = [
    {"role": "system", "content": "Sei un assistente utile e conciso."},
    {"role": "user", "content": "dimmi un numero casuale tra 1 e 100."},
]
try:
    logger.info(
        f"Invio richiesta al modello '{modello}' ({len(messaggi)} messaggi in cronologia)"
    )  # conoscere i messaggi in cronologia mi fa capire se il context window si sta riempiendo
    # invio le richieste al modello voluto
    risposta1 = client.chat.completions.create(
        model=modello,
        messages=messaggi,
        temperature=0,
    )
    if risposta1.usage is not None:
        logger.info(
            f"Risposta ricevuta - token usati: {risposta1.usage.total_tokens} "
            f"(prompt: {risposta1.usage.prompt_tokens}, completion: {risposta1.usage.completion_tokens})"
        )
    else:
        logger.info("Risposta ricevuta - i dati sui token non sono disponibili.")
except Exception as e:
    logger.error(f"Errore durante la chiamata al modello: {e}")
    raise
# contiene la prima risposta del modello, quella in posizione [0], potrei richiedere risposte diverse alla stessa domanda
print("Turno 1:", risposta1.choices[0].message.content)

# Aggiungiamo la risposta del modello alla cronologia(cioè aggiorno il contesto del modello)
messaggi.append({"role": "assistant", "content": risposta1.choices[0].message.content})

# preparo il nuovo turno dell'utente aggiornando il messaggio contenente il contesto della conversazione
messaggi.append(
    {"role": "user", "content": "che numero casuale mi hai detto?"}
)  # commentando questa riga il modello non ricorda il numero che mi aveva detto, la memoria dei modelli devo gestirla io tramite script
try:
    logger.info(
        f"Invio richiesta al modello '{modello}' ({len(messaggi)} messaggi in cronologia)"
    )
    # invio la seconda richiesta al modello contenente tutto il contesto della conversazione (ciò che ha detto l' utente + ciò che ha detto il modello)
    risposta2 = client.chat.completions.create(
        model=modello,
        messages=messaggi,
        temperature=0,  # 0=più preciso, 1=più creativo
    )
    if risposta2.usage is not None:
        logger.info(
            f"Risposta ricevuta - token usati: {risposta2.usage.total_tokens} "
            f"(prompt: {risposta2.usage.prompt_tokens}, completion: {risposta2.usage.completion_tokens})"
        )
    else:
        logger.info("Risposta ricevuta - i dati sui token non sono disponibili.")
except Exception as e:
    logger.error(f"Errore durante la chiamata al modello: {e}")
    raise
print("Turno 2:", risposta2.choices[0].message.content)
