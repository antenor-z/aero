def validate_runway(head1, head2, runway_length, runway_width):
    head1_number = int(head1[0:2])
    head2_number = int(head2[0:2])
    
    head1_letter = head1[2] if len(head1) > 2 else None
    head2_letter = head2[2] if len(head2) > 2 else None

    if abs(head1_number - head2_number) != 18:
        raise ValueError("Erro no número das cabeceiras", 
                         "A diferença entre estes números deve ser de 18")
    if not (100 <= runway_length <= 5000):
        raise ValueError("Comprimento de pista inválido")
    
    if not (20 <= runway_width <= 80):
        raise ValueError("Largura de pista inválida")
    
    if not (1 <= head1_number <= 36) or not (1 <= head2_number <= 36):
        raise ValueError("Cabeceira inválida", 
                         "Os números de cabeceira devem estar entre 01 e 36")
    
    if head1_letter == 'L' and head2_letter != 'R':
        raise ValueError("Erro nas letras das cabeceiras", 
                         "Se uma cabeceira for 'L', a outra deve ser 'R'")
    elif head1_letter == 'R' and head2_letter != 'L':
        raise ValueError("Erro nas letras das cabeceiras", 
                         "Se uma cabeceira for 'R', a outra deve ser 'L'")
    elif head1_letter == 'C' and head2_letter != 'C':
        raise ValueError("Erro nas letras das cabeceiras", 
                         "Se uma cabeceira for 'C', a outra deve ser 'C'")
    elif head1_letter is None and head2_letter is not None:
        raise ValueError("Erro nas letras das cabeceiras", 
                          "Se uma cabeceira não tiver letra, a outra também não deve ter")
    