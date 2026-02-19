import os
import pandas as pd
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# ==================================================
# CONFIG (CHANGE ONLY THESE IF NEEDED)
# ==================================================
CSV_FILE = r"C:\LLM SLM VAC PG\ML-Dataset.csv"   # 🔁 your inventory CSV
DB_LOCATION = "./vector_store/inventory_db"
COLLECTION_NAME = "inventory_management_data"
EMBED_MODEL = "mxbai-embed-large"

# ==================================================
# GET RETRIEVER (USED BY STREAMLIT APP)
# ==================================================
def get_retriever():
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=DB_LOCATION,
        embedding_function=embeddings
    )

    # ⚠️ IMPORTANT: k is defined HERE, not during invoke()
    return vector_store.as_retriever(search_kwargs={"k": 10})


# ==================================================
# INGEST INVENTORY CSV INTO CHROMA
# ==================================================
def ingest_csv():
    print("🚀 Starting Inventory CSV ingestion...")

    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(f"❌ CSV file not found: {CSV_FILE}")

    df = pd.read_csv(CSV_FILE)
    print(f"📄 Rows found in CSV: {len(df)}")

    embeddings = OllamaEmbeddings(model=EMBED_MODEL)

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=DB_LOCATION,
        embedding_function=embeddings
    )

    # Prevent duplicate ingestion
    existing_count = vector_store._collection.count()
    if existing_count > 0:
        print(f"✅ Database already has {existing_count} records. Skipping ingestion.")
        return

    documents = []
    ids = []

    for idx, row in df.iterrows():
        content = (
            f"Product ID: {row.get('ProductID', idx)}. "
            f"Product Name: {row.get('ProductName', 'Unknown')}. "
            f"Category: {row.get('Category', 'General')}. "
            f"Available quantity is {row.get('Quantity', 'N/A')} units. "
            f"Reorder level is {row.get('ReorderLevel', 'N/A')} units. "
            f"Supplier: {row.get('Supplier', 'Unknown')}. "
            f"Unit price is {row.get('Price', 'N/A')} USD. "
            f"Warehouse location: {row.get('Warehouse', 'Main')}. "
            f"Last updated on {row.get('LastUpdated', 'Unknown')}."
        )

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "product_id": str(row.get("ProductID", idx)),
                    "category": str(row.get("Category", "General")),
                    "warehouse": str(row.get("Warehouse", "Main"))
                }
            )
        )

        ids.append(str(idx))

    vector_store.add_documents(documents=documents, ids=ids)
    vector_store.persist()

    print(f"🎉 Ingestion completed successfully!")
    print(f"📦 Total inventory records ingested: {len(documents)}")


# ==================================================
# RUN ONLY WHEN EXECUTED DIRECTLY
# ==================================================
if __name__ == "__main__":
    ingest_csv()
