# Intelligent-Warehouse-Inventory-Application
This project implements a warehouse inventory assistance system aimed at improving stock visibility and operational efficiency. The application supports inventory tracking, product management, stock updates, and analytical reporting. Designed with scalability in mind, it enables data-driven warehouse decision-making and workflow optimization.


🏭 **Warehouse AI Assistant Dashboard**

An AI-powered Warehouse Inventory Assistance System built using
**Streamlit, Ollama (Gemma3), ChromaDB, and LangChain**.\
This project implements a Retrieval-Augmented Generation (RAG) pipeline
to provide accurate, data-driven answers based strictly on warehouse
inventory records.

------------------------------------------------------------------------

🚀 **Features**

-   📊 Interactive Streamlit dashboard
-   📁 CSV / Excel inventory upload support
-   🧠 RAG-based AI assistant (Chroma + Ollama)
-   🔎 Top-K semantic retrieval (k=10)
-   📈 Inventory visualization with Plotly
-   📦 Product lookup & stock monitoring
-   ⚠ Reorder-level analysis
-   💬 Conversational warehouse assistant

------------------------------------------------------------------------

🏗 **Architecture**

User Query\
→ Retriever (ChromaDB)\
→ Relevant Inventory Records\
→ Ollama LLM (Gemma3)\
→ Context-Aware Response

**Tech Stack**

-   Frontend: Streamlit\
-   LLM: Ollama (gemma3:latest)\
-   Embeddings: mxbai-embed-large\
-   Vector Database: ChromaDB\
-   Framework: LangChain\
-   Visualization: Plotly\
-   Data Handling: Pandas

------------------------------------------------------------------------

📂 **Project Structure**

    ├── main1.py              # Streamlit Dashboard & Chat Interface
    ├── vector1.py            # CSV ingestion & Chroma vector setup
    ├── ML-Dataset.csv        # Warehouse inventory dataset
    ├── vector_store/         # Persistent Chroma database
    └── README.md

------------------------------------------------------------------------

⚙️ **Installation & Setup**

1️⃣ **Clone Repository**

    git clone https://github.com/your-username/warehouse-ai-assistant.git
    cd warehouse-ai-assistant

2️⃣ **Create Virtual Environment**

    python -m venv venv
    venv\Scripts\activate   # Windows

3️⃣ **Install Dependencies
**
    pip install -r requirements.txt

4️⃣ **Start Ollama Model**

    ollama run gemma3

5️⃣ **Ingest Dataset**

    python vector1.py

6️⃣ **Run Application**

    streamlit run main1.py

------------------------------------------------------------------------

🧪 **Evaluation Summary**

-   Retrieval: Top-K Semantic Search
-   Model Constraint: Uses only retrieved inventory records
-   Accuracy Score: \~90% (lookup & filter queries highly accurate)
-   Limitation: Aggregation queries require additional computation logic

------------------------------------------------------------------------

📊** Example Queries
**
-   What is the available quantity of ProductID 101?
-   Which products are below reorder level?
-   Who supplies Category Electronics?
-   Show warehouse location of Product XYZ.

------------------------------------------------------------------------

🔒 **System Constraints**

-   The assistant responds only using inventory data.
-   If data is unavailable, it returns: `"Data not available."`
-   No external knowledge is used.

------------------------------------------------------------------------

🎯** Use Cases**

-   Smart warehouse management
-   Inventory monitoring
-   Academic RAG demonstration project
-   AI-based decision support system

------------------------------------------------------------------------

📌 **Future Improvements**

-   Add numerical aggregation logic (SUM, COUNT)
-   Role-based access control
-   Real-time inventory API integration
-   Deployment via Docker / Cloud

------------------------------------------------------------------------

👨‍💻 **Author**

Warehouse AI Project -- LLM & SLM VAC

------------------------------------------------------------------------

📜 **License**

This project is for academic and educational purposes.
