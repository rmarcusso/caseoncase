#/bin/bash

f_inicio(){
    echo "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
    date "+Inicio do processo em %H:%M:%S, %d de %B de %Y."
    echo "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
}

f_fim(){
    echo "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
    date "+Processo finalizado em %H:%M:%S, %d de %B de %Y."
    echo "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
}

f_mensagem(){
    local texto
    texto="${1}"
    echo "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
    echo "MENSAGEM -> ${texto}"
    echo "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
}

f_exit(){
    local texto
    texto="${1}"
    echo "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
    echo "ENCERRANDO O PROCESSO -> ${texto}"
    echo "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
    exit
}

f_update(){
    f_mensagem "Baixando atualizacoes"
    sudo apt-get update
    f_mensagem "Aplicando atualizacoes"
    sudo apt-get upgrade
    
}

f_instalador_python(){
    local rc
        
    f_mensagem "Primeiro passo: Instalacao Primeiros pacotes"
    sudo apt install software-properties-common
    rc=${?}
    if [[ ${rc} -ne 0 ]]; then
        f_exit "Problemas para realizar instalacao das dependencias."
    fi
    
    f_mensagem "Adicionando novos recursos ao repositorio"
    sudo add-apt-repository ppa:deadsnakes/ppa
    rc=${?}
    if [[ ${rc} -ne 0 ]]; then
        # f_exit "Problemas para inserir novos recursos ao repositorio. Tente executar novamente"
        f_mensagem "Problemas para inserir novos recursos ao repositorio. Tente executar novamente"
    fi

    f_mensagem "Atualizando novos recursos..."
    f_update
    rc=${?}
    if [[ ${rc} -ne 0 ]]; then
        f_exit "Problema em aplicar as atualizacoes aos sistema linux."
    fi

    f_mensagem "Instalando Python..."
    sudo apt-get install python3.7
    rc=${?}
    if [[ ${rc} -ne 0 ]]; then
        f_exit "Problemas ao instalar o Python 3.7"
    else
        versao=$(f_versao_python)
        f_mensagem "Versao instalado do python -> ${versao}"
    fi

}

f_versao_python(){
    python3.7 --version
}

f_criando_venv(){
    f_mensagem "Inicio do processo de criacao da env."
    sudo apt-get install python3-pip

    f_mensagem "Atualizando pip..."
    python3.7 -m pip install --upgrade pip

    f_mensagem "Instalando virtualenv..."
    sudo apt-get install python3.7-venv 
    sudo apt-get install python3-venv

    f_mensagem "Criando Virtual Env para execucao do projeto..."
    # virtualenv ~/git/caseoncase/venv 
    python3.7 -m venv ~/git/caseoncase/venv
    
    f_mensagem "Atualizando pip..."
    ~/git/caseoncase/venv/bin/python3.7 -m pip install --upgrade pip

}

f_instalador_git(){
    sudo apt-get install git
}

f_clone_crawler(){
    local rcmkdir

    f_mensagem "Criando pasta git na /home"
    if [[ ! -d ~/git ]]; then
        echo "Diretorio nao existe"
        mkdir ~/git
        rcmkdir=${?}
        if [[ ${rc} -ne 0 ]]; then
            f_mensagem "Pasta já existe. Continuando o processo."
        fi    
        cd ~/git
    else
        echo "Diretorio existe"
    fi

    local rc

    git clone https://github.com/rmarcusso/caseoncase.git
    rc=${?}
    if [[ ${rc} -ne 0 ]]; then
        f_exit "Problema ao realizar clone do projeto"
    fi

}

f_instalacao_libs(){
    local=rc
    ~/git/caseoncase/venv/bin/python3.7 -m pip install -r     ~/git/caseoncase/requirements.txt
    rc=${?}
    if [[ ${rc} -ne 0 ]]; then
        f_exit "Problema na instalacao das libs necessárias"
    fi
}

f_prepara_ambiente(){
    f_inicio

    f_mensagem "Instalando atualizacoes..."
    f_instalador_python
    
    f_mensagem "Instalando git"
    f_instalador_git
    
    f_mensagem "Fazendo clone do Projeto"
    f_clone_crawler
        
    f_mensagem "Criando virtual Env"
    f_criando_venv

    f_mensagem "Instalacao do Scrapy para executar o projeto."
    f_instalacao_libs

    f_mensagem "Ambiente preparado"    
    f_fim
}

f_executa_crawler(){
    . ~/git/caseoncase/venv/bin/activate
    cd ~/git/caseoncase/caseOncase
    f_mensagem "Inicio do crawler..."
    f_inicio
    
    scrapy crawl fatos -s HTTPCACHED_ENABLED=1 -o ~/git/caseoncase/caseOncase/arquivos/dados.json

    f_mensagem "Fim do processo de Crawler"
    f_fim

}

f_executa_analise(){

    . ~/git/caseoncase/venv/bin/activate

    f_mensagem "Executando chamada do python que realiza a geração dos gráficos."
    cd ~/git/caseoncase/caseOncase/analise/

    ~/git/caseoncase/venv/bin/python3.7



}

f_main(){
    f_prepara_ambiente
    f_executa_crawler
}

f_main
