menu = """
[d] = Depositar
[s] = Sacar
[e] = Extrato
[q] = Sair

=> """

# Variáveis
saldo = 0.0
limite = 500
extrato = ''
num_saques = 0
LIMITE_SAQUE = 3

# Loop de Seleção
while True:
    option = input(menu)

    # Opção Depósito
    if option == 'd':
        value = float(input('Informe o valor que deseja depositar: R$ '))
        if value > 0:
            saldo += value
            extrato += (f'\033[92m'
                        f'Depósito: \tR$ {value:.2f}'
                        f'\033[m\n')
        else:
            print('Operação falhou! Valor informado inválido.')

    # Opção Saque
    elif option == 's':
        value = float(input("Informe o valor que deseja sacar: R$ "))
        if value > saldo:
            print('Operação falhou! Você não tem saldo suficiente.')
        elif value > limite:
            print('Operação falhou! Valor do saque maior que o limite permitido.')
        elif num_saques >= LIMITE_SAQUE:
            print('Operação falhou! Número de saques excedidos')
        elif value > 0:
            saldo -= value
            extrato += (f'\033[91m'
                        f'Saque: \t\tR$ {value:.2f}'
                        f'\033[m\n')
            num_saques += 1
        else:
            print('Operação falhou! Valor informado é inválido.')

    # Opção Extrato
    elif option == 'e':
        title = 'EXTRATO'
        print(f'{title:=^35}')
        print("Sem movimentações" if not extrato else extrato)
        print(f'\033[94m'
              f'Saldo: \t\tR$ {saldo:.2f}'
              f'\033[m')
        print(f'{"":=^35}')

    # Opção Sair
    elif option == 'q':
        break

    # Opção Default
    else:
        print('Operação inválida, pro favor selecione novamente a operação desejada.')