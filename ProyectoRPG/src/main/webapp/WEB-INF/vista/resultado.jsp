<%@ page contentType="text/html; charset=UTF-8" isELIgnored="false" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>Objetos de ${raza}</title>
  <link rel="stylesheet" href="${pageContext.request.contextPath}/assets/css/styles.css">
  <style>
    :root{
      --bg-url: url('${pageContext.request.contextPath}/assets/img/bg-dark.png');
    }
  </style>
</head>
<body>
  <h1>Objetos de la raza seleccionada</h1>

  <div class="header">
    <span class="badge">Raza: <c:out value="${raza}" default="(sin raza)"/></span>
  </div>

  <div class="grid">
    <!-- Cuerpo -->
    <div class="card">
      <div class="thumb"
           style="background-image:url('${pageContext.request.contextPath}/assets/img/${raza}-cuerpo.png?v=2');">
      </div>
      <div class="content">
        <h3 class="title">Cuerpo</h3>
        <p><c:out value="${desCuerpo}" default="No disponible."/></p>
      </div>
    </div>

    <!-- Montura -->
    <div class="card">
      <div class="thumb"
           style="background-image:url('${pageContext.request.contextPath}/assets/img/${raza}-montura.png?v=2');">
      </div>
      <div class="content">
        <h3 class="title">Montura</h3>
        <p><c:out value="${desMontura}" default="No disponible."/></p>
      </div>
    </div>

    <!-- Arma -->
    <div class="card">
      <div class="thumb"
           style="background-image:url('${pageContext.request.contextPath}/assets/img/${raza}-arma.png?v=2');">
      </div>
      <div class="content">
        <h3 class="title">Arma</h3>
        <p><c:out value="${desArma}" default="No disponible."/></p>
      </div>
    </div>

    <!-- Armadura -->
    <div class="card">
      <div class="thumb"
           style="background-image:url('${pageContext.request.contextPath}/assets/img/${raza}-armadura.png?v=2');">
      </div>
      <div class="content">
        <h3 class="title">Armadura</h3>
        <p><c:out value="${desArmadura}" default="No disponible."/></p>
      </div>
    </div>
  </div>

  <a class="btn" href="${pageContext.request.contextPath}/rpg/cliente">Volver</a>
</body>
</html>
