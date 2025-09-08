#include "MenuCalculadora.h"
#include "../m/Calculadora.h"
#include "../m/CalculadoraBinario.h"
#include "../m/CalculadoraDecimal.h"
#include "../m/CalculadoraOctal.h"
#include "../v/LimpiarPantalla.h"
#include <iostream>
#include <cstdlib>

using namespace std;

void MenuCalculadora::ejecutarMenu(){
    int x1, x2, operacion;
	Calculadora* calculadora = nullptr;
	LimpiarPantalla limpiarPantalla;
	limpiarPantalla.Limpiar();


   	while(true){
		cout << "1. Binario" << endl << "2. Octal" << endl << "3. Decimal" << endl << ": ";
   		if(cin >> x1 && x1 > 0 && x1 <=3){ break; }
		else{
			cout << "Dato invalido" << endl;
			limpiarPantalla.Limpiar();
			cin.clear();
			cin.ignore();
		}
   	}


	if(x1 == 1){
		calculadora = new CalculadoraBinario();
	}else if(x1 == 2){
		calculadora = new CalculadoraOctal();
	}else if(x1 == 3){
		calculadora = new CalculadoraDecimal();
	}
	limpiarPantalla.Limpiar();

	while(true){
			cout << "Numero 1: ";
		if(cin >> x1 && calculadora->validarNumero(x1)){ break; }
		else{
				limpiarPantalla.Limpiar();
				cout << "Dato invalido" << endl;
		}
		cin.clear();
		cin.ignore();
	}
	limpiarPantalla.Limpiar();
	

   	while(true){
       	cout << "Numero 2: ";
       	if(cin >> x2 && calculadora->validarNumero(x2)){ break; }
		else{
			limpiarPantalla.Limpiar();
			cout << "Dato invalido" << endl;
		}
		cin.clear();
		cin.ignore();
   	}


	calculadora->setN1(calculadora->convercionEntrada(x1));
   	calculadora->setN2(calculadora->convercionEntrada(x2));


   	while(true){
       	limpiarPantalla.Limpiar();
       	cout << "1. Suma (" << calculadora->getN1() << "+" << calculadora->getN2() << ")" << endl << "2. Resta (" << calculadora->getN1() << "-" << calculadora->getN2() << ")" << endl;
       	if(cin >> operacion && operacion > 0 && operacion <= 2){ break; }
   	}
   	if(operacion == 1){
   		calculadora->setResultado(calculadora->suma());
   	}else{
   		calculadora->setResultado(calculadora->resta());
   	}

	
	limpiarPantalla.Limpiar();
   	cout << calculadora->convercionSalida() << endl;
};