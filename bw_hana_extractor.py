# ===================================================================
# == Script de Automação BW HANA (VERSÃO FINAL COM BOTÃO DIRETO)   ==
# ===================================================================

import sys
import os
from playwright.sync_api import sync_playwright, TimeoutError

def run_automation(username, password):
    DOWNLOAD_PATH = "C:\\Users\\Robo01\\Desktop"

    with sync_playwright() as p:
        browser = None
        try:
            print("Iniciando o navegador Google Chrome...")
            browser = p.chromium.launch(channel="chrome", headless=False)
            page = browser.new_page()
            page.set_default_timeout(60000)

            print("Acessando o portal BW HANA...")
            page.goto("https://lar-bi-portal.whirlpool.com/irj/portal")

            print("Preenchendo credenciais...")
            # Lembre-se de verificar se os seletores de login estão corretos
            page.fill("#logonuidfield", username)
            page.fill("#logonpassfield", password)
            
            print("Realizando login...")
            page.get_by_role("button", name="Efetuar logon").click()
            page.wait_for_load_state("networkidle")
            
            if page.locator("#logonpassfield").is_visible(timeout=5000):
                raise Exception("Login falhou. Verifique as credenciais.")
            
            print("Login realizado com sucesso.")

            print("Acessando favoritos...")
            page.click("text=Favoritos")

            print("Clicando no relatório 'IMPUT PÇS'...")
            page.click("text=IMPUT PÇS")
            page.wait_for_load_state("networkidle")

            print("Entrando no iframe principal: #contentAreaFrame")
            frame_principal = page.frame_locator("#contentAreaFrame")
            
            print("Entrando no iframe do relatório: #isolatedWorkArea")
            frame_relatorio = frame_principal.frame_locator("#isolatedWorkArea")
            
            print("Clicando em OK para gerar o relatório...")
            frame_relatorio.locator("#DLG_VARIABLE_dlgBase_BTNOK").click()
            
            # --- LÓGICA DE EXPORTAÇÃO FINAL E SIMPLIFICADA ---
            
            # 1. Define o seletor do botão "Exportar para Excel" usando o ID que você encontrou.
            export_button_selector = "#BUTTON_TOOLBAR_2_btn3_acButton"
            
            # 2. Espera o botão de exportar estar visível (sinal de que o relatório está pronto).
            print(f"Aguardando o botão de exportação ('{export_button_selector}') aparecer...")
            frame_relatorio.locator(export_button_selector).wait_for(state="visible", timeout=120000)
            
            # 3. Prepara para o download e clica no botão.
            print("Clicando em 'Exportar para Excel'...")
            with page.expect_download(timeout=120000) as download_info:
                frame_relatorio.locator(export_button_selector).click()
            
            download = download_info.value
            
            # 4. Salva o arquivo com o nome e extensão corretos.
            download_target_path = os.path.join(DOWNLOAD_PATH, "BW.xls")
            download.save_as(download_target_path)
            
            print(f"SUCESSO: Arquivo salvo em {download_target_path}")

        except TimeoutError as te:
            print(f"ERRO: A automação falhou por timeout. Uma etapa demorou demais. Verifique se os seletores (login, OK, exportar) estão corretos. Detalhes: {te}")
        except Exception as e:
            print(f"ERRO: A automação falhou. Causa: {e}")
        
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("ERRO: Usuário e senha são necessários para executar o script.")
        sys.exit(1)
        
    user_arg = sys.argv[1]
    pass_arg = sys.argv[2]
    run_automation(user_arg, pass_arg)