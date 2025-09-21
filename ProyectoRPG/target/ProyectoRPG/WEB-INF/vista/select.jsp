<%@ page contentType="text/html; charset=UTF-8" %>
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>Proyecto RPG - Selección</title>
  <link rel="stylesheet" href="${pageContext.request.contextPath}/assets/css/styles.css">
  <!-- Usa el mismo fondo oscuro que en resultado.jsp -->
  <style>
    :root{
      --bg-url: url('${pageContext.request.contextPath}/assets/img/bg-dark.png');
    }
  </style>
</head>
<body class="center-page">
  <main class="panel">
    <header class="panel__header">
      <h1 class="panel__title">Proyecto RPG</h1>
      <p class="panel__subtitle">Elige tu raza para generar el personaje y sus objetos</p>
    </header>

    <form class="form form--compact" action="${pageContext.request.contextPath}/rpg/cliente" method="post">
      <fieldset class="fieldset">
        <legend class="legend">Selecciona una raza</legend>

        <div class="radio-grid">
          <label class="chip">
            <input class="chip__input" type="radio" name="raza" value="humanos" required>
            <span class="chip__label">Humanos</span>
          </label>

          <label class="chip">
            <input class="chip__input" type="radio" name="raza" value="elfos">
            <span class="chip__label">Elfos</span>
          </label>

          <label class="chip">
            <input class="chip__input" type="radio" name="raza" value="orcos">
            <span class="chip__label">Orcos</span>
          </label>

          <label class="chip">
            <input class="chip__input" type="radio" name="raza" value="enanos">
            <span class="chip__label">Enanos</span>
          </label>
        </div>
      </fieldset>

      <button class="btn btn--primary" type="submit">Crear</button>
    </form>
  </main>
</body>
</html>
