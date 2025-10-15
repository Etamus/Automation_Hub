# ===================================================================
# == Script Finalizador de Processos (ATUALIZADO)                  ==
# ===================================================================

# Lista dos nomes dos processos que queremos encerrar (sem o .exe)
# Adicionados "chrome" e "msedge" à lista
$processosParaFinalizar = @(
    "EXCEL",
    "saplogon",
    "sapgui",
    "chrome",
    "msedge"
)

$mensagens = @()

foreach ($nome in $processosParaFinalizar) {
    # Tenta encontrar o processo sem gerar um erro se ele não existir
    $processo = Get-Process -Name $nome -ErrorAction SilentlyContinue

    if ($processo) {
        try {
            # Se encontrou, força o encerramento
            Stop-Process -Name $nome -Force -ErrorAction Stop
            $mensagens += "SUCESSO: Processo '$nome' foi finalizado."
        }
        catch {
            $mensagens += "ERRO: Falha ao tentar finalizar o processo '$nome'."
        }
    }
    else {
        $mensagens += "INFO: Processo '$nome' não estava em execução."
    }
}

# Retorna um resumo de tudo o que foi feito
Write-Output ($mensagens -join "`r`n")