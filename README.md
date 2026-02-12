# Enkelversion av RAGbot

Avskalad RAG som bara gör: webbsök (Google CSE), extraktion (trafilatura), embeddings (Bedrock Titan), Qdrantsök, kort svar (OpenAI gpt-4o-mini). Ingen caching, inga citat, inga bilder, ingen frontend utöver Streamlit.

## Setup
1. Skapa `.env` i samma mapp:
   ```
   OPENAI_API_KEY=...
   GOOGLE_API_KEY=...
   GOOGLE_CSE_ID=...
   QDRANT_HOST=localhost
   QDRANT_PORT=6333
   AWS_ACCESS_KEY=...
   AWS_SECRET_KEY=...
   AWS_REGION=eu-north-1
   QDRANT_COLLECTION=enkel_rag
   SEARCH_LIMIT=3
   RAG_TOP_K=3
   ```
2. Starta Qdrant (exempelvis med Docker):
   ```bash
   docker run -d --name qdrant-simple -p 6333:6333 qdrant/qdrant:latest
   ```
3. Installera requirements och kör streamlit:
   ```bash
   pip install -r requirements.txt
   streamlit run streamlit_app.py --server.port 8501
   ```

## Filer
- `streamlit_app.py` – UI med en sökruta och svarsruta.
- `rag_pipeline.py` – sök, extraktion, embeddings, Qdrant, svar.
- `search_service.py` – Google CSE.
- `extractor.py` – enkel textextraktion.
- `embedding_service.py` – Bedrock Titan embeddings + chunks.
- `qdrant_service.py` – enkel Qdrant wrapper.
- `content_generator.py` – OpenAI svar angivet kontext.

## Praktisk användning
Liknar ett förenklat Perplexity flöde: hämtar några källor, sammanfattar med kontext, svarar kort. Passar små interna kunskapsbaser där man behöver mer precision änn ren LLM chatt men utan tunga systemkrav.

### Utmaningar
- Beror på externa API:er (CSE, OpenAI, Bedrock); kostnad och rate limits kan slå ut svar.
- Qdrant måste vara uppe annars faller retrieval.
- Ingen citat- eller källvalidering, så svar kan vara svåra att verifiera.
- Ingen cache vilket medför fler API anrop och högre latency.

### Möjligheter
- Byt embeddings till lokalt (t.ex. sentence-transformers) för lägre kostnad.
- Lägg till citationspipeline när man behöver källkritik.
- Lägg till cache (Redis) om mandu vill sänka latency och kostnad.
