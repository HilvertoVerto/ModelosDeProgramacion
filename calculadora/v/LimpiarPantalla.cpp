#include "LimpiarPantalla.h"
#include <cstdlib>

void LimpiarPantalla::Limpiar(){
    #ifdef _WIN32
        system("cls");
    #else
        system("clear");
    #endif
};
