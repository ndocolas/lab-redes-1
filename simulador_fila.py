import random

def simulador_fila(servidores, capacidade, chegada_min, chegada_max, atend_min, atend_max, num_aleatorios, primeira_chegada, semente=None):
    """
    Simulador de fila G/G/c/K por eventos.
    
    Parâmetros:
    - servidores: número de servidores (c)
    - capacidade: capacidade total do sistema (K) = fila + servidores
    - chegada_min, chegada_max: intervalo uniforme para tempo entre chegadas
    - atend_min, atend_max: intervalo uniforme para tempo de atendimento
    - num_aleatorios: quantidade máxima de números aleatórios a consumir
    - primeira_chegada: tempo da primeira chegada
    - semente: seed para reprodutibilidade (opcional)
    """
    
    if semente is not None:
        random.seed(semente)
    
    # Contadores
    aleatorios_usados = 0
    perdas = 0
    
    # Estado do sistema
    estado_atual = 0  # número de clientes no sistema
    tempo_atual = 0.0
    
    # Acumuladores de tempo por estado
    tempos_estado = [0.0] * (capacidade + 1)  # estados de 0 a K
    
    # Lista de eventos: (tempo, tipo)
    # tipo: 'chegada' ou 'saida'
    eventos = []
    
    # Função para gerar número aleatório e contar
    def gerar_aleatorio():
        nonlocal aleatorios_usados
        aleatorios_usados += 1
        return random.random()
    
    def tempo_entre_chegadas():
        r = gerar_aleatorio()
        return chegada_min + (chegada_max - chegada_min) * r
    
    def tempo_atendimento():
        r = gerar_aleatorio()
        return atend_min + (atend_max - atend_min) * r
    
    # Agenda primeira chegada no tempo especificado
    eventos.append((primeira_chegada, 'chegada'))
    # A primeira chegada consome 1 aleatório (para o tempo entre chegadas que gerou o 2.0)
    # Na verdade, a primeira chegada é fixa em 2.0, então não consome aleatório.
    # Os aleatórios são usados a partir da segunda chegada e dos atendimentos.
    
    # Simulação por eventos
    while eventos:
        # Ordena eventos por tempo (pega o mais próximo)
        eventos.sort(key=lambda x: x[0])
        
        # Pega próximo evento
        tempo_evento, tipo_evento = eventos.pop(0)
        
        # Acumula tempo no estado atual
        dt = tempo_evento - tempo_atual
        tempos_estado[estado_atual] += dt
        tempo_atual = tempo_evento
        
        if tipo_evento == 'chegada':
            # Verifica se o sistema tem capacidade
            if estado_atual < capacidade:
                estado_atual += 1
                
                # Se há servidor livre, inicia atendimento
                # Servidores ocupados = min(estado_anterior, servidores)
                # Se estado_anterior < servidores, há servidor livre
                if estado_atual <= servidores:
                    # Há servidor livre, agenda saída
                    if aleatorios_usados < num_aleatorios:
                        t_atend = tempo_atendimento()
                        eventos.append((tempo_atual + t_atend, 'saida'))
                    # Se não pode gerar mais aleatórios, não agenda saída
                    # mas o cliente já entrou no sistema
            else:
                # Sistema cheio, cliente perdido
                perdas += 1
            
            # Agenda próxima chegada (se ainda temos aleatórios)
            if aleatorios_usados < num_aleatorios:
                t_chegada = tempo_entre_chegadas()
                eventos.append((tempo_atual + t_chegada, 'chegada'))
            # Se não pode gerar, não agenda mais chegadas
        
        elif tipo_evento == 'saida':
            estado_atual -= 1
            
            # Se há clientes na fila esperando, inicia atendimento do próximo
            if estado_atual >= servidores:
                if aleatorios_usados < num_aleatorios:
                    t_atend = tempo_atendimento()
                    eventos.append((tempo_atual + t_atend, 'saida'))
    
    # Tempo global
    tempo_global = tempo_atual
    
    # Distribuição de probabilidades
    print("=" * 60)
    print(f"Simulação G/G/{servidores}/{capacidade}")
    print(f"Chegadas: U[{chegada_min}..{chegada_max}]")
    print(f"Atendimento: U[{atend_min}..{atend_max}]")
    print(f"Primeira chegada em t = {primeira_chegada}")
    print(f"Números aleatórios utilizados: {aleatorios_usados}")
    print("=" * 60)
    print()
    print(f"{'Estado':<10} {'Tempo':<20} {'Probabilidade':<15}")
    print("-" * 45)
    
    for i in range(capacidade + 1):
        prob = tempos_estado[i] / tempo_global if tempo_global > 0 else 0
        print(f"{i:<10} {tempos_estado[i]:<20.4f} {prob:<15.4f}")
    
    print("-" * 45)
    print(f"Tempo global de simulação: {tempo_global:.4f}")
    print(f"Número de perdas: {perdas}")
    print(f"Total de aleatórios usados: {aleatorios_usados}")
    print()
    
    return {
        'tempos_estado': tempos_estado,
        'tempo_global': tempo_global,
        'perdas': perdas,
        'aleatorios_usados': aleatorios_usados
    }


# =============================================
# EXECUÇÃO DAS SIMULAÇÕES
# =============================================

print("*" * 60)
print("SIMULADOR DE FILAS - TRABALHO")
print("*" * 60)
print()

# Simulação 1: G/G/1/5
print(">>> SIMULAÇÃO 1: G/G/1/5 <<<")
print()
resultado1 = simulador_fila(
    servidores=1,
    capacidade=5,
    chegada_min=2,
    chegada_max=5,
    atend_min=3,
    atend_max=5,
    num_aleatorios=100000,
    primeira_chegada=2.0,
    semente=42  # Remova ou altere a semente se quiser resultados diferentes
)

print()
print(">>> SIMULAÇÃO 2: G/G/2/5 <<<")
print()
resultado2 = simulador_fila(
    servidores=2,
    capacidade=5,
    chegada_min=2,
    chegada_max=5,
    atend_min=3,
    atend_max=5,
    num_aleatorios=100000,
    primeira_chegada=2.0,
    semente=42  # Mesma semente para comparação (opcional)
)