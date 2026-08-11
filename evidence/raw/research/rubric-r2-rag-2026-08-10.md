---
source: "Deep research R2 — Production RAG interview rubric (2026)"
added: 2026-08-10
---

# **Senior AI Engineer Interview Rubric: Production RAG Systems (2026)**

## **Ingestion / chunking / embeddings**

### **Comfortable bar**

A competent candidate demonstrates a solid understanding of semantic chunking over rigid character-count splitting, applying overlapping windows to preserve local context. The candidate successfully distinguishes between dense embeddings designed for semantic similarity and sparse embeddings (e.g., BM25, SPLADE) utilized for exact keyword matching1. The individual implements basic metadata tagging (such as timestamps, authorship, and document IDs) during the ingestion phase to support downstream hybrid search filtering. When processing complex PDFs, the candidate recognizes the limitations of standard OCR for tabular data, avoiding architectures that flatten columns into incoherent text strings.

### **Strong bar**

An expert candidate treats ingestion as a lossy data transformation step and proactively implements mitigation strategies. The individual architecturally defaults to Contextual Retrieval, leveraging a cost-effective language model to prepend global explanatory context to every isolated chunk before embedding generation2. The candidate significantly reduces the operational costs of this process by applying prompt caching to the source document3. Furthermore, the candidate advocates for multimodal ingestion pipelines, processing complex PDFs by routing tables and diagrams through vision-language models to extract Markdown or structured JSON, ensuring mathematical and relational integrity remains intact.

### **Symptom → technique decision table**

| Observed Symptom | Underlying Cause | Recommended Technique |
| :---- | :---- | :---- |
| Coreference resolution failure (e.g., "The company" instead of "ACME Corp") | Naive chunking severs entity names from their preceding descriptive context. | Contextual Retrieval (prepend document summary to chunks)3. |
| Dense retrieval misses specific SKUs or error codes | Vector embeddings flatten rare lexical tokens into generic spatial neighborhoods. | Hybrid Search utilizing sparse vectors (BM25 or SPLADE)1. |
| Tabular data retrieved but LLM misinterprets rows | Standard OCR flattens distinct table columns into unreadable text strings. | Vision-LLM pre-processing to convert tables directly into Markdown/HTML. |
| Ingestion pipeline costs scale exponentially | Repetitive LLM calls to generate contextual data for overlapping chunks. | LLM KV/Prompt Caching applied globally to the source document3. |

### **Probe questions (5)**

> 1. How does the architecture resolve dangling pronouns in a 200-token chunk when the subject was introduced five pages prior in the source material?  
> 2. What specific embedding model architectures are selected for multilingual queries versus domain-specific (e.g., biomedical) corpora?  
> 3. How is tabular data within financial PDFs extracted, embedded, and preserved to ensure mathematical relationships remain intact during generation?  
> 4. What is the estimated operational cost per million tokens to process documents using contextual enrichment, and how is it computationally optimized?  
> 5. In a highly volatile dataset where documents are updated daily, how does the system manage chunk invalidation and sparse/dense embedding updates?

### **Metric / design pitfalls**

A common failure mode is assuming that large chunk overlap solves context loss; instead, it merely bloats the index while frequently splitting critical sentences and diluting retrieval precision. Another critical pitfall is mixing embedding models (e.g., Cohere and OpenAI) within the same vector collection, which mathematically breaks vector similarity operations7.

### **Anti-goals**

* Developing custom PDF parsers from scratch instead of utilizing mature libraries or specialized API services.  
* Over-engineering dynamic chunking algorithms for datasets under 100,000 tokens where full-context prompting is cheaper, faster, and more effective3.

## **Vector indexes & hybrid search**

### **Comfortable bar**

The candidate can clearly articulate the mechanical differences between brute-force (Flat) search, Inverted File Index (IVF), and Hierarchical Navigable Small World (HNSW) graphs. The individual successfully implements hybrid search by merging dense vector similarities with BM25 keyword scores using Reciprocal Rank Fusion (RRF)8. The candidate understands the basic tradeoff between search recall and latency when querying approximate nearest neighbor (ANN) indexes.

### **Strong bar**

