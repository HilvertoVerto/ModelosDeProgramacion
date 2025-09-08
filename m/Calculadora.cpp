#include "Calculadora.h"
#include <string>
#include <algorithm>
#include <cmath>

Calculadora::Calculadora(){};

int Calculadora::suma(){ return n1 + n2; };

int Calculadora::resta(){ return n1 - n2; };

int Calculadora::getN1(){ return n1; };
void Calculadora::setN1(int _n1){ n1 = _n1; };

int Calculadora::getN2(){ return n2; };
void Calculadora::setN2(int _n2){ n2 = _n2; };

int Calculadora::getResultado(){ return resultado; };
void Calculadora::setResultado(int _resultado){ resultado = _resultado; };

std::string Calculadora::convercionSalida(){
	if(resultado == 0){ return "0"; }
	std::string digitos = numerosValidos;
	std::string numeroConvertido = "";
	while(resultado > 0){
		numeroConvertido += digitos[resultado % baseNumerica];
		resultado /= baseNumerica;
	}
	reverse(numeroConvertido.begin(), numeroConvertido.end());
	return numeroConvertido;
};

int Calculadora::convercionEntrada(int entrada){
	std::string entradaStr = std::to_string(entrada);
	int largo = entradaStr.length();
	int resultado = 0;

	for(int i = 1; i <= largo; i++){
		resultado += ((entradaStr[largo - i] - '0') * pow(baseNumerica, i-1));
	}
	return resultado;
}

bool Calculadora::validarNumero(int numero){
	std::string numeroStr = std::to_string(numero);
	int contador = 0;

	for(int i = 0; i < numerosValidos.length(); i++){
		for(int j = 0; j < numeroStr.length(); j++){
			if(numeroStr[j] == numerosValidos[i]){
				contador++;
			}
		}
	}
	if(contador == numeroStr.length()){ return true; }
	else{ return false; }
};
