# librerie

import os
import logging
import time
import openai
from dotenv import load_dotenv
from openai.types.chat import ChatCompletionMessageParam

# funzioni


def chiama_con_retry_e_fallback(client, modello, messaggi, tentativi_massimi=3):
    for tentativo in range(1, tentativi_massimi + 1):
        try:
            logger.info(
                f"Tentativo {tentativo}/{tentativi_massimi} - invio richiesta al modello '{modello}' ({len(messaggi)} messaggi in cronologia)"
            )
            risposta = client.chat.completions.create(
                model=modello,
                messages=messaggi,
                temperature=0,
                # timeout=0.001,  # per testare il retry, timeout molto basso
            )
            if risposta.usage is not None:
                logger.info(
                    f"Risposta ricevuta - token usati: {risposta.usage.total_tokens} "
                    f"(prompt: {risposta.usage.prompt_tokens}, completion: {risposta.usage.completion_tokens})"
                )
            else:
                logger.info(
                    "Risposta ricevuta - i dati sui token non sono disponibili."
                )
            logger.info(f"Successo al tentativo {tentativo}")
            messaggi.append(
                {"role": "assistant", "content": risposta.choices[0].message.content}
            )
            return risposta.choices[0].message.content

        except (
            openai.RateLimitError,
            openai.APITimeoutError,
            openai.APIConnectionError,
            openai.InternalServerError,
        ) as e:
            if tentativo == tentativi_massimi:
                logger.error(f"Falliti tutti i {tentativi_massimi} tentativi: {e}")
                raise
            attesa = 2 ** (tentativo - 1)
            logger.warning(f"retry: Errore transitorio ({e}), riprovo tra {attesa}s")
            time.sleep(attesa)
        except (
            openai.AuthenticationError,
            openai.NotFoundError,
            openai.BadRequestError,
        ) as e:
            logger.error(f"Errore permanente, non ritento: {e}")
            raise
        except Exception as e:
            logger.error(
                f"fallback(rete di sicurezza finale):Errore imprevisto o non gestito durante la chiamata: {e}",
            )
            raise


# logica di esecuzione

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

load_dotenv()

client = openai.OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

modello = "gemini-3-flash-preview"

messaggi: list[ChatCompletionMessageParam] = [
    {"role": "system", "content": "Sei un assistente utile e conciso."},
    {"role": "user", "content": "dimmi un numero casuale tra 1 e 100."},
]

print(
    "Turno 1:",
    chiama_con_retry_e_fallback(client, modello, messaggi, tentativi_massimi=3),
)

messaggi.append({"role": "user", "content": "che numero casuale mi hai detto?"})

print(
    "Turno 2:",
    chiama_con_retry_e_fallback(client, modello, messaggi, tentativi_massimi=3),
)
