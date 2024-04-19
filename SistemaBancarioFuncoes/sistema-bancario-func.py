import funcoesBank as fb

# Constantes
LIMITE_SAQUE = 3
AGENCY = '0001'

# Variáveis Globais
saldo = 0.0
limite = 500
extrato = ''
num_saques = 0
users = []
accounts = []

# Loop de Seleção
while True:
    # Exibição Menu
    option = fb.menu().upper()

    # Opção Depósito
    if option == 'D':
        # Input
        value = float(input('Informe o valor que deseja depositar: R$'))
        # Retorno
        saldo, extrato = fb.depositar(saldo, value, extrato)

    # Opção Saque
    elif option == 'S':
        # Input
        value = float(input("Informe o valor que deseja sacar: R$"))
        # Retorno
        saldo, extrato = fb.sacar(
            saldo=saldo,
            value=value,
            extract=extrato,
            limit=limite,
            num_saques=num_saques,
            limite_saques=LIMITE_SAQUE,
        )

    # Opção Extrato
    elif option == 'E':
        fb.visualizar_historico(saldo, extract=extrato)

    # Opção Novo Usuário
    elif option == 'U':
        fb.create_user(users)

    # Opção Nova Conta
    elif option == 'N':
        num_account = len(accounts) + 1
        conta = fb.create_current_account(AGENCY, num_account, users)
        
        if conta:
            accounts.append(conta)

    # Opção Listar Contas
    elif option == 'L':
        fb.list_accounts(accounts)

    # Opção Sair
    elif option == 'Q':
        break

    # Opção Default
    else:
        print('Operação inválida, por favor selecione novamente a operação desejada.')