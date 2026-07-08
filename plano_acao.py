import streamlit as st
import pandas as pd
import dataclasses
from datetime import date
from typing import List, Optional
import io

@dataclasses.dataclass
class ActionItem:
    """Representa um item do Plano de Ação IEG-M com campos estratégicos avançados."""
    dimensao: str
    meta_estrategica: str
    indicador_desempenho: str
    acao: str
    descricao_acao: str
    fragilidades: str
    meta: str
    resultados_esperados: str
    integracao_planejamento_municipal: str
    alinhamento_ods: str
    data_inicio: Optional[date]
    data_conclusao: Optional[date]
    periodo_report: str
    responsavel: str
    forma_execucao: str
    evidencias: str
    status: str

def init_session_state():
    """Inicializa os dados estruturados com as novas colunas e exemplos reais."""
    if "plano_acao_db" not in st.session_state:
        st.session_state.plano_acao_db = [
            {
                "dimensao": "i-Educ",
                "meta_estrategica": "ADEQUAÇÃO DO ESPAÇO POR ALUNO",
                "indicador_desempenho": "Área Física Disponível",
                "acao": "Levantamento técnico das salas",
                "descricao_acao": "Medição de todas as salas de aula para otimização de espaço físico.",
                "fragilidades": "Falta de engenheiro permanente na secretaria para homologar laudos.",
                "meta": "Atingir 100% das salas mapeadas",
                "resultados_esperados": "Redução em 15% de salas superlotadas",
                "integracao_planejamento_municipal": "Sim (PPA/LDO)",
                "alinhamento_ods": "ODS 4 - Educação de Qualidade",
                "data_inicio": date(2026, 2, 2),
                "data_conclusao": date(2026, 6, 30),
                "periodo_report": "Trimestral",
                "responsavel": "Misma/Patrícia",
                "forma_execucao": "Medição in loco",
                "evidencias": "Relatório fotográfico e laudos assinados",
                "status": "🟢 Verde - Atendido"
            },
            {
                "dimensao": "i-Gov TI",
                "meta_estrategica": "SEGURANÇA DA INFORMAÇÃO",
                "indicador_desempenho": "Índice de Proteção de Dados",
                "acao": "Implementação de Backup em Nuvem Automatizado",
                "descricao_acao": "Configurar rotinas de backup criptografado para os sistemas financeiros.",
                "fragilidades": "Servidores locais obsoletos com risco de perda iminente de dados.",
                "meta": "100% dos servidores críticos espelhados",
                "resultados_esperados": "Zero perda de dados em caso de sinistro",
                "integracao_planejamento_municipal": "Sim (LOA)",
                "alinhamento_ods": "ODS 9 - Indústria, Inovação e Infraestrutura",
                "data_inicio": date(2026, 3, 1),
                "data_conclusao": date(2026, 12, 15),
                "periodo_report": "Mensal",
                "responsavel": "Departamento de TI",
                "forma_execucao": "Contratação de storage cloud",
                "evidencias": "Contrato ativo e logs de sincronização",
                "status": "🔴 Vermelho - Pendente"
            }
        ]

def converter_para_df() -> pd.DataFrame:
    if not st.session_state.plano_acao_db:
        return pd.DataFrame(columns=[f.name for f in dataclasses.fields(ActionItem)])
    return pd.DataFrame(st.session_state.plano_acao_db)

