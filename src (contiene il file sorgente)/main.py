from openai import OpenAI

# creo un client per interagire con l'API di Ollama in locale
client = OpenAI(
    base_url="http://localhost:11434/v1",  # Quando Ollama è in esecuzione, espone automaticamente un server web locale sulla porta 11434
    api_key="ollama",  # valore fittizio, Ollama non lo controlla (è obbligatorio inserire un API key, ma ollama che lavora in locale non lo controlla)
)
# invio le richieste al modello voluto
response = client.chat.completions.create(
    model="qwen3.5:9b",  # deve corrispondere a un modello che hai scaricato
    # creo una lista a turni della conversazione: role (chi sta "parlando": system per le istruzioni di comportamento, user per l'input dell'utente) e content (il testo vero e proprio)
    messages=[
        {"role": "system", "content": "Sei un assistente utile e conciso."},
        {
            "role": "user",
            "content": "Ciao! Dimmi in una frase cos'è un virtual environment in Python.",
        },
    ],
)
# contiene la prima risposta del modello, quella in posizione [0], potrei richiedere risposte diverse alla stessa domanda
print(response.choices[0].message.content)
