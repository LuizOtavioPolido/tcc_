def validate_and_correct_plate(plate):
    """Valida e corrige a placa para o formato."""
    # Corrigir para o padrão Mercosul
    if len(plate) != 7:
        return plate
    
    corrected_plate = ""

    for i, char in enumerate(plate):
        if i in (0, 1, 2):
            corrected_plate += char if char.isalpha() else 'O' if char == '0' else 'I' if char == '1' else char
        elif i == 3:  # Quarta posição deve ser número
            corrected_plate += char if char.isdigit() else '0'
        elif i == 4:  # Quinta posição deve ser letra
            corrected_plate += char if char.isalpha() else 'O' if char == '0' else 'I' if char == '1' else char
        elif i in (5, 6):  # Sexta e sétima posições devem ser números
            corrected_plate += char if char.isdigit() else '0'
 
    return corrected_plate
