import matplotlib.pyplot as plt
import numpy as np

plt.style.use('bmh')

# ==========================================
# 1. DADOS DOS TESTES
# ==========================================

cenarios = ['200 Utilizadores', '500 Utilizadores', '2000 Utilizadores']
x = np.arange(len(cenarios))
largura = 0.2

# ==========================================
# LATÊNCIA (ms) - NODE.JS
# ==========================================

node_rest = [6.30, 85.27, 1759.53]
node_graphql = [6.75, 91.61, 1701.85]
node_soap = [6.15, 86.35, 1648.68]
node_grpc = [2.25, 2.17, 2.46]

# ==========================================
# LATÊNCIA (ms) - PYTHON
# ==========================================

py_rest = [7.86, 93.33, 1645.02]
py_graphql = [10.43, 282.32, 15196.21]
py_soap = [9.91, 85.94, 1778.56]
py_grpc = [2.95, 2.80, 3.15]

# ==========================================
# THROUGHPUT (RPS) - NODE.JS
# ==========================================

node_rest_rps = [21.1, 44.6, 0.1]
node_graphql_rps = [19.1, 45.3, 0.2]
node_soap_rps = [19.7, 46.0, 0.1]
node_grpc_rps = [19.2, 41.6, 1.0]

# ==========================================
# THROUGHPUT (RPS) - PYTHON
# ==========================================

py_rest_rps = [21.4, 42.6, 0.1]
py_graphql_rps = [19.8, 42.7, 0.3]
py_soap_rps = [18.8, 42.9, 0.4]
py_grpc_rps = [22.7, 44.2, 0.6]

# ==========================================
# CORES
# ==========================================

cor_rest = '#3498db'
cor_graphql = '#9b59b6'
cor_soap = '#f1c40f'
cor_grpc = '#e74c3c'

# ==========================================
# FUNÇÃO PARA ADICIONAR RÓTULOS
# ==========================================

def adicionar_rotulos(ax, barras):
    for barra in barras:
        altura = barra.get_height()

        if altura >= 1000:
            texto = f'{altura:.0f}'
        elif altura >= 100:
            texto = f'{altura:.1f}'
        else:
            texto = f'{altura:.2f}'

        ax.annotate(
            texto,
            xy=(barra.get_x() + barra.get_width()/2, altura),
            xytext=(0, 3),
            textcoords="offset points",
            ha='center',
            va='bottom',
            fontsize=8
        )

# ==========================================
# FIGURA 1 E 2
# LATÊNCIA POR PROTOCOLO
# ==========================================

def gerar_grafico_latencia(
        titulo,
        nome_ficheiro,
        dados_rest,
        dados_graphql,
        dados_soap,
        dados_grpc):

    fig, ax = plt.subplots(figsize=(12, 7))

    bar1 = ax.bar(
        x - largura*1.5,
        dados_rest,
        largura,
        label='REST',
        color=cor_rest
    )

    bar2 = ax.bar(
        x - largura*0.5,
        dados_graphql,
        largura,
        label='GraphQL',
        color=cor_graphql
    )

    bar3 = ax.bar(
        x + largura*0.5,
        dados_soap,
        largura,
        label='SOAP',
        color=cor_soap
    )

    bar4 = ax.bar(
        x + largura*1.5,
        dados_grpc,
        largura,
        label='gRPC',
        color=cor_grpc
    )

    ax.set_yscale('log')

    ax.set_title(
        titulo,
        fontsize=16,
        fontweight='bold'
    )

    ax.set_ylabel(
        'Tempo Médio de Resposta (ms) - Escala Logarítmica',
        fontsize=12
    )

    ax.set_xticks(x)
    ax.set_xticklabels(cenarios)

    ax.legend()
    ax.grid(True, axis='y')

    adicionar_rotulos(ax, bar1)
    adicionar_rotulos(ax, bar2)
    adicionar_rotulos(ax, bar3)
    adicionar_rotulos(ax, bar4)

    plt.tight_layout()
    plt.savefig(nome_ficheiro, dpi=300, bbox_inches='tight')
    plt.close()

