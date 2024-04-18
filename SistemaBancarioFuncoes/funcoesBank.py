LIMITE_SAQUE = 3

def deposito(saldo: float, extrato: str) -> tuple:
    value = float(input('Informe o valor que deseja depositar: R$ '))
    if value > 0:
        saldo += value
        extrato += (f'\033[92m'
                    f'Depósito: \tR$ {value:.2f}'
                    f'\033[m\n')
    else:
        print('Operação falhou! Valor informado inválido.')
    return saldo, extrato


def saque(saldo: float, extrato: str, num_saques: int) -> tuple:
    limite = 500
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
    return saldo, extrato, num_saques

def show_extrato(saldo: float, extrato: str):
    title = 'EXTRATO'
    print(f'{title:=^30}')
    print("Sem movimentações" if not extrato else extrato)
    print(f'\033[94m'
          f'Saldo: \t\tR$ {saldo:.2f}'
          f'\033[m')
    print(f'{"":=^30}')