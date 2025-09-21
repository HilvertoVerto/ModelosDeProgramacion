package controlador;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.RequestDispatcher;
import java.io.IOException;

import modelo.fabricas.*;
import modelo.productos.*;

@WebServlet(name = "Cliente", urlPatterns = {"/rpg/cliente"})
public class Cliente extends HttpServlet {

    private FabricaAbstracta seleccionarFabrica(String raza) {
        if (raza == null) return null;
        switch (raza) {
            case "humanos": return FabricaHumanos.getInstancia();
            case "elfos":   return FabricaElfos.getInstancia();
            case "orcos":   return FabricaOrcos.getInstancia();
            case "enanos":  return FabricaEnanos.getInstancia();
            default:        return null;
        }
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        RequestDispatcher rd = req.getRequestDispatcher("/WEB-INF/vista/select.jsp");
        rd.forward(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
        throws ServletException, IOException {

        String raza = req.getParameter("raza"); // ahora solo llega la raza
        FabricaAbstracta fabrica = seleccionarFabrica(raza);

    if (fabrica == null) {
        req.setAttribute("error", "Selecciona una raza válida.");
        req.getRequestDispatcher("/WEB-INF/vista/select.jsp").forward(req, resp);
        return;
    }

    // Crear UNA VEZ cada producto y tomar su descripción de forma segura
    ICuerpo   cuerpo   = fabrica.crearCuerpo();
    IMontura  montura  = fabrica.crearMontura();
    IArma     arma     = fabrica.crearArma();
    IArmadura armadura = fabrica.crearArmadura();

    String desCuerpo   = (cuerpo   != null) ? String.valueOf(cuerpo.obtenerDescripcion())     : "No disponible.";
    String desMontura  = (montura  != null) ? String.valueOf(montura.obtenerDescripcion())    : "No disponible.";
    String desArma     = (arma     != null) ? String.valueOf(arma.obtenerDescripcion())       : "No disponible.";
    String desArmadura = (armadura != null) ? String.valueOf(armadura.obtenerDescripcion())   : "No disponible.";

    req.setAttribute("raza", raza);
    req.setAttribute("desCuerpo", desCuerpo);
    req.setAttribute("desMontura", desMontura);
    req.setAttribute("desArma", desArma);
    req.setAttribute("desArmadura", desArmadura);

    req.getRequestDispatcher("/WEB-INF/vista/resultado.jsp").forward(req, resp);
}
}
