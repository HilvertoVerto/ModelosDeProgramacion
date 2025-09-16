#ifndef CALCULADORA_H
#define CALCULADORA_H
#include <string>

class Calculadora{
    protected:
        int n1, n2, resultado, baseNumerica;
        std::string numerosValidos;
    public:
        Calculadora();
        
        int suma();
        int resta();
        std::string convercionSalida();
        int convercionEntrada(int entrada);
        bool validarNumero(int numero);

        int getN1();
        void setN1(int _n1);

        int getN2();
        void setN2(int _n2);

        int getResultado();
        void setResultado(int _resultado);
};

#endif
