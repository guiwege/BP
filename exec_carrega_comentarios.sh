#!/bin/bash
###############################################################
# Script/Rotina que carrega a tabela comments e envia alerta
# quando a palavra linux é encontrada
# Autor: Guilherme Wege Chagas
###############################################################

step=$1
log=$(date +'%Y%m%d_%H%M%S').log

# Se step não for passado, começa do 1
if [ -z "$step" ]
then
	step="step01"
fi

function echoCabec {
	echo "##################################################################"
	echo "# $1"
	echo "##################################################################"
}

cd /media/sf_Programacao/Python/exercicio_Brasil_Paralelo

case $step in
	step01)
		echoCabec "Iniciando step01"
		python3 01_crawler.py 2>&1 | tee -a $log
		rc=$?
		if [ "$?" -eq "0" ] 
		then
			echoCabec "step01 finalizou com sucesso"
		else
			echoCabec "step01 finalizou com erro"
			exit $rc
		fi
	;&
	step02)
		echoCabec "Iniciando step02"
		python3 02_carrega_target.py 2>&1 | tee -a $log
                rc=$?
                if [ "$?" -eq "0" ]
                then
                        echoCabec "step02 finalizou com sucesso"
                else
                        echoCabec "step02 finalizou com erro"
                        exit $rc
                fi
	;&
	step03)
		echoCabec "Iniciando step03"
                python3 03_envia_alerta.py 2>&1 | tee -a $log
                rc=$?
                if [ "$?" -eq "0" ]
                then
                        echoCabec "step03 finalizou com sucesso"
                else
                        echoCabec "step03 finalizou com erro"
                        exit $rc
                fi
	;;
esac