A senior engineer deeply understands the HNSW memory/latency/recall tradeoff space and tunes index parameters (M, efConstruction, efSearch) dynamically based on production workloads9. The candidate diagnoses the failure modes of metadata filtering—specifically how naive post-filtering destroys recall by discarding matches after nearest neighbors are computed11. The expert advocates for single-pass payload filtering (e.g., Qdrant's filterable HNSW) or iterative index scans (e.g., pgvector 0.8+) for highly selective queries12. The candidate actively utilizes scalar or binary quantization to compress memory footprints by up to 32x while mitigating the resulting recall loss via second-stage reranking7.

### **Symptom → technique decision table**

| Observed Symptom | Underlying Cause | Recommended Technique |
| :---- | :---- | :---- |
| Strict metadata filter returns zero results, despite matches existing | Naive post-filtering drops valid candidates that lay outside the initially retrieved top-K vectors11. | Filter-aware index traversal (filterable HNSW) or strict Pre-filtering11. |
| HNSW index exhausts available RAM | float32 vectors scale linearly; 1M vectors consume \~6GB memory11. | Scalar (int8) or Binary quantization11. |
| Recall degrades rapidly under high concurrency | efSearch parameter is set too low relative to the requested k value. | Ensure efSearch is scaled proportionally, ideally \>= 2x k10. |
| High insertion latency during batch updates | High efConstruction and M values cause heavy graph rewiring operations. | Lower graph density or utilize a tiered index (DiskANN / IVF-HNSW)10. |

### **Probe questions (5)**

> 1. When configuring an HNSW index, how do the M and efConstruction parameters dictate the specific tradeoff between build time and query recall?  
> 2. If a query requires filtering down to 0.1% of the corpus, explain why standard vector search followed by post-filtering will likely fail to return complete results.  
> 3. How does the system handle ranking convergence when combining sparse and dense scores of vastly different mathematical distributions via RRF?  
> 4. What is the mathematical impact of normalizing vectors to unit length before executing dot product versus cosine similarity searches?  
> 5. Under what exact data volume or latency constraints does the architecture abandon RAM-based HNSW for DiskANN or disk-backed index variants?

### **Metric / design pitfalls**

A fatal production error is querying an HNSW index with an efSearch parameter lower than the requested top k results, guaranteeing suboptimal recall and rendering the ANN graph ineffective10. Additionally, relying on public vector database benchmarks without testing the exact metadata filtering selectivity of the specific production workload leads to severe architectural missteps7.

### **Anti-goals**

* Defaulting to complex distributed vector databases for datasets under 5 million vectors where local or PostgreSQL-native extensions (pgvector) easily suffice7.  
* Writing custom indexing algorithms instead of tuning established libraries (e.g., FAISS).

## **RAG evaluation**

### **Comfortable bar**

The candidate rejects "vibes-based" evaluation and implements a deterministic, automated testing pipeline. The individual categorizes metrics into retrieval quality (Context Precision, Context Recall, MRR, nDCG) and generation quality (Faithfulness, Answer Relevancy) using established frameworks such as RAGAS, DeepEval, or TruLens14. The candidate understands that a faithful response might still fail to answer the user's actual question, necessitating separate measurements for groundedness and relevancy15.

### **Strong bar**

The expert candidate anticipates and rigorously mitigates LLM-as-judge biases. The individual explicitly controls for positional bias (the model favoring the first response) by running bidirectional pairwise swaps, and verbosity bias (the model rewarding length over correctness) by utilizing decomposed, dimension-specific rubrics rather than holistic scores18. The candidate implements synthetic test data generation to ensure continuous coverage and routinely measures the "Precision Gap"—the delta between the first-stage retriever's top-K and the true top-K21.

### **Symptom → technique decision table**

| Observed Symptom | Underlying Cause | Recommended Technique |
| :---- | :---- | :---- |
| Generated answer contradicts the retrieved chunks | The generation model hallucinates independent world knowledge over provided context. | Gating deployments on Faithfulness / Response Groundedness metrics14. |
| Accurate, well-cited response does not answer the user's prompt | The model generated a technically correct summary of irrelevant retrieved chunks. | Gating on Answer Relevancy / Response Relevancy metrics15. |
| LLM-as-judge consistently scores "Model A" higher than "Model B" | Positional bias; the judge inherently favors the first presented option18. | Swap evaluation order and measure winner agreement20. |
| Verbose, unhelpful responses achieve high evaluation scores | Verbosity bias; LLM judges equate response length with response quality18. | Implement length-normalized scoring or discrete 4-dimension rubrics20. |

### **Probe questions (5)**

> 1. How does the evaluation pipeline programmatically differentiate between a hallucinated fact and a valid synthesis of external knowledge?  
> 2. Explain the mechanism by which Context Recall calculates False Negatives when evaluating the effectiveness of a retriever.  
> 3. How are LLM-as-judge prompts engineered to eliminate verbosity bias when comparing a concise correct answer against a lengthy partially correct one?  
> 4. What statistical methods are used to determine if an observed 0.05 nDCG improvement is genuine or merely an artifact of self-preference bias?  
> 5. How is "context rot" (the loss of LLM attention on middle chunks) explicitly tested in the evaluation suite?

### **Metric / design pitfalls**

Using a single holistic LLM-as-judge prompt to score a response from 1 to 10 conflates surface fluency with information density, allowing verbose hallucinations to pass as high-quality outputs20. Furthermore, evaluating Faithfulness alone is a trap; a perfectly faithful summary of irrelevant documents lets user-facing errors bypass the deployment gate entirely15.

### **Anti-goals**

* Utilizing exact-match metrics (e.g., BLEU, ROUGE) to evaluate semantic generative tasks, which penalize valid paraphrasing25.  
* Assuming a proprietary LLM-as-judge correlates 1:1 with human domain experts without continually cross-validating a sample set24.

## **Advanced RAG pattern selection**

### **Comfortable bar**

The candidate understands that naive bi-encoder retrieval lacks precision. The individual successfully integrates a cross-encoder reranking stage to score the joint interaction between query and document tokens, moving the most relevant contexts into high-attention prompt positions21. The candidate recognizes when to utilize basic query rewriting to resolve conversational ambiguities before executing a retrieval pass.

### **Strong bar**

The senior candidate matches highly specialized architectural patterns to precise failure domains. To circumvent the high latency of full cross-encoders, the candidate deploys late-interaction models (e.g., ColBERT) for sub-100ms precise token-level matching at scale5. The candidate employs Adaptive RAG to route queries based on complexity, utilizing CRAG (Corrective RAG) for fallback web searches when internal knowledge fails, and Self-RAG for internal reflection and generation gating28. For queries requiring global corpus summarization, the individual correctly discards standard vector search in favor of GraphRAG (entity-relation traversal) or RAPTOR (hierarchical tree summarization)28.

### **Symptom → technique decision table**

| Observed Symptom | Underlying Cause | Recommended Technique |
| :---- | :---- | :---- |
| High recall but poor top-K precision (The "Precision Gap") | Bi-encoders cannot evaluate token-to-token interactions (e.g., negations, conditions)5. | Cross-encoder Reranking on the top 50-100 candidates21. |
| Reranker induces unacceptable latency (\>500ms) | Joint forward passes on deep transformer layers are computationally heavy5. | ColBERT (Late Interaction) or strictly bounded Score Threshold Filtering5. |
| System fails at "What are the main themes of the entire dataset?" | Standard RAG retrieves highly localized chunks, missing global themes and overarching trends. | GraphRAG or RAPTOR (recursive tree summarization)28. |
| LLM confidently generates answers when retrieved context is irrelevant | Lack of internal reflection, grading, or fallback mechanisms. | CRAG (Corrective RAG) / Self-RAG with strict routing rules28. |

### **Probe questions (5)**

> 1. Detail the mathematical difference between a bi-encoder's cosine similarity computation and a cross-encoder's joint attention mechanism.  
> 2. Under what specific hardware or latency constraints does an agentic framework switch from a full cross-encoder to a late-interaction ColBERT model?  
> 3. How does GraphRAG construct its entity-relation boundaries, and at what dataset scale does its computational cost outweigh its benefits?  
> 4. Explain the execution graph of a Self-RAG implementation when it detects that the initially retrieved documents do not contain the required answer.  
> 5. In a production pipeline processing 1,000 queries per second, how is the Adaptive RAG routing layer structured to avoid latency bottlenecks?

### **Metric / design pitfalls**

Running a full cross-encoder against thousands of documents instead of a truncated top-K candidate list leads to complete latency collapse26. Implementing agentic multi-hop routing for simple factual lookups overcomplicates the architecture, adding unnecessary failure points, latency overhead, and token costs without improving answer quality.

### **Anti-goals**

* Implementing complex GraphRAG pipelines for simple exact-match lookup requirements.  
* Using an LLM as a zero-shot reranker in hard real-time latency paths without stringent cost and speed profiling5.  
* Deploying unbound conversational agents without strict iteration limits, risking infinite loops during complex retrieval failures.

## **Minimal golden-set recipe**

* **Size and Composition:** A minimum of 200–500 manually verified examples. The dataset must be heavily stratified to include single-hop lookups, multi-hop reasoning, complex aggregations, and adversarial queries (e.g., explicit negatives or queries where the answer does not exist in the corpus).  
* **Label Structure:** Each entry must consist of the user\_query, the ground\_truth\_answer, a list of required\_fact\_strings (must-have entities/claims to satisfy recall), and the exact source\_document\_ids containing the evidence.  
* **Leakage Prevention:** Golden sets must be strictly isolated from the training sets of any fine-tuned embedding models or LLM-as-judge few-shot prompts. Synthetic data generators used to bulk up the set must use a separate LLM family than the generation and evaluation LLMs to prevent self-preference bias.  
* **Refresh Cadence:** The golden set must be version-controlled and refreshed quarterly, or immediately upon a major ingestion schema change, domain expansion, or measured data drift in production telemetrics.

#### **Works cited**

> 1. Semantic Search vs Keyword Search: Which Your AI Product, [https://www.institutepm.com/knowledge-hub/semantic-search-vs-keyword-search](https://www.institutepm.com/knowledge-hub/semantic-search-vs-keyword-search)  
> 2. Anthropic's Contextual Retrieval: A Guide With Implementation \- DataCamp, [https://www.datacamp.com/tutorial/contextual-retrieval-anthropic](https://www.datacamp.com/tutorial/contextual-retrieval-anthropic)  
> 3. Contextual Retrieval in AI Systems \- Anthropic, [https://www.anthropic.com/engineering/contextual-retrieval](https://www.anthropic.com/engineering/contextual-retrieval)  
> 4. Implementing Anthropic's Contextual Retrieval with Async Processing \- Instructor, [https://python.useinstructor.com/blog/2024/09/26/implementing-anthropics-contextual-retrieval-with-async-processing/](https://python.useinstructor.com/blog/2024/09/26/implementing-anthropics-contextual-retrieval-with-async-processing/)  
> 5. RAG Reranking: Improving Retrieval Quality with Cross-Encoders \- BigData Boutique, [https://bigdataboutique.com/blog/rag-reranking-improving-retrieval-quality-with-cross-encoders](https://bigdataboutique.com/blog/rag-reranking-improving-retrieval-quality-with-cross-encoders)  
> 6. Late Chunking vs Contextual Retrieval: The Math Behind RAG's Context Problem \- Medium, [https://medium.com/kx-systems/late-chunking-vs-contextual-retrieval-the-math-behind-rags-context-problem-d5a26b9bbd38](https://medium.com/kx-systems/late-chunking-vs-contextual-retrieval-the-math-behind-rags-context-problem-d5a26b9bbd38)  
> 7. Vector Databases Compared: pgvector vs Pinecone vs Qdrant for AI-Powered Business Apps in 2026 \- SofttechOver, [https://softtechover.com/post/vector-databases-compared-pgvector-vs-pinecone-vs-qdrant-for-ai-powered-business-apps-in-2026](https://softtechover.com/post/vector-databases-compared-pgvector-vs-pinecone-vs-qdrant-for-ai-powered-business-apps-in-2026)  
> 8. Implement contextual RAG from Anthropic \- Together AI docs, [https://docs.together.ai/docs/how-to-implement-contextual-rag-from-anthropic](https://docs.together.ai/docs/how-to-implement-contextual-rag-from-anthropic)  
> 9. Skip List Meets Graph: Understanding HNSW Indexing \- Kaggle, [https://www.kaggle.com/code/anotherbadcode/skip-list-meets-graph-understanding-hnsw-indexing](https://www.kaggle.com/code/anotherbadcode/skip-list-meets-graph-understanding-hnsw-indexing)  
> 10. How to Create HNSW Index \- OneUptime, [https://oneuptime.com/blog/post/2026-01-30-vector-db-hnsw-index/view](https://oneuptime.com/blog/post/2026-01-30-vector-db-hnsw-index/view)  
> 11. Vector Databases 2026: pgvector vs Pinecone vs Qdrant | Aaron's Generative AI Feeds, [https://fp8.co/articles/Vector-Database-Comparison-pgvector-Pinecone-Qdrant-Weaviate-Milvus](https://fp8.co/articles/Vector-Database-Comparison-pgvector-Pinecone-Qdrant-Weaviate-Milvus)  
> 12. pgvector vs Qdrant: Which Should You Use in 2026? \- Rivestack, [https://rivestack.io/blog/pgvector-vs-qdrant](https://rivestack.io/blog/pgvector-vs-qdrant)  
> 13. Filtered Approximate Nearest Neighbor Search in Vector Databases: System Design and Performance Analysis \- arXiv, [https://arxiv.org/html/2602.11443](https://arxiv.org/html/2602.11443)  
> 14. RAGAs. Retrieval-Augmented Generation… | by Nidish\_N\_Rao | Medium, [https://medium.com/@nidishnrao/ragas-e0bf700a63c6](https://medium.com/@nidishnrao/ragas-e0bf700a63c6)  
> 15. How to Build a RAG Evaluation Framework in 4 Metrics \- Autonoma AI, [https://getautonoma.com/blog/rag-evaluation-metrics](https://getautonoma.com/blog/rag-evaluation-metrics)  
> 16. Answer Relevancy \- The LLM Evaluation Framework \- DeepEval, [https://deepeval.com/docs/metrics-answer-relevancy](https://deepeval.com/docs/metrics-answer-relevancy)  
> 17. Answer Relevance \- Ragas, [https://docs.ragas.io/en/v0.1.21/concepts/metrics/answer\_relevance.html](https://docs.ragas.io/en/v0.1.21/concepts/metrics/answer_relevance.html)  
> 18. CoEval: Ranking Language Models for Custom Tasks Without Labeled Data or Trustworthy Benchmarks \- arXiv, [https://arxiv.org/pdf/2606.03650](https://arxiv.org/pdf/2606.03650)  
> 19. A Survey on LLM-as-a-Judge \- arXiv, [https://arxiv.org/html/2411.15594v6](https://arxiv.org/html/2411.15594v6)  
> 20. Leveraging Resolved Incident History for LLM-Assisted Software Bug Diagnosis \- arXiv, [https://arxiv.org/html/2607.21911v1](https://arxiv.org/html/2607.21911v1)  
> 21. Why Your Reranker Is the Last Line You Forgot to Build | Ranjan Kumar, [https://ranjankumar.in/rag-engineering-reranking-precision-gap](https://ranjankumar.in/rag-engineering-reranking-precision-gap)  
> 22. Humans or LLMs as the Judge? A Study on Judgement Bias | Request PDF \- ResearchGate, [https://www.researchgate.net/publication/386187780\_Humans\_or\_LLMs\_as\_the\_Judge\_A\_Study\_on\_Judgement\_Bias](https://www.researchgate.net/publication/386187780_Humans_or_LLMs_as_the_Judge_A_Study_on_Judgement_Bias)  
> 23. Summarization is Not Dead Yet \- arXiv, [https://arxiv.org/html/2606.08000v1](https://arxiv.org/html/2606.08000v1)  
> 24. Summarization is Not Dead Yet \- arXiv, [https://arxiv.org/pdf/2606.08000](https://arxiv.org/pdf/2606.08000)  
> 25. LLM-as-a-Judge in Healthcare: A Scoping Analysis of Applications, Methods, and Human Alignment \- arXiv, [https://arxiv.org/html/2605.25273v1](https://arxiv.org/html/2605.25273v1)  
> 26. Top Reranking Models to Boost RAG Accuracy in 2026 \- Redis, [https://redis.io/blog/top-reranking-models-rag-accuracy/](https://redis.io/blog/top-reranking-models-rag-accuracy/)  
> 27. RAG Is More Than Retrieval — It's Search & Judge | by Fanghua (Joshua) Yu | Medium, [https://medium.com/@yu-joshua/rag-is-more-than-retrieval-its-search-judge-9f8e0364fe5b](https://medium.com/@yu-joshua/rag-is-more-than-retrieval-its-search-judge-9f8e0364fe5b)  
> 28. Advanced RAG Techniques — .md Directory \- Neura Market, [https://www.neura.market/directories/md-directory/rag-md-agentic-ai-course-05-advanced-rag-montwwlh](https://www.neura.market/directories/md-directory/rag-md-agentic-ai-course-05-advanced-rag-montwwlh)  
> 29. From BM25 to Corrective RAG: Benchmarking Retrieval ... \- OPUS, [https://opus4.kobv.de/opus4-haw/frontdoor/deliver/index/docId/6863/file/2604.01733v1.pdf](https://opus4.kobv.de/opus4-haw/frontdoor/deliver/index/docId/6863/file/2604.01733v1.pdf)  
> 30. How does a Reranker work? \- Outcome School, [https://outcomeschool.com/blog/how-does-a-reranker-work](https://outcomeschool.com/blog/how-does-a-reranker-work)
