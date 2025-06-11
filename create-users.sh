#!/bin/bash

# Aguardar o RT estar completamente inicializado
echo "Aguardando RT inicializar..."
sleep 30

# Verificar se RT está respondendo
until curl -f http://rt:80 > /dev/null 2>&1; do
    echo "Aguardando RT estar disponível..."
    sleep 10
done

echo "RT disponível! Criando usuários..."

# Criar usuários usando rt-setup-database
cat << 'EOF' > /tmp/users.txt
@Users = (
    {
        Name         => 'admin_user',
        Password     => 'admin123',
        EmailAddress => 'admin@suaempresa.com',
        RealName     => 'Administrador do Sistema',
        Privileged   => 1,
        Disabled     => 0,
    },
    {
        Name         => 'suporte',
        Password     => 'suporte123',
        EmailAddress => 'suporte@suaempresa.com',
        RealName     => 'Equipe de Suporte',
        Privileged   => 1,
        Disabled     => 0,
    },
    {
        Name         => 'usuario_comum',
        Password     => 'user123',
        EmailAddress => 'user@suaempresa.com',
        RealName     => 'Usuário Comum',
        Privileged   => 0,
        Disabled     => 0,
    }
);

@ACL = (
    # Admin com todos os privilégios
    {
        UserId      => 'admin_user',
        Right       => 'SuperUser',
        Object      => '$RT::System',
    },
    
    # Suporte com privilégios de operação
    {
        UserId      => 'suporte',
        Right       => 'CreateTicket',
        Object      => '$RT::System',
    },
    {
        UserId      => 'suporte',
        Right       => 'SeeQueue',
        Object      => '$RT::System',
    },
    {
        UserId      => 'suporte',
        Right       => 'ShowTicket',
        Object      => '$RT::System',
    },
    {
        UserId      => 'suporte',
        Right       => 'ModifyTicket',
        Object      => '$RT::System',
    },
    {
        UserId      => 'suporte',
        Right       => 'OwnTicket',
        Object      => '$RT::System',
    },
    
    # Usuário comum - apenas criar e ver próprios tickets
    {
        UserId      => 'usuario_comum',
        Right       => 'CreateTicket',
        Object      => '$RT::System',
    }
);
EOF

# Executar a criação dos usuários
/opt/rt4/sbin/rt-setup-database --action insert --datafile /tmp/users.txt

echo "Usuários criados com sucesso!"
echo ""
echo "=== CREDENCIAIS DE ACESSO ==="
echo "1. root / password (SuperUser original)"
echo "2. admin_user / admin123 (Administrador)"
echo "3. suporte / suporte123 (Equipe de Suporte)"
echo "4. usuario_comum / user123 (Usuário Final)"
echo ""
echo "Acesse: http://localhost:8080"