def mostrar_formulario_plano_acao():
    init_session_state()
    df_completo = converter_para_df()
    
    # --- CABEÇALHO CORPORATIVO ---
    st.title("🎯 Painel Estratégico do Plano de Ação — IEG-M")
    st.caption("Central de Monitoramento de Metas, Fragilidades e Cronogramas")
    
    # Opções fixas do IEG-M solicitadas
    dimensoes_iegm = ["i-Cidade", "i-Educ", "i-Gov TI", "i-Amb", "i-Plan", "i-Fiscal", "i-Saúde"]
    lista_status = ["🟢 Verde - Atendido", "🟡 Amarelo - Em análise", "🔴 Vermelho - Pendente"]
    periodos_report = ["Mensal", "Bimestral", "Trimestral", "Semestral", "Anual"]

    # ----------------------------------------------------
    # CONTROLADORES DE FILTROS NA SIDEBAR
    # ----------------------------------------------------
    st.sidebar.header("🔍 Central de Filtros Avançados")
    
    filtro_dim = st.sidebar.selectbox("Filtrar por Dimensão IEG-M", ["Todas"] + dimensoes_iegm)
    filtro_status = st.sidebar.selectbox("Filtrar por Status", ["Todos"] + lista_status)
    
    # Executando filtros no DataFrame de exibição
    df_filtrado = df_completo.copy()
    if filtro_dim != "Todas":
        df_filtrado = df_filtrado[df_filtrado["dimensao"] == filtro_dim]
    if filtro_status != "Todos":
        df_filtrado = df_filtrado[df_filtrado["status"] == filtro_status]

    # ----------------------------------------------------
    # CARDS VISUAIS DE PERFORMANCE (KPIs)
    # ----------------------------------------------------
    totais = df_completo["status"].value_counts()
    qtd_verde = totais.get("🟢 Verde - Atendido", 0)
    qtd_amarelo = totais.get("🟡 Amarelo - Em análise", 0)
    qtd_vermelho = totais.get("🔴 Vermelho - Pendente", 0)
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="📋 Total de Ações", value=len(df_completo))
    with m2:
        st.markdown(f"<div style='border-left: 5px solid #28a745; padding-left: 10px;'><strong>Atendidas</strong><h2 style='color:#28a745; margin:0;'>{qtd_verde}</h2></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div style='border-left: 5px solid #ffc107; padding-left: 10px;'><strong>Em Análise</strong><h2 style='color:#ffc107; margin:0;'>{qtd_amarelo}</h2></div>", unsafe_allow_html=True)
    with m4:
        st.markdown(f"<div style='border-left: 5px solid #dc3545; padding-left: 10px;'><strong>Pendentes (Riscos)</strong><h2 style='color:#dc3545; margin:0;'>{qtd_vermelho}</h2></div>", unsafe_allow_html=True)
        
    st.markdown("---")

    # --- NAVEGAÇÃO POR ABAS INTERNAS ---
    tab_dashboard, tab_cronograma, tab_cadastrar, tab_import_export = st.tabs([
        "📊 Banco de Dados & Edição", 
        "📅 Cronograma de Execução",
        "➕ Nova Ação Estratégica", 
        "💾 Cargas e Modelos Extenos"
    ])

    # ----------------------------------------------------
    # ABA 1: TABELA E EDITOR MATRICIAL
    # ----------------------------------------------------
    with tab_dashboard:
        st.markdown("### 📝 Linhas de Ação Registradas")
        st.write("Ajuste qualquer registro diretamente na planilha abaixo. Utilize a barra lateral para filtrar.")
        
        if df_filtrado.empty:
            st.warning("Nenhum item localizado para os filtros selecionados.")
        else:
            edited_df = st.data_editor(
                df_filtrado,
                use_container_width=True,
                num_rows="dynamic",
                column_config={
                    "dimensao": st.column_config.SelectboxColumn("Dimensão IEG-M", options=dimensoes_iegm, required=True),
                    "status": st.column_config.SelectboxColumn("Status Atual", options=lista_status, required=True),
                    "periodo_report": st.column_config.SelectboxColumn("Report", options=periodos_report, required=True),
                    "data_inicio": st.column_config.DateColumn("Início", format="DD/MM/YYYY"),
                    "data_conclusao": st.column_config.DateColumn("Prazo Final", format="DD/MM/YYYY"),
                    "fragilidades": st.column_config.TextColumn("⚠️ Fragilidades Mapeadas", width="medium"),
                },
                key="plano_acao_editor_v3"
            )
            
            if st.button("💾 Salvar Alterações da Planilha", type="primary", use_container_width=True):
                if filtro_dim != "Todas" or filtro_status != "Todos":
                    for idx in edited_df.index:
                        st.session_state.plano_acao_db[idx] = edited_df.loc[idx].to_dict()
                else:
                    st.session_state.plano_acao_db = edited_df.to_dict(orient="records")
                    
                st.success("✨ Alterações integradas com sucesso à base de dados principal!")
                st.rerun()

    # ----------------------------------------------------
    # ABA 2: CRONOGRAMA VISUAL (LINHA DO TEMPO)
    # ----------------------------------------------------
    with tab_cronograma:
        st.markdown("### 📅 Cronograma Geral e Prazos Críticos")
        st.write("Abaixo você visualiza os marcos temporais e prazos finais ordenados por proximidade.")
        
        if df_filtrado.empty:
            st.info("Insira ações ou limpe os filtros para visualizar a linha do tempo.")
        else:
            # Ordenando ações por data de conclusão para priorização de prazos
            df_cronograma = df_filtrado.copy().sort_values(by="data_conclusao")
            
            for index, row in df_cronograma.iterrows():
                # Cor do card baseada no status
                cor_alerta = "#28a745" if "Verde" in row["status"] else "#ffc107" if "Amarelo" in row["status"] else "#dc3545"
                
                # Montagem da estrutura visual da linha do tempo
                st.markdown(f"""
                <div style="border-left: 4px solid {cor_alerta}; padding-left: 15px; margin-bottom: 20px; background-color: rgba(255,255,255,0.05); padding-top: 10px; padding-bottom: 10px; border-radius: 0 8px 8px 0;">
                    <span style="background-color: {cor_alerta}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;">{row['dimensao'].upper()}</span>
                    <h4 style="margin: 5px 0 2px 0;">{row['acao']}</h4>
                    <p style="margin: 0; font-size: 13px; color: #a3a3a3;"><strong>Responsável:</strong> {row['responsavel']} | <strong>Report:</strong> {row['periodo_report']}</p>
                    <p style="margin: 5px 0 0 0; font-size: 13px; color: #dc3545;">⚠️ <strong>Fragilidade Cadastrada:</strong> {row['fragilidades']}</p>
                    <div style="margin-top: 8px; font-size: 12px; font-weight: bold;">
                        📅 Período Executivo: {row['data_inicio'].strftime('%d/%m/%Y')} até {row['data_conclusao'].strftime('%d/%m/%Y')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # ABA 3: FORMULÁRIO DE CADASTRO EXPANDIDO
    # ----------------------------------------------------
    with tab_cadastrar:
        st.markdown("### ⚡ Cadastro Avançado de Metas Planejadas")
        
        with st.form("form_novo_item_v3", clear_on_submit=True):
            st.markdown("#### 🔍 1. Núcleo de Alinhamento Institucional")
            c1, c2 = st.columns(2)
            with c1:
                dimensao_sel = st.selectbox("📌 Dimensão Vinculada (IEG-M)", dimensoes_iegm)
                meta_estrategica = st.text_input("🎯 Meta Estratégica", placeholder="Ex: ADEQUAÇÃO DO ESPAÇO POR ALUNO")
            with c2:
                indicador_desempenho = st.text_input("📈 Indicador de Desempenho", placeholder="Ex: Área Física Disponível")
                alinhamento_ods = st.text_input("🇺🇳 Alinhamento ODS", placeholder="Ex: ODS 4 - Educação de Qualidade")

            st.markdown("#### 📋 2. Diagnóstico Operacional & Execução")
            c3, c4 = st.columns(2)
            with c3:
                acao = st.text_input("⚡ Título Prático da Ação", placeholder="Ex: Implementação de Backup em Nuvem")
                meta = st.text_input("🏁 Meta Alvo", placeholder="Ex: Atingir 100% da meta de conformidade")
                responsavel = st.text_input("👤 Responsável Principal", placeholder="Ex: Setor de TI / Coordenação")
            with c4:
                descricao_acao = st.text_area("📝 Descrição da Operação", placeholder="Detalhamento operacional da execução...")
                fragilidades = st.text_area("⚠️ Fragilidades Identificadas (Riscos)", placeholder="Mapeie aqui os gargalos e vulnerabilidades atuais que atrasam esta meta...")

            st.markdown("#### 🕒 3. Cronograma, Período de Report e Governança")
            c5, c6, c7 = st.columns(3)
            with c5:
                data_ini = st.date_input("📅 Início da Execução", value=date.today())
                data_fim = st.date_input("📅 Prazo Limite", value=date.today())
            with c6:
                periodo_rep_sel = st.selectbox("🔄 Período de Report (Frequência)", periodos_report)
                integracao = st.selectbox("🗺️ Integração ao Planejamento", ["Sim (PPA/LDO/LOA)", "Parcial", "Não Integrado"])
            with c7:
                forma_execucao = st.text_input("⚙️ Forma de Execução", placeholder="Ex: Auditoria ou Medição in loco")
                evidencias = st.text_input("📂 Comprovações/Evidências", placeholder="Ex: Laudos técnicos / Decretos oficiais")
            
            status_sel = st.selectbox("🚥 Status Inicial da Demanda", lista_status)

            st.markdown("<br>", unsafe_allow_html=True)
            submit_btn = st.form_submit_button("🚀 Publicar Nova Ação no Plano", use_container_width=True)
            
            if submit_btn:
                if not acao or not responsavel:
                    st.error("❌ Atenção: Os campos 'Título Prático da Ação' e 'Responsável' são de preenchimento obrigatório.")
                else:
                    novo_item = {
                        "dimensao": dimensao_sel,
                        "meta_estrategica": meta_estrategica,
                        "indicador_desempenho": indicador_desempenho,
                        "acao": acao,
                        "descricao_acao": descricao_acao,
                        "fragilidades": fragilidades,
                        "meta": meta,
                        "resultados_esperados": "Definidos em escopo",
                        "integracao_planejamento_municipal": integracao,
                        "alinhamento_ods": alinhamento_ods,
                        "data_inicio": data_ini,
                        "data_conclusao": data_fim,
                        "periodo_report": periodo_rep_sel,
                        "responsavel": responsavel,
                        "forma_execucao": forma_execucao,
                        "evidencias": evidencias,
                        "status": status_sel
                    }
                    st.session_state.plano_acao_db.append(novo_item)
                    st.success(f"🎉 Sucesso! Ação '{acao}' vinculada com sucesso à dimensão {dimensao_sel}.")
                    st.rerun()

    # ----------------------------------------------------
    # ABA 4: HUB DE INTEGRAÇÃO EXTERNA (CSV)
    # ----------------------------------------------------
    with tab_import_export:
        st.markdown("### 📂 Central de Cargas e Backups de Segurança")
        
        headers = [
            "dimensao", "meta_estrategica", "indicador_desempenho", "acao", "descricao_acao", 
            "fragilidades", "meta", "resultados_esperados", "integracao_planejamento_municipal", 
            "alinhamento_ods", "data_inicio", "data_conclusao", "periodo_report",
            "responsavel", "forma_execucao", "evidencias", "status"
        ]
        
        template_df = pd.DataFrame(columns=headers)
        csv_buffer = io.StringIO()
        template_df.to_csv(csv_buffer, sep="\t", index=False)
        
        col_down, col_up = st.columns(2)
        with col_down:
            st.info("💡 Baixe nosso layout tabular atualizado para preenchimento em massa no Excel.")
            st.download_button(
                label="📥 Baixar Template Estrutural (.CSV)",
                data=csv_buffer.getvalue(),
                file_name="layout_plano_acao_v3.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_up:
            st.success("💾 Salve uma cópia completa de segurança contendo todas as dimensões preenchidas.")
            csv_backup = io.StringIO()
            converter_para_df().to_csv(csv_backup, sep="\t", index=False)
            st.download_button(
                label="📦 Exportar Backup de Segurança do Plano",
                data=csv_backup.getvalue(),
                file_name="backup_plano_acao_completo.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        st.markdown("---")
        st.markdown("### 📤 Upload e Carga Direta")
        uploaded_file = st.file_uploader("Arraste seu arquivo CSV tabulado exportado aqui", type=["csv"])
        
        if uploaded_file is not None:
            try:
                df_importado = pd.read_csv(uploaded_file, sep="\t")
                if set(headers).issubset(df_importado.columns):
                    if st.button("🚨 Substituir Base Ativa e Rodar Carga", use_container_width=True, type="primary"):
                        df_importado['data_inicio'] = pd.to_datetime(df_importado['data_inicio']).dt.date
                        df_importado['data_conclusao'] = pd.to_datetime(df_importado['data_conclusao']).dt.date
                        st.session_state.plano_acao_db = df_importado.to_dict(orient="records")
                        st.success("🔥 Banco de dados reconfigurado e atualizado com sucesso!")
                        st.rerun()
                else:
                    st.error("❌ O arquivo enviado não possui as novas colunas obrigatórias do IEG-M.")
            except Exception as e:
                st.error(f"Erro crítico no processamento das colunas: {e}")