# ==========================================
# FIGURA 3
# COMPARATIVO DE THROUGHPUT
# ==========================================

def gerar_grafico_rps():

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(
        cenarios,
        node_rest_rps,
        marker='o',
        linewidth=3,
        label='REST Node.js'
    )

    ax.plot(
        cenarios,
        node_graphql_rps,
        marker='o',
        linewidth=3,
        label='GraphQL Node.js'
    )

    ax.plot(
        cenarios,
        node_soap_rps,
        marker='o',
        linewidth=3,
        label='SOAP Node.js'
    )

    ax.plot(
        cenarios,
        node_grpc_rps,
        marker='o',
        linewidth=3,
        label='gRPC Node.js'
    )

    ax.plot(
        cenarios,
        py_rest_rps,
        marker='s',
        linestyle='--',
        linewidth=2,
        label='REST Python'
    )

    ax.plot(
        cenarios,
        py_graphql_rps,
        marker='s',
        linestyle='--',
        linewidth=2,
        label='GraphQL Python'
    )

    ax.plot(
        cenarios,
        py_soap_rps,
        marker='s',
        linestyle='--',
        linewidth=2,
        label='SOAP Python'
    )

    ax.plot(
        cenarios,
        py_grpc_rps,
        marker='s',
        linestyle='--',
        linewidth=2,
        label='gRPC Python'
    )

    ax.set_title(
        'Comparativo de Throughput (RPS)',
        fontsize=16,
        fontweight='bold'
    )

    ax.set_ylabel(
        'Requisições por Segundo (RPS)',
        fontsize=12
    )

    ax.grid(True)
    ax.legend(ncol=2)

    plt.tight_layout()
    plt.savefig(
        'grafico_rps.png',
        dpi=300,
        bbox_inches='tight'
    )

    plt.close()

# ==========================================
# FIGURA 4
# REST VS gRPC
# ==========================================

def gerar_grafico_rest_vs_grpc():

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(
        cenarios,
        node_rest,
        marker='o',
        linewidth=3,
        markersize=8,
        label='REST Node.js'
    )

    ax.plot(
        cenarios,
        node_grpc,
        marker='o',
        linewidth=3,
        markersize=8,
        label='gRPC Node.js'
    )

    ax.plot(
        cenarios,
        py_rest,
        marker='s',
        linewidth=3,
        markersize=8,
        label='REST Python'
    )

    ax.plot(
        cenarios,
        py_grpc,
        marker='s',
        linewidth=3,
        markersize=8,
        label='gRPC Python'
    )

    ax.set_yscale('log')

    ax.set_title(
        'REST vs gRPC - Evolução da Latência',
        fontsize=16,
        fontweight='bold'
    )

    ax.set_ylabel(
        'Tempo Médio de Resposta (ms)',
        fontsize=12
    )

    ax.grid(True)
    ax.legend()

    plt.tight_layout()

    plt.savefig(
        'grafico_rest_vs_grpc.png',
        dpi=300,
        bbox_inches='tight'
    )

    plt.close()

# ==========================================
# EXECUÇÃO
# ==========================================

print("A gerar Figura 1 - Node.js...")
gerar_grafico_latencia(
    'Comparativo de Latência por Protocolo em Node.js',
    'grafico_comparativo_node.png',
    node_rest,
    node_graphql,
    node_soap,
    node_grpc
)

print("A gerar Figura 2 - Python...")
gerar_grafico_latencia(
    'Comparativo de Latência por Protocolo em Python',
    'grafico_comparativo_python.png',
    py_rest,
    py_graphql,
    py_soap,
    py_grpc
)

print("A gerar Figura 3 - Throughput...")
gerar_grafico_rps()

print("A gerar Figura 4 - REST vs gRPC...")
gerar_grafico_rest_vs_grpc()

print("\nGráficos gerados com sucesso!")
print("Arquivos criados:")
print(" - grafico_comparativo_node.png")
print(" - grafico_comparativo_python.png")
print(" - grafico_rps.png")
print(" - grafico_rest_vs_grpc.png")