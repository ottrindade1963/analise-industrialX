"""
Script para adicionar bloco de compatibilidade Colab a todos os pipelines.
Garante que sys.path e os.chdir estão corretos quando executados via !python3 no Colab.
"""
import os

COLAB_BLOCK = '''import os
import sys

# ═══ Compatibilidade Colab: garantir que os módulos locais são encontrados ═══
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
os.chdir(_SCRIPT_DIR)
# ═══════════════════════════════════════════════════════════════════════════════

'''

# Pipelines que são chamados diretamente via !python3 no notebook
PIPELINES = [
    'passo1_master_pipeline.py',
    'passo2_master_pipeline.py',
    'passo2_1_master_pipeline.py',
    'passo3_feat_eng_pipeline.py',
    'passo4_model_train_pipeline.py',
    'passo5_eval_pipeline.py',
    'passo6_strategy_pipeline.py',
    'passo7_shap_pipeline.py',
    'passo8_geo_pipeline.py',
    'passo9_advanced_pipeline.py',
]

for pipeline in PIPELINES:
    if not os.path.exists(pipeline):
        print(f'  SKIP: {pipeline} (não existe)')
        continue
    
    with open(pipeline, 'r') as f:
        content = f.read()
    
    # Verificar se já tem o bloco
    if '_SCRIPT_DIR' in content:
        print(f'  OK (já tem): {pipeline}')
        continue
    
    # Encontrar onde inserir: após a docstring (se houver) ou no início
    lines = content.split('\n')
    insert_idx = 0
    
    # Pular docstring se existir
    if lines[0].startswith('"""') or lines[0].startswith("'''"):
        quote = lines[0][:3]
        if lines[0].count(quote) >= 2:
            # Docstring numa só linha
            insert_idx = 1
        else:
            # Docstring multi-linha
            for i in range(1, len(lines)):
                if quote in lines[i]:
                    insert_idx = i + 1
                    break
    
    # Remover imports de os e sys que já existam (vamos incluí-los no bloco)
    new_lines = lines[:insert_idx]
    remaining = lines[insert_idx:]
    
    # Filtrar imports duplicados de os e sys
    filtered_remaining = []
    for line in remaining:
        if line.strip() in ['import os', 'import sys', 'import os, sys']:
            continue
        filtered_remaining.append(line)
    
    # Reconstruir
    new_content = '\n'.join(new_lines) + '\n' + COLAB_BLOCK + '\n'.join(filtered_remaining)
    
    with open(pipeline, 'w') as f:
        f.write(new_content)
    
    print(f'  FIXED: {pipeline}')

print('\nTodos os pipelines corrigidos!')
