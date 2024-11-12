import nltk
nltk.download('punkt')

import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

# 1. Preparar el dataset (lista de documentos)
documents = [
    "I love machine learning. It's my favorite subject.",
    "I enjoy learning about data science.",
    "Artificial intelligence is the future.",
    "Machine learning and artificial intelligence are closely related.",
    "I like to write Python code.",
    "Data science projects are really interesting."
]

# 2. Preprocesar los documentos para tokenizarlos y etiquetarlos
tagged_documents = [TaggedDocument(words=word_tokenize(doc.lower()), tags=[str(i)]) for i, doc in enumerate(documents)]

# 3. Entrenar el modelo Doc2Vec
model = Doc2Vec(tagged_documents, vector_size=20, window=2, min_count=1, workers=4, epochs=100)

# 4. Guardar el modelo entrenado (opcional)
model.save("d2v.model")

# 5. Inferir un vector para un nuevo documento
new_document = "I love coding in Python and learning about machine learning."
new_vector = model.infer_vector(word_tokenize(new_document.lower()))
print("Vector representation of the new document:\n", new_vector)

# 6. Buscar documentos similares en el corpus
similar_docs = model.dv.most_similar([new_vector], topn=3)
print("Top 3 similar documents:")
for doc_id, similarity in similar_docs:
    print(f"Document {doc_id}: {documents[int(doc_id)]} (Similarity: {similarity})")
