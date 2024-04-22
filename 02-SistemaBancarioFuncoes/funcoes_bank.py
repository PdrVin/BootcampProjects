import textwrap


def menu():
    title = " MENU "
    menu = f"""
    {title:=^22}
    [D]\tDepositar
    [S]\tSacar
    [E]\tExtrato
    [U]\tNovo Usuário
    [N]\tNova Conta
    [L]\tListar Contas
    [Q]\tSair
    => """
    return input(textwrap.dedent(menu))


# Deposito
def depositar(saldo: float, value: float, extract: str, /) -> tuple:
    if value > 0:
        saldo += value
        extract += (f'\033[92m'
                    f'Depósito:\tR$ {value:.2f}'
                    f'\033[m\n')
        print('\033[92m'
            'Depósito realizado com sucesso!'
            '\033[m')
    
    else:
        print('\033[91m'
            'Operação falhou! Valor informado inválido.'
            '\033[m')
    
    return saldo, extract


# Saque
def sacar(*, saldo: float, value: float, extract: str, limit, num_saques: int, limite_saques: int) -> tuple:
    saldo_exceeded = value > saldo
    limit_exceeded = value > limit
    saque_exceeded = num_saques > limite_saques
    
    if saldo_exceeded:
        print('\033[91m'
            'Operação falhou! Você não tem saldo suficiente.'
            '\033[m')
    
    elif limit_exceeded:
        print('\033[91m'
            'Operação falhou! Valor do saque maior que o limite permitido.'
            '\033[m')
    
    elif saque_exceeded:
        print('\033[91m'
            'Operação falhou! Número de saques excedidos.'
            '\033[m')
    
    elif value > 0:
        saldo -= value
        extract += (f'\033[91m'
                    f'Saque: \t\tR$ {value:.2f}'
                    f'\033[m\n')
        num_saques += 1
    
    else:
        print('\033[91m'
            'Operação falhou! Valor informado é inválido.'
            '\033[m')
    
    return saldo, extract


# Extrato
def visualizar_historico(saldo: float, /, *, extract: str):
    title = ' EXTRATO '
    print(f'{title:=^26}')
    
    print("Sem movimentações" if not extract else extract)
    
    print(f'\033[94m'
        f'Saldo:\t\tR$ {saldo:.2f}'
        f'\033[m')
    
    print(f'{"":=^26}')


# Novas Funções
# Criar Usuário
def create_user(users: list) -> list:
    cpf = input('Informe o CPF (somente números): ')
    user = filter_users(cpf, users)
    
    valid_cpf = cpf.isdigit() and len(cpf) == 11
    if not valid_cpf:
        print('CPF inválido! Tente novamente')
        return
    
    if user:
        print("\nUsuário já cadastrado com este CPF!")
        return
    
    user_data = {
        'name':input('Informe o nome completo: '),
        'birth_date': input('Informe a data de nascimento (dd-mm-aaaa): '),
        'cpf': cpf,
        'address': input('Informe o endereço (logradouro, num - bairro - cidade/uf): ')
    }
    
    users.append(user_data)
    
    print('\033[92m'
        'Usuário cadastrado com sucesso!'
        '\033[m')


# Filtrar Usuários
def filter_users(cpf: int, users: list):
    filtered_users = [user for user in users if user['cpf'] == cpf]
    return filtered_users[0] if filtered_users else None


# Criar Conta Corrente
def create_current_account(agency: str, account_num: int, users: list) -> dict:
    cpf = input('Informe o CPF do Usuário (somente números): ')
    user = filter_users(cpf, users)
    
    valid_cpf = cpf.isdigit() and len(cpf) == 11
    if not valid_cpf:
        print('CPF inválido! Tente novamente')
        return
    
    if user:
        print('\033[92m'
            'Conta criada com sucesso!'
            '\033[m')
        return {'agency': agency,
                'account_num': account_num,
                'user': user}
    
    print('\033[91m'
        'Usuário não encontrado, Fluxo de criação de conta encerrado!'
        '\033[m')


# Listar Contas
def list_accounts(accounts: list):
    for conta in accounts:
        linha = f"""\
            Agência:\t{conta['agency']}
            C/C:\t\t{conta['account_num']}
            Titular:\t{conta['user']['name']}
        """
        print('=' * 100)
        print(textwrap.dedent(linha))
    return