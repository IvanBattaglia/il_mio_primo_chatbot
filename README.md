# IL_MIO_PRIMO_CHATBOT_V1:

Chatbot da riga di comando che comunica con LLM tramite endpoint compatibili OpenAI (Ollama locale, Groq, Google Gemini), con gestione di errori, retry con backoff esponenziale, logging e streaming della risposta.

## Caratteristiche

- Compatibile con qualsiasi provider che espone un endpoint OpenAI-style (Ollama, Groq, Gemini, OpenAI stesso)
- Retry automatico con backoff esponenziale sugli errori transitori (rate limit, timeout, errori di rete)
- Distinzione tra errori transitori (da ritentare) e permanenti (da segnalare subito)
- Streaming della risposta in tempo reale
- Logging di richieste, risposte, token usati ed errori
- Gestione delle credenziali tramite `.env`

## Installazione

```bash

git clone https://github.com/IvanBattaglia/il_mio_primo_chatbot.git
cd il_mio_primo_chatbot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
cp .env.example .env #cmd: copy .env.example .env ;powershell: Copy-Item .env.example .env
# Poi apri .env e inserisci le tue chiavi nei campi GROQ_API_KEY e GOOGLE_API_KEY (opzionali se usi solo Ollama)

```

## Utilizzo

Apri `src/main.py`, apri `main.py`, scegli il provider copiando il blocco corrispondente (Ollama, Groq o Gemini), Per Ollama serve prima scaricare un modello, ad esempio qwen3.5:9b:
`ollama pull qwen3.5:9b`
poi lancia:
`python src/main.py`

#### ricorda che i nomi dei modelli cambiano nel tempo, cerca i modelli più recenti nei siti ufficiali di Ollama, Groq e Gemini

### modifiche di main.py se usi Ollama in locale (nessuna chiave richiesta):

```python

client = openai.OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)
modello = "qwen3.5:9b"

```

### modifiche di main.py se usi Groq:

```python

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
)
modello = "openai/gpt-oss-120b"

```

### modifiche di main.py se usi Gemini:

```python

client = openai.OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GOOGLE_API_KEY"),
)
modello = "gemini-3-flash-preview"

```

## Cosa ho imparato in questo progetto

- Gestione di un progetto Python con git e github (venv, `.gitignore`, `requirements.txt`)
- Come funzionano token, context window e temperature
- Perché e come implementare retry con backoff esponenziale
- Streaming di risposte LLM
- Gestione sicura di credenziali API