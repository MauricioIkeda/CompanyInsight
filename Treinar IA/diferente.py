import spacy
from spacy.tokens import DocBin
from spacy.training.example import Example
from tqdm import tqdm
import json

# 1. Carregar o modelo existente
nlp = spacy.load("IaAntigo")  # Substitua pelo caminho do modelo antigo
ner = nlp.get_pipe("ner")

# 2. Carregar os dados antigos
# Certifique-se de ter um arquivo com os dados antigos no formato DocBin
old_data_path = "./old_training_data.spacy"  # Caminho para os dados antigos
old_data = DocBin().from_disk(old_data_path).get_docs(nlp.vocab)

# 3. Carregar os novos dados de treinamento
db = DocBin()  # Cria o objeto DocBin para novos dados
with open('training_data.json', encoding='utf-8') as f:
    NEW_TRAIN_DATA = json.load(f)

for text, annot in tqdm(NEW_TRAIN_DATA['annotations']):
    doc = nlp.make_doc(text)
    ents = []
    for start, end, label in annot["entities"]:
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is None:
            print(f"Skipping entity in text: {text}")
        else:
            ents.append(span)
    doc.ents = ents
    db.add(doc)

# Salvar os novos dados no formato DocBin
new_data_path = "./new_training_data.spacy"
db.to_disk(new_data_path)

# 4. Mesclar os dados antigos e novos
new_data = DocBin().from_disk(new_data_path).get_docs(nlp.vocab)
combined_data = list(old_data) + list(new_data)

# 5. Criar exemplos de treinamento combinados
examples = [
    Example.from_dict(
        doc, {"entities": [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]}
    )
    for doc in combined_data
]

# 6. Treinar o modelo incrementalmente
optimizer = nlp.resume_training()

for epoch in range(23):  # Ajuste o número de épocas conforme necessário
    losses = {}
    for example in tqdm(examples):
        nlp.update([example], drop=0.2, losses=losses)
    print(f"Losses after epoch {epoch}: {losses}")

# 7. Salvar o modelo atualizado
nlp.to_disk("./NovaIA")
print("Modelo atualizado salvo com sucesso!")
