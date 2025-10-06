# ===================================================================
<<<<<<< HEAD
# == Script Finalizador de Processos: cleanup_processes.ps1        ==
# ===================================================================

# Lista dos nomes dos processos que queremos encerrar (sem o .exe)
$processosParaFinalizar = @(
    "EXCEL",
    "saplogon",
    "sapgui"
=======
# == Script Finalizador de Processos (ATUALIZADO)                  ==
# ===================================================================

# Adicionados "chrome" e "msedge" � lista
$processosParaFinalizar = @(
    "EXCEL",
    "saplogon",
    "sapgui",
    "chrome",
    "msedge"
>>>>>>> 450f75c (Atualizações Gerais e Novos Aprimoramentos)
)

$mensagens = @()

foreach ($nome in $processosParaFinalizar) {
<<<<<<< HEAD
    # Tenta encontrar o processo sem gerar um erro se ele não existir
    $processo = Get-Process -Name $nome -ErrorAction SilentlyContinue

    if ($processo) {
        try {
            # Se encontrou, força o encerramento
=======
    # ... (o resto do c�digo continua o mesmo) ...
    $processo = Get-Process -Name $nome -ErrorAction SilentlyContinue
    if ($processo) {
        try {
>>>>>>> 450f75c (Atualizações Gerais e Novos Aprimoramentos)
            Stop-Process -Name $nome -Force -ErrorAction Stop
            $mensagens += "SUCESSO: Processo '$nome' foi finalizado."
        }
        catch {
            $mensagens += "ERRO: Falha ao tentar finalizar o processo '$nome'."
        }
    }
    else {
<<<<<<< HEAD
        $mensagens += "INFO: Processo '$nome' não estava em execução."
    }
}

# Retorna um resumo de tudo o que foi feito
=======
        $mensagens += "INFO: Processo '$nome' n�o estava em execu��o."
    }
}

>>>>>>> 450f75c (Atualizações Gerais e Novos Aprimoramentos)
Write-Output ($mensagens -join "`r`n")