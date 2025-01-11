predictions = [
    "SEZ25H17",
    "AVE1222",
    "AUE0D041",
    "AJA8I00",
    "D0QU4211",
    "AAA7H12"
]
correct = ['SEZ5H17', 'AVE1222', 'AUE0041', 'AJA8I00', 'OQU4211','AAA7H12']

correct_plates = 0

# Comparar placas inteiras
for pred, gt in zip(predictions, correct):
    if pred == gt:
        correct_plates += 1

# Cálculo da taxa de acerto por placa
accuracy_plates = (correct_plates / len(correct)) * 100
print(f"Taxa de Acerto por Placa Completa: {accuracy_plates:.2f}%